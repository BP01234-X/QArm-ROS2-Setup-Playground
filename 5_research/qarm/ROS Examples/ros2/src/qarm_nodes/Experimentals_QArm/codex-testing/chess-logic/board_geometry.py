"""Board geometry helpers for square naming and world-coordinate lookup."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled at runtime
    yaml = None
    YAML_IMPORT_ERROR = exc
else:
    YAML_IMPORT_ERROR = None

from models import XYZ

FILES = "abcdefgh"
RANKS = "12345678"


@dataclass(frozen=True)
class BoardGeometry:
    """Converts chess squares into board and world coordinates."""

    board_origin_world_xyz: XYZ
    square_size_m: float
    board_height_z: float
    board_frame_name: str

    @classmethod
    def from_yaml(cls, path: str | Path) -> "BoardGeometry":
        """Load board geometry from YAML config."""

        if yaml is None:
            raise RuntimeError("PyYAML is required to load board.yaml") from YAML_IMPORT_ERROR
        payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        origin = tuple(float(v) for v in payload["board_origin_world_xyz"])
        return cls(
            board_origin_world_xyz=origin,
            square_size_m=float(payload["square_size_m"]),
            board_height_z=float(payload["board_height_z"]),
            board_frame_name=str(payload["board_frame_name"]),
        )

    @property
    def board_surface_world_z(self) -> float:
        """Absolute world z for the board surface."""

        return float(self.board_origin_world_xyz[2] + self.board_height_z)

    def all_squares(self) -> list[str]:
        """Return squares ordered from a1 through h8."""

        return [f"{file_char}{rank_char}" for rank_char in RANKS for file_char in FILES]

    def square_to_indices(self, square: str) -> tuple[int, int]:
        """Convert a square like `e4` into zero-based file/rank indices."""

        normalized = square.strip().lower()
        if len(normalized) != 2 or normalized[0] not in FILES or normalized[1] not in RANKS:
            raise ValueError(f"Invalid chess square: {square!r}")
        file_index = FILES.index(normalized[0])
        rank_index = RANKS.index(normalized[1])
        return file_index, rank_index

    def indices_to_square(self, file_index: int, rank_index: int) -> str:
        """Convert zero-based file/rank indices into chess notation."""

        if not (0 <= file_index < 8 and 0 <= rank_index < 8):
            raise ValueError("File and rank indices must be in [0, 7].")
        return f"{FILES[file_index]}{RANKS[rank_index]}"

    def square_center_board(self, square: str) -> XYZ:
        """Return the square center in the board frame."""

        file_index, rank_index = self.square_to_indices(square)
        x = (file_index + 0.5) * self.square_size_m
        y = (rank_index + 0.5) * self.square_size_m
        return (x, y, self.board_height_z)

    def square_center_world(self, square: str, z_offset_m: float = 0.0) -> XYZ:
        """Return the world-frame center for a square with an optional z offset."""

        board_x, board_y, _ = self.square_center_board(square)
        origin_x, origin_y, origin_z = self.board_origin_world_xyz
        return (
            origin_x + board_x,
            origin_y + board_y,
            origin_z + self.board_height_z + z_offset_m,
        )

    def board_to_world(self, board_xyz: XYZ) -> XYZ:
        """Convert a board-frame xyz into world coordinates."""

        origin_x, origin_y, origin_z = self.board_origin_world_xyz
        return (
            origin_x + board_xyz[0],
            origin_y + board_xyz[1],
            origin_z + board_xyz[2],
        )
