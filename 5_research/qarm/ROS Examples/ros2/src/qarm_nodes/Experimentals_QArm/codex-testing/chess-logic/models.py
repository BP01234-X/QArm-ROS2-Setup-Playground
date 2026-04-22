"""Shared dataclasses for the Phase 3 chess prototype."""

from __future__ import annotations

from dataclasses import dataclass, field

XYZ = tuple[float, float, float]


@dataclass(frozen=True)
class PieceObservation:
    """Single observed piece hypothesis for one board square."""

    piece_name: str
    square: str
    world_xyz: XYZ | None
    yaw_rad: float | None
    confidence: float


@dataclass
class ObservedBoard:
    """Board snapshot generated only while the arm is at observer pose."""

    by_square: dict[str, str | None]
    observations: dict[str, PieceObservation]
    timestamp: float


@dataclass
class ExpectedBoard:
    """Symbolic board state maintained by the chess rule engine."""

    by_square: dict[str, str | None]
    fen: str
    move_number: int
    side_to_move: str


@dataclass(frozen=True)
class ChessMoveCommand:
    """A validated symbolic chess move prepared for physical execution."""

    uci: str
    source: str
    target: str
    piece_name: str | None
    is_capture: bool
    promotion: str | None


@dataclass(frozen=True)
class GraspPlan:
    """Board-square-level pick/place plan independent of ROS 2 transport."""

    source_square: str
    target_square: str
    source_world_xyz: XYZ
    target_world_xyz: XYZ
    approach_height_m: float
    pick_height_m: float
    place_height_m: float
    gripper_vertical: bool
    gripper_open_value: float = 0.7
    gripper_close_value: float = 0.9


@dataclass(frozen=True)
class MotionPlan:
    """Higher-level motion phases built from a chess move and grasp plan."""

    move: ChessMoveCommand
    grasp_plan: GraspPlan
    phases: list[str]
    notes: list[str] = field(default_factory=list)


@dataclass
class FSMStatus:
    """Public state snapshot for live orchestration and debugging."""

    state: str
    robot_busy: bool
    last_error: str | None
    pending_move_uci: str | None


@dataclass(frozen=True)
class VerificationResult:
    """Comparison result between expected and observed board states."""

    success: bool
    mismatches: list[str]
