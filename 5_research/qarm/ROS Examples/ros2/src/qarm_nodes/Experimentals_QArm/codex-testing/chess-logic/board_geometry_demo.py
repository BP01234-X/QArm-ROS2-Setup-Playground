"""Standalone Phase 4 board-geometry demo."""

from __future__ import annotations

import time
from pathlib import Path

from board_geometry import BoardCalibration, BoardGeometry
from board_observer import CameraFrameBundle, ConfiguredBoardFrameEstimator


def main() -> None:
    """Load calibration, build board grid, and test square assignment helpers."""

    config_dir = Path(__file__).resolve().parent / "config"
    geometry = BoardGeometry.from_yaml(config_dir / "board.yaml")
    calibration = BoardCalibration.from_yaml(config_dir / "board_calibration.yaml")
    estimator = ConfiguredBoardFrameEstimator(calibration=calibration)

    frame_bundle = CameraFrameBundle(
        rgb_image=[[0]],
        depth_image=_synthetic_depth_image(width=640, height=480),
        intrinsics=None,
        color_frame_name="camera_color",
        depth_frame_name="left_ir_optical_frame",
        timestamp=time.time(),
        metadata={},
    )
    board_frame = estimator.estimate_board_frame(
        frame_bundle=frame_bundle,
        geometry=geometry,
        transform_provider=None,
    )

    print(f"board_source={board_frame.source}")
    print(f"board_detection_mode={board_frame.board_detection_mode}")
    print(f"fit_state={board_frame.fit_state}")
    print(f"used_live_fit={board_frame.used_live_fit}")
    print(f"used_manual_fallback={board_frame.used_manual_fallback}")
    print(f"corner_confidence={board_frame.corner_confidence}")
    print(f"visible_board_fraction={board_frame.visible_board_fraction}")
    print(f"live_fit_confidence={board_frame.live_fit_confidence}")
    print(f"square_spacing_validation={board_frame.square_spacing_validation}")

    for square in ("a1", "e4", "h8"):
        print(
            f"{square}: "
            f"world_center={board_frame.square_centers_world[square]} "
            f"image_center={board_frame.square_centers_image.get(square)}"
        )

    a1_uv = board_frame.square_centers_image["a1"]
    h8_uv = board_frame.square_centers_image["h8"]
    orientation_ok = a1_uv[0] < h8_uv[0] and a1_uv[1] > h8_uv[1]
    print(f"orientation_check_a1_lower_left_h8_upper_right={orientation_ok}")

    sample_pixel = board_frame.square_centers_image["d5"]
    assigned_square_from_pixel = geometry.point_to_square_image(
        pixel_uv=sample_pixel,
        square_polygons_image=board_frame.square_polygons_image,
        square_centers_image=board_frame.square_centers_image,
    )
    print(f"sample_pixel={sample_pixel} -> square={assigned_square_from_pixel}")

    sample_world = board_frame.square_centers_world["b2"]
    assigned_square_from_world = geometry.point_to_square_world(
        world_xyz=sample_world,
        square_centers_world=board_frame.square_centers_world,
        max_distance_m=board_frame.assignment_margin_m,
    )
    print(f"sample_world={sample_world} -> square={assigned_square_from_world}")


def _synthetic_depth_image(width: int, height: int) -> list[list[float]]:
    """Build a simple synthetic depth frame with a board-like rectangle."""

    image = [[1.20 for _ in range(width)] for _ in range(height)]
    min_u, max_u = 220, 580
    min_v, max_v = 170, 430
    for v in range(min_v, max_v + 1):
        row = image[v]
        for u in range(min_u, max_u + 1):
            row[u] = 1.00
    return image


if __name__ == "__main__":
    main()
