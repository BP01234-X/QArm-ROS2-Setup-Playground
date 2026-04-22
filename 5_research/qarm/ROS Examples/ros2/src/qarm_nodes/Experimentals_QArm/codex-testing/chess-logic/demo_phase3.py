"""Runnable Phase 3 CLI demo for the isolated chess orchestration prototype."""

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
    """Run the full Phase 3 mock demo for a single UCI move."""

    parser = argparse.ArgumentParser(description="Phase 3 chess/QArm orchestration demo.")
    parser.add_argument("--move", default=None, help="Single UCI move to execute, e.g. e2e4.")
    parser.add_argument(
        "--simulate-mismatch",
        action="store_true",
        help="Force board verification to fail after the mock move.",
    )
    args = parser.parse_args()

    move_text = (args.move or input("Enter one UCI move [e2e4]: ").strip() or "e2e4").lower()
    initial_observed_board = build_starting_board_map()
    verification_board = build_verified_board_map(move_text)
    if args.simulate_mismatch:
        verification_board = dict(verification_board)
        verification_board["e4"] = None

    orchestrator = GameOrchestrator(
        mock_mode=True,
        initial_observed_board=initial_observed_board,
    )
    display = AsciiDisplay()

    print("=== BOOT ===")
    observed = orchestrator.boot()
    print(display.show_fsm_status(orchestrator.motion_fsm.status))
    print(display.show_observed_board(observed))
    print(display.show_expected_board(orchestrator.current_expected_board()))

    print("=== MOVE REQUEST ===")
    print(display.show_last_move(move_text))
    result = orchestrator.execute_one_move(move_text, verification_board=verification_board)

    print("=== FINAL SNAPSHOT ===")
    print(orchestrator.debug_snapshot())
    print(display.show_expected_board(orchestrator.current_expected_board()))
    print(display.show_verification(result))

    print("=== EXECUTOR LOG ===")
    for entry in orchestrator.move_executor.action_log:
        print(entry)

    if orchestrator.motion_fsm.status.state == "ERROR_RECOVERY":
        print("System ended in ERROR_RECOVERY. Run recover_to_observer() after inspection.")


if __name__ == "__main__":
    main()
