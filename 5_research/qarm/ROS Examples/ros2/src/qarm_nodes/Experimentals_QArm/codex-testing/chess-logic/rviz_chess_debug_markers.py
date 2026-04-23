"""RViz MarkerArray builder for Phase 4 chessboard debug visualization."""

from __future__ import annotations

from dataclasses import dataclass

from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker, MarkerArray

from board_observer import BoardFrameEstimate
from models import ObservedBoard, XYZ


@dataclass(frozen=True)
class MarkerStyle:
    """Reusable marker style configuration."""

    border_rgba: tuple[float, float, float, float] = (1.0, 0.85, 0.2, 0.95)
    grid_rgba: tuple[float, float, float, float] = (0.6, 0.6, 0.6, 0.8)
    centers_rgba: tuple[float, float, float, float] = (0.1, 0.7, 1.0, 0.9)
    text_rgba: tuple[float, float, float, float] = (0.95, 0.95, 0.95, 0.95)
    pieces_rgba: tuple[float, float, float, float] = (1.0, 0.3, 0.3, 0.95)
    assignment_rgba: tuple[float, float, float, float] = (0.1, 1.0, 0.8, 0.9)
    occupied_rgba: tuple[float, float, float, float] = (0.2, 1.0, 0.2, 0.22)
    a1_rgba: tuple[float, float, float, float] = (0.2, 1.0, 0.2, 1.0)
    h8_rgba: tuple[float, float, float, float] = (1.0, 0.35, 0.35, 1.0)
    border_live_rgba: tuple[float, float, float, float] = (0.1, 1.0, 0.3, 0.95)
    border_fallback_rgba: tuple[float, float, float, float] = (1.0, 0.55, 0.15, 0.95)
    border_weak_rgba: tuple[float, float, float, float] = (0.95, 0.95, 0.20, 0.95)
    border_stale_rgba: tuple[float, float, float, float] = (1.0, 0.35, 0.35, 0.95)


