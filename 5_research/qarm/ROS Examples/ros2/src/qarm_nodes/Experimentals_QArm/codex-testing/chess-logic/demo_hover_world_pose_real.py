"""Hover-only real test using explicit planner world poses (no pick/place)."""

from __future__ import annotations

import argparse
from pathlib import Path

from chess_logic import ChessLogicController
from game_orchestrator import GameOrchestrator
from move_executor import MoveExecutor


def build_starting_board_map() -> dict[str, str | None]:
    controller = ChessLogicController()
    controller.reset_to_starting_position()
    return controller.expected_board().by_square


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="e2", help="Source square, e.g. e2.")
    parser.add_argument("--target", default="e4", help="Target square, e.g. e4.")
    parser.add_argument(
        "--bridge-dir",
        default=None,
        help="Path to codex-testing bridge directory containing target_pose.json/status.json.",
    )
    args = parser.parse_args()

    source = args.source.strip().lower()
    target = args.target.strip().lower()

    orchestrator = GameOrchestrator(
        mock_mode=False,
        initial_observed_board=build_starting_board_map(),
    )
    if args.bridge_dir is not None:
        orchestrator.move_executor = MoveExecutor.from_yaml(
            Path(__file__).resolve().parent / "config" / "observer_pose.yaml",
            mock_mode=False,
            bridge_dir=args.bridge_dir,
        )
        orchestrator.move_executor.set_board_square_centers(
            square_centers_world=orchestrator.manipulation_square_centers_world,
            board_source=orchestrator.manipulation_board_source,
        )

    print("WARNING: hover-only real mode commands QArm through target_pose.json.")
    print(f"Hover request: {source} -> {target}")
    print("=== MOVE TO CHESS_OBSERVER (BOOT) ===")
    observed = orchestrator.boot()
    print(f"Boot observed timestamp={observed.timestamp:.3f}")

    board_debug = orchestrator.manipulation_board_debug()
    print("=== ACTIVE MANIPULATION BOARD ===")
    print(f"source={board_debug['source']}")
    print(f"corners_world={board_debug['corners_world']}")
    print(f"square_center[{source}]={orchestrator.manipulation_square_center_world(source)}")
    print(f"square_center[{target}]={orchestrator.manipulation_square_center_world(target)}")

    plan = orchestrator.preview_square_move_plan(source, target)
    gp = plan.grasp_plan
    print("=== HOVER PLAN (EXPLICIT WORLD) ===")
    print(
        "planner_marker_center_mode="
        f"{orchestrator.grasp_planner.rules.marker_center_mode} "
        f"marker_center_clearance_m={orchestrator.grasp_planner.rules.marker_center_clearance_m:.3f}"
    )
    print(f"source_approach={gp.source_approach_world_xyz}")
    print(f"target_approach={gp.target_approach_world_xyz}")
    print(
        "command_frame="
        f"{orchestrator.move_executor.command_frame_name} units={orchestrator.move_executor.command_units} "
        f"tcp_offset_xyz_m={orchestrator.move_executor.tcp_offset_xyz_m}"
    )

    try:
        orchestrator.move_executor.set_gripper(0.7)
        orchestrator.move_executor.wait_until_done()
        orchestrator.move_executor.move_to_world_pose(
            stage_name="hover_source_approach",
            world_xyz=gp.source_approach_world_xyz,
            note=f"Hover-only source approach for {source}.",
        )
        orchestrator.move_executor.wait_until_done()
        orchestrator.move_executor.move_to_world_pose(
            stage_name="hover_target_approach",
            world_xyz=gp.target_approach_world_xyz,
            note=f"Hover-only target approach for {target}.",
        )
        orchestrator.move_executor.wait_until_done()
        orchestrator.move_executor.move_to_observer_pose()
        orchestrator.move_executor.wait_until_done()
    except Exception as exc:
        print(f"ERROR: hover sequence failed: {exc}")
        print("Attempting safety recovery to chess_observer pose...")
        try:
            orchestrator.move_executor.set_gripper(0.7)
            orchestrator.move_executor.wait_until_done()
            orchestrator.move_executor.move_to_observer_pose()
            orchestrator.move_executor.wait_until_done()
            print("Safety recovery finished.")
        except Exception as recover_exc:
            print(f"Safety recovery also failed: {recover_exc}")
        raise SystemExit(1) from exc

    print("=== EXECUTOR LOG ===")
    for entry in orchestrator.move_executor.action_log:
        print(entry)


if __name__ == "__main__":
    main()
