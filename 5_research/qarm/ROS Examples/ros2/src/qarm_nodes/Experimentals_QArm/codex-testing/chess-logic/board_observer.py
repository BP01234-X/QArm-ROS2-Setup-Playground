"""Board observation pipeline with mock and camera-backed modes.

This module stays outside ROS 2 node registration. It provides a pure-Python
integration layer that can be called only while the FSM is in
`CHESS_OBSERVER`.
"""

from __future__ import annotations

import math
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from board_geometry import BoardGeometry
from models import ObservedBoard, PieceObservation, XYZ

PixelUV = tuple[float, float]


@dataclass(frozen=True)
class CameraIntrinsics:
    """Pinhole camera intrinsics for depth-to-3D projection."""

    fx: float
    fy: float
    cx: float
    cy: float
    frame_name: str | None = None
    width: int | None = None
    height: int | None = None


@dataclass
class CameraFrameBundle:
    """Single observer-pose RGB/depth capture with optional metadata."""

    rgb_image: Any
    depth_image: Any
    intrinsics: CameraIntrinsics | None
    color_frame_name: str | None
    depth_frame_name: str | None
    timestamp: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DetectedPieceCandidate:
    """Piece candidate produced by a detector before square assignment."""

    piece_name: str
    confidence: float
    pixel_uv: PixelUV | None = None
    world_xyz: XYZ | None = None
    yaw_rad: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SquareRegion:
    """World-frame square center and corners for board partitioning."""

    square: str
    center_world_xyz: XYZ
    corners_world_xyz: tuple[XYZ, XYZ, XYZ, XYZ]


@dataclass(frozen=True)
class BoardFrameEstimate:
    """Board frame estimate used for square generation and assignment."""

    frame_name: str
    origin_world_xyz: XYZ
    x_axis_world: XYZ
    y_axis_world: XYZ
    z_axis_world: XYZ
    square_centers_world: dict[str, XYZ]
    square_regions: dict[str, SquareRegion]
    source: str


@runtime_checkable
class FrameSource(Protocol):
    """Supplies observer-pose RGB/depth frames for perception."""

    def get_observer_frame(self) -> CameraFrameBundle:
        """Capture or return the latest observer-pose frame bundle."""


@runtime_checkable
class TransformProvider(Protocol):
    """Converts camera pixels and depth into world coordinates."""

    def pixel_to_world(
        self,
        pixel_uv: PixelUV,
        depth_m: float,
        intrinsics: CameraIntrinsics | None,
        depth_frame_name: str | None,
    ) -> XYZ | None:
        """Return the world xyz for one pixel/depth sample."""


@runtime_checkable
class BoardFrameEstimator(Protocol):
    """Optional board-frame estimator for observer-pose perception."""

    def estimate_board_frame(
        self,
        frame_bundle: CameraFrameBundle,
        geometry: BoardGeometry,
        transform_provider: TransformProvider | None,
    ) -> BoardFrameEstimate:
        """Estimate the board frame from RGB/depth and available transforms."""


@runtime_checkable
class PieceDetector(Protocol):
    """Optional piece detector hook for camera-backed observation."""

    def detect_pieces(
        self,
        frame_bundle: CameraFrameBundle,
        board_frame: BoardFrameEstimate,
    ) -> list[DetectedPieceCandidate]:
        """Return piece candidates from the current observer frame."""


