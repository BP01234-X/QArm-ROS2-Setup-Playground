"""Factory helpers for building Phase 2-backed board observers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from board_geometry import BoardCalibration, BoardGeometry
from board_observer import BoardObserver, ConfiguredBoardFrameEstimator
from phase2_frame_source import Phase2FrameConfig, Phase2FrameSource
from phase2_piece_detector import Phase2PieceDetector
from phase2_transform_provider import Matrix4, Phase2TransformProvider, identity_matrix4


def build_camera_observer(
    *,
    config_dir: str | Path | None = None,
    geometry: BoardGeometry | None = None,
    rgb_provider=None,
    depth_provider=None,
    metadata_provider=None,
    static_rgb_image: Any = None,
    static_depth_image: Any = None,
    static_metadata: dict[str, Any] | None = None,
    camera_to_world_matrix: Matrix4 | None = None,
    allow_mock_fallback: bool = True,
    mock_observations: dict[str, str | None] | None = None,
    calibration: BoardCalibration | None = None,
) -> BoardObserver:
    """Build a camera-mode `BoardObserver` with Phase 2 adapters."""

    base_dir = Path(config_dir or Path(__file__).resolve().parent / "config")
    board_geometry = geometry or BoardGeometry.from_yaml(base_dir / "board.yaml")
    board_calibration = calibration or BoardCalibration.from_yaml(base_dir / "board_calibration.yaml")
    frame_config = Phase2FrameConfig()
    frame_source = Phase2FrameSource(
        rgb_provider=rgb_provider,
        depth_provider=depth_provider,
        metadata_provider=metadata_provider,
        intrinsics=frame_config.intrinsics(),
        color_frame_name=frame_config.color_frame_name,
        depth_frame_name=frame_config.depth_frame_name,
        static_rgb_image=static_rgb_image,
        static_depth_image=static_depth_image,
        static_metadata=static_metadata,
    )
    transform_provider = Phase2TransformProvider(
        camera_to_world_matrix=camera_to_world_matrix or identity_matrix4(),
    )
    return BoardObserver(
        board_geometry,
        mock_observations=mock_observations,
        mode="camera",
        frame_source=frame_source,
        transform_provider=transform_provider,
        board_frame_estimator=ConfiguredBoardFrameEstimator(calibration=board_calibration),
        piece_detector=Phase2PieceDetector(),
        allow_mock_fallback=allow_mock_fallback,
        calibration=board_calibration,
    )


def build_mock_observer(
    *,
    config_dir: str | Path | None = None,
    mock_observations: dict[str, str | None] | None = None,
    calibration: BoardCalibration | None = None,
) -> BoardObserver:
    """Build a plain mock-mode observer for tests and fallback."""

    base_dir = Path(config_dir or Path(__file__).resolve().parent / "config")
    geometry = BoardGeometry.from_yaml(base_dir / "board.yaml")
    board_calibration = calibration or BoardCalibration.from_yaml(base_dir / "board_calibration.yaml")
    return BoardObserver(
        geometry,
        mock_observations=mock_observations,
        mode="mock",
        calibration=board_calibration,
    )
