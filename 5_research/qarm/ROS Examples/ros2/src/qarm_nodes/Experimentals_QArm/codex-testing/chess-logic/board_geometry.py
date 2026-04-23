"""Board geometry helpers for board calibration and square mapping.

Phase 4 extends this module with:
- board calibration loading (manual/automatic/hybrid mode metadata)
- outer-corner to 8x8 grid generation
- square center/polygon generation in world and image domains
- nearest-square assignment helpers for world points and image pixels
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled at runtime
    yaml = None
    YAML_IMPORT_ERROR = exc
else:
    YAML_IMPORT_ERROR = None

from models import XYZ

FILES = "abcdefgh"
RANKS = "12345678"
CORNER_KEYS = ("a1", "h1", "h8", "a8")
UV = tuple[float, float]
PolygonUV = tuple[UV, UV, UV, UV]
PolygonXYZ = tuple[XYZ, XYZ, XYZ, XYZ]


@dataclass(frozen=True)
class BoardGeometry:
    """Converts chess squares into board/world geometry."""

    board_origin_world_xyz: XYZ
    square_size_m: float
    board_height_z: float
    board_frame_name: str

    @classmethod
    def from_yaml(cls, path: str | Path) -> "BoardGeometry":
        """Load board geometry from YAML config."""

        if yaml is None:
            raise RuntimeError("PyYAML is required to load board.yaml") from YAML_IMPORT_ERROR
        payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        origin = tuple(float(v) for v in payload["board_origin_world_xyz"])
        return cls(
            board_origin_world_xyz=origin,
            square_size_m=float(payload["square_size_m"]),
            board_height_z=float(payload["board_height_z"]),
            board_frame_name=str(payload["board_frame_name"]),
        )

    @property
    def board_surface_world_z(self) -> float:
        """Absolute world z for the board surface."""

        return float(self.board_origin_world_xyz[2] + self.board_height_z)

    def outer_corners_world_from_origin(self) -> dict[str, XYZ]:
        """Return world corners inferred from axis-aligned board config.

        Corner convention:
        - `a1`: lower-left from the camera-image perspective
        - `h8`: upper-right from the camera-image perspective
        """

        origin_x, origin_y, origin_z = self.board_origin_world_xyz
        board_size = self.square_size_m * 8.0
        board_z = origin_z + self.board_height_z
        return {
            "a1": (origin_x, origin_y, board_z),
            "h1": (origin_x + board_size, origin_y, board_z),
            "h8": (origin_x + board_size, origin_y + board_size, board_z),
            "a8": (origin_x, origin_y + board_size, board_z),
        }

    def all_squares(self) -> list[str]:
        """Return squares ordered from a1 through h8."""

        return [f"{file_char}{rank_char}" for rank_char in RANKS for file_char in FILES]

    def square_to_indices(self, square: str) -> tuple[int, int]:
        """Convert a square like `e4` into zero-based file/rank indices."""

        normalized = square.strip().lower()
        if len(normalized) != 2 or normalized[0] not in FILES or normalized[1] not in RANKS:
            raise ValueError(f"Invalid chess square: {square!r}")
        file_index = FILES.index(normalized[0])
        rank_index = RANKS.index(normalized[1])
        return file_index, rank_index

    def indices_to_square(self, file_index: int, rank_index: int) -> str:
        """Convert zero-based file/rank indices into chess notation."""

        if not (0 <= file_index < 8 and 0 <= rank_index < 8):
            raise ValueError("File and rank indices must be in [0, 7].")
        return f"{FILES[file_index]}{RANKS[rank_index]}"

    def square_center_board(self, square: str) -> XYZ:
        """Return the square center in the board frame."""

        file_index, rank_index = self.square_to_indices(square)
        x = (file_index + 0.5) * self.square_size_m
        y = (rank_index + 0.5) * self.square_size_m
        return (x, y, self.board_height_z)

    def square_center_world(self, square: str, z_offset_m: float = 0.0) -> XYZ:
        """Return the world-frame center for a square with an optional z offset."""

        board_x, board_y, _ = self.square_center_board(square)
        origin_x, origin_y, origin_z = self.board_origin_world_xyz
        return (
            origin_x + board_x,
            origin_y + board_y,
            origin_z + self.board_height_z + z_offset_m,
        )

    def board_to_world(self, board_xyz: XYZ) -> XYZ:
        """Convert a board-frame xyz into world coordinates."""

        origin_x, origin_y, origin_z = self.board_origin_world_xyz
        return (
            origin_x + board_xyz[0],
            origin_y + board_xyz[1],
            origin_z + board_xyz[2],
        )

    def square_centers_from_outer_corners_world(
        self,
        outer_corners_world: dict[str, XYZ],
    ) -> dict[str, XYZ]:
        """Generate all 64 world square centers from four board corners."""

        return self._square_centers_from_outer_corners_xyz(outer_corners_world)

    def square_polygons_from_outer_corners_world(
        self,
        outer_corners_world: dict[str, XYZ],
    ) -> dict[str, PolygonXYZ]:
        """Generate all 64 world square polygons from four board corners."""

        return self._square_polygons_from_outer_corners_xyz(outer_corners_world)

    def square_centers_from_outer_corners_image(
        self,
        outer_corners_image: dict[str, UV],
    ) -> dict[str, UV]:
        """Generate all 64 image square centers from four board corners."""

        corners = _normalize_corner_map_2d(outer_corners_image)
        centers: dict[str, UV] = {}
        for rank_index in range(8):
            for file_index in range(8):
                square = self.indices_to_square(file_index, rank_index)
                u = (file_index + 0.5) / 8.0
                v = (rank_index + 0.5) / 8.0
                centers[square] = _bilinear_2d(corners, u=u, v=v)
        return centers

    def square_polygons_from_outer_corners_image(
        self,
        outer_corners_image: dict[str, UV],
    ) -> dict[str, PolygonUV]:
        """Generate all 64 image square polygons from four board corners."""

        corners = _normalize_corner_map_2d(outer_corners_image)
        polygons: dict[str, PolygonUV] = {}
        for rank_index in range(8):
            for file_index in range(8):
                square = self.indices_to_square(file_index, rank_index)
                u0 = file_index / 8.0
                u1 = (file_index + 1) / 8.0
                v0 = rank_index / 8.0
                v1 = (rank_index + 1) / 8.0
                polygons[square] = (
                    _bilinear_2d(corners, u=u0, v=v0),
                    _bilinear_2d(corners, u=u1, v=v0),
                    _bilinear_2d(corners, u=u1, v=v1),
                    _bilinear_2d(corners, u=u0, v=v1),
                )
        return polygons

    def point_to_square_world(
        self,
        world_xyz: XYZ,
        square_centers_world: dict[str, XYZ],
        max_distance_m: float | None = None,
    ) -> str | None:
        """Assign a world point to the nearest square center."""

        if not square_centers_world:
            return None
        limit = self.square_size_m if max_distance_m is None else max_distance_m
        best_square: str | None = None
        best_distance = float("inf")
        for square, center in square_centers_world.items():
            dist = ((world_xyz[0] - center[0]) ** 2 + (world_xyz[1] - center[1]) ** 2) ** 0.5
            if dist < best_distance:
                best_distance = dist
                best_square = square
        if best_square is None or best_distance > limit:
            return None
        return best_square

    def point_to_square_image(
        self,
        pixel_uv: UV,
        square_polygons_image: dict[str, PolygonUV],
        square_centers_image: dict[str, UV] | None = None,
        max_distance_px: float | None = None,
    ) -> str | None:
        """Assign an image point to a square polygon, fallback to nearest center."""

        if not square_polygons_image:
            return None
        for square, polygon in square_polygons_image.items():
            if _point_in_quad(pixel_uv, polygon):
                return square

        if not square_centers_image:
            return None
        best_square: str | None = None
        best_distance = float("inf")
        for square, center in square_centers_image.items():
            dist = ((pixel_uv[0] - center[0]) ** 2 + (pixel_uv[1] - center[1]) ** 2) ** 0.5
            if dist < best_distance:
                best_distance = dist
                best_square = square
        if best_square is None:
            return None
        if max_distance_px is not None and best_distance > max_distance_px:
            return None
        return best_square

    def validate_square_spacing_world(
        self,
        square_centers_world: dict[str, XYZ],
        min_square_size_m: float,
        max_square_size_m: float,
    ) -> dict[str, float | bool]:
        """Validate measured world square spacing against configured bounds."""

        distances: list[float] = []
        for rank_index in range(8):
            for file_index in range(7):
                sq_a = self.indices_to_square(file_index, rank_index)
                sq_b = self.indices_to_square(file_index + 1, rank_index)
                if sq_a in square_centers_world and sq_b in square_centers_world:
                    distances.append(_xy_dist(square_centers_world[sq_a], square_centers_world[sq_b]))
        for rank_index in range(7):
            for file_index in range(8):
                sq_a = self.indices_to_square(file_index, rank_index)
                sq_b = self.indices_to_square(file_index, rank_index + 1)
                if sq_a in square_centers_world and sq_b in square_centers_world:
                    distances.append(_xy_dist(square_centers_world[sq_a], square_centers_world[sq_b]))

        if not distances:
            return {
                "samples": 0.0,
                "measured_min_m": 0.0,
                "measured_max_m": 0.0,
                "nominal_m": self.square_size_m,
                "within_tolerance": False,
            }
        measured_min = min(distances)
        measured_max = max(distances)
        return {
            "samples": float(len(distances)),
            "measured_min_m": measured_min,
            "measured_max_m": measured_max,
            "nominal_m": self.square_size_m,
            "within_tolerance": measured_min >= min_square_size_m and measured_max <= max_square_size_m,
        }

    def _square_centers_from_outer_corners_xyz(
        self,
        outer_corners_world: dict[str, XYZ],
    ) -> dict[str, XYZ]:
        corners = _normalize_corner_map_3d(outer_corners_world)
        centers: dict[str, XYZ] = {}
        for rank_index in range(8):
            for file_index in range(8):
                square = self.indices_to_square(file_index, rank_index)
                u = (file_index + 0.5) / 8.0
                v = (rank_index + 0.5) / 8.0
                centers[square] = _bilinear_3d(corners, u=u, v=v)
        return centers

    def _square_polygons_from_outer_corners_xyz(
        self,
        outer_corners_world: dict[str, XYZ],
    ) -> dict[str, PolygonXYZ]:
        corners = _normalize_corner_map_3d(outer_corners_world)
        polygons: dict[str, PolygonXYZ] = {}
        for rank_index in range(8):
            for file_index in range(8):
                square = self.indices_to_square(file_index, rank_index)
                u0 = file_index / 8.0
                u1 = (file_index + 1) / 8.0
                v0 = rank_index / 8.0
                v1 = (rank_index + 1) / 8.0
                polygons[square] = (
                    _bilinear_3d(corners, u=u0, v=v0),
                    _bilinear_3d(corners, u=u1, v=v0),
                    _bilinear_3d(corners, u=u1, v=v1),
                    _bilinear_3d(corners, u=u0, v=v1),
                )
        return polygons


@dataclass(frozen=True)
class BoardCalibration:
    """Calibration metadata for stage-A/stage-B board identification."""

    board_detection_mode: str
    board_orientation: str
    a1_reference: str
    nominal_square_size_cm: float
    min_square_size_cm: float
    max_square_size_cm: float
    board_outer_corners_image: dict[str, UV] | None
    board_outer_corners_world: dict[str, XYZ] | None
    min_corner_confidence: float = 0.35
    min_visible_board_fraction: float = 0.45
    min_live_fit_confidence: float = 0.55
    fallback_to_manual_if_live_fit_fails: bool = True
    live_corner_search_radius_px: int = 24
    live_corner_edge_samples: int = 18
    live_corner_min_gradient_m: float = 0.003
    live_keep_last_good_confidence: float = 0.18
    live_stale_timeout_sec: float = 2.0
    live_corner_smoothing_alpha: float = 0.35
    observer_settle_frames: int = 3
    observer_settle_reset_gap_sec: float = 0.9

    @classmethod
    def from_yaml(cls, path: str | Path) -> "BoardCalibration":
        """Load board calibration from YAML."""

        if yaml is None:
            raise RuntimeError("PyYAML is required to load board_calibration.yaml") from YAML_IMPORT_ERROR
        payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        calibration = cls(
            board_detection_mode=str(payload.get("board_detection_mode", "manual")).lower(),
            board_orientation=str(
                payload.get("board_orientation", "a1_lower_left_h8_upper_right")
            ).lower(),
            a1_reference=str(payload.get("a1_reference", "image_lower_left")).lower(),
            nominal_square_size_cm=float(payload.get("nominal_square_size_cm", 3.6)),
            min_square_size_cm=float(payload.get("min_square_size_cm", 3.4)),
            max_square_size_cm=float(payload.get("max_square_size_cm", 3.78)),
            board_outer_corners_image=_optional_corner_map_2d(payload.get("board_outer_corners_image")),
            board_outer_corners_world=_optional_corner_map_3d(payload.get("board_outer_corners_world")),
            min_corner_confidence=float(payload.get("min_corner_confidence", 0.35)),
            min_visible_board_fraction=float(payload.get("min_visible_board_fraction", 0.45)),
            min_live_fit_confidence=float(payload.get("min_live_fit_confidence", 0.55)),
            fallback_to_manual_if_live_fit_fails=bool(
                payload.get("fallback_to_manual_if_live_fit_fails", True)
            ),
            live_corner_search_radius_px=int(payload.get("live_corner_search_radius_px", 24)),
            live_corner_edge_samples=int(payload.get("live_corner_edge_samples", 18)),
            live_corner_min_gradient_m=float(payload.get("live_corner_min_gradient_m", 0.003)),
            live_keep_last_good_confidence=float(
                payload.get("live_keep_last_good_confidence", 0.18)
            ),
            live_stale_timeout_sec=float(payload.get("live_stale_timeout_sec", 2.0)),
            live_corner_smoothing_alpha=float(payload.get("live_corner_smoothing_alpha", 0.35)),
            observer_settle_frames=int(payload.get("observer_settle_frames", 3)),
            observer_settle_reset_gap_sec=float(payload.get("observer_settle_reset_gap_sec", 0.9)),
        )
        calibration.validate_orientation()
        return calibration

    def validate_orientation(self) -> None:
        """Validate expected A1/H8 orientation convention for Phase 4."""

        if self.board_orientation != "a1_lower_left_h8_upper_right":
            raise ValueError(
                "Unsupported board_orientation. Expected 'a1_lower_left_h8_upper_right'."
            )
        if self.a1_reference != "image_lower_left":
            raise ValueError("Unsupported a1_reference. Expected 'image_lower_left'.")
        if self.min_square_size_cm > self.nominal_square_size_cm:
            raise ValueError("min_square_size_cm cannot exceed nominal_square_size_cm.")
        if self.max_square_size_cm < self.nominal_square_size_cm:
            raise ValueError("max_square_size_cm cannot be below nominal_square_size_cm.")
        if not (0.0 <= self.min_corner_confidence <= 1.0):
            raise ValueError("min_corner_confidence must be in [0.0, 1.0].")
        if not (0.0 <= self.min_visible_board_fraction <= 1.0):
            raise ValueError("min_visible_board_fraction must be in [0.0, 1.0].")
        if not (0.0 <= self.min_live_fit_confidence <= 1.0):
            raise ValueError("min_live_fit_confidence must be in [0.0, 1.0].")
        if self.live_corner_search_radius_px <= 0:
            raise ValueError("live_corner_search_radius_px must be positive.")
        if self.live_corner_edge_samples <= 2:
            raise ValueError("live_corner_edge_samples must be greater than 2.")
        if self.live_corner_min_gradient_m <= 0.0:
            raise ValueError("live_corner_min_gradient_m must be positive.")
        if not (0.0 <= self.live_keep_last_good_confidence <= 1.0):
            raise ValueError("live_keep_last_good_confidence must be in [0.0, 1.0].")
        if self.live_stale_timeout_sec < 0.0:
            raise ValueError("live_stale_timeout_sec must be >= 0.0.")
        if not (0.0 <= self.live_corner_smoothing_alpha <= 1.0):
            raise ValueError("live_corner_smoothing_alpha must be in [0.0, 1.0].")
        if self.observer_settle_frames < 0:
            raise ValueError("observer_settle_frames must be >= 0.")
        if self.observer_settle_reset_gap_sec < 0.0:
            raise ValueError("observer_settle_reset_gap_sec must be >= 0.0.")

    @property
    def nominal_square_size_m(self) -> float:
        return self.nominal_square_size_cm / 100.0

    @property
    def min_square_size_m(self) -> float:
        return self.min_square_size_cm / 100.0

    @property
    def max_square_size_m(self) -> float:
        return self.max_square_size_cm / 100.0


def _normalize_corner_map_2d(corners: dict[str, UV]) -> dict[str, UV]:
    """Validate and normalize a 2D corner map."""

    normalized: dict[str, UV] = {}
    for key in CORNER_KEYS:
        if key not in corners:
            raise ValueError(f"Missing required corner {key!r}.")
        uv = corners[key]
        normalized[key] = (float(uv[0]), float(uv[1]))
    return normalized


def _normalize_corner_map_3d(corners: dict[str, XYZ]) -> dict[str, XYZ]:
    """Validate and normalize a 3D corner map."""

    normalized: dict[str, XYZ] = {}
    for key in CORNER_KEYS:
        if key not in corners:
            raise ValueError(f"Missing required corner {key!r}.")
        xyz = corners[key]
        normalized[key] = (float(xyz[0]), float(xyz[1]), float(xyz[2]))
    return normalized


def _optional_corner_map_2d(value: Any) -> dict[str, UV] | None:
    """Parse an optional 2D corner map from YAML."""

    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("board_outer_corners_image must be a mapping.")
    parsed: dict[str, UV] = {}
    for key in CORNER_KEYS:
        if key not in value:
            raise ValueError(f"board_outer_corners_image missing key {key!r}.")
        parsed[key] = _as_uv(value[key])
    return parsed


def _optional_corner_map_3d(value: Any) -> dict[str, XYZ] | None:
    """Parse an optional 3D corner map from YAML."""

    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("board_outer_corners_world must be a mapping.")
    parsed: dict[str, XYZ] = {}
    for key in CORNER_KEYS:
        if key not in value:
            raise ValueError(f"board_outer_corners_world missing key {key!r}.")
        parsed[key] = _as_xyz(value[key])
    return parsed


def canonicalize_image_corners(
    corners: Mapping[str, UV],
) -> tuple[dict[str, UV], dict[str, str]]:
    """Return corners re-labeled to Phase 4 orientation.

    The output always follows:
    - a1: image lower-left
    - h1: image lower-right
    - h8: image upper-right
    - a8: image upper-left

    Also returns `{canonical_key: source_key}` so paired world corners can be
    remapped with the same permutation.
    """

    normalized = _normalize_corner_map_2d(dict(corners))
    points = [(key, uv[0], uv[1]) for key, uv in normalized.items()]
    by_v = sorted(points, key=lambda item: item[2])  # smaller v is upper
    top = sorted(by_v[:2], key=lambda item: item[1])  # left->right
    bottom = sorted(by_v[-2:], key=lambda item: item[1])  # left->right
    source_for = {
        "a1": bottom[0][0],
        "h1": bottom[1][0],
        "h8": top[1][0],
        "a8": top[0][0],
    }
    if len(set(source_for.values())) != 4:
        raise ValueError("Unable to canonicalize board corners; degenerate corner layout.")
    oriented = {canonical: normalized[source] for canonical, source in source_for.items()}
    return oriented, source_for


def remap_world_corners_by_image_permutation(
    world_corners: Mapping[str, XYZ],
    canonical_to_source: Mapping[str, str],
) -> dict[str, XYZ]:
    """Apply image-derived corner permutation to world corners."""

    normalized = _normalize_corner_map_3d(dict(world_corners))
    remapped: dict[str, XYZ] = {}
    for canonical_key in CORNER_KEYS:
        source_key = canonical_to_source[canonical_key]
        remapped[canonical_key] = normalized[source_key]
    return remapped


def _as_uv(value: Any) -> UV:
    try:
        u, v = value
    except (TypeError, ValueError) as exc:  # pragma: no cover - malformed config
        raise ValueError(f"Expected [u, v], got {value!r}") from exc
    return (float(u), float(v))


def _as_xyz(value: Any) -> XYZ:
    try:
        x, y, z = value
    except (TypeError, ValueError) as exc:  # pragma: no cover - malformed config
        raise ValueError(f"Expected [x, y, z], got {value!r}") from exc
    return (float(x), float(y), float(z))


def _bilinear_2d(corners: dict[str, UV], u: float, v: float) -> UV:
    a1 = corners["a1"]
    h1 = corners["h1"]
    h8 = corners["h8"]
    a8 = corners["a8"]
    x = (
        (1.0 - u) * (1.0 - v) * a1[0]
        + u * (1.0 - v) * h1[0]
        + u * v * h8[0]
        + (1.0 - u) * v * a8[0]
    )
    y = (
        (1.0 - u) * (1.0 - v) * a1[1]
        + u * (1.0 - v) * h1[1]
        + u * v * h8[1]
        + (1.0 - u) * v * a8[1]
    )
    return (x, y)


def _bilinear_3d(corners: dict[str, XYZ], u: float, v: float) -> XYZ:
    a1 = corners["a1"]
    h1 = corners["h1"]
    h8 = corners["h8"]
    a8 = corners["a8"]
    x = (
        (1.0 - u) * (1.0 - v) * a1[0]
        + u * (1.0 - v) * h1[0]
        + u * v * h8[0]
        + (1.0 - u) * v * a8[0]
    )
    y = (
        (1.0 - u) * (1.0 - v) * a1[1]
        + u * (1.0 - v) * h1[1]
        + u * v * h8[1]
        + (1.0 - u) * v * a8[1]
    )
    z = (
        (1.0 - u) * (1.0 - v) * a1[2]
        + u * (1.0 - v) * h1[2]
        + u * v * h8[2]
        + (1.0 - u) * v * a8[2]
    )
    return (x, y, z)


def _xy_dist(a: XYZ, b: XYZ) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _point_in_quad(point: UV, quad: PolygonUV) -> bool:
    """Return True if point lies inside a convex quadrilateral."""

    def cross(o: UV, a: UV, b: UV) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    signs: list[float] = []
    p = point
    for idx in range(4):
        a = quad[idx]
        b = quad[(idx + 1) % 4]
        signs.append(cross(a, b, p))
    has_pos = any(value > 0 for value in signs)
    has_neg = any(value < 0 for value in signs)
    return not (has_pos and has_neg)