class ConfiguredBoardFrameEstimator:
    """Stage-A board estimator using configured board geometry.

    This is the first-pass implementation requested for Phase 3 integration.
    Automatic corner finding can be added later behind the same interface.
    """

    def estimate_board_frame(
        self,
        frame_bundle: CameraFrameBundle,
        geometry: BoardGeometry,
        transform_provider: TransformProvider | None,
    ) -> BoardFrameEstimate:
        del frame_bundle
        del transform_provider
        square_centers = {
            square: geometry.square_center_world(square)
            for square in geometry.all_squares()
        }
        square_regions = {
            square: self._square_region(geometry, square)
            for square in geometry.all_squares()
        }
        return BoardFrameEstimate(
            frame_name=geometry.board_frame_name,
            origin_world_xyz=geometry.board_origin_world_xyz,
            x_axis_world=(1.0, 0.0, 0.0),
            y_axis_world=(0.0, 1.0, 0.0),
            z_axis_world=(0.0, 0.0, 1.0),
            square_centers_world=square_centers,
            square_regions=square_regions,
            source="configured_geometry",
        )

    @staticmethod
    def _square_region(geometry: BoardGeometry, square: str) -> SquareRegion:
        """Return the square center and corners in world coordinates."""

        half_size = geometry.square_size_m / 2.0
        center_x, center_y, center_z = geometry.square_center_world(square)
        min_x = center_x - half_size
        max_x = center_x + half_size
        min_y = center_y - half_size
        max_y = center_y + half_size
        corners = (
            (min_x, min_y, center_z),
            (max_x, min_y, center_z),
            (max_x, max_y, center_z),
            (min_x, max_y, center_z),
        )
        return SquareRegion(
            square=square,
            center_world_xyz=(center_x, center_y, center_z),
            corners_world_xyz=corners,
        )


class MetadataPieceDetector:
    """Detector hook that consumes precomputed piece candidates from metadata.

    Expected metadata format:

    `frame_bundle.metadata["piece_candidates"] = [ ... ]`

    Each item may be either a `DetectedPieceCandidate` or a mapping with keys:
    - `piece_name`
    - `confidence`
    - `pixel_uv`
    - `world_xyz`
    - `yaw_rad`

    TODO: Replace or augment this with a real RGB/depth detector model.
    """

    def detect_pieces(
        self,
        frame_bundle: CameraFrameBundle,
        board_frame: BoardFrameEstimate,
    ) -> list[DetectedPieceCandidate]:
        del board_frame
        raw_candidates = frame_bundle.metadata.get("piece_candidates", [])
        normalized: list[DetectedPieceCandidate] = []
        for item in raw_candidates:
            if isinstance(item, DetectedPieceCandidate):
                normalized.append(item)
                continue
            if not isinstance(item, Mapping):
                continue
            normalized.append(
                DetectedPieceCandidate(
                    piece_name=str(item["piece_name"]),
                    confidence=float(item.get("confidence", 0.0)),
                    pixel_uv=_normalize_pixel(item.get("pixel_uv")),
                    world_xyz=_normalize_xyz(item.get("world_xyz")),
                    yaw_rad=_optional_float(item.get("yaw_rad")),
                    metadata=dict(item.get("metadata", {})),
                )
            )
        return normalized


