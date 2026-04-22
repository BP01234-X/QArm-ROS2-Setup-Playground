"""Mockable physical execution layer for Phase 3."""

from __future__ import annotations

import time
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled at runtime
    yaml = None
    YAML_IMPORT_ERROR = exc
else:
    YAML_IMPORT_ERROR = None

from board_geometry import BoardGeometry
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
    ) -> None:
        self.observer_pose_name = observer_pose_name
        self.observer_world_xyz = observer_world_xyz
        self.observer_rpy = observer_rpy
        self.mock_mode = mock_mode
        self.action_duration_s = action_duration_s
        self.bridge_client = bridge_client
        self.geometry = geometry
        self.grasp_rules = grasp_rules
        self._busy_until = 0.0
        self.action_log: list[str] = []
        self.current_gripper_target: float | None = None
        self.current_pose: list[float] | None = None
        self._pending_goal_id: str | None = None
        self._pending_error: str | None = None
        self._last_grasp_plan: GraspPlan | None = None
        self._retreat_pose: list[float] | None = None

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
        config_dir = Path(path).resolve().parent
        geometry = BoardGeometry.from_yaml(config_dir / "board.yaml")
        grasp_rules = GraspRules.from_yaml(config_dir / "grasp_rules.yaml")
        return cls(
            observer_pose_name=str(payload["observer_pose_name"]),
            observer_world_xyz=tuple(float(v) for v in payload["observer_world_xyz"]),
            observer_rpy=tuple(float(v) for v in payload["observer_rpy"]),
            mock_mode=mock_mode,
            action_duration_s=action_duration_s,
            bridge_client=None if mock_mode else QArmBridgeClient(bridge_dir=bridge_dir),
            geometry=geometry,
            grasp_rules=grasp_rules,
        )

    def move_to_observer_pose(self) -> None:
        """Command the arm to the fixed board observer pose."""

        target_pose = [
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
            goal_pose=target_pose,
            note=f"Phase 3 move to observer pose '{self.observer_pose_name}'.",
        )

    def move_to_square_above(self, square: str) -> None:
        """Move to an approach pose above the given square."""

        self._require_geometry()
        self._require_grasp_rules()
        center_world = self.geometry.square_center_world(square)
        target_pose = [
            float(center_world[0]),
            float(center_world[1]),
            float(self.geometry.board_surface_world_z + self.grasp_rules.approach_height_m),
            float(self.observer_rpy[2]),
        ]
        self._dispatch_pose(
            action_description=f"move_to_square_above square={square}",
            goal_pose=target_pose,
            note=f"Phase 3 approach above square {square}.",
        )

    def execute_pick(self, grasp_plan: GraspPlan) -> None:
        """Execute the downward pick motion.

        Gripper state is handled explicitly by the orchestrator so the move flow
        makes the 0.7/0.9 policy visible in logs and state transitions.
        """

        self._last_grasp_plan = grasp_plan
        target_pose = [
            float(grasp_plan.source_world_xyz[0]),
            float(grasp_plan.source_world_xyz[1]),
            float(grasp_plan.pick_height_m),
            float(self.observer_rpy[2]),
        ]
        self._dispatch_pose(
            action_description=(
                f"execute_pick square={grasp_plan.source_square} "
                f"pick_height_m={grasp_plan.pick_height_m:.3f}"
            ),
            goal_pose=target_pose,
            note=f"Phase 3 descend to pick on {grasp_plan.source_square}.",
        )

    def lift_piece(self, grasp_plan: GraspPlan) -> None:
        """Lift vertically after grasping the source piece."""

        self._last_grasp_plan = grasp_plan
        target_pose = [
            float(grasp_plan.source_world_xyz[0]),
            float(grasp_plan.source_world_xyz[1]),
            float(self.geometry.board_surface_world_z + grasp_plan.approach_height_m),
            float(self.observer_rpy[2]),
        ]
        self._dispatch_pose(
            action_description=(
                f"lift_piece square={grasp_plan.source_square} "
                f"approach_height_m={grasp_plan.approach_height_m:.3f}"
            ),
            goal_pose=target_pose,
            note=f"Phase 3 vertical lift from {grasp_plan.source_square}.",
        )

    def execute_place(self, grasp_plan: GraspPlan) -> None:
        """Execute the downward place motion.

        Gripper release is handled explicitly by the orchestrator so reopening to
        0.7 happens before retreat.
        """

        self._last_grasp_plan = grasp_plan
        self._retreat_pose = [
            float(grasp_plan.target_world_xyz[0]),
            float(grasp_plan.target_world_xyz[1]),
            float(self.geometry.board_surface_world_z + grasp_plan.approach_height_m),
            float(self.observer_rpy[2]),
        ]
        target_pose = [
            float(grasp_plan.target_world_xyz[0]),
            float(grasp_plan.target_world_xyz[1]),
            float(grasp_plan.place_height_m),
            float(self.observer_rpy[2]),
        ]
        self._dispatch_pose(
            action_description=(
                f"execute_place square={grasp_plan.target_square} "
                f"place_height_m={grasp_plan.place_height_m:.3f}"
            ),
            goal_pose=target_pose,
            note=f"Phase 3 descend to place on {grasp_plan.target_square}.",
        )

    def retreat(self) -> None:
        """Move upward safely after placing the piece."""

        retreat_pose = self._retreat_pose
        if retreat_pose is None:
            if self._last_grasp_plan is None:
                raise RuntimeError("Retreat requested without a prior place target.")
            retreat_pose = [
                float(self._last_grasp_plan.target_world_xyz[0]),
                float(self._last_grasp_plan.target_world_xyz[1]),
                float(self.geometry.board_surface_world_z + self._last_grasp_plan.approach_height_m),
                float(self.observer_rpy[2]),
            ]
        self._dispatch_pose(
            action_description="retreat_vertical",
            goal_pose=retreat_pose,
            note="Phase 3 upward retreat after placement.",
        )

    def set_gripper(self, position: float) -> None:
        """Set the gripper target position.

        TODO: Replace this mock log with the real Phase 2 gripper command path.
        """

        self.current_gripper_target = float(position)
        if self.mock_mode:
            self._start_action(f"set_gripper({self.current_gripper_target:.1f})")
            return

        goal_pose = self._best_known_pose_for_gripper()
        goal_id = self._send_real_command(
            action_description=f"set_gripper({self.current_gripper_target:.1f})",
            goal_pose=goal_pose,
            gripper=self.current_gripper_target,
            note=f"Phase 3 set gripper to {self.current_gripper_target:.1f}.",
            goal_prefix="phase3-gripper",
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

    def wait_until_done(self, timeout_s: float = 5.0, poll_interval_s: float = 0.01) -> None:
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

    def _dispatch_pose(self, *, action_description: str, goal_pose: list[float], note: str) -> None:
        """Send a pose command through the active executor mode."""

        if self.mock_mode:
            self.current_pose = [float(value) for value in goal_pose]
            self._start_action(action_description)
            return

        goal_id = self._send_real_command(
            action_description=action_description,
            goal_pose=goal_pose,
            gripper=None,
            note=note,
            goal_prefix="phase3-move",
        )
        self._pending_goal_id = goal_id
        self._pending_error = None

    def _send_real_command(
        self,
        *,
        action_description: str,
        goal_pose: list[float],
        gripper: float | None,
        note: str,
        goal_prefix: str,
    ) -> str:
        """Send a real bridge command through `target_pose.json`."""

        self._require_bridge_client()
        normalized_pose = [float(value) for value in goal_pose]
        self._start_action(action_description)
        goal_id = self.bridge_client.send_command(
            goal_pose=normalized_pose,
            gripper=gripper,
            note=note,
            goal_id=self.bridge_client.build_goal_id(goal_prefix),
            enabled=True,
        )
        self.current_pose = normalized_pose
        return goal_id

    def _is_real_motion_done(self) -> bool:
        """Poll `status.json` for the current real command."""

        if self._pending_goal_id is None:
            return True
        self._require_bridge_client()
        done, error, status = self.bridge_client.command_state(self._pending_goal_id)
        if not done:
            return False
        self._pending_error = error
        active_goal_pose = status.get("active_goal_pose")
        if isinstance(active_goal_pose, list) and len(active_goal_pose) == 4:
            self.current_pose = [float(value) for value in active_goal_pose]
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

    def _require_bridge_client(self) -> None:
        """Fail fast if real mode is selected without a bridge client."""

        if self.bridge_client is None:
            raise RuntimeError("Real MoveExecutor mode requires a QArmBridgeClient.")

    def _require_geometry(self) -> None:
        """Fail fast if geometry data is missing."""

        if self.geometry is None:
            raise RuntimeError("MoveExecutor requires board geometry.")

    def _require_grasp_rules(self) -> None:
        """Fail fast if grasp rules are missing."""

        if self.grasp_rules is None:
            raise RuntimeError("MoveExecutor requires grasp rules.")
