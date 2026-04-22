"""Symbolic chess rule engine wrapper backed by python-chess."""

from __future__ import annotations

from dataclasses import dataclass

try:
    import chess
except ImportError as exc:  # pragma: no cover - handled at runtime
    chess = None
    CHESS_IMPORT_ERROR = exc
else:
    CHESS_IMPORT_ERROR = None

from board_geometry import FILES, RANKS
from models import ChessMoveCommand, ExpectedBoard, ObservedBoard, VerificationResult

PIECE_NAMES = {
    "p": "pawn",
    "n": "knight",
    "b": "bishop",
    "r": "rook",
    "q": "queen",
    "k": "king",
}


def piece_name_from_symbol(symbol: str) -> str:
    """Convert a FEN symbol like `P` into a stable piece name."""

    color = "white" if symbol.isupper() else "black"
    return f"{color}_{PIECE_NAMES[symbol.lower()]}"


def piece_symbol_from_name(piece_name: str) -> str:
    """Convert a stable piece name into a FEN symbol."""

    raw = piece_name.strip()
    if len(raw) == 1 and raw.lower() in {"p", "n", "b", "r", "q", "k"}:
        return raw
    normalized = raw.lower()
    color, piece = normalized.split("_", maxsplit=1)
    symbol = next(symbol for symbol, name in PIECE_NAMES.items() if name == piece)
    return symbol.upper() if color == "white" else symbol


@dataclass
class ChessLogicController:
    """Owns the symbolic expected board and legal move validation."""

    board: "chess.Board"
    move_history: list[str]

    def __init__(self) -> None:
        if chess is None:
            raise RuntimeError("python-chess is required for Phase 3") from CHESS_IMPORT_ERROR
        self.board = chess.Board()
        self.move_history = []

    def reset_to_starting_position(self) -> None:
        """Reset the symbolic board to the standard initial chess position."""

        self.board.reset()
        self.move_history.clear()

    def set_from_observed_board(self, observed_board: ObservedBoard) -> None:
        """Initialize or replace the symbolic board from an observed board.

        This assumes the observed board already reflects a legal arrangement.
        Unknown castling rights and en passant state are conservatively reset.
        """

        board = chess.Board.empty()
        for square, piece_name in observed_board.by_square.items():
            if piece_name is None:
                continue
            board.set_piece_at(
                chess.parse_square(square),
                chess.Piece.from_symbol(piece_symbol_from_name(piece_name)),
            )
        board.turn = chess.WHITE
        board.castling_rights = chess.BB_EMPTY
        board.ep_square = None
        board.halfmove_clock = 0
        board.fullmove_number = 1
        board.clear_stack()
        self.board = board
        self.move_history.clear()

    def validate_move_uci(self, uci: str) -> bool:
        """Return whether a UCI move is legal in the current symbolic state."""

        try:
            move = self.board.parse_uci(uci.strip().lower())
        except ValueError:
            return False
        return move in self.board.legal_moves

    def apply_move_uci(self, uci: str) -> ChessMoveCommand:
        """Validate and apply a UCI move, updating the expected board."""

        normalized = uci.strip().lower()
        move = self.board.parse_uci(normalized)
        if move not in self.board.legal_moves:
            raise ValueError(f"Illegal move for current board state: {normalized}")

        source_square = chess.square_name(move.from_square)
        target_square = chess.square_name(move.to_square)
        moving_piece = self.board.piece_at(move.from_square)
        piece_name = piece_name_from_symbol(moving_piece.symbol()) if moving_piece else None
        is_capture = self.board.is_capture(move)
        promotion = PIECE_NAMES.get(chess.piece_symbol(move.promotion), None) if move.promotion else None

        self.board.push(move)
        self.move_history.append(normalized)
        return ChessMoveCommand(
            uci=normalized,
            source=source_square,
            target=target_square,
            piece_name=piece_name,
            is_capture=is_capture,
            promotion=promotion,
        )

    def expected_board(self) -> ExpectedBoard:
        """Export the current symbolic board as a comparison-friendly snapshot."""

        return ExpectedBoard(
            by_square=self.square_map_from_board(self.board),
            fen=self.board.fen(),
            move_number=int(self.board.fullmove_number),
            side_to_move="white" if self.board.turn == chess.WHITE else "black",
        )

    def compare_with_observed(self, observed_board: ObservedBoard) -> VerificationResult:
        """Compare the symbolic expected board against observer output."""

        expected = self.expected_board().by_square
        mismatches: list[str] = []
        for rank_char in reversed(RANKS):
            for file_char in FILES:
                square = f"{file_char}{rank_char}"
                expected_piece = expected.get(square)
                observed_piece = observed_board.by_square.get(square)
                if expected_piece != observed_piece:
                    mismatches.append(
                        f"{square}: expected {expected_piece or 'empty'}, "
                        f"observed {observed_piece or 'empty'}"
                    )
        return VerificationResult(success=not mismatches, mismatches=mismatches)

    def fen_summary(self) -> str:
        """Return the current FEN string for debugging."""

        return self.board.fen()

    def move_history_summary(self) -> str:
        """Return the move history as a printable string."""

        return ", ".join(self.move_history) or "<none>"

    @staticmethod
    def square_map_from_board(board: "chess.Board") -> dict[str, str | None]:
        """Convert a python-chess board into a 64-square piece-name map."""

        square_map: dict[str, str | None] = {}
        for rank_char in RANKS:
            for file_char in FILES:
                square = f"{file_char}{rank_char}"
                piece = board.piece_at(chess.parse_square(square))
                square_map[square] = piece_name_from_symbol(piece.symbol()) if piece else None
        return square_map

    @classmethod
    def square_map_from_fen(cls, fen: str) -> dict[str, str | None]:
        """Build a 64-square piece-name map from any valid FEN."""

        if chess is None:
            raise RuntimeError("python-chess is required for Phase 3") from CHESS_IMPORT_ERROR
        board = chess.Board(fen)
        return cls.square_map_from_board(board)
