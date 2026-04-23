"""Direct square-to-square real-move integration demo for Phase 4."""

from __future__ import annotations

import argparse
from pathlib import Path

from ascii_display import AsciiDisplay
from chess_logic import ChessLogicController
from game_orchestrator import GameOrchestrator
from move_executor import MoveExecutor


def build_starting_board_map() -> dict[str, str | None]:
    """Return a square map for the standard initial chess position."""

    controller = ChessLogicController()
    controller.reset_to_starting_position()
    return controller.expected_board().by_square


def build_expected_after_square_move(source_square: str, target_square: str) -> dict[str, str | None]:
    """Return expected board after one legal move from the start position."""

    controller = ChessLogicController()
    controller.reset_to_starting_position()
    controller.apply_move_uci(f"{source_square}{target_square}")
    return controller.expected_board().by_square


def main() -> None:
    """Execute one real square move through the existing orchestration stack."""

    parser = argparse.ArgumentParser(description="Phase 4 direct square-move real demo.")
    parser.add_argument("--source", default="e2", help="Source square, e.g. e2.")
    parser.add_argument("--target", default="e4", help="Target square, e.g. e4.")
    parser.add_argument(
        "--piece-name",
        default=None,
        help="Optional piece name hint, e.g. white_pawn.",
    )
    parser.add_argument(
        "--verify-mode",
        choices=("mock_expected", "observer"),
        default="mock_expected",
        help=(
            "mock_expected: force post-move observer map to expected board for deterministic hardware testing; "
            "observer: use live observer output for verification."
        ),
    )
    parser.add_argument(
        "--bridge-dir",
        default=None,
        help="Optional path to codex-testing bridge directory containing target_pose.json/status.json.",
    )
    args = parser.parse_args()

    source = args.source.strip().lower()
    target = args.target.strip().lower()
    piece_name = args.piece_name.strip().lower() if args.piece_name is not None else None

    initial_observed_board = build_starting_board_map()
    verification_board = None
    if args.verify_mode == "mock_expected":
        verification_board = build_expected_after_square_move(source, target)

    orchestrator = GameOrchestrator(
        mock_mode=False,
        initial_observed_board=initial_observed_board,
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

    display = AsciiDisplay()
    print("WARNING: real mode will command QArm via codex-testing/target_pose.json.")
    print("Ensure move_qarm bridge launch is running before this demo.")
    print(f"Requested square move: {source} -> {target}")
    print(f"Verification mode: {args.verify_mode}")
    print("=== MOVE TO CHESS_OBSERVER (BOOT) ===")
    observed = orchestrator.boot()
    print(display.show_fsm_status(orchestrator.motion_fsm.status))
    print(display.show_observed_board(observed))

    board_debug = orchestrator.manipulation_board_debug()
    print("=== ACTIVE BOARD MODEL ===")
    print(f"manipulation_board_source={board_debug['source']}")
    print(f"board_outer_corners_world={board_debug['corners_world']}")
    print(f"square_center[{source}]={orchestrator.manipulation_square_center_world(source)}")
    print(f"square_center[{target}]={orchestrator.manipulation_square_center_world(target)}")
    print(f"planner_board_source={orchestrator.grasp_planner.board_source}")
    print(
        "command_frame="
        f"{orchestrator.move_executor.command_frame_name} units={orchestrator.move_executor.command_units} "
        f"tcp_offset_xyz_m={orchestrator.move_executor.tcp_offset_xyz_m}"
    )

    plan = orchestrator.preview_square_move_plan(source, target, piece_name=piece_name)
    gp = plan.grasp_plan
    print("=== SQUARE TO POSE BRIDGE ===")
    print(
        "planner_marker_center_mode="
        f"{orchestrator.grasp_planner.rules.marker_center_mode} "
        f"marker_center_clearance_m={orchestrator.grasp_planner.rules.marker_center_clearance_m:.3f}"
    )
    print(f"source_approach={gp.source_approach_world_xyz}")
    print(f"source_pick={gp.source_pick_world_xyz}")
    print(f"source_lift={gp.source_lift_world_xyz}")
    print(f"target_approach={gp.target_approach_world_xyz}")
    print(f"target_place={gp.target_place_world_xyz}")
    print(f"target_retreat={gp.target_retreat_world_xyz}")
    print(f"gripper_open={gp.gripper_open_value} gripper_close={gp.gripper_close_value}")

    print("=== EXECUTE DIRECT SQUARE MOVE ===")
    try:
        result = orchestrator.execute_square_move(
            source_square=source,
            target_square=target,
            piece_name=piece_name,
            verification_board=verification_board,
        )
    except Exception as exc:
        print(f"ERROR: square move failed: {exc}")
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

    print("=== FINAL SNAPSHOT ===")
    print(orchestrator.debug_snapshot())
    print(display.show_verification(result))

    print("=== EXECUTOR LOG ===")
    for entry in orchestrator.move_executor.action_log:
        print(entry)


if __name__ == "__main__":
    main()
