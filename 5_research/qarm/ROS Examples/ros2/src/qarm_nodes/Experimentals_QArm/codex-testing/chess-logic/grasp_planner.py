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
    tcp_offset_xyz_m: tuple[float, float, float]
    marker_center_mode: bool
    marker_center_clearance_m: float

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
            tcp_offset_xyz_m=tuple(float(v) for v in payload.get("tcp_offset_xyz_m", [0.0, 0.0, 0.0])),
            marker_center_mode=bool(payload.get("marker_center_mode", False)),
            marker_center_clearance_m=float(payload.get("marker_center_clearance_m", 0.0)),
        )


class GraspPlanner:
    """Converts a validated chess move into a deterministic motion sketch."""

    def __init__(
        self,
        geometry: BoardGeometry,
        rules: GraspRules,
        *,
        square_centers_world_override: dict[str, tuple[float, float, float]] | None = None,
        board_surface_world_z_override: float | None = None,
        board_source: str = "default_board_geometry",
    ) -> None:
        self.geometry = geometry
        self.rules = rules
        self.square_centers_world_override = (
            dict(square_centers_world_override) if square_centers_world_override else None
        )
        self.board_surface_world_z_override = (
            float(board_surface_world_z_override)
            if board_surface_world_z_override is not None
            else None
        )
        self.board_source = board_source

    @classmethod
    def from_yaml(cls, geometry: BoardGeometry, path: str | Path) -> "GraspPlanner":
        """Load planner rules and construct the planner."""

        return cls(geometry=geometry, rules=GraspRules.from_yaml(path))

    def set_board_square_centers(
        self,
        *,
        square_centers_world: dict[str, tuple[float, float, float]],
        board_surface_world_z: float | None,
        board_source: str,
    ) -> None:
        """Update the active square->world map used for manipulation planning."""

        self.square_centers_world_override = dict(square_centers_world)
        self.board_surface_world_z_override = (
            float(board_surface_world_z) if board_surface_world_z is not None else None
        )
        self.board_source = board_source

    def plan_move(self, move: ChessMoveCommand) -> MotionPlan:
        """Return a grasp plan and phase list for one symbolic move."""

        grasp_plan = self.build_grasp_plan(move)

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

    def build_grasp_plan(self, move: ChessMoveCommand) -> GraspPlan:
        """Build explicit source/target manipulation targets from chess squares."""

        source_center = self._square_center_world(move.source)
        target_center = self._square_center_world(move.target)
        board_z = (
            float(self.board_surface_world_z_override)
            if self.board_surface_world_z_override is not None
            else float((source_center[2] + target_center[2]) * 0.5)
        )
        approach_height_m = float(self.rules.approach_height_m)
        lift_height_m = float(max(self.rules.lift_height_m, self.rules.approach_height_m))
        pick_height_m = float(board_z + self.rules.pick_height_offset_m)
        place_height_m = float(board_z + self.rules.place_height_offset_m)
        if self.rules.marker_center_mode:
            # Keep conservative Z policy even in marker-center bring-up mode.
            # Marker-center checks should be done with hover demos, not board-plane contact.
            min_pick_place_z = float(board_z + self.rules.marker_center_clearance_m)
            pick_height_m = max(pick_height_m, min_pick_place_z)
            place_height_m = max(place_height_m, min_pick_place_z)

        source_approach = (source_center[0], source_center[1], board_z + approach_height_m)
        source_pick = (source_center[0], source_center[1], pick_height_m)
        source_lift = (source_center[0], source_center[1], board_z + lift_height_m)
        target_approach = (target_center[0], target_center[1], board_z + approach_height_m)
        target_place = (target_center[0], target_center[1], place_height_m)
        target_retreat = (target_center[0], target_center[1], board_z + lift_height_m)

        return GraspPlan(
            source_square=move.source,
            target_square=move.target,
            source_world_xyz=source_center,
            target_world_xyz=target_center,
            source_approach_world_xyz=source_approach,
            source_pick_world_xyz=source_pick,
            source_lift_world_xyz=source_lift,
            target_approach_world_xyz=target_approach,
            target_place_world_xyz=target_place,
            target_retreat_world_xyz=target_retreat,
            approach_height_m=approach_height_m,
            lift_height_m=lift_height_m,
            pick_height_m=pick_height_m,
            place_height_m=place_height_m,
            gripper_vertical=self.rules.preferred_vertical_grasp,
            gripper_open_value=0.7,
            gripper_close_value=0.9,
        )

    def _square_center_world(self, square: str) -> tuple[float, float, float]:
        normalized = square.strip().lower()
        if self.square_centers_world_override is not None:
            center = self.square_centers_world_override.get(normalized)
            if center is None:
                raise KeyError(
                    f"Square {normalized!r} missing from active manipulation board source {self.board_source!r}."
                )
            return (float(center[0]), float(center[1]), float(center[2]))
        return self.geometry.square_center_world(normalized)

    def plan_square_transfer(
        self,
        *,
        source_square: str,
        target_square: str,
        piece_name: str | None = None,
        is_capture: bool = False,
        promotion: str | None = None,
    ) -> MotionPlan:
        """Plan direct square-to-square motion before engine/autonomy layers."""

        source = source_square.strip().lower()
        target = target_square.strip().lower()
        uci = f"{source}{target}{promotion or ''}"
        move = ChessMoveCommand(
            uci=uci,
            source=source,
            target=target,
            piece_name=piece_name,
            is_capture=is_capture,
            promotion=promotion,
        )
        return self.plan_move(move)
