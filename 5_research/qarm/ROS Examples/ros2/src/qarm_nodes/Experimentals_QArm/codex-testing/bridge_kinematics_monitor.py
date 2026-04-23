#!/usr/bin/env python3

"""Bridge-side kinematics monitor for observer-pose tuning."""

from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from pathlib import Path
from typing import Any


def _ensure_chess_logic_path(bridge_dir: Path) -> None:
    """Make the chess-logic helper importable from the bridge folder."""

    chess_logic_dir = bridge_dir / "chess-logic"
    chess_logic_str = str(chess_logic_dir)
    if chess_logic_dir.exists() and chess_logic_str not in sys.path:
        sys.path.insert(0, chess_logic_str)


def _snapshot_dict(snapshot: Any) -> dict[str, Any]:
    return {
        "bridge_state": snapshot.bridge_state,
        "active_goal_id": snapshot.active_goal_id,
        "active_goal_pose": list(snapshot.active_goal_pose) if snapshot.active_goal_pose is not None else None,
        "live_task_space_pose": list(snapshot.live_task_space_pose) if snapshot.live_task_space_pose is not None else None,
        "target_goal_pose": list(snapshot.target_goal_pose) if snapshot.target_goal_pose is not None else None,
        "camera_center_depth_m": snapshot.camera_center_depth_m,
        "camera_rgb_shape": list(snapshot.camera_rgb_shape) if snapshot.camera_rgb_shape is not None else None,
        "camera_depth_shape": list(snapshot.camera_depth_shape) if snapshot.camera_depth_shape is not None else None,
    }


def _pose_score_dict(score: Any) -> dict[str, Any]:
    return {
        "xyz": list(score.xyz),
        "wrist": score.wrist,
        "extrinsic_name": score.extrinsic_name,
        "projected_center_uv": list(score.projected_center_uv) if score.projected_center_uv is not None else None,
        "board_axis_intersection_world": (
            list(score.board_axis_intersection_world) if score.board_axis_intersection_world is not None else None
        ),
        "visible_corner_count": score.visible_corner_count,
        "projected_area_px2": score.projected_area_px2,
        "center_error_px": score.center_error_px,
        "axis_error_m": score.axis_error_m,
        "axis_depth_m": score.axis_depth_m,
        "score": score.score,
        "phi_optimal": list(score.phi_optimal),
        "camera_world_xyz": list(score.camera_world_xyz),
    }


def _build_payload(
    bridge_dir: Path,
    config_dir: Path,
    output_file: Path,
    top: int,
    seed_source: str,
) -> dict[str, Any]:
    _ensure_chess_logic_path(bridge_dir)

    from kinematics.bridge_kinematics_helper import BridgeKinematicsHelper

    helper = BridgeKinematicsHelper(config_dir=config_dir, bridge_dir=bridge_dir)
    snapshot = helper.bridge_snapshot()
    seed_xyz, wrist = helper.resolve_seed_pose(seed_source)
    selected_extrinsic = helper.refresh_camera_extrinsic(
        seed_xyz=seed_xyz,
        wrist=wrist,
        center_depth_m=snapshot.camera_center_depth_m,
    )
    ranked = helper.rank_grid_around_seed(
        seed_xyz=seed_xyz,
        wrist=wrist,
        x_offsets=[-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03],
        y_offsets=[-0.02, -0.01, 0.0, 0.01, 0.02],
        z_offsets=[-0.03, -0.02, -0.01, 0.0, 0.01],
    )
    live_score = helper.score_current_live_pose()

    return {
        "state": "ok",
        "timestamp": time.time(),
        "bridge_dir": str(bridge_dir),
        "config_dir": str(config_dir),
        "output_file": str(output_file),
        "seed_source": seed_source,
        "seed_pose": {
            "xyz": list(seed_xyz),
            "wrist": wrist,
        },
        "selected_extrinsic_name": selected_extrinsic,
        "bridge_snapshot": _snapshot_dict(snapshot),
        "current_live_score": None if live_score is None else _pose_score_dict(live_score),
        "top_candidates": [_pose_score_dict(item) for item in ranked[:top]],
    }


def _write_payload(output_file: Path, payload: dict[str, Any]) -> None:
    output_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Write bridge-aware observer kinematics status JSON.")
    parser.add_argument("--bridge-dir", type=str, required=True, help="Path to codex-testing.")
    parser.add_argument("--config-dir", type=str, default=None, help="Path to chess-logic/config.")
    parser.add_argument("--output-file", type=str, default=None, help="Path to kinematics_status.json.")
    parser.add_argument("--top", type=int, default=8, help="Number of ranked candidates to keep.")
    parser.add_argument("--period-sec", type=float, default=1.0, help="Refresh period in seconds.")
    parser.add_argument(
        "--seed-source",
        choices=["bridge", "config", "live", "target", "active"],
        default="bridge",
        help="How to choose the observer-pose seed for the local search.",
    )
    args = parser.parse_args()

    bridge_dir = Path(args.bridge_dir).expanduser().resolve()
    config_dir = Path(args.config_dir).expanduser().resolve() if args.config_dir else bridge_dir / "chess-logic" / "config"
    output_file = Path(args.output_file).expanduser().resolve() if args.output_file else bridge_dir / "kinematics_status.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    while True:
        try:
            payload = _build_payload(
                bridge_dir=bridge_dir,
                config_dir=config_dir,
                output_file=output_file,
                top=args.top,
                seed_source=args.seed_source,
            )
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            payload = {
                "state": "error",
                "timestamp": time.time(),
                "bridge_dir": str(bridge_dir),
                "config_dir": str(config_dir),
                "output_file": str(output_file),
                "seed_source": args.seed_source,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }

        _write_payload(output_file, payload)
        time.sleep(args.period_sec)


if __name__ == "__main__":
    main()
