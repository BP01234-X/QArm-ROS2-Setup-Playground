"""High-level one-move-at-a-time coordinator for Phase 3."""

from __future__ import annotations

from pathlib import Path

from ascii_display import AsciiDisplay
from board_geometry import BoardGeometry
from board_observer import BoardObserver
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
        self.geometry = BoardGeometry.from_yaml(base_dir / "board.yaml")
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

    def boot(self) -> ObservedBoard:
        """Initialize interfaces, move to observer pose, and seed the board."""

        self._transition(Events.BOOT)
        self.board_observer.freeze()
        self._run_action(lambda: self.move_executor.set_gripper(0.7))
        self._run_action(self.move_executor.move_to_observer_pose)
        self._transition(Events.REACHED_OBSERVER_POSE)
        self.board_observer.allow_observation()
        observed = self.board_observer.observe_board()
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

    def execute_one_move(
        self,
        move_text: str,
        verification_board: dict[str, str | None] | None = None,
    ) -> VerificationResult:
        """Run the full one-move flow from plan through observer verification."""

        if self.motion_fsm.status.state != States.IDLE.value:
            raise RuntimeError(f"Cannot accept a move while state={self.motion_fsm.status.state}")

        uci = self.receive_move_from_user(move_text)
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
        self.last_motion_plan = self.grasp_planner.plan_move(move_command)
        grasp_plan = self.last_motion_plan.grasp_plan

        self._transition(Events.MOVE_PLANNED)
        self.board_observer.freeze()
        self._run_action(lambda: self.move_executor.set_gripper(grasp_plan.gripper_open_value))

        self._run_step(
            action=lambda: self.move_executor.move_to_square_above(grasp_plan.source_square),
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
            action=lambda: self.move_executor.move_to_square_above(grasp_plan.target_square),
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
        if self.last_motion_plan is not None:
            lines.append(f"PLANNED PHASES | {' -> '.join(self.last_motion_plan.phases)}")
            lines.append(
                "PLANNED GRIPPER | "
                f"open={self.last_motion_plan.grasp_plan.gripper_open_value:.1f} "
                f"close={self.last_motion_plan.grasp_plan.gripper_close_value:.1f}"
            )
        lines.append(f"FEN | {self.chess_logic.fen_summary()}")
        lines.append(f"HISTORY | {self.chess_logic.move_history_summary()}")
        return "\n".join(lines)

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