class BoardObserver:
    """Observer interface with mock and camera-backed modes.

    Perception is intentionally frozen while the arm is moving because the
    camera pose is not stable during motion. Observation is only valid at the
    fixed observer pose.
    """

    def __init__(
        self,
        geometry: BoardGeometry,
        mock_observations: Mapping[str, str | None] | None = None,
        *,
        mode: str = "mock",
        frame_source: FrameSource | None = None,
        transform_provider: TransformProvider | None = None,
        board_frame_estimator: BoardFrameEstimator | None = None,
        piece_detector: PieceDetector | None = None,
        allow_mock_fallback: bool = True,
    ) -> None:
        self.geometry = geometry
        self.mode = mode
        self.frame_source = frame_source
        self.transform_provider = transform_provider
        self.board_frame_estimator = board_frame_estimator or ConfiguredBoardFrameEstimator()
        self.piece_detector = piece_detector or MetadataPieceDetector()
        self.allow_mock_fallback = allow_mock_fallback
        self._mock_observations = self._normalize_square_map(mock_observations or {})
        self._frozen = False
        self._validate_mode()

    def set_mode(self, mode: str) -> None:
        """Switch between `mock` and `camera` observation modes."""

        self.mode = mode
        self._validate_mode()

    def configure_camera_mode(
        self,
        *,
        frame_source: FrameSource | None = None,
        transform_provider: TransformProvider | None = None,
        board_frame_estimator: BoardFrameEstimator | None = None,
        piece_detector: PieceDetector | None = None,
        allow_mock_fallback: bool | None = None,
    ) -> None:
        """Update the pure-Python camera observer interfaces."""

        if frame_source is not None:
            self.frame_source = frame_source
        if transform_provider is not None:
            self.transform_provider = transform_provider
        if board_frame_estimator is not None:
            self.board_frame_estimator = board_frame_estimator
        if piece_detector is not None:
            self.piece_detector = piece_detector
        if allow_mock_fallback is not None:
            self.allow_mock_fallback = allow_mock_fallback

    def set_mock_observations(self, mock_observations: Mapping[str, str | None]) -> None:
        """Replace the current mock observed board."""

        self._mock_observations = self._normalize_square_map(mock_observations)

    def freeze(self) -> None:
        """Disallow observation while the arm is moving."""

        self._frozen = True

    def allow_observation(self) -> None:
        """Allow observation again once the arm returns to observer pose."""

        self._frozen = False

    def observe_board(
        self,
        stubbed_board: Mapping[str, str | None] | None = None,
    ) -> ObservedBoard:
        """Return an observed board from camera or mock input.

        Camera mode pipeline:
        RGB/depth -> board frame estimate -> square layout -> piece detection ->
        piece center localization -> nearest-square assignment -> ObservedBoard

        `stubbed_board` always forces a mock observation for tests/debugging.
        """

        if self._frozen:
            raise RuntimeError("Board observation is frozen while robot motion is in progress.")

        if stubbed_board is not None:
            return self._observe_mock_board(stubbed_board)

        if self.mode == "camera":
            try:
                return self._observe_camera_board()
            except RuntimeError:
                if not self.allow_mock_fallback:
                    raise
                return self._observe_mock_board()

        return self._observe_mock_board()

    def estimate_board_frame(self, frame_bundle: CameraFrameBundle) -> BoardFrameEstimate:
        """Estimate the board frame for the current observer frame."""

        return self.board_frame_estimator.estimate_board_frame(
            frame_bundle=frame_bundle,
            geometry=self.geometry,
            transform_provider=self.transform_provider,
        )

    def square_centers(self, board_frame: BoardFrameEstimate) -> dict[str, XYZ]:
        """Return all square centers for the current board frame."""

        return dict(board_frame.square_centers_world)

    def square_regions(self, board_frame: BoardFrameEstimate) -> dict[str, SquareRegion]:
        """Return all square regions for the current board frame."""

        return dict(board_frame.square_regions)

    def detect_piece_candidates(
        self,
        frame_bundle: CameraFrameBundle,
        board_frame: BoardFrameEstimate,
    ) -> list[DetectedPieceCandidate]:
        """Run the injected detector hook on RGB/depth observer data."""

        return self.piece_detector.detect_pieces(frame_bundle, board_frame)

    def assign_piece_to_square(
        self,
        world_xyz: XYZ,
        square_centers_world: Mapping[str, XYZ],
    ) -> str | None:
        """Assign a piece world position to the nearest board square."""

        max_xy_distance = self.geometry.square_size_m * 0.80
        best_square: str | None = None
        best_distance = math.inf
        for square, center_world_xyz in square_centers_world.items():
            distance = math.dist(world_xyz[:2], center_world_xyz[:2])
            if distance < best_distance:
                best_distance = distance
                best_square = square
        if best_square is None or best_distance > max_xy_distance:
            return None
        return best_square

    def locate_piece_center_world(
        self,
        candidate: DetectedPieceCandidate,
        frame_bundle: CameraFrameBundle,
    ) -> XYZ | None:
        """Resolve a candidate to world coordinates using depth and transforms."""

        if candidate.world_xyz is not None:
            return candidate.world_xyz
        if candidate.pixel_uv is None or self.transform_provider is None:
            return None
        depth_m = self._depth_at_pixel(frame_bundle.depth_image, candidate.pixel_uv)
        if depth_m is None:
            return None
        return self.transform_provider.pixel_to_world(
            pixel_uv=candidate.pixel_uv,
            depth_m=depth_m,
            intrinsics=frame_bundle.intrinsics,
            depth_frame_name=frame_bundle.depth_frame_name,
        )

    def build_observed_board_from_candidates(
        self,
        candidates: list[DetectedPieceCandidate],
        board_frame: BoardFrameEstimate,
        frame_bundle: CameraFrameBundle,
    ) -> ObservedBoard:
        """Assign detected pieces to squares and build `ObservedBoard`."""

        square_map = self._normalize_square_map({})
        observations: dict[str, PieceObservation] = {}

        for candidate in candidates:
            world_xyz = self.locate_piece_center_world(candidate, frame_bundle)
            if world_xyz is None:
                continue
            square = self.assign_piece_to_square(world_xyz, board_frame.square_centers_world)
            if square is None:
                continue
            observation = PieceObservation(
                piece_name=candidate.piece_name,
                square=square,
                world_xyz=world_xyz,
                yaw_rad=candidate.yaw_rad,
                confidence=candidate.confidence,
            )
            existing = observations.get(square)
            if existing is not None and existing.confidence >= observation.confidence:
                continue
            observations[square] = observation
            square_map[square] = candidate.piece_name

        return ObservedBoard(
            by_square=square_map,
            observations=observations,
            timestamp=float(frame_bundle.timestamp),
        )

    def _observe_camera_board(self) -> ObservedBoard:
        """Camera-backed board observation path."""

        if self.frame_source is None:
            raise RuntimeError("Camera mode requires a frame_source.")

        frame_bundle = self.frame_source.get_observer_frame()
        board_frame = self.estimate_board_frame(frame_bundle)
        candidates = self.detect_piece_candidates(frame_bundle, board_frame)
        return self.build_observed_board_from_candidates(candidates, board_frame, frame_bundle)

    def _observe_mock_board(
        self,
        stubbed_board: Mapping[str, str | None] | None = None,
    ) -> ObservedBoard:
        """Mock observation path used for tests and fallback."""

        square_map = self._normalize_square_map(self._mock_observations)
        if stubbed_board is not None:
            square_map.update(self._normalize_square_map(stubbed_board))

        observations: dict[str, PieceObservation] = {}
        for square, piece_name in square_map.items():
            if piece_name is None:
                continue
            observations[square] = PieceObservation(
                piece_name=piece_name,
                square=square,
                world_xyz=self.geometry.square_center_world(square),
                yaw_rad=0.0,
                confidence=0.99,
            )

        return ObservedBoard(
            by_square=square_map,
            observations=observations,
            timestamp=time.time(),
        )

    def _validate_mode(self) -> None:
        """Validate the current observation mode."""

        if self.mode not in {"mock", "camera"}:
            raise ValueError(f"Unsupported BoardObserver mode: {self.mode!r}")

    def _normalize_square_map(
        self,
        square_map: Mapping[str, str | None],
    ) -> dict[str, str | None]:
        """Return a full 64-square map with missing squares filled as empty."""

        normalized = {square: None for square in self.geometry.all_squares()}
        for square, piece_name in square_map.items():
            normalized[square.lower()] = piece_name
        return normalized

    def _depth_at_pixel(self, depth_image: Any, pixel_uv: PixelUV) -> float | None:
        """Sample the depth image at the nearest integer pixel location."""

        row_count = _sequence_length(depth_image)
        if row_count is None or row_count <= 0:
            return None
        u = int(round(pixel_uv[0]))
        v = int(round(pixel_uv[1]))
        if v < 0 or v >= row_count:
            return None
        row = depth_image[v]
        col_count = _sequence_length(row)
        if col_count is None or u < 0 or u >= col_count:
            return None
        try:
            depth_value = float(row[u])
        except (TypeError, ValueError):
            return None
        if not math.isfinite(depth_value) or depth_value <= 0.0:
            return None
        return depth_value


def _normalize_pixel(value: Any) -> PixelUV | None:
    """Normalize a pixel tuple-like value into `(u, v)`."""

    if value is None:
        return None
    try:
        u, v = value
    except (TypeError, ValueError):
        return None
    return (float(u), float(v))


def _normalize_xyz(value: Any) -> XYZ | None:
    """Normalize a world-coordinate tuple-like value into `XYZ`."""

    if value is None:
        return None
    try:
        x, y, z = value
    except (TypeError, ValueError):
        return None
    return (float(x), float(y), float(z))


def _optional_float(value: Any) -> float | None:
    """Normalize optional numeric values."""

    if value is None:
        return None
    return float(value)


def _sequence_length(value: Any) -> int | None:
    """Return the sequence length if available."""

    try:
        return len(value)
    except TypeError:
        return None
