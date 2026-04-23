"""Print manual comparison notes for Phase 3 observer pose candidates."""

from __future__ import annotations

from pathlib import Path

import yaml

from board_geometry import BoardGeometry


def board_center_world(geometry: BoardGeometry) -> tuple[float, float, float]:
    """Return the board center in world coordinates."""

    side_m = geometry.square_size_m * 8.0
    origin_x, origin_y, origin_z = geometry.board_origin_world_xyz
    return (
        origin_x + side_m / 2.0,
        origin_y + side_m / 2.0,
        origin_z + geometry.board_height_z,
    )


def main() -> None:
    """Print observer candidate summaries for manual RViz/camera review."""

    base_dir = Path(__file__).resolve().parent / "config"
    observer_payload = yaml.safe_load((base_dir / "observer_pose.yaml").read_text(encoding="utf-8"))
    geometry = BoardGeometry.from_yaml(base_dir / "board.yaml")
    center_x, center_y, center_z = board_center_world(geometry)

    default_name = str(observer_payload.get("default_observer_pose", observer_payload["observer_pose_name"]))
    candidates = observer_payload.get("observer_pose_candidates", {})
    baseline = candidates.get("chess_observer_current")

    print("Observer Pose Review")
    print(f"Board center world xyz: ({center_x:.3f}, {center_y:.3f}, {center_z:.3f})")
    print(f"Recommended default: {default_name}")
    print("")

    baseline_xyz = None
    if baseline is not None:
        baseline_xyz = tuple(float(v) for v in baseline["observer_world_xyz"])

    for name, candidate in candidates.items():
        xyz = tuple(float(v) for v in candidate["observer_world_xyz"])
        rpy = tuple(float(v) for v in candidate["observer_rpy"])
        dx_center = xyz[0] - center_x
        dy_center = xyz[1] - center_y
        dz_board = xyz[2] - center_z
        print(f"[{name}]")
        print(f"  xyz: ({xyz[0]:.3f}, {xyz[1]:.3f}, {xyz[2]:.3f})")
        print(f"  rpy: ({rpy[0]:.3f}, {rpy[1]:.3f}, {rpy[2]:.3f})")
        print(f"  offset_from_board_center_xy: dx={dx_center:+.3f} dy={dy_center:+.3f}")
        print(f"  height_above_board_surface: {dz_board:.3f} m")
        if baseline_xyz is not None:
            print(
                "  delta_from_current: "
                f"dx={xyz[0] - baseline_xyz[0]:+.3f} "
                f"dy={xyz[1] - baseline_xyz[1]:+.3f} "
                f"dz={xyz[2] - baseline_xyz[2]:+.3f}"
            )
        print(f"  note: {candidate.get('note', '')}")
        print(f"  evaluation_focus: {candidate.get('evaluation_focus', '')}")
        print("")

    print("Manual checklist")
    print("  1. Full board visible with margin on all four edges.")
    print("  2. Board center close to image center.")
    print("  3. Arm/gripper not blocking the board center or far corners.")
    print("  4. Pieces separated enough for future square assignment.")
    print("  5. Outer squares still visible for future geometry fitting.")


if __name__ == "__main__":
    main()
