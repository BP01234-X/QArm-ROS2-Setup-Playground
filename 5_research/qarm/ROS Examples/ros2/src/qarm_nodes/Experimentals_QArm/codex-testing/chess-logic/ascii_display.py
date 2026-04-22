"""Terminal display helpers for the Phase 3 chess prototype."""

from __future__ import annotations

from board_geometry import FILES
from models import ExpectedBoard, FSMStatus, ObservedBoard, VerificationResult

PIECE_ABBREVIATIONS = {
    None: "..",
    "white_pawn": "WP",
    "white_knight": "WN",
    "white_bishop": "WB",
    "white_rook": "WR",
    "white_queen": "WQ",
    "white_king": "WK",
    "black_pawn": "BP",
    "black_knight": "BN",
    "black_bishop": "BB",
    "black_rook": "BR",
    "black_queen": "BQ",
    "black_king": "BK",
}


class AsciiDisplay:
    """Pretty-printers for boards, FSM status, and verification results."""

    def render_square_map(self, square_map: dict[str, str | None], title: str) -> str:
        """Render a board map as a compact ASCII table."""

        lines = [title]
        for rank in range(8, 0, -1):
            row = []
            for file_char in FILES:
                square = f"{file_char}{rank}"
                piece_name = square_map.get(square)
                row.append(PIECE_ABBREVIATIONS.get(piece_name, "??"))
            lines.append(f"{rank} | {' '.join(row)}")
        lines.append("    " + " ".join(file_char.upper() for file_char in FILES))
        return "\n".join(lines)

    def show_expected_board(self, board: ExpectedBoard) -> str:
        """Render the symbolic expected board."""

        return self.render_square_map(
            board.by_square,
            title=f"EXPECTED BOARD | side={board.side_to_move} | move={board.move_number}",
        )

    def show_observed_board(self, board: ObservedBoard) -> str:
        """Render the current observed board."""

        return self.render_square_map(board.by_square, title=f"OBSERVED BOARD | t={board.timestamp:.3f}")

    def show_fsm_status(self, status: FSMStatus) -> str:
        """Render the current FSM status."""

        return (
            f"FSM state={status.state} | robot_busy={status.robot_busy} | "
            f"pending_move={status.pending_move_uci or '<none>'} | "
            f"last_error={status.last_error or '<none>'}"
        )

    def show_last_move(self, uci: str) -> str:
        """Render the last requested move."""

        return f"LAST MOVE | {uci}"

    def show_gripper_target(self, target: float | None) -> str:
        """Render the current target gripper value."""

        return f"GRIPPER TARGET | {target if target is not None else '<none>'}"

    def show_verification(self, result: VerificationResult) -> str:
        """Render the verification outcome."""

        if result.success:
            return "VERIFICATION | success"
        lines = ["VERIFICATION | mismatch detected"]
        lines.extend(f"  - {mismatch}" for mismatch in result.mismatches)
        return "\n".join(lines)