class ChessDebugMarkerBuilder:
    """Builds `visualization_msgs/MarkerArray` for chessboard debug overlays."""

    def __init__(self, *, frame_id: str = "world", style: MarkerStyle | None = None) -> None:
        self.frame_id = frame_id
        self.style = style or MarkerStyle()

    def build(
        self,
        board_frame: BoardFrameEstimate,
        observed_board: ObservedBoard,
        *,
        stamp,
    ) -> MarkerArray:
        """Create full debug marker set from board frame + observed occupancy."""

        marker_array = MarkerArray()
        marker_id = 0

        marker_array.markers.append(self._board_border_marker(board_frame, stamp, marker_id))
        marker_id += 1
        marker_array.markers.append(self._grid_marker(board_frame, stamp, marker_id))
        marker_id += 1
        marker_array.markers.append(self._centers_marker(board_frame, stamp, marker_id))
        marker_id += 1
        marker_array.markers.append(self._occupied_squares_marker(board_frame, observed_board, stamp, marker_id))
        marker_id += 1
        marker_array.markers.append(self._piece_points_marker(observed_board, stamp, marker_id))
        marker_id += 1
        marker_array.markers.append(self._assignment_lines_marker(board_frame, observed_board, stamp, marker_id))
        marker_id += 1

        for square in sorted(board_frame.square_centers_world.keys(), key=_square_sort_key):
            marker_array.markers.append(self._square_label_marker(board_frame, square, stamp, marker_id))
            marker_id += 1
        marker_array.markers.append(self._orientation_label_marker(board_frame, "a1", stamp, marker_id))
        marker_id += 1
        marker_array.markers.append(self._orientation_label_marker(board_frame, "h8", stamp, marker_id))
        marker_id += 1
        marker_array.markers.append(self._status_label_marker(board_frame, stamp, marker_id))

        return marker_array

    def build_fixed_manual(
        self,
        *,
        board_outer_corners_world: dict[str, XYZ],
        square_centers_world: dict[str, XYZ],
        source: str,
        stamp,
    ) -> MarkerArray:
        """Build a persistent manual-calibration marker layer."""

        observed_board = ObservedBoard(
            by_square={square: None for square in square_centers_world},
            observations={},
            timestamp=0.0,
        )
        board_frame = BoardFrameEstimate(
            frame_name=self.frame_id,
            origin_world_xyz=board_outer_corners_world["a1"],
            x_axis_world=_unit_axis(board_outer_corners_world["a1"], board_outer_corners_world["h1"]),
            y_axis_world=_unit_axis(board_outer_corners_world["a1"], board_outer_corners_world["a8"]),
            z_axis_world=(0.0, 0.0, 1.0),
            square_centers_world=dict(square_centers_world),
            square_regions={},
            source=f"fixed_manual:{source}",
            board_detection_mode="manual",
            board_outer_corners_world=dict(board_outer_corners_world),
            fit_state="manual_fixed",
            used_live_fit=False,
            used_manual_fallback=False,
        )
        return self.build(board_frame, observed_board, stamp=stamp)

    def _board_border_marker(self, board_frame: BoardFrameEstimate, stamp, marker_id: int) -> Marker:
        marker = self._new_marker("board_border", marker_id, Marker.LINE_STRIP, stamp)
        marker.scale.x = 0.004
        if board_frame.fit_state == "live":
            marker.color = _rgba(*self.style.border_live_rgba)
        elif board_frame.fit_state == "weak_held":
            marker.color = _rgba(*self.style.border_weak_rgba)
        elif board_frame.fit_state == "stale_manual":
            marker.color = _rgba(*self.style.border_stale_rgba)
        elif board_frame.used_manual_fallback:
            marker.color = _rgba(*self.style.border_fallback_rgba)
        else:
            marker.color = _rgba(*self.style.border_rgba)
        corners = board_frame.board_outer_corners_world
        sequence = ["a1", "h1", "h8", "a8", "a1"]
        marker.points = [_point(corners[key]) for key in sequence if key in corners]
        return marker

    def _grid_marker(self, board_frame: BoardFrameEstimate, stamp, marker_id: int) -> Marker:
        marker = self._new_marker("board_grid", marker_id, Marker.LINE_LIST, stamp)
        marker.scale.x = 0.0018
        marker.color = _rgba(*self.style.grid_rgba)
        corners = board_frame.board_outer_corners_world
        if not all(key in corners for key in ("a1", "h1", "h8", "a8")):
            return marker

        for idx in range(9):
            t = idx / 8.0
            bottom = _lerp3(corners["a1"], corners["h1"], t)
            top = _lerp3(corners["a8"], corners["h8"], t)
            marker.points.append(_point(bottom))
            marker.points.append(_point(top))

        for idx in range(9):
            t = idx / 8.0
            left = _lerp3(corners["a1"], corners["a8"], t)
            right = _lerp3(corners["h1"], corners["h8"], t)
            marker.points.append(_point(left))
            marker.points.append(_point(right))
        return marker

    def _centers_marker(self, board_frame: BoardFrameEstimate, stamp, marker_id: int) -> Marker:
        marker = self._new_marker("square_centers", marker_id, Marker.SPHERE_LIST, stamp)
        marker.scale.x = 0.007
        marker.scale.y = 0.007
        marker.scale.z = 0.007
        marker.color = _rgba(*self.style.centers_rgba)
        marker.points = [_point(center) for center in board_frame.square_centers_world.values()]
        return marker

    def _occupied_squares_marker(
        self,
        board_frame: BoardFrameEstimate,
        observed_board: ObservedBoard,
        stamp,
        marker_id: int,
    ) -> Marker:
        marker = self._new_marker("occupied_squares", marker_id, Marker.CUBE_LIST, stamp)
        marker.scale.x = 0.033
        marker.scale.y = 0.033
        marker.scale.z = 0.0015
        marker.color = _rgba(*self.style.occupied_rgba)
        for square, piece_name in observed_board.by_square.items():
            if piece_name is None:
                continue
            center = board_frame.square_centers_world.get(square)
            if center is None:
                continue
            marker.points.append(_point((center[0], center[1], center[2] + 0.0006)))
        return marker

    def _piece_points_marker(self, observed_board: ObservedBoard, stamp, marker_id: int) -> Marker:
        marker = self._new_marker("pieces", marker_id, Marker.SPHERE_LIST, stamp)
        marker.scale.x = 0.018
        marker.scale.y = 0.018
        marker.scale.z = 0.018
        marker.color = _rgba(*self.style.pieces_rgba)
        for observation in observed_board.observations.values():
            if observation.world_xyz is None:
                continue
            marker.points.append(_point((observation.world_xyz[0], observation.world_xyz[1], observation.world_xyz[2] + 0.012)))
        return marker

    def _assignment_lines_marker(
        self,
        board_frame: BoardFrameEstimate,
        observed_board: ObservedBoard,
        stamp,
        marker_id: int,
    ) -> Marker:
        marker = self._new_marker("piece_assignments", marker_id, Marker.LINE_LIST, stamp)
        marker.scale.x = 0.0015
        marker.color = _rgba(*self.style.assignment_rgba)
        for square, observation in observed_board.observations.items():
            if observation.world_xyz is None:
                continue
            center = board_frame.square_centers_world.get(square)
            if center is None:
                continue
            piece_pt = (observation.world_xyz[0], observation.world_xyz[1], observation.world_xyz[2] + 0.012)
            center_pt = (center[0], center[1], center[2] + 0.001)
            marker.points.append(_point(piece_pt))
            marker.points.append(_point(center_pt))
        return marker

    def _square_label_marker(
        self,
        board_frame: BoardFrameEstimate,
        square: str,
        stamp,
        marker_id: int,
    ) -> Marker:
        center = board_frame.square_centers_world[square]
        marker = self._new_marker("square_labels", marker_id, Marker.TEXT_VIEW_FACING, stamp)
        marker.pose.position = _point((center[0], center[1], center[2] + 0.016))
        marker.scale.z = 0.012
        marker.color = _rgba(*self.style.text_rgba)
        marker.text = square
        return marker

    def _orientation_label_marker(
        self,
        board_frame: BoardFrameEstimate,
        square: str,
        stamp,
        marker_id: int,
    ) -> Marker:
        center = board_frame.square_centers_world[square]
        marker = self._new_marker("orientation_labels", marker_id, Marker.TEXT_VIEW_FACING, stamp)
        marker.pose.position = _point((center[0], center[1], center[2] + 0.03))
        marker.scale.z = 0.018
        marker.color = _rgba(*(self.style.a1_rgba if square == "a1" else self.style.h8_rgba))
        marker.text = square.upper()
        return marker

    def _status_label_marker(self, board_frame: BoardFrameEstimate, stamp, marker_id: int) -> Marker:
        center = board_frame.square_centers_world.get("a8") or next(
            iter(board_frame.square_centers_world.values())
        )
        marker = self._new_marker("status", marker_id, Marker.TEXT_VIEW_FACING, stamp)
        marker.pose.position = _point((center[0], center[1], center[2] + 0.055))
        marker.scale.z = 0.015
        marker.color = _rgba(*self.style.text_rgba)
        mode = board_frame.fit_state or (
            "manual_fallback" if board_frame.used_manual_fallback else "manual"
        )
        marker.text = (
            f"mode={mode} src={board_frame.source} "
            f"fit={board_frame.live_fit_confidence if board_frame.live_fit_confidence is not None else 0.0:.2f}"
        )
        return marker

    def _new_marker(self, namespace: str, marker_id: int, marker_type: int, stamp) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = stamp
        marker.ns = namespace
        marker.id = marker_id
        marker.type = marker_type
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0
        return marker


def _rgba(r: float, g: float, b: float, a: float) -> ColorRGBA:
    color = ColorRGBA()
    color.r = float(r)
    color.g = float(g)
    color.b = float(b)
    color.a = float(a)
    return color


def _point(xyz: XYZ) -> Point:
    pt = Point()
    pt.x = float(xyz[0])
    pt.y = float(xyz[1])
    pt.z = float(xyz[2])
    return pt


def _lerp3(a: XYZ, b: XYZ, t: float) -> XYZ:
    return (
        a[0] + (b[0] - a[0]) * t,
        a[1] + (b[1] - a[1]) * t,
        a[2] + (b[2] - a[2]) * t,
    )


def _square_sort_key(square: str) -> tuple[int, int]:
    file_idx = "abcdefgh".index(square[0])
    rank_idx = "12345678".index(square[1])
    return (rank_idx, file_idx)


def _unit_axis(a: XYZ, b: XYZ) -> XYZ:
    dx = float(b[0] - a[0])
    dy = float(b[1] - a[1])
    dz = float(b[2] - a[2])
    norm = (dx * dx + dy * dy + dz * dz) ** 0.5
    if norm <= 1e-9:
        return (0.0, 0.0, 0.0)
    return (dx / norm, dy / norm, dz / norm)
