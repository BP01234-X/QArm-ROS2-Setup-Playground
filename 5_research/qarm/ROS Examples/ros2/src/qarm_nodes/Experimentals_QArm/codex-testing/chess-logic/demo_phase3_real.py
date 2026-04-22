"""Run the Phase 3 orchestration with the real executor edge enabled."""

from __future__ import annotations

import argparse

from ascii_display import AsciiDisplay
from chess_logic import ChessLogicController
from game_orchestrator import GameOrchestrator


def build_starting_board_map() -> dict[str, str | None]:
    """Return a square map for the standard initial chess position."""

    controller = ChessLogicController()
    controller.reset_to_starting_position()
    return controller.expected_board().by_square


def build_verified_board_map(uci: str) -> dict[str, str | None]:
    """Return the expected board after applying one move from the start position."""

    controller = ChessLogicController()
    controller.reset_to_starting_position()
    controller.apply_move_uci(uci)
    return controller.expected_board().by_square


def main() -> None:
    """Drive the real QArm bridge through the existing Phase 3 executor API."""

    parser = argparse.ArgumentParser(description="Phase 3 real-hardware executor demo.")
    parser.add_argument("--move", default="e2e4", help="Single UCI move to execute, e.g. e2e4.")
    parser.add_argument(
        "--bridge-dir",
        default=None,
        help="Optional path to the existing codex-testing bridge directory.",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip overriding observer mock data for post-move verification.",
    )
    args = parser.parse_args()

    move_text = args.move.strip().lower()
    initial_observed_board = build_starting_board_map()
    verification_board = None if args.skip_verify else build_verified_board_map(move_text)

    orchestrator = GameOrchestrator(
        mock_mode=False,
        initial_observed_board=initial_observed_board,
    )
    if args.bridge_dir is not None:
        from move_executor import MoveExecutor

        orchestrator.move_executor = MoveExecutor.from_yaml(
            Path(__file__).resolve().parent / "config" / "observer_pose.yaml",
            mock_mode=False,
            bridge_dir=args.bridge_dir,
        )

    display = AsciiDisplay()
    print("WARNING: real executor mode will send commands through codex-testing/target_pose.json")
    print("Ensure `ros2 launch qarm_nodes move_qarm.py` is already running in a ROS terminal.")

    print("=== BOOT ===")
    observed = orchestrator.boot()
    print(display.show_fsm_status(orchestrator.motion_fsm.status))
    print(display.show_observed_board(observed))

    print("=== MOVE REQUEST ===")
    print(display.show_last_move(move_text))
    result = orchestrator.execute_one_move(move_text, verification_board=verification_board)

    print("=== FINAL SNAPSHOT ===")
    print(orchestrator.debug_snapshot())
    print(display.show_verification(result))

    print("=== EXECUTOR LOG ===")
    for entry in orchestrator.move_executor.action_log:
        print(entry)


if __name__ == "__main__":
    from pathlib import Path

    main()
