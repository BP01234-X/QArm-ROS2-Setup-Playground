"""Demo the camera-backed board observer with Phase 2 adapter classes."""

from __future__ import annotations

from observer_factory import build_camera_observer


def main() -> None:
    """Run a pure-Python camera-mode observer demo."""

    rgb_image = [[(0, 0, 0)]]
    depth_image = [[1.0]]
    metadata = {
        "phase2_square_assignments": [
            {"square": "e2", "piece_name": "white_pawn", "confidence": 0.97},
            {"square": "e7", "piece_name": "black_pawn", "confidence": 0.98},
            {"square": "g1", "piece_name": "white_knight", "confidence": 0.96},
        ]
    }

    observer = build_camera_observer(
        static_rgb_image=rgb_image,
        static_depth_image=depth_image,
        static_metadata=metadata,
        allow_mock_fallback=False,
    )

    frame_bundle = observer.frame_source.get_observer_frame()
    board_frame = observer.estimate_board_frame(frame_bundle)
    candidates = observer.detect_piece_candidates(frame_bundle, board_frame)
    observed = observer.build_observed_board_from_candidates(candidates, board_frame, frame_bundle)

    print(f"board_frame_source={board_frame.source}")
    print(f"board_frame_name={board_frame.frame_name}")
    print("candidates:")
    for candidate in candidates:
        print(
            f"  piece={candidate.piece_name} "
            f"confidence={candidate.confidence:.2f} "
            f"world_xyz={candidate.world_xyz}"
        )
    print("observed_board:")
    for square in ("e2", "e7", "g1"):
        print(f"  {square}: {observed.by_square[square]}")
    print(f"observation_count={len(observed.observations)}")


if __name__ == "__main__":
    main()
