#!/usr/bin/env python3

"""ROS 2 RViz debug publisher for Phase 4 chessboard geometry overlays."""

from __future__ import annotations

import json
import struct
import time
from pathlib import Path
from typing import Any

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from geometry_msgs.msg import Point
from sensor_msgs.msg import Image
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker, MarkerArray

from calibrated_board_model import load_fixed_calibrated_board_model
from board_observer import DetectedPieceCandidate
from observer_factory import build_camera_observer
from rviz_chess_debug_markers import ChessDebugMarkerBuilder


class ChessRvizDebugNode(Node):
    """Publishes chessboard debug MarkerArray aligned to world frame."""

    def __init__(self) -> None:
        super().__init__("chess_rviz_debug")

        default_config_dir = Path(__file__).resolve().parent / "config"
        default_status_file = Path(__file__).resolve().parents[1] / "status.json"

        self.declare_parameter("marker_topic", "/chess/debug/markers")
        self.declare_parameter("fixed_frame", "world")
        self.declare_parameter("color_topic", "qarm_camera/color")
        self.declare_parameter("depth_topic", "qarm_camera/depth")
        self.declare_parameter("update_hz", 2.0)
        self.declare_parameter("observer_only", True)
        self.declare_parameter("observer_goal_keyword", "chess_observ")
        self.declare_parameter("status_file", str(default_status_file))
        self.declare_parameter("config_dir", str(default_config_dir))
        self.declare_parameter("candidate_file", "")
        self.declare_parameter("allow_mock_fallback", True)
        self.declare_parameter("camera_overlay_topic", "/chess/debug/camera_markers")
        self.declare_parameter("publish_camera_overlay", True)
        self.declare_parameter("fixed_manual_marker_topic", "/chess/debug/fixed_manual_markers")
        self.declare_parameter("command_marker_topic", "/chess/debug/command_markers")
        self.declare_parameter("command_trace_file", str(Path(__file__).resolve().parent.parent / "command_trace.json"))
        self.declare_parameter(
            "board_frame_export_file",
            str(Path(__file__).resolve().parent.parent / "board_frame_world.json"),
        )

        self.marker_topic = str(self.get_parameter("marker_topic").value)
        self.camera_overlay_topic = str(self.get_parameter("camera_overlay_topic").value)
        self.fixed_frame = str(self.get_parameter("fixed_frame").value)
        self.color_topic = str(self.get_parameter("color_topic").value)
        self.depth_topic = str(self.get_parameter("depth_topic").value)
        self.update_hz = float(self.get_parameter("update_hz").value)
        self.observer_only = bool(self.get_parameter("observer_only").value)
        self.observer_goal_keyword = str(self.get_parameter("observer_goal_keyword").value).lower()
        self.status_file = Path(str(self.get_parameter("status_file").value))
        self.config_dir = Path(str(self.get_parameter("config_dir").value))
        self.candidate_file = str(self.get_parameter("candidate_file").value).strip()
        self.allow_mock_fallback = bool(self.get_parameter("allow_mock_fallback").value)
        self.publish_camera_overlay = bool(self.get_parameter("publish_camera_overlay").value)
        self.fixed_manual_marker_topic = str(self.get_parameter("fixed_manual_marker_topic").value)
        self.command_marker_topic = str(self.get_parameter("command_marker_topic").value)
        command_trace_param = str(self.get_parameter("command_trace_file").value).strip()
        self.command_trace_file = (
            Path(command_trace_param)
            if command_trace_param
            else (Path(__file__).resolve().parent.parent / "command_trace.json")
        )
        board_export_param = str(self.get_parameter("board_frame_export_file").value).strip()
        self.board_frame_export_file = (
            Path(board_export_param)
            if board_export_param
            else (Path(__file__).resolve().parent.parent / "board_frame_world.json")
        )

        self._latest_color: Image | None = None
        self._latest_depth: Image | None = None
        self._last_markers: MarkerArray | None = None
        self._last_camera_markers: MarkerArray | None = None
        self._last_refresh_reason = "none"
        self._last_diag_log_sec = 0.0

        self.create_subscription(Image, self.color_topic, self._color_cb, 10)
        self.create_subscription(Image, self.depth_topic, self._depth_cb, 10)
        self.marker_pub = self.create_publisher(MarkerArray, self.marker_topic, 10)
        self.camera_marker_pub = self.create_publisher(MarkerArray, self.camera_overlay_topic, 10)
        self.fixed_manual_marker_pub = self.create_publisher(
            MarkerArray,
            self.fixed_manual_marker_topic,
            10,
        )
        self.command_marker_pub = self.create_publisher(
            MarkerArray,
            self.command_marker_topic,
            10,
        )

        self.observer = build_camera_observer(
            config_dir=self.config_dir,
            rgb_provider=self._rgb_provider,
            depth_provider=self._depth_provider,
            metadata_provider=self._metadata_provider,
            allow_mock_fallback=self.allow_mock_fallback,
        )
        self.marker_builder = ChessDebugMarkerBuilder(frame_id=self.fixed_frame)
        self.fixed_manual_board_model = load_fixed_calibrated_board_model(config_dir=self.config_dir)
        self._fixed_manual_markers = self.marker_builder.build_fixed_manual(
            board_outer_corners_world=self.fixed_manual_board_model.board_outer_corners_world,
            square_centers_world=self.fixed_manual_board_model.square_centers_world,
            source=self.fixed_manual_board_model.source,
            stamp=self.get_clock().now().to_msg(),
        )
        self._last_command_markers: MarkerArray | None = None

        period = 1.0 / max(self.update_hz, 0.1)
        self.create_timer(period, self._tick)
        self.get_logger().info(
            f"Publishing chess debug markers on {self.marker_topic} (fixed_frame={self.fixed_frame}, "
            f"observer_only={self.observer_only})"
        )

    def _color_cb(self, msg: Image) -> None:
        self._latest_color = msg

    def _depth_cb(self, msg: Image) -> None:
        self._latest_depth = msg

    def _tick(self) -> None:
        refresh_allowed = self._should_refresh_snapshot()
        if refresh_allowed:
            try:
                frame_bundle = self.observer.frame_source.get_observer_frame()
                board_frame = self.observer.estimate_board_frame(frame_bundle)
                candidates = self.observer.detect_piece_candidates(frame_bundle, board_frame)
                observed_board = self.observer.build_observed_board_from_candidates(
                    candidates,
                    board_frame,
                    frame_bundle,
                )
                self._last_markers = self.marker_builder.build(
                    board_frame,
                    observed_board,
                    stamp=self.get_clock().now().to_msg(),
                )
                if self.publish_camera_overlay:
                    self._last_camera_markers = self._build_camera_overlay_markers(
                        frame_bundle=frame_bundle,
                        board_frame=board_frame,
                        candidates=candidates,
                    )
                self._export_board_frame(board_frame)
                self._last_refresh_reason = "observer_snapshot_refresh"
            except RuntimeError as exc:
                self._last_refresh_reason = f"refresh_failed:{exc}"
                self._throttled_diag_log(
                    f"Chess debug refresh failed: {exc}",
                    level="warn",
                )

        if self._last_markers is None:
            self._throttled_diag_log(
                "No marker snapshot yet "
                f"(refresh_allowed={refresh_allowed}, reason={self._last_refresh_reason})",
                level="info",
            )
        else:
            self._retimestamp(self._last_markers)
            self.marker_pub.publish(self._last_markers)
            if self.publish_camera_overlay and self._last_camera_markers is not None:
                self._retimestamp(self._last_camera_markers)
                self.camera_marker_pub.publish(self._last_camera_markers)
        self._retimestamp(self._fixed_manual_markers)
        self.fixed_manual_marker_pub.publish(self._fixed_manual_markers)
        command_markers = self._load_command_markers()
        if command_markers is not None:
            self._last_command_markers = command_markers
        if self._last_command_markers is not None:
            self._retimestamp(self._last_command_markers)
            self.command_marker_pub.publish(self._last_command_markers)

    def _should_refresh_snapshot(self) -> bool:
        if not self.observer_only:
            self._last_refresh_reason = "observer_only_disabled"
            return True
        status = self._read_status()
        if status is None:
            self._last_refresh_reason = f"status_unavailable:{self.status_file}"
            return False
        if str(status.get("state", "")).lower() != "succeeded":
            self._last_refresh_reason = f"status_state_not_succeeded:{status.get('state')}"
            return False
        goal_id = str(status.get("active_goal_id", "")).lower()
        if self.observer_goal_keyword and self.observer_goal_keyword not in goal_id:
            self._last_refresh_reason = f"status_goal_filtered:{goal_id}"
            return False
        self._last_refresh_reason = "status_gate_passed"
        return True

    def _read_status(self) -> dict[str, Any] | None:
        try:
            return json.loads(self.status_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def _export_board_frame(self, board_frame) -> None:
        """Export latest world board frame for manipulation consumers."""

        corners_world = _coerce_corner_xyz_map(board_frame.board_outer_corners_world)
        if len(corners_world) != 4:
            return
        square_centers_world = {
            square: [float(xyz[0]), float(xyz[1]), float(xyz[2])]
            for square, xyz in board_frame.square_centers_world.items()
        }
        payload = {
            "frame_name": self.fixed_frame,
            "source": str(board_frame.source),
            "fit_state": str(board_frame.fit_state),
            "used_live_fit": bool(board_frame.used_live_fit),
            "used_manual_fallback": bool(board_frame.used_manual_fallback),
            "board_outer_corners_world": {
                key: [float(corners_world[key][0]), float(corners_world[key][1]), float(corners_world[key][2])]
                for key in ("a1", "h1", "h8", "a8")
            },
            "square_centers_world": square_centers_world,
            "updated_at_sec": float(time.time()),
        }
        self.board_frame_export_file.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.board_frame_export_file.with_suffix(self.board_frame_export_file.suffix + ".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        tmp_path.replace(self.board_frame_export_file)

    def _rgb_provider(self):
        if self._latest_color is None:
            return [[0.0]]
        decoded = _decode_rgb_image(self._latest_color)
        if decoded is None:
            return [[0.0]]
        return decoded

    def _depth_provider(self):
        if self._latest_depth is None:
            return [[1.0]]
        decoded = _decode_depth_image(self._latest_depth)
        if decoded is None:
            return [[1.0]]
        return decoded

    def _metadata_provider(self) -> dict[str, Any]:
        if not self.candidate_file:
            return {}
        path = Path(self.candidate_file)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        if isinstance(payload, list):
            return {"phase2_piece_candidates": payload}
        if isinstance(payload, dict):
            return payload
        return {}

    def _load_command_markers(self) -> MarkerArray | None:
        """Load planner->bridge command trace and convert it to world markers."""

        try:
            payload = json.loads(self.command_trace_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        if not isinstance(payload, dict):
            return None
        commands = payload.get("commands")
        if not isinstance(commands, list):
            return None
        return self._build_command_markers(commands)

    def _build_command_markers(self, commands: list[Any]) -> MarkerArray:
        markers = MarkerArray()
        stamp = self.get_clock().now().to_msg()

        delete_all = Marker()
        delete_all.header.frame_id = self.fixed_frame
        delete_all.header.stamp = stamp
        delete_all.action = Marker.DELETEALL
        markers.markers.append(delete_all)

        recent = [item for item in commands if isinstance(item, dict)][-40:]
        planner_points: list[Point] = []
        tcp_points: list[Point] = []
        bridge_points: list[Point] = []
        line_points: list[Point] = []

        text_id = 2000
        for item in recent:
            planner = _coerce_pose4(item.get("planner_pose"))
            tcp_corrected = _coerce_pose4(item.get("tcp_corrected_pose"))
            bridge = _coerce_pose4(item.get("bridge_goal_pose"))
            stage = str(item.get("stage", "unknown"))

            if planner is not None:
                planner_points.append(_point((planner[0], planner[1], planner[2])))
            if tcp_corrected is not None:
                tcp_points.append(_point((tcp_corrected[0], tcp_corrected[1], tcp_corrected[2])))
            if bridge is not None:
                bridge_points.append(_point((bridge[0], bridge[1], bridge[2])))

            if planner is not None and tcp_corrected is not None:
                line_points.append(_point((planner[0], planner[1], planner[2])))
                line_points.append(_point((tcp_corrected[0], tcp_corrected[1], tcp_corrected[2])))
            if tcp_corrected is not None and bridge is not None:
                line_points.append(_point((tcp_corrected[0], tcp_corrected[1], tcp_corrected[2])))
                line_points.append(_point((bridge[0], bridge[1], bridge[2])))

            label_pose = bridge or tcp_corrected or planner
            if label_pose is not None:
                label = Marker()
                label.header.frame_id = self.fixed_frame
                label.header.stamp = stamp
                label.ns = "command_stage_labels"
                label.id = text_id
                text_id += 1
                label.type = Marker.TEXT_VIEW_FACING
                label.action = Marker.ADD
                label.scale.z = 0.016
                label.color = _rgba(0.95, 0.95, 0.95, 0.95)
                label.pose.orientation.w = 1.0
                label.pose.position = _point((label_pose[0], label_pose[1], label_pose[2] + 0.02))
                label.text = stage
                markers.markers.append(label)

        planner_marker = Marker()
        planner_marker.header.frame_id = self.fixed_frame
        planner_marker.header.stamp = stamp
        planner_marker.ns = "planner_pose_targets"
        planner_marker.id = 1001
        planner_marker.type = Marker.SPHERE_LIST
        planner_marker.action = Marker.ADD
        planner_marker.scale.x = 0.009
        planner_marker.scale.y = 0.009
        planner_marker.scale.z = 0.009
        planner_marker.color = _rgba(0.2, 0.7, 1.0, 0.9)
        planner_marker.pose.orientation.w = 1.0
        planner_marker.points = planner_points
        markers.markers.append(planner_marker)

        tcp_marker = Marker()
        tcp_marker.header.frame_id = self.fixed_frame
        tcp_marker.header.stamp = stamp
        tcp_marker.ns = "tcp_corrected_targets"
        tcp_marker.id = 1002
        tcp_marker.type = Marker.SPHERE_LIST
        tcp_marker.action = Marker.ADD
        tcp_marker.scale.x = 0.008
        tcp_marker.scale.y = 0.008
        tcp_marker.scale.z = 0.008
        tcp_marker.color = _rgba(1.0, 0.85, 0.2, 0.95)
        tcp_marker.pose.orientation.w = 1.0
        tcp_marker.points = tcp_points
        markers.markers.append(tcp_marker)

        bridge_marker = Marker()
        bridge_marker.header.frame_id = self.fixed_frame
        bridge_marker.header.stamp = stamp
        bridge_marker.ns = "bridge_goal_targets"
        bridge_marker.id = 1003
        bridge_marker.type = Marker.SPHERE_LIST
        bridge_marker.action = Marker.ADD
        bridge_marker.scale.x = 0.007
        bridge_marker.scale.y = 0.007
        bridge_marker.scale.z = 0.007
        bridge_marker.color = _rgba(1.0, 0.25, 0.7, 0.95)
        bridge_marker.pose.orientation.w = 1.0
        bridge_marker.points = bridge_points
        markers.markers.append(bridge_marker)

        line_marker = Marker()
        line_marker.header.frame_id = self.fixed_frame
        line_marker.header.stamp = stamp
        line_marker.ns = "planner_to_bridge_lines"
        line_marker.id = 1004
        line_marker.type = Marker.LINE_LIST
        line_marker.action = Marker.ADD
        line_marker.scale.x = 0.0015
        line_marker.color = _rgba(0.95, 0.6, 0.2, 0.85)
        line_marker.pose.orientation.w = 1.0
        line_marker.points = line_points
        markers.markers.append(line_marker)
        return markers

    def _retimestamp(self, marker_array: MarkerArray) -> None:
        stamp = self.get_clock().now().to_msg()
        for marker in marker_array.markers:
            marker.header.stamp = stamp

    def _build_camera_overlay_markers(
        self,
        *,
        frame_bundle,
        board_frame,
        candidates: list[DetectedPieceCandidate],
    ) -> MarkerArray:
        frame_id = frame_bundle.depth_frame_name or "left_ir_optical_frame"
        stamp = self.get_clock().now().to_msg()
        markers = MarkerArray()

        delete_all = Marker()
        delete_all.header.frame_id = frame_id
        delete_all.header.stamp = stamp
        delete_all.action = Marker.DELETEALL
        markers.markers.append(delete_all)

        live_debug = board_frame.live_fit_debug if isinstance(board_frame.live_fit_debug, dict) else {}
        fitted_pixels = _coerce_corner_map(live_debug.get("fitted_corner_pixels"))
        if not fitted_pixels:
            fitted_pixels = _coerce_corner_map(board_frame.board_outer_corners_image)
        depth_pixels = _coerce_corner_map(live_debug.get("projected_corner_depth_pixels"))

        corners_camera: dict[str, tuple[float, float, float]] = {}
        for key in ("a1", "h1", "h8", "a8"):
            uv_fit = fitted_pixels.get(key) if fitted_pixels else None
            if uv_fit is None:
                continue
            uv_depth = depth_pixels.get(key) if depth_pixels and key in depth_pixels else uv_fit
            xyz = self._pixel_to_camera_xyz(frame_bundle, uv_depth)
            if xyz is not None:
                corners_camera[key] = xyz

        plane_centers = _square_centers_from_camera_corners(corners_camera)

        corners_marker = Marker()
        corners_marker.header.frame_id = frame_id
        corners_marker.header.stamp = stamp
        corners_marker.ns = "camera_fit_corners"
        corners_marker.id = 1
        corners_marker.type = Marker.SPHERE_LIST
        corners_marker.action = Marker.ADD
        corners_marker.scale.x = 0.014
        corners_marker.scale.y = 0.014
        corners_marker.scale.z = 0.014
        corners_marker.color = _rgba(1.0, 0.9, 0.1, 0.95)
        corners_marker.pose.orientation.w = 1.0
        for key in ("a1", "h1", "h8", "a8"):
            if key in corners_camera:
                corners_marker.points.append(_point(corners_camera[key]))
        markers.markers.append(corners_marker)

        border = Marker()
        border.header.frame_id = frame_id
        border.header.stamp = stamp
        border.ns = "camera_board_border"
        border.id = 2
        border.type = Marker.LINE_STRIP
        border.action = Marker.ADD
        border.scale.x = 0.003
        border.color = _rgba(0.2, 0.95, 1.0, 0.95)
        border.pose.orientation.w = 1.0
        if all(k in corners_camera for k in ("a1", "h1", "h8", "a8")):
            for key in ("a1", "h1", "h8", "a8", "a1"):
                border.points.append(_point(corners_camera[key]))
        markers.markers.append(border)

        centers = Marker()
        centers.header.frame_id = frame_id
        centers.header.stamp = stamp
        centers.ns = "camera_square_centers"
        centers.id = 3
        centers.type = Marker.SPHERE_LIST
        centers.action = Marker.ADD
        centers.scale.x = 0.006
        centers.scale.y = 0.006
        centers.scale.z = 0.006
        centers.color = _rgba(0.15, 0.75, 1.0, 0.8)
        centers.pose.orientation.w = 1.0
        for square in sorted(plane_centers):
            centers.points.append(_point(plane_centers[square]))
        markers.markers.append(centers)

        label_id = 100
        for square in sorted(plane_centers):
            label = Marker()
            label.header.frame_id = frame_id
            label.header.stamp = stamp
            label.ns = "camera_square_labels"
            label.id = label_id
            label_id += 1
            label.type = Marker.TEXT_VIEW_FACING
            label.action = Marker.ADD
            label.scale.z = 0.015
            label.color = _rgba(0.2, 0.9, 0.9, 0.9)
            label.pose.orientation.w = 1.0
            center_xyz = plane_centers[square]
            label.pose.position = _point((center_xyz[0], center_xyz[1], center_xyz[2] + 0.01))
            label.text = square
            markers.markers.append(label)

        pieces = Marker()
        pieces.header.frame_id = frame_id
        pieces.header.stamp = stamp
        pieces.ns = "camera_pieces"
        pieces.id = 4
        pieces.type = Marker.SPHERE_LIST
        pieces.action = Marker.ADD
        pieces.scale.x = 0.018
        pieces.scale.y = 0.018
        pieces.scale.z = 0.018
        pieces.color = _rgba(1.0, 0.25, 0.25, 0.95)
        pieces.pose.orientation.w = 1.0
        for candidate in candidates:
            if candidate.pixel_uv is None:
                continue
            xyz = self._pixel_to_camera_xyz(frame_bundle, candidate.pixel_uv)
            if xyz is not None:
                pieces.points.append(_point(xyz))
        markers.markers.append(pieces)

        assignment_lines = Marker()
        assignment_lines.header.frame_id = frame_id
        assignment_lines.header.stamp = stamp
        assignment_lines.ns = "camera_piece_assignments"
        assignment_lines.id = 6
        assignment_lines.type = Marker.LINE_LIST
        assignment_lines.action = Marker.ADD
        assignment_lines.scale.x = 0.002
        assignment_lines.color = _rgba(1.0, 0.5, 0.1, 0.9)
        assignment_lines.pose.orientation.w = 1.0

        assignment_label_id = 700
        for candidate in candidates:
            if candidate.pixel_uv is None:
                continue
            square = self.observer.assign_pixel_to_square(candidate.pixel_uv, board_frame)
            if square is None or square not in plane_centers:
                continue
            piece_xyz = self._pixel_to_camera_xyz(frame_bundle, candidate.pixel_uv)
            if piece_xyz is None:
                continue
            target_xyz = plane_centers[square]
            assignment_lines.points.append(_point(piece_xyz))
            assignment_lines.points.append(_point(target_xyz))

            assignment_label = Marker()
            assignment_label.header.frame_id = frame_id
            assignment_label.header.stamp = stamp
            assignment_label.ns = "camera_piece_square_labels"
            assignment_label.id = assignment_label_id
            assignment_label_id += 1
            assignment_label.type = Marker.TEXT_VIEW_FACING
            assignment_label.action = Marker.ADD
            assignment_label.scale.z = 0.018
            assignment_label.color = _rgba(1.0, 0.75, 0.2, 0.95)
            assignment_label.pose.orientation.w = 1.0
            assignment_label.pose.position = _point((piece_xyz[0], piece_xyz[1], piece_xyz[2] + 0.02))
            assignment_label.text = square
            markers.markers.append(assignment_label)
        markers.markers.append(assignment_lines)

        status = Marker()
        status.header.frame_id = frame_id
        status.header.stamp = stamp
        status.ns = "camera_fit_status"
        status.id = 5
        status.type = Marker.TEXT_VIEW_FACING
        status.action = Marker.ADD
        status.scale.z = 0.03
        status.color = _rgba(0.95, 0.95, 0.95, 0.95)
        status.pose.orientation.w = 1.0
        text_anchor = None
        if "a1" in corners_camera and "h8" in corners_camera:
            a1 = corners_camera["a1"]
            h8 = corners_camera["h8"]
            text_anchor = (
                (a1[0] + h8[0]) * 0.5,
                (a1[1] + h8[1]) * 0.5,
                max(a1[2], h8[2]) + 0.03,
            )
        elif centers.points:
            c = centers.points[min(10, len(centers.points) - 1)]
            text_anchor = (c.x, c.y, c.z + 0.03)
        else:
            text_anchor = (0.0, 0.0, 0.25)
        status.pose.position = _point(text_anchor)
        mode = board_frame.fit_state or (
            "manual_fallback" if board_frame.used_manual_fallback else "manual"
        )
        status.text = (
            f"camera-fit mode={mode} "
            f"fit={board_frame.live_fit_confidence if board_frame.live_fit_confidence is not None else 0.0:.2f}"
        )
        markers.markers.append(status)
        self._log_live_fit_debug(
            board_frame=board_frame,
            frame_bundle=frame_bundle,
            fitted_pixels=fitted_pixels,
            depth_pixels=depth_pixels,
            corners_camera=corners_camera,
        )
        return markers

    def _pixel_to_camera_xyz(self, frame_bundle, pixel_uv) -> tuple[float, float, float] | None:
        intrinsics = frame_bundle.intrinsics
        if intrinsics is None:
            return None
        depth_m = _depth_at_uv(frame_bundle.depth_image, pixel_uv, search_radius_px=4)
        if depth_m is None:
            return None
        u, v = pixel_uv
        x = (float(u) - intrinsics.cx) * depth_m / intrinsics.fx
        y = (float(v) - intrinsics.cy) * depth_m / intrinsics.fy
        return (float(x), float(y), float(depth_m))

    def _log_live_fit_debug(
        self,
        *,
        board_frame,
        frame_bundle,
        fitted_pixels: dict[str, tuple[float, float]],
        depth_pixels: dict[str, tuple[float, float]],
        corners_camera: dict[str, tuple[float, float, float]],
    ) -> None:
        if board_frame.board_detection_mode == "manual" and not board_frame.used_live_fit:
            return
        debug = board_frame.live_fit_debug if isinstance(board_frame.live_fit_debug, dict) else {}
        mode = str(debug.get("fit_coordinate_mode", "unknown"))
        alignment_active = bool(debug.get("alignment_active", False))
        color_size = debug.get("color_image_size")
        depth_size = debug.get("depth_image_size")
        intrinsics = debug.get("intrinsics") or {}
        projected_world = _coerce_corner_xyz_map(debug.get("projected_corner_world"))
        self._throttled_diag_log(
            "live-fit "
            f"mode={mode} aligned={alignment_active} "
            f"color_size={color_size} depth_size={depth_size} "
            f"intrinsics={intrinsics} "
            f"fitted_px={_format_uv_map(fitted_pixels)} "
            f"depth_px={_format_uv_map(depth_pixels)} "
            f"corners_world={_format_xyz_map(projected_world)} "
            f"corners_camera={_format_xyz_map(corners_camera)} "
            f"color_frame={frame_bundle.color_frame_name} depth_frame={frame_bundle.depth_frame_name}",
            level="info",
        )

    def _throttled_diag_log(self, message: str, *, level: str) -> None:
        now = time.monotonic()
        if now - self._last_diag_log_sec < 2.0:
            return
        self._last_diag_log_sec = now
        if level == "warn":
            self.get_logger().warn(message)
        else:
            self.get_logger().info(message)


def _coerce_corner_map(value: Any) -> dict[str, tuple[float, float]]:
    if not isinstance(value, dict):
        return {}
    parsed: dict[str, tuple[float, float]] = {}
    for key in ("a1", "h1", "h8", "a8"):
        raw = value.get(key)
        if not isinstance(raw, (list, tuple)) or len(raw) < 2:
            continue
        try:
            parsed[key] = (float(raw[0]), float(raw[1]))
        except (TypeError, ValueError):
            continue
    return parsed


def _coerce_corner_xyz_map(value: Any) -> dict[str, tuple[float, float, float]]:
    if not isinstance(value, dict):
        return {}
    parsed: dict[str, tuple[float, float, float]] = {}
    for key in ("a1", "h1", "h8", "a8"):
        raw = value.get(key)
        if not isinstance(raw, (list, tuple)) or len(raw) < 3:
            continue
        try:
            parsed[key] = (float(raw[0]), float(raw[1]), float(raw[2]))
        except (TypeError, ValueError):
            continue
    return parsed


def _coerce_pose4(value: Any) -> tuple[float, float, float, float] | None:
    if not isinstance(value, (list, tuple)) or len(value) < 4:
        return None
    try:
        return (float(value[0]), float(value[1]), float(value[2]), float(value[3]))
    except (TypeError, ValueError):
        return None


def _square_centers_from_camera_corners(
    corners_camera: dict[str, tuple[float, float, float]],
) -> dict[str, tuple[float, float, float]]:
    if not all(key in corners_camera for key in ("a1", "h1", "h8", "a8")):
        return {}
    centers: dict[str, tuple[float, float, float]] = {}
    files = "abcdefgh"
    ranks = "12345678"
    for rank_index in range(8):
        for file_index in range(8):
            square = f"{files[file_index]}{ranks[rank_index]}"
            u = (file_index + 0.5) / 8.0
            v = (rank_index + 0.5) / 8.0
            centers[square] = _bilinear_xyz(corners_camera, u=u, v=v)
    return centers


def _bilinear_xyz(
    corners: dict[str, tuple[float, float, float]],
    *,
    u: float,
    v: float,
) -> tuple[float, float, float]:
    a1 = corners["a1"]
    h1 = corners["h1"]
    h8 = corners["h8"]
    a8 = corners["a8"]
    x = (
        (1.0 - u) * (1.0 - v) * a1[0]
        + u * (1.0 - v) * h1[0]
        + u * v * h8[0]
        + (1.0 - u) * v * a8[0]
    )
    y = (
        (1.0 - u) * (1.0 - v) * a1[1]
        + u * (1.0 - v) * h1[1]
        + u * v * h8[1]
        + (1.0 - u) * v * a8[1]
    )
    z = (
        (1.0 - u) * (1.0 - v) * a1[2]
        + u * (1.0 - v) * h1[2]
        + u * v * h8[2]
        + (1.0 - u) * v * a8[2]
    )
    return (x, y, z)


def _format_uv_map(values: dict[str, tuple[float, float]]) -> str:
    if not values:
        return "{}"
    ordered = []
    for key in ("a1", "h1", "h8", "a8"):
        if key not in values:
            continue
        uv = values[key]
        ordered.append(f"{key}=({uv[0]:.1f},{uv[1]:.1f})")
    return "{" + ", ".join(ordered) + "}"


def _format_xyz_map(values: dict[str, tuple[float, float, float]]) -> str:
    if not values:
        return "{}"
    ordered = []
    for key in ("a1", "h1", "h8", "a8"):
        if key not in values:
            continue
        xyz = values[key]
        ordered.append(f"{key}=({xyz[0]:.3f},{xyz[1]:.3f},{xyz[2]:.3f})")
    return "{" + ", ".join(ordered) + "}"


def _decode_depth_image(msg: Image):
    encoding = msg.encoding.upper()
    width = int(msg.width)
    height = int(msg.height)
    step = int(msg.step)
    data = memoryview(msg.data)
    if width <= 0 or height <= 0:
        return None

    rows: list[list[float]] = []
    if encoding == "32FC1":
        for row_idx in range(height):
            row_offset = row_idx * step
            row: list[float] = []
            for col_idx in range(width):
                value = struct.unpack_from("<f", data, row_offset + col_idx * 4)[0]
                row.append(float(value))
            rows.append(row)
        return rows

    if encoding == "16UC1":
        for row_idx in range(height):
            row_offset = row_idx * step
            row = []
            for col_idx in range(width):
                value_mm = struct.unpack_from("<H", data, row_offset + col_idx * 2)[0]
                row.append(float(value_mm) / 1000.0)
            rows.append(row)
        return rows
    return None


def _decode_rgb_image(msg: Image):
    encoding = msg.encoding.lower()
    width = int(msg.width)
    height = int(msg.height)
    step = int(msg.step)
    data = memoryview(msg.data)
    if width <= 0 or height <= 0:
        return None
    rows: list[list[float]] = []

    if encoding in {"rgb8", "bgr8"}:
        channel_order = (0, 1, 2) if encoding == "rgb8" else (2, 1, 0)
        for row_idx in range(height):
            row_offset = row_idx * step
            row: list[float] = []
            for col_idx in range(width):
                pixel_offset = row_offset + col_idx * 3
                r = data[pixel_offset + channel_order[0]]
                g = data[pixel_offset + channel_order[1]]
                b = data[pixel_offset + channel_order[2]]
                gray = 0.299 * float(r) + 0.587 * float(g) + 0.114 * float(b)
                row.append(gray)
            rows.append(row)
        return rows

    if encoding == "mono8":
        for row_idx in range(height):
            row_offset = row_idx * step
            row = []
            for col_idx in range(width):
                row.append(float(data[row_offset + col_idx]))
            rows.append(row)
        return rows
    return None


def _depth_at_uv(depth_image, pixel_uv, search_radius_px: int) -> float | None:
    u0 = int(round(pixel_uv[0]))
    v0 = int(round(pixel_uv[1]))
    for radius in range(max(0, search_radius_px) + 1):
        if radius == 0:
            depth_value = _depth_at_idx(depth_image, u0, v0)
            if depth_value is not None:
                return depth_value
            continue
        for dv in range(-radius, radius + 1):
            for du in range(-radius, radius + 1):
                if abs(du) != radius and abs(dv) != radius:
                    continue
                depth_value = _depth_at_idx(depth_image, u0 + du, v0 + dv)
                if depth_value is not None:
                    return depth_value
    return None


def _depth_at_idx(depth_image, u: int, v: int) -> float | None:
    if v < 0 or u < 0:
        return None
    try:
        row = depth_image[v]
        depth_value = float(row[u])
    except (IndexError, TypeError, ValueError):
        return None
    if not (depth_value > 0.0):
        return None
    return depth_value


def _point(xyz: tuple[float, float, float]) -> Point:
    point = Point()
    point.x = float(xyz[0])
    point.y = float(xyz[1])
    point.z = float(xyz[2])
    return point


def _rgba(r: float, g: float, b: float, a: float) -> ColorRGBA:
    color = ColorRGBA()
    color.r = float(r)
    color.g = float(g)
    color.b = float(b)
    color.a = float(a)
    return color


def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = ChessRvizDebugNode()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == "__main__":
    main()
