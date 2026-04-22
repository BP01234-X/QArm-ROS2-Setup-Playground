"""Phase 2 piece-detector adapter for the Phase 3 observer pipeline."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from board_observer import (
    BoardFrameEstimate,
    CameraFrameBundle,
    DetectedPieceCandidate,
    MetadataPieceDetector,
    PieceDetector,
)


class Phase2PieceDetector(PieceDetector):
    """First-pass Phase 2 detector adapter.

    Supported metadata paths:
    - `phase2_piece_candidates`: explicit piece candidates with `pixel_uv` or `world_xyz`
    - `phase2_square_assignments`: mappings with `square` and `piece_name`

    TODO: Replace the metadata path with a real RGB/depth detector model and a
    board-corner localization step if automatic detection is approved.
    """

    def __init__(self) -> None:
        self._metadata_detector = MetadataPieceDetector()

    def detect_pieces(
        self,
        frame_bundle: CameraFrameBundle,
        board_frame: BoardFrameEstimate,
    ) -> list[DetectedPieceCandidate]:
        """Return Phase 2 piece candidates for observer-pose assignment."""

        metadata = dict(frame_bundle.metadata)
        if "phase2_piece_candidates" in metadata:
            metadata["piece_candidates"] = metadata["phase2_piece_candidates"]
            return self._metadata_detector.detect_pieces(
                CameraFrameBundle(
                    rgb_image=frame_bundle.rgb_image,
                    depth_image=frame_bundle.depth_image,
                    intrinsics=frame_bundle.intrinsics,
                    color_frame_name=frame_bundle.color_frame_name,
                    depth_frame_name=frame_bundle.depth_frame_name,
                    timestamp=frame_bundle.timestamp,
                    metadata=metadata,
                ),
                board_frame,
            )

        square_assignments = metadata.get("phase2_square_assignments", [])
        candidates: list[DetectedPieceCandidate] = []
        for item in square_assignments:
            if not isinstance(item, Mapping):
                continue
            square = str(item["square"]).lower()
            center_world_xyz = board_frame.square_centers_world.get(square)
            if center_world_xyz is None:
                continue
            candidates.append(
                DetectedPieceCandidate(
                    piece_name=str(item["piece_name"]),
                    confidence=float(item.get("confidence", 0.99)),
                    world_xyz=center_world_xyz,
                    yaw_rad=float(item.get("yaw_rad", 0.0)),
                    metadata={"square_hint": square},
                )
            )
        return candidates
