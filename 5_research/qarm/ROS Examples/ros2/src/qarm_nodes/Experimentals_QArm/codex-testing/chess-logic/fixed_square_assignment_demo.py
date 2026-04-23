#!/usr/bin/env python3

"""Quick test for fixed observer-grid piece-to-square assignment."""

from __future__ import annotations

import time
from pathlib import Path

from board_geometry import BoardCalibration, BoardGeometry
from board_observer import (
    BoardObserver,
    CameraFrameBundle,
    ConfiguredBoardFrameEstimator,
    DetectedPieceCandidate,
)


def main() -> None:
    config_dir = Path(__file__).resolve().parent / "config"
    geometry = BoardGeometry.from_yaml(config_dir / "board.yaml")
    calibration = BoardCalibration.from_yaml(config_dir / "board_calibration.yaml")
    calibration = BoardCalibration(
        board_detection_mode="manual",
        board_orientation=calibration.board_orientation,
        a1_reference=calibration.a1_reference,
        nominal_square_size_cm=calibration.nominal_square_size_cm,
        min_square_size_cm=calibration.min_square_size_cm,
        max_square_size_cm=calibration.max_square_size_cm,
        board_outer_corners_image=calibration.board_outer_corners_image,
        board_outer_corners_world=calibration.board_outer_corners_world,
        min_corner_confidence=calibration.min_corner_confidence,
        min_visible_board_fraction=calibration.min_visible_board_fraction,
        min_live_fit_confidence=calibration.min_live_fit_confidence,
        fallback_to_manual_if_live_fit_fails=calibration.fallback_to_manual_if_live_fit_fails,
        live_corner_search_radius_px=calibration.live_corner_search_radius_px,
        live_corner_edge_samples=calibration.live_corner_edge_samples,
        live_corner_min_gradient_m=calibration.live_corner_min_gradient_m,
        live_keep_last_good_confidence=calibration.live_keep_last_good_confidence,
        live_stale_timeout_sec=calibration.live_stale_timeout_sec,
        live_corner_smoothing_alpha=calibration.live_corner_smoothing_alpha,
        observer_settle_frames=calibration.observer_settle_frames,
        observer_settle_reset_gap_sec=calibration.observer_settle_reset_gap_sec,
    )
    estimator = ConfiguredBoardFrameEstimator(calibration=calibration)
    observer = BoardObserver(geometry=geometry, mode="mock", calibration=calibration)

    frame_bundle = CameraFrameBundle(
        rgb_image=[[0.0] * 640 for _ in range(480)],
        depth_image=[[1.0] * 640 for _ in range(480)],
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

    def sample(square: str, du: float, dv: float, piece: str) -> DetectedPieceCandidate:
        center = board_frame.square_centers_image[square]
        return DetectedPieceCandidate(
            piece_name=piece,
            confidence=0.95,
            pixel_uv=(center[0] + du, center[1] + dv),
            world_xyz=None,
            yaw_rad=0.0,
            metadata={},
        )

    candidates = [
        sample("e2", du=2.0, dv=-1.0, piece="white_pawn"),
        sample("e7", du=-1.5, dv=1.0, piece="black_pawn"),
        sample("g1", du=1.0, dv=2.0, piece="white_knight"),
    ]

    observed = observer.build_observed_board_from_candidates(candidates, board_frame, frame_bundle)
    print(f"board_source={board_frame.source}")
    print(f"mode={board_frame.board_detection_mode} fit_state={board_frame.fit_state}")
    for square in ("e2", "e7", "g1"):
        print(f"{square} -> {observed.by_square[square]}")


if __name__ == "__main__":
    main()
