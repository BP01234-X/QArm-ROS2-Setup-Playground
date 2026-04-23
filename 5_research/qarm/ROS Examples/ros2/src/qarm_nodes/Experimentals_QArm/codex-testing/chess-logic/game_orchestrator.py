"""High-level one-move-at-a-time coordinator for Phase 3."""

from __future__ import annotations

import json
from pathlib import Path

from ascii_display import AsciiDisplay
from board_geometry import BoardGeometry
from board_observer import BoardObserver
from calibrated_board_model import load_fixed_calibrated_board_model
from chess_logic import ChessLogicController
from grasp_planner import GraspPlanner
from models import MotionPlan, ObservedBoard, VerificationResult
from motion_fsm import Events, MotionFSM, States
from move_executor import MoveExecutor


class GameOrchestrator:
    """Coordinates symbolic chess, physical motion flow, and verification."""

    def __init__(
        self,
        config_dir: str | Path | None = None,
        mock_mode: bool = True,
        initial_observed_board: dict[str, str | None] | None = None,
        board_observer: BoardObserver | None = None,
        action_duration_s: float = 0.05,
    ) -> None:
        base_dir = Path(config_dir or Path(__file__).resolve().parent / "config")
        self.config_dir = base_dir
        self.geometry = BoardGeometry.from_yaml(base_dir / "board.yaml")
        self.fixed_board_model = load_fixed_calibrated_board_model(
            config_dir=base_dir,
            geometry=self.geometry,
        )
        self.board_observer = board_observer or BoardObserver(
            self.geometry,
            mock_observations=initial_observed_board,
        )
        self.chess_logic = ChessLogicController()
        self.grasp_planner = GraspPlanner.from_yaml(self.geometry, base_dir / "grasp_rules.yaml")
        self.motion_fsm = MotionFSM()
        self.move_executor = MoveExecutor.from_yaml(
            base_dir / "observer_pose.yaml",
            mock_mode=mock_mode,
            action_duration_s=action_duration_s,
        )
        self.ascii_display = AsciiDisplay()
        self.expected_initialized = False
        self.last_motion_plan: MotionPlan | None = None
        self.last_move_uci: str | None = None
        self.manipulation_board_source = self.fixed_board_model.source
        self.manipulation_board_corners_world = dict(self.fixed_board_model.board_outer_corners_world)
        self.manipulation_square_centers_world = dict(self.fixed_board_model.square_centers_world)
        self.manipulation_board_surface_world_z = float(self.fixed_board_model.board_surface_world_z)
        self.external_board_frame_file = self.config_dir.parent.parent / "board_frame_world.json"
        self._apply_manipulation_board_model(
            source=self.fixed_board_model.source,
            board_outer_corners_world=self.fixed_board_model.board_outer_corners_world,
            square_centers_world=self.fixed_board_model.square_centers_world,
            board_surface_world_z=self.fixed_board_model.board_surface_world_z,
        )
        self._load_external_board_frame_override()

    def boot(self) -> ObservedBoard:
        """Initialize interfaces, move to observer pose, and seed the board."""

        self._load_external_board_frame_override()
        self._transition(Events.BOOT)
        self.board_observer.freeze()
        self._run_action(lambda: self.move_executor.set_gripper(0.7))
        self._run_action(self.move_executor.move_to_observer_pose)
        self._transition(Events.REACHED_OBSERVER_POSE)
        self.board_observer.allow_observation()
        observed = self.board_observer.observe_board()
        self._sync_manipulation_board_from_observer()
        if not self.expected_initialized:
            self.chess_logic.set_from_observed_board(observed)
            self.expected_initialized = True
        self._transition(Events.BOARD_OBSERVED)
        return observed

    def receive_move_from_user(self, move_text: str) -> str:
        """Normalize a move from manual text input."""

        return move_text.strip().lower()

    def receive_move_from_gpt(self, move_text: str) -> str:
        """Placeholder hook for a future GPT move source."""

        return self.receive_move_from_user(move_text)

    def receive_move_from_engine(self, move_text: str) -> str:
        """Placeholder hook for a future engine move source."""

        return self.receive_move_from_user(move_text)

    def preview_square_move_plan(
        self,
        source_square: str,
        target_square: str,
        piece_name: str | None = None,
    ) -> MotionPlan:
        """Return a square->pose manipulation plan without executing motion."""

        return self.grasp_planner.plan_square_transfer(
            source_square=source_square,
            target_square=target_square,
            piece_name=piece_name,
        )

    def execute_one_move(
        self,
        move_text: str,
        verification_board: dict[str, str | None] | None = None,
    ) -> VerificationResult:
        """Run one UCI move through chess validation and physical execution."""

        uci = self.receive_move_from_user(move_text)
        return self._execute_uci_move(
            uci=uci,
            verification_board=verification_board,
            piece_name_hint=None,
        )

    def execute_square_move(
        self,
        source_square: str,
        target_square: str,
        *,
        piece_name: str | None = None,
        promotion: str | None = None,
        verification_board: dict[str, str | None] | None = None,
    ) -> VerificationResult:
        """Run one direct square->square move through the same move pipeline."""

        source = source_square.strip().lower()
        target = target_square.strip().lower()
        promotion_suffix = (promotion or "").strip().lower()
        uci = f"{source}{target}{promotion_suffix}"
        return self._execute_uci_move(
            uci=uci,
            verification_board=verification_board,
            piece_name_hint=piece_name,
        )

    def _execute_uci_move(
        self,
        *,
        uci: str,
        verification_board: dict[str, str | None] | None,
        piece_name_hint: str | None,
    ) -> VerificationResult:
        """Execute one validated UCI move using the fixed one-move-at-a-time loop."""

        if self.motion_fsm.status.state != States.IDLE.value:
            raise RuntimeError(f"Cannot accept a move while state={self.motion_fsm.status.state}")

        self.last_move_uci = uci
        self._transition(Events.REQUEST_MOVE, pending_move_uci=uci)

        if not self.chess_logic.validate_move_uci(uci):
            error = f"Illegal move for current board state: {uci}"
            self.motion_fsm.status.state = States.IDLE.value
            self.motion_fsm.status.robot_busy = False
            self.motion_fsm.status.last_error = error
            self.motion_fsm.status.pending_move_uci = None
            raise ValueError(error)

        move_command = self.chess_logic.apply_move_uci(uci)
        if piece_name_hint is not None and move_command.piece_name is not None:
            normalized_hint = piece_name_hint.strip().lower()
            if normalized_hint != move_command.piece_name:
                raise ValueError(
                    f"Piece hint mismatch for {uci}: hinted={normalized_hint}, "
                    f"board_has={move_command.piece_name}."
                )
        self.last_motion_plan = self.grasp_planner.plan_move(move_command)
        grasp_plan = self.last_motion_plan.grasp_plan

        self._transition(Events.MOVE_PLANNED)
        self.board_observer.freeze()
        self._run_action(lambda: self.move_executor.set_gripper(grasp_plan.gripper_open_value))

        self._run_step(
            action=lambda: self.move_executor.move_to_world_pose(
                stage_name="source_approach",
                world_xyz=grasp_plan.source_approach_world_xyz,
                note=f"Phase 3 source approach for {grasp_plan.source_square}.",
            ),
            event=Events.REACHED_PICK_APPROACH,
        )
        self._run_step(
            action=lambda: self.move_executor.set_gripper(grasp_plan.gripper_open_value),
            event=Events.GRIPPER_PREPARED,
        )
        self._run_step(
            action=lambda: self.move_executor.execute_pick(grasp_plan),
            event=Events.PICKED,
        )
        self._run_action(lambda: self.move_executor.set_gripper(grasp_plan.gripper_close_value))
        self._run_step(
            action=lambda: self.move_executor.lift_piece(grasp_plan),
            event=Events.LIFTED,
        )
        self._run_action(lambda: self.move_executor.set_gripper(grasp_plan.gripper_close_value))
        self._run_step(
            action=lambda: self.move_executor.move_to_world_pose(
                stage_name="target_approach",
                world_xyz=grasp_plan.target_approach_world_xyz,
                note=f"Phase 3 target approach for {grasp_plan.target_square}.",
            ),
            event=Events.REACHED_PLACE,
        )
        self._run_step(
            action=lambda: self.move_executor.execute_place(grasp_plan),
            event=Events.PLACED,
        )
        self._run_action(lambda: self.move_executor.set_gripper(grasp_plan.gripper_open_value))
        self._run_step(
            action=self.move_executor.retreat,
            event=Events.RETREATED,
        )
        self._transition(Events.MOVEMENT_FINISHED)

        self._run_action(lambda: self.move_executor.set_gripper(grasp_plan.gripper_open_value))
        self._run_action(self.move_executor.move_to_observer_pose)
        self._transition(Events.REACHED_OBSERVER_POSE)
        self.board_observer.allow_observation()
        if verification_board is not None:
            self.board_observer.set_mock_observations(verification_board)
        observed_after = self.board_observer.observe_board()
        self._sync_manipulation_board_from_observer()
        self._transition(Events.VERIFICATION_REQUESTED)
        result = self.chess_logic.compare_with_observed(observed_after)
        if result.success:
            self._transition(Events.VERIFICATION_OK)
        else:
            self._transition(Events.VERIFICATION_FAILED, error="Observed board does not match expected board.")
        return result

    def recover_to_observer(self) -> ObservedBoard:
        """Minimal recovery flow that returns to observer pose and re-observes."""

        if self.motion_fsm.status.state != States.ERROR_RECOVERY.value:
            raise RuntimeError("Recovery is only valid from ERROR_RECOVERY.")
        self._transition(Events.RECOVER)
        self._run_action(lambda: self.move_executor.set_gripper(0.7))
        self._run_action(self.move_executor.move_to_observer_pose)
        self._transition(Events.REACHED_OBSERVER_POSE)
        self.board_observer.allow_observation()
        observed = self.board_observer.observe_board()
        self._sync_manipulation_board_from_observer()
        self._transition(Events.BOARD_OBSERVED)
        return observed

    def current_expected_board(self):
        """Expose the current expected symbolic board."""

        return self.chess_logic.expected_board()

    def debug_snapshot(self) -> str:
        """Return a compact textual snapshot for debugging."""

        lines = [self.ascii_display.show_fsm_status(self.motion_fsm.status)]
        if self.last_move_uci is not None:
            lines.append(self.ascii_display.show_last_move(self.last_move_uci))
        lines.append(self.ascii_display.show_gripper_target(self.move_executor.current_gripper_target))
        lines.append(f"MANIP BOARD SOURCE | {self.manipulation_board_source}")
        lines.append(f"MANIP BOARD CORNERS | {self.manipulation_board_corners_world}")
        if self.last_motion_plan is not None:
            lines.append(f"PLANNED PHASES | {' -> '.join(self.last_motion_plan.phases)}")
            lines.append(
                "PLANNED GRIPPER | "
                f"open={self.last_motion_plan.grasp_plan.gripper_open_value:.1f} "
                f"close={self.last_motion_plan.grasp_plan.gripper_close_value:.1f}"
            )
            gp = self.last_motion_plan.grasp_plan
            lines.append(
                "PLANNED POSES | "
                f"src_approach={gp.source_approach_world_xyz} src_pick={gp.source_pick_world_xyz} "
                f"src_lift={gp.source_lift_world_xyz}"
            )
            lines.append(
                "PLANNED POSES | "
                f"tgt_approach={gp.target_approach_world_xyz} tgt_place={gp.target_place_world_xyz} "
                f"tgt_retreat={gp.target_retreat_world_xyz}"
            )
        lines.append(f"FEN | {self.chess_logic.fen_summary()}")
        lines.append(f"HISTORY | {self.chess_logic.move_history_summary()}")
        return "\n".join(lines)

    def manipulation_board_debug(self) -> dict[str, object]:
        """Expose active board source/corners used by manipulation planning."""

        return {
            "source": self.manipulation_board_source,
            "corners_world": dict(self.manipulation_board_corners_world),
            "board_surface_world_z": float(self.manipulation_board_surface_world_z),
        }

    def manipulation_square_center_world(self, square: str) -> tuple[float, float, float]:
        """Return one active manipulation square center in world coordinates."""

        normalized = square.strip().lower()
        if normalized not in self.manipulation_square_centers_world:
            raise KeyError(f"Unknown square {square!r} in active manipulation board model.")
        center = self.manipulation_square_centers_world[normalized]
        return (float(center[0]), float(center[1]), float(center[2]))

    def _run_step(self, action, event: Events) -> None:
        """Execute one mocked physical step and then advance the FSM."""

        self._run_action(action)
        self._transition(event)

    def _run_action(self, action) -> None:
        """Execute and wait for the mocked physical action."""

        action()
        self.move_executor.wait_until_done()

    def _transition(
        self,
        event: Events,
        pending_move_uci: str | None = None,
        error: str | None = None,
    ) -> None:
        """Advance the FSM and enforce perception freeze policy."""

        self.motion_fsm.transition(event, pending_move_uci=pending_move_uci, error=error)
        if self.motion_fsm.perception_allowed(self.motion_fsm.status.state):
            self.board_observer.allow_observation()
        else:
            self.board_observer.freeze()

    def _sync_manipulation_board_from_observer(self) -> None:
        """Sync manipulation square centers to the latest observer board frame."""

        latest_frame = self.board_observer.latest_board_frame()
        if latest_frame is None:
            return
        corners = latest_frame.board_outer_corners_world or self.manipulation_board_corners_world
        board_surface_z = float(sum(corners[key][2] for key in ("a1", "h1", "h8", "a8")) / 4.0)
        self._apply_manipulation_board_model(
            source=f"observer_frame:{latest_frame.source}",
            board_outer_corners_world=corners,
            square_centers_world=latest_frame.square_centers_world,
            board_surface_world_z=board_surface_z,
        )

    def _apply_manipulation_board_model(
        self,
        *,
        source: str,
        board_outer_corners_world: dict[str, tuple[float, float, float]],
        square_centers_world: dict[str, tuple[float, float, float]],
        board_surface_world_z: float,
    ) -> None:
        """Apply one board model consistently to planner and executor."""

        self.manipulation_board_source = source
        self.manipulation_board_corners_world = {
            key: (float(value[0]), float(value[1]), float(value[2]))
            for key, value in board_outer_corners_world.items()
        }
        self.manipulation_square_centers_world = {
            key: (float(value[0]), float(value[1]), float(value[2]))
            for key, value in square_centers_world.items()
        }
        self.manipulation_board_surface_world_z = float(board_surface_world_z)
        self.grasp_planner.set_board_square_centers(
            square_centers_world=self.manipulation_square_centers_world,
            board_surface_world_z=self.manipulation_board_surface_world_z,
            board_source=self.manipulation_board_source,
        )
        self.move_executor.set_board_square_centers(
            square_centers_world=self.manipulation_square_centers_world,
            board_source=self.manipulation_board_source,
        )

    def _load_external_board_frame_override(self) -> None:
        """Load optional board frame export generated by RViz debug node."""

        path = self.external_board_frame_file
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        if not isinstance(payload, dict):
            return
        raw_corners = payload.get("board_outer_corners_world")
        raw_centers = payload.get("square_centers_world")
        if not isinstance(raw_corners, dict) or not isinstance(raw_centers, dict):
            return

        try:
            corners_world = {
                key: (
                    float(raw_corners[key][0]),
                    float(raw_corners[key][1]),
                    float(raw_corners[key][2]),
                )
                for key in ("a1", "h1", "h8", "a8")
            }
        except (KeyError, TypeError, ValueError, IndexError):
            return

        centers_world: dict[str, tuple[float, float, float]] = {}
        for square, value in raw_centers.items():
            if not isinstance(square, str):
                continue
            if not isinstance(value, (list, tuple)) or len(value) < 3:
                continue
            try:
                centers_world[square.strip().lower()] = (
                    float(value[0]),
                    float(value[1]),
                    float(value[2]),
                )
            except (TypeError, ValueError):
                continue
        if len(centers_world) < 64:
            return
        board_surface_world_z = float(sum(corners_world[key][2] for key in ("a1", "h1", "h8", "a8")) / 4.0)
        source = f"external_board_frame:{payload.get('source', 'unknown')}"
        self._apply_manipulation_board_model(
            source=source,
            board_outer_corners_world=corners_world,
            square_centers_world=centers_world,
            board_surface_world_z=board_surface_world_z,
        )
