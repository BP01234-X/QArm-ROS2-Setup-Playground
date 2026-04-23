"""Mockable physical execution layer for Phase 3."""

from __future__ import annotations

import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled at runtime
    yaml = None
    YAML_IMPORT_ERROR = exc
else:
    YAML_IMPORT_ERROR = None

from board_geometry import BoardGeometry
from calibrated_board_model import load_fixed_calibrated_board_model
from grasp_planner import GraspRules
from models import GraspPlan
from qarm_bridge_client import QArmBridgeClient


class MoveExecutor:
    """Abstracted physical move executor with a pure-Python mock mode.

    TODO: Replace the mock action log with real ROS 2 action/service/topic calls
    once the Phase 3 prototype is approved.
    """

    def __init__(
        self,
        observer_pose_name: str,
        observer_world_xyz: tuple[float, float, float],
        observer_rpy: tuple[float, float, float],
        mock_mode: bool = True,
        action_duration_s: float = 0.05,
        bridge_client: QArmBridgeClient | None = None,
        geometry: BoardGeometry | None = None,
        grasp_rules: GraspRules | None = None,
        command_frame_name: str = "world",
        command_units: str = "m",
        tcp_offset_xyz_m: tuple[float, float, float] = (0.0, 0.0, 0.0),
        trace_file: str | Path | None = None,
        postcheck_position_tolerance_m: float = 0.012,
        postcheck_orientation_tolerance_rad: float = 0.03,
        postcheck_timeout_s: float = 3.5,
        postcheck_poll_interval_s: float = 0.05,
    ) -> None:
        self.observer_pose_name = observer_pose_name
        self.observer_world_xyz = observer_world_xyz
        self.observer_rpy = observer_rpy
        self.mock_mode = mock_mode
        self.action_duration_s = action_duration_s
        self.bridge_client = bridge_client
        self.geometry = geometry
        self.grasp_rules = grasp_rules
        self.command_frame_name = command_frame_name
        self.command_units = command_units
        self.tcp_offset_xyz_m = (
            float(tcp_offset_xyz_m[0]),
            float(tcp_offset_xyz_m[1]),
            float(tcp_offset_xyz_m[2]),
        )
        self.postcheck_position_tolerance_m = float(postcheck_position_tolerance_m)
        self.postcheck_orientation_tolerance_rad = float(postcheck_orientation_tolerance_rad)
        self.postcheck_timeout_s = float(postcheck_timeout_s)
        self.postcheck_poll_interval_s = float(postcheck_poll_interval_s)
        self._busy_until = 0.0
        self.action_log: list[str] = []
        self.current_gripper_target: float | None = None
        self.current_pose: list[float] | None = None
        self._pending_goal_id: str | None = None
        self._pending_error: str | None = None
        self._pending_goal_pose_by_id: dict[str, list[float]] = {}
        self._pending_pose_check_by_id: dict[str, bool] = {}
        self._last_grasp_plan: GraspPlan | None = None
        self._retreat_pose: list[float] | None = None
        self.square_centers_world_override: dict[str, tuple[float, float, float]] | None = None
        self.board_source: str = "default_board_geometry"
        self.trace_file = Path(trace_file).expanduser().resolve() if trace_file is not None else None
        self._trace_commands: list[dict[str, object]] = []
        self._pending_trace_indices: dict[str, int] = {}

    @classmethod
    def from_yaml(
        cls,
        path: str | Path,
        mock_mode: bool = True,
        action_duration_s: float = 0.05,
        bridge_dir: str | Path | None = None,
    ) -> "MoveExecutor":
        """Load observer-pose settings from YAML config."""

        if yaml is None:
            raise RuntimeError("PyYAML is required to load observer_pose.yaml") from YAML_IMPORT_ERROR
        payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        observer_name, observer_xyz, observer_rpy = cls._resolve_observer_pose(payload)
        config_dir = Path(path).resolve().parent
        geometry = BoardGeometry.from_yaml(config_dir / "board.yaml")
        grasp_rules = GraspRules.from_yaml(config_dir / "grasp_rules.yaml")
        bridge_client = None if mock_mode else QArmBridgeClient(bridge_dir=bridge_dir)
        executor = cls(
            observer_pose_name=observer_name,
            observer_world_xyz=observer_xyz,
            observer_rpy=observer_rpy,
            mock_mode=mock_mode,
            action_duration_s=action_duration_s,
            bridge_client=bridge_client,
            geometry=geometry,
            grasp_rules=grasp_rules,
            command_frame_name="world",
            command_units="m",
            tcp_offset_xyz_m=grasp_rules.tcp_offset_xyz_m,
            trace_file=(
                None
                if mock_mode
                else (bridge_client.paths.bridge_dir / "command_trace.json")
            ),
        )
        fixed_board_model = load_fixed_calibrated_board_model(
            config_dir=config_dir,
            geometry=geometry,
        )
        executor.set_board_square_centers(
            square_centers_world=fixed_board_model.square_centers_world,
            board_source=fixed_board_model.source,
        )
        return executor

    @staticmethod
    def _resolve_observer_pose(payload: dict) -> tuple[str, tuple[float, float, float], tuple[float, float, float]]:
        """Resolve the active observer pose from either legacy or candidate config."""

        if "observer_pose_candidates" in payload:
            selected_name = str(payload.get("default_observer_pose") or payload["observer_pose_name"])
            candidates = payload["observer_pose_candidates"]
            if selected_name not in candidates:
                available = ", ".join(sorted(candidates))
                raise KeyError(
                    f"Observer pose {selected_name!r} not found in observer_pose_candidates. "
                    f"Available: {available}"
                )
            selected = candidates[selected_name]
            return (
                selected_name,
                tuple(float(v) for v in selected["observer_world_xyz"]),
                tuple(float(v) for v in selected["observer_rpy"]),
            )

        return (
            str(payload["observer_pose_name"]),
            tuple(float(v) for v in payload["observer_world_xyz"]),
            tuple(float(v) for v in payload["observer_rpy"]),
        )

    def move_to_observer_pose(self) -> None:
        """Command the arm to the fixed board observer pose."""

        planner_pose = [
            float(self.observer_world_xyz[0]),
            float(self.observer_world_xyz[1]),
            float(self.observer_world_xyz[2]),
            float(self.observer_rpy[2]),
        ]
        self._dispatch_pose(
            action_description=(
                f"move_to_observer_pose name={self.observer_pose_name} "
                f"xyz={self.observer_world_xyz} rpy={self.observer_rpy}"
            ),
            planner_pose=planner_pose,
            note=f"Phase 3 move to observer pose '{self.observer_pose_name}'.",
            stage_name="observer_pose",
            apply_tcp_offset=False,
        )

    def move_to_world_pose(
        self,
        *,
        stage_name: str,
        world_xyz: tuple[float, float, float],
        yaw_rad: float | None = None,
        note: str = "",
    ) -> None:
        """Move to one explicit world pose from the planner without re-lookup."""

        planner_pose = [
            float(world_xyz[0]),
            float(world_xyz[1]),
            float(world_xyz[2]),
            float(self.observer_rpy[2] if yaw_rad is None else yaw_rad),
        ]
        self._dispatch_pose(
            action_description=f"move_to_world_pose stage={stage_name} xyz={tuple(world_xyz)}",
            planner_pose=planner_pose,
            note=note or f"Phase 3 explicit world-pose command for stage {stage_name}.",
            stage_name=stage_name,
            apply_tcp_offset=True,
        )

    def move_to_square_above(self, square: str, height_m: float | None = None) -> None:
        """Move to an approach pose above the given square."""

        self._require_grasp_rules()
        center_world = self._square_center_world(square)
        approach_height = (
            float(self.grasp_rules.approach_height_m)
            if height_m is None
            else float(height_m)
        )
        planner_pose = [
            float(center_world[0]),
            float(center_world[1]),
            float(center_world[2] + approach_height),
            float(self.observer_rpy[2]),
        ]
        self._dispatch_pose(
            action_description=f"move_to_square_above square={square} height_m={approach_height:.3f}",
            planner_pose=planner_pose,
            note=f"Phase 3 approach above square {square}.",
            stage_name=f"square_above_{square.strip().lower()}",
            apply_tcp_offset=True,
        )

    def set_board_square_centers(
        self,
        *,
        square_centers_world: dict[str, tuple[float, float, float]],
        board_source: str,
    ) -> None:
        """Set square centers used by square-addressed movement calls."""

        self.square_centers_world_override = dict(square_centers_world)
        self.board_source = board_source

    def execute_pick(self, grasp_plan: GraspPlan) -> None:
        """Execute the downward pick motion.

        Gripper state is handled explicitly by the orchestrator so the move flow
        makes the 0.7/0.9 policy visible in logs and state transitions.
        """

        self._last_grasp_plan = grasp_plan
        planner_pose = [
            float(grasp_plan.source_pick_world_xyz[0]),
            float(grasp_plan.source_pick_world_xyz[1]),
            float(grasp_plan.source_pick_world_xyz[2]),
            float(self.observer_rpy[2]),
        ]
        self._dispatch_pose(
            action_description=(
                f"execute_pick square={grasp_plan.source_square} "
                f"pick_height_m={grasp_plan.pick_height_m:.3f}"
            ),
            planner_pose=planner_pose,
            note=f"Phase 3 descend to pick on {grasp_plan.source_square}.",
            stage_name=f"pick_{grasp_plan.source_square}",
            apply_tcp_offset=True,
        )

    def lift_piece(self, grasp_plan: GraspPlan) -> None:
        """Lift vertically after grasping the source piece."""

        self._last_grasp_plan = grasp_plan
        planner_pose = [
            float(grasp_plan.source_lift_world_xyz[0]),
            float(grasp_plan.source_lift_world_xyz[1]),
            float(grasp_plan.source_lift_world_xyz[2]),
            float(self.observer_rpy[2]),
        ]
        self._dispatch_pose(
            action_description=(
                f"lift_piece square={grasp_plan.source_square} "
                f"lift_height_m={grasp_plan.lift_height_m:.3f}"
            ),
            planner_pose=planner_pose,
            note=f"Phase 3 vertical lift from {grasp_plan.source_square}.",
            stage_name=f"lift_{grasp_plan.source_square}",
            apply_tcp_offset=True,
        )

    def execute_place(self, grasp_plan: GraspPlan) -> None:
        """Execute the downward place motion.

        Gripper release is handled explicitly by the orchestrator so reopening to
        0.7 happens before retreat.
        """

        self._last_grasp_plan = grasp_plan
        self._retreat_pose = [
            float(grasp_plan.target_retreat_world_xyz[0]),
            float(grasp_plan.target_retreat_world_xyz[1]),
            float(grasp_plan.target_retreat_world_xyz[2]),
            float(self.observer_rpy[2]),
        ]
        planner_pose = [
            float(grasp_plan.target_place_world_xyz[0]),
            float(grasp_plan.target_place_world_xyz[1]),
            float(grasp_plan.target_place_world_xyz[2]),
            float(self.observer_rpy[2]),
        ]
        self._dispatch_pose(
            action_description=(
                f"execute_place square={grasp_plan.target_square} "
                f"place_height_m={grasp_plan.place_height_m:.3f}"
            ),
            planner_pose=planner_pose,
            note=f"Phase 3 descend to place on {grasp_plan.target_square}.",
            stage_name=f"place_{grasp_plan.target_square}",
            apply_tcp_offset=True,
        )

    def retreat(self) -> None:
        """Move upward safely after placing the piece."""

        retreat_pose = self._retreat_pose
        if retreat_pose is None:
            if self._last_grasp_plan is None:
                raise RuntimeError("Retreat requested without a prior place target.")
            retreat_pose = [
                float(self._last_grasp_plan.target_retreat_world_xyz[0]),
                float(self._last_grasp_plan.target_retreat_world_xyz[1]),
                float(self._last_grasp_plan.target_retreat_world_xyz[2]),
                float(self.observer_rpy[2]),
            ]
        self._dispatch_pose(
            action_description="retreat_vertical",
            planner_pose=retreat_pose,
            note="Phase 3 upward retreat after placement.",
            stage_name="retreat_vertical",
            apply_tcp_offset=True,
        )

    def set_gripper(self, position: float) -> None:
        """Set the gripper target position.

        TODO: Replace this mock log with the real Phase 2 gripper command path.
        """

        requested = float(position)
        if self.current_gripper_target is not None and abs(self.current_gripper_target - requested) <= 1e-6:
            prefix = "MOCK" if self.mock_mode else "REAL"
            self.action_log.append(f"{prefix}: set_gripper({requested:.1f}) skipped (already set)")
            return
        self.current_gripper_target = requested
        if self.mock_mode:
            self._start_action(f"set_gripper({self.current_gripper_target:.1f})")
            return

        goal_pose = self._best_known_pose_for_gripper()
        goal_id = self._send_real_command(
            action_description=f"set_gripper({self.current_gripper_target:.1f})",
            goal_pose=goal_pose,
            planner_pose=None,
            gripper=self.current_gripper_target,
            note=f"Phase 3 set gripper to {self.current_gripper_target:.1f}.",
            goal_prefix="phase3-gripper",
            stage_name="gripper_command",
            apply_tcp_offset=False,
        )
        self._pending_goal_id = goal_id
        self._pending_error = None

    def open_gripper(self) -> None:
        """Convenience wrapper for the safe travel/open value."""

        self.set_gripper(0.7)

    def close_gripper(self) -> None:
        """Convenience wrapper for the pickup/hold value."""

        self.set_gripper(0.9)

    def is_motion_done(self) -> bool:
        """Return whether the most recent action has completed."""

        if not self.mock_mode:
            return self._is_real_motion_done()
        return time.time() >= self._busy_until

    def wait_until_done(self, timeout_s: float = 20.0, poll_interval_s: float = 0.01) -> None:
        """Block until the current action completes in mock mode."""

        if not self.mock_mode:
            deadline = time.time() + timeout_s
            while not self.is_motion_done():
                if time.time() > deadline:
                    raise TimeoutError("Real bridge motion did not finish before timeout.")
                time.sleep(poll_interval_s)
            if self._pending_error is not None:
                error = self._pending_error
                self._pending_error = None
                raise RuntimeError(error)
            return

        deadline = time.time() + timeout_s
        while not self.is_motion_done():
            if time.time() > deadline:
                raise TimeoutError("Mock motion did not finish before timeout.")
            time.sleep(poll_interval_s)

    def _start_action(self, description: str) -> None:
        """Record a mock action and mark the executor busy briefly."""

        prefix = "MOCK" if self.mock_mode else "REAL"
        self.action_log.append(f"{prefix}: {description}")
        if self.mock_mode:
            self._busy_until = max(time.time(), self._busy_until) + self.action_duration_s

    def _dispatch_pose(
        self,
        *,
        action_description: str,
        planner_pose: list[float],
        note: str,
        stage_name: str,
        apply_tcp_offset: bool,
    ) -> None:
        """Send a pose command through the active executor mode."""

        planner_pose_normalized = [float(value) for value in planner_pose]
        commanded_pose = (
            self._apply_tcp_offset(planner_pose_normalized)
            if apply_tcp_offset
            else planner_pose_normalized
        )
        if self.mock_mode:
            self.current_pose = [float(value) for value in commanded_pose]
            self.action_log.append(
                "MOCK: pose_trace "
                f"stage={stage_name} planner={tuple(planner_pose_normalized)} "
                f"tcp_corrected={tuple(commanded_pose)} frame={self.command_frame_name} units={self.command_units}"
            )
            self._start_action(action_description)
            return

        goal_id = self._send_real_command(
            action_description=action_description,
            goal_pose=commanded_pose,
            planner_pose=planner_pose_normalized,
            gripper=None,
            note=note,
            goal_prefix="phase3-move",
            stage_name=stage_name,
            apply_tcp_offset=apply_tcp_offset,
        )
        self._pending_goal_id = goal_id
        self._pending_error = None

    def _send_real_command(
        self,
        *,
        action_description: str,
        goal_pose: list[float],
        planner_pose: list[float] | None,
        gripper: float | None,
        note: str,
        goal_prefix: str,
        stage_name: str,
        apply_tcp_offset: bool,
    ) -> str:
        """Send a real bridge command through `target_pose.json`."""

        self._require_bridge_client()
        normalized_pose = [float(value) for value in goal_pose]
        normalized_planner_pose = (
            [float(value) for value in planner_pose] if planner_pose is not None else None
        )
        self._start_action(action_description)
        self.action_log.append(
            "REAL: pose_trace "
            f"stage={stage_name} planner={tuple(normalized_planner_pose) if normalized_planner_pose is not None else None} "
            f"tcp_offset={self.tcp_offset_xyz_m} tcp_applied={apply_tcp_offset} "
            f"tcp_corrected={tuple(normalized_pose)} frame={self.command_frame_name} units={self.command_units}"
        )
        goal_id = self.bridge_client.send_command(
            goal_pose=normalized_pose,
            gripper=gripper,
            note=note,
            goal_id=self.bridge_client.build_goal_id(goal_prefix),
            enabled=True,
        )
        target_file_pose = self._read_target_file_goal_pose()
        self.action_log.append(
            f"REAL: bridge_goal_pose={tuple(normalized_pose)} target_file_pose={target_file_pose} goal_id={goal_id}"
        )
        self._append_trace_command(
            {
                "timestamp_utc": self._utc_now_iso(),
                "stage": stage_name,
                "action_description": action_description,
                "frame_name": self.command_frame_name,
                "units": self.command_units,
                "planner_pose": normalized_planner_pose,
                "tcp_offset_xyz_m": list(self.tcp_offset_xyz_m),
                "tcp_offset_applied": bool(apply_tcp_offset),
                "tcp_corrected_pose": normalized_pose,
                "bridge_goal_pose": normalized_pose,
                "target_file_goal_pose": target_file_pose,
                "goal_id": goal_id,
                "gripper": gripper,
                "status_state": "sent",
            }
        )
        self._pending_goal_pose_by_id[goal_id] = list(normalized_pose)
        self._pending_pose_check_by_id[goal_id] = bool(gripper is None)
        self.current_pose = normalized_pose
        return goal_id

    def _is_real_motion_done(self) -> bool:
        """Poll `status.json` for the current real command."""

        if self._pending_goal_id is None:
            return True
        self._require_bridge_client()
        goal_id = self._pending_goal_id
        done, error, status = self.bridge_client.command_state(goal_id)
        if not done:
            return False
        self._pending_error = error
        active_goal_pose = status.get("active_goal_pose")
        consumed_pose: list[float] | None = None
        if isinstance(active_goal_pose, list) and len(active_goal_pose) == 4:
            consumed_pose = [float(value) for value in active_goal_pose]
            self.current_pose = list(consumed_pose)
        if goal_id is not None:
            self._mark_trace_done(
                goal_id=goal_id,
                status=status,
                consumed_pose=consumed_pose,
                error=error,
            )
        expected_pose = self._pending_goal_pose_by_id.pop(goal_id, None)
        pose_check_required = self._pending_pose_check_by_id.pop(goal_id, False)
        if error is None and pose_check_required and expected_pose is not None:
            pose_check_error = self._postcheck_live_pose(goal_id=goal_id, expected_pose=expected_pose)
            if pose_check_error is not None:
                self._pending_error = pose_check_error
        self._pending_goal_id = None
        return True

    def _best_known_pose_for_gripper(self) -> list[float]:
        """Return the safest current pose to pair with a gripper update."""

        if self.current_pose is not None:
            return [float(value) for value in self.current_pose]
        self._require_bridge_client()
        known_pose = self.bridge_client.best_known_pose()
        if known_pose is not None:
            self.current_pose = [float(value) for value in known_pose]
            return [float(value) for value in known_pose]
        return [
            float(self.observer_world_xyz[0]),
            float(self.observer_world_xyz[1]),
            float(self.observer_world_xyz[2]),
            float(self.observer_rpy[2]),
        ]

    def _apply_tcp_offset(self, planner_pose: list[float]) -> list[float]:
        """Convert planner grasp-point pose into tool-origin command pose."""

        x, y, z, yaw = (float(planner_pose[0]), float(planner_pose[1]), float(planner_pose[2]), float(planner_pose[3]))
        off_x, off_y, off_z = self.tcp_offset_xyz_m
        if abs(off_x) <= 1e-9 and abs(off_y) <= 1e-9 and abs(off_z) <= 1e-9:
            return [x, y, z, yaw]
        cos_yaw = math.cos(yaw)
        sin_yaw = math.sin(yaw)
        world_off_x = cos_yaw * off_x - sin_yaw * off_y
        world_off_y = sin_yaw * off_x + cos_yaw * off_y
        world_off_z = off_z
        return [x - world_off_x, y - world_off_y, z - world_off_z, yaw]

    def _postcheck_live_pose(self, *, goal_id: str, expected_pose: list[float]) -> str | None:
        """Validate that live task-space pose actually converged to the commanded target."""

        self._require_bridge_client()
        deadline = time.time() + self.postcheck_timeout_s
        last_live_pose: list[float] | None = None
        last_pos_err: float | None = None
        last_yaw_err: float | None = None
        last_status: dict[str, object] | None = None
        while time.time() <= deadline:
            try:
                status = self.bridge_client.read_status()
            except RuntimeError:
                time.sleep(self.postcheck_poll_interval_s)
                continue
            last_status = status
            active_goal_id = status.get("active_goal_id")
            state = str(status.get("state", "")).lower()
            # The bridge can leave terminal state and clear active_goal_id quickly.
            # Do not require active_goal_id match once a terminal status is visible.
            if active_goal_id != goal_id and state not in {"succeeded", "idle"}:
                time.sleep(self.postcheck_poll_interval_s)
                continue
            live_pose_raw = status.get("live_task_space_pose")
            if isinstance(live_pose_raw, list) and len(live_pose_raw) == 4:
                live_pose = [float(value) for value in live_pose_raw]
                position_error_m = math.sqrt(
                    (live_pose[0] - expected_pose[0]) ** 2
                    + (live_pose[1] - expected_pose[1]) ** 2
                    + (live_pose[2] - expected_pose[2]) ** 2
                )
                yaw_error_rad = self._angle_abs_diff(live_pose[3], expected_pose[3])
                last_live_pose = live_pose
                last_pos_err = position_error_m
                last_yaw_err = yaw_error_rad
                if (
                    position_error_m <= self.postcheck_position_tolerance_m
                    and yaw_error_rad <= self.postcheck_orientation_tolerance_rad
                ):
                    self.action_log.append(
                        "REAL: postcheck_ok "
                        f"goal_id={goal_id} position_error_m={position_error_m:.4f} "
                        f"yaw_error_rad={yaw_error_rad:.4f}"
                    )
                    return None
            time.sleep(self.postcheck_poll_interval_s)
        if last_live_pose is None:
            status_pose = None
            if isinstance(last_status, dict):
                status_pose_raw = last_status.get("active_goal_pose")
                if isinstance(status_pose_raw, list) and len(status_pose_raw) == 4:
                    status_pose = [float(value) for value in status_pose_raw]
            if status_pose is not None:
                position_error_m = math.sqrt(
                    (status_pose[0] - expected_pose[0]) ** 2
                    + (status_pose[1] - expected_pose[1]) ** 2
                    + (status_pose[2] - expected_pose[2]) ** 2
                )
                yaw_error_rad = self._angle_abs_diff(status_pose[3], expected_pose[3])
                if (
                    position_error_m <= self.postcheck_position_tolerance_m
                    and yaw_error_rad <= self.postcheck_orientation_tolerance_rad
                ):
                    self.action_log.append(
                        "REAL: postcheck_fallback_ok "
                        f"goal_id={goal_id} source=active_goal_pose "
                        f"position_error_m={position_error_m:.4f} yaw_error_rad={yaw_error_rad:.4f}"
                    )
                    return None
                return (
                    f"Postcheck failed for {goal_id}: fallback status pose is outside tolerance "
                    f"(position_error_m={position_error_m:.4f}, yaw_error_rad={yaw_error_rad:.4f}, "
                    f"tol_pos_m={self.postcheck_position_tolerance_m:.4f}, "
                    f"tol_yaw_rad={self.postcheck_orientation_tolerance_rad:.4f}, "
                    f"expected={expected_pose}, status_pose={status_pose})."
                )
            self.action_log.append(
                "REAL: postcheck_skipped "
                f"goal_id={goal_id} reason=no_live_task_space_pose_within_{self.postcheck_timeout_s:.1f}s"
            )
            return None
        return (
            f"Postcheck failed for {goal_id}: commanded pose was not reached tightly enough "
            f"(position_error_m={last_pos_err:.4f}, yaw_error_rad={last_yaw_err:.4f}, "
            f"tol_pos_m={self.postcheck_position_tolerance_m:.4f}, "
            f"tol_yaw_rad={self.postcheck_orientation_tolerance_rad:.4f}, "
            f"expected={expected_pose}, live={last_live_pose})."
        )

    @staticmethod
    def _angle_abs_diff(a: float, b: float) -> float:
        """Smallest absolute wrapped-angle difference in radians."""

        return abs((a - b + math.pi) % (2.0 * math.pi) - math.pi)

    def _append_trace_command(self, entry: dict[str, object]) -> None:
        """Append one command trace entry and persist it for RViz/debug tools."""

        self._trace_commands.append(entry)
        if len(self._trace_commands) > 400:
            self._trace_commands = self._trace_commands[-400:]
        goal_id = entry.get("goal_id")
        if isinstance(goal_id, str):
            self._pending_trace_indices[goal_id] = len(self._trace_commands) - 1
        self._write_trace_file()

    def _mark_trace_done(
        self,
        *,
        goal_id: str,
        status: dict[str, object],
        consumed_pose: list[float] | None,
        error: str | None,
    ) -> None:
        """Update one trace entry after bridge completion feedback is available."""

        index = self._pending_trace_indices.pop(goal_id, None)
        if index is None or not (0 <= index < len(self._trace_commands)):
            return
        entry = dict(self._trace_commands[index])
        entry["done_timestamp_utc"] = self._utc_now_iso()
        entry["status_state"] = status.get("state")
        entry["status_message"] = status.get("message")
        entry["bridge_consumed_pose"] = consumed_pose
        entry["error"] = error
        self._trace_commands[index] = entry
        self.action_log.append(
            "REAL: bridge_feedback "
            f"goal_id={goal_id} state={status.get('state')} "
            f"message={status.get('message')} consumed_pose={consumed_pose} error={error}"
        )
        self._write_trace_file()

    def _write_trace_file(self) -> None:
        """Persist command trace to JSON for external debug publishers."""

        if self.trace_file is None:
            return
        payload = {
            "frame_name": self.command_frame_name,
            "units": self.command_units,
            "tcp_offset_xyz_m": list(self.tcp_offset_xyz_m),
            "updated_at_utc": self._utc_now_iso(),
            "commands": self._trace_commands,
        }
        self.trace_file.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.trace_file.with_suffix(self.trace_file.suffix + ".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        tmp_path.replace(self.trace_file)

    def _read_target_file_goal_pose(self) -> list[float] | None:
        """Read the latest goal_pose from target_pose.json for trace parity checks."""

        if self.bridge_client is None:
            return None
        try:
            payload = json.loads(self.bridge_client.paths.target_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        raw_pose = payload.get("goal_pose")
        if not isinstance(raw_pose, list) or len(raw_pose) != 4:
            return None
        try:
            return [float(value) for value in raw_pose]
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _utc_now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _require_bridge_client(self) -> None:
        """Fail fast if real mode is selected without a bridge client."""

        if self.bridge_client is None:
            raise RuntimeError("Real MoveExecutor mode requires a QArmBridgeClient.")

    def _require_geometry(self) -> None:
        """Fail fast if geometry data is missing."""

        if self.geometry is None:
            raise RuntimeError("MoveExecutor requires board geometry.")

    def _square_center_world(self, square: str) -> tuple[float, float, float]:
        """Resolve square center from calibrated override map or board.yaml geometry."""

        normalized = square.strip().lower()
        if self.square_centers_world_override is not None:
            center = self.square_centers_world_override.get(normalized)
            if center is None:
                raise KeyError(
                    f"Square {normalized!r} missing from active executor board source {self.board_source!r}."
                )
            return (float(center[0]), float(center[1]), float(center[2]))
        self._require_geometry()
        return self.geometry.square_center_world(normalized)

    def _require_grasp_rules(self) -> None:
        """Fail fast if grasp rules are missing."""

        if self.grasp_rules is None:
            raise RuntimeError("MoveExecutor requires grasp rules.")
