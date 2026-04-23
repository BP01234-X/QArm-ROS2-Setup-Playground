"""Shared fixed-calibration board model for perception and manipulation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from board_geometry import (
    BoardCalibration,
    BoardGeometry,
    canonicalize_image_corners,
    remap_world_corners_by_image_permutation,
)
from models import XYZ

UV = tuple[float, float]


@dataclass(frozen=True)
class CalibratedBoardModel:
    """Authoritative square/world model built from fixed calibration."""

    source: str
    board_outer_corners_world: dict[str, XYZ]
    square_centers_world: dict[str, XYZ]
    board_outer_corners_image: dict[str, UV]
    square_centers_image: dict[str, UV]
    board_surface_world_z: float

    def square_center_world(self, square: str) -> XYZ:
        """Return one square center in world from the calibrated map."""

        normalized = square.strip().lower()
        if normalized not in self.square_centers_world:
            raise KeyError(f"Unknown square {square!r} for calibrated board model.")
        return self.square_centers_world[normalized]


def load_fixed_calibrated_board_model(
    *,
    config_dir: str | Path | None = None,
    geometry: BoardGeometry | None = None,
    calibration: BoardCalibration | None = None,
) -> CalibratedBoardModel:
    """Build the fixed board model from board.yaml + board_calibration.yaml."""

    base_dir = Path(config_dir or Path(__file__).resolve().parent / "config")
    board_geometry = geometry or BoardGeometry.from_yaml(base_dir / "board.yaml")
    board_calibration = calibration or BoardCalibration.from_yaml(base_dir / "board_calibration.yaml")

    oriented_image: dict[str, UV] = {}
    permutation: dict[str, str] | None = None
    if board_calibration.board_outer_corners_image is not None:
        oriented_image, permutation = canonicalize_image_corners(
            board_calibration.board_outer_corners_image
        )

    if board_calibration.board_outer_corners_world is not None:
        corners_world = dict(board_calibration.board_outer_corners_world)
        source = "fixed_calibrated_world"
        if permutation is not None:
            corners_world = remap_world_corners_by_image_permutation(corners_world, permutation)
            source = "fixed_calibrated_world_oriented_by_image"
    else:
        corners_world = board_geometry.outer_corners_world_from_origin()
        source = "default_board_yaml_fallback"

    square_centers_world = board_geometry.square_centers_from_outer_corners_world(corners_world)
    square_centers_image = (
        board_geometry.square_centers_from_outer_corners_image(oriented_image)
        if oriented_image
        else {}
    )

    board_surface_world_z = float(sum(corners_world[key][2] for key in ("a1", "h1", "h8", "a8")) / 4.0)

    return CalibratedBoardModel(
        source=source,
        board_outer_corners_world=corners_world,
        square_centers_world=square_centers_world,
        board_outer_corners_image=oriented_image,
        square_centers_image=square_centers_image,
        board_surface_world_z=board_surface_world_z,
    )
