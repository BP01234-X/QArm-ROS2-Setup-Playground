"""Deterministic top-down grasp planning for chess-piece manipulation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled at runtime
    yaml = None
    YAML_IMPORT_ERROR = exc
else:
    YAML_IMPORT_ERROR = None

from board_geometry import BoardGeometry
from models import ChessMoveCommand, GraspPlan, MotionPlan


@dataclass(frozen=True)
class GraspRules:
    """Config values for a conservative top-down chess grasp."""

    approach_height_m: float
    lift_height_m: float
    pick_height_offset_m: float
    place_height_offset_m: float
    preferred_vertical_grasp: bool
    avoid_tilt_band_deg: tuple[float, float]

    @classmethod
    def from_yaml(cls, path: str | Path) -> "GraspRules":
        """Load planner rules from YAML config."""

        if yaml is None:
            raise RuntimeError("PyYAML is required to load grasp_rules.yaml") from YAML_IMPORT_ERROR
        payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return cls(
            approach_height_m=float(payload["approach_height_m"]),
            lift_height_m=float(payload["lift_height_m"]),
            pick_height_offset_m=float(payload["pick_height_offset_m"]),
            place_height_offset_m=float(payload["place_height_offset_m"]),
            preferred_vertical_grasp=bool(payload["preferred_vertical_grasp"]),
            avoid_tilt_band_deg=tuple(float(v) for v in payload["avoid_tilt_band_deg"]),
        )


class GraspPlanner:
    """Converts a validated chess move into a deterministic motion sketch."""

    def __init__(self, geometry: BoardGeometry, rules: GraspRules) -> None:
        self.geometry = geometry
        self.rules = rules

    @classmethod
    def from_yaml(cls, geometry: BoardGeometry, path: str | Path) -> "GraspPlanner":
        """Load planner rules and construct the planner."""

        return cls(geometry=geometry, rules=GraspRules.from_yaml(path))

    def plan_move(self, move: ChessMoveCommand) -> MotionPlan:
        """Return a grasp plan and phase list for one symbolic move."""

        grasp_plan = GraspPlan(
            source_square=move.source,
            target_square=move.target,
            source_world_xyz=self.geometry.square_center_world(move.source),
            target_world_xyz=self.geometry.square_center_world(move.target),
            approach_height_m=self.rules.approach_height_m,
            pick_height_m=self.geometry.board_surface_world_z + self.rules.pick_height_offset_m,
            place_height_m=self.geometry.board_surface_world_z + self.rules.place_height_offset_m,
            gripper_vertical=self.rules.preferred_vertical_grasp,
            gripper_open_value=0.7,
            gripper_close_value=0.9,
        )

        notes = [
            "Top-down grasp only; gripper must remain vertical.",
            "Lift vertically before any lateral travel.",
            "Observer, idle, and non-contact approach states keep the gripper at 0.7.",
            "Pickup, hold, and carry states keep the gripper at 0.9 until release.",
            (
                "TODO: Add piece-height-specific grasp offsets, collision checks, "
                "and exact jaw-width planning."
            ),
        ]
        if move.is_capture:
            notes.append("TODO: Plan captured-piece removal to a graveyard area before placement.")

        return MotionPlan(
            move=move,
            grasp_plan=grasp_plan,
            phases=[
                "PLAN_MOVE",
                "MOVE_TO_PICK",
                "GRIPPER_PREPARE",
                "PICK",
                "LIFT",
                "MOVE_TO_PLACE",
                "PLACE",
                "RETREAT",
                "END_MOVEMENT",
            ],
            notes=notes,
        )
