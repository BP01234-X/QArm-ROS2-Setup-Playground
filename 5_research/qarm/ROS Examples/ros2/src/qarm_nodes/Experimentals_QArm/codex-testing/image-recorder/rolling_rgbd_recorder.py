#!/usr/bin/env python3

"""Save a rolling window of RGB/depth snapshots from the experimental QArm feed."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import Image


@dataclass
class FrameData:
    """Latest decoded image frame and its ROS metadata."""

    image: np.ndarray
    frame_id: str
    stamp_sec: int
    stamp_nanosec: int

    @property
    def stamp_float(self) -> float:
        return float(self.stamp_sec) + float(self.stamp_nanosec) / 1_000_000_000.0

    @property
    def stamp_label(self) -> str:
        return f"{self.stamp_sec:010d}_{self.stamp_nanosec:09d}"


class RollingRgbdRecorder(Node):
    """Subscribe to RGB/depth topics and maintain a bounded on-disk snapshot buffer."""

    def __init__(self) -> None:
        super().__init__("rolling_rgbd_recorder")
        script_dir = Path(__file__).resolve().parent
        self.declare_parameter("output_dir", str(script_dir))
        self.declare_parameter("frames_subdir", "frames")
        self.declare_parameter("status_file", "recorder_status.json")
        self.declare_parameter("color_topic", "qarm_camera/color")
        self.declare_parameter("depth_topic", "qarm_camera/depth")
        self.declare_parameter("max_bundles", 30)
        self.declare_parameter("save_period_sec", 0.5)
        self.declare_parameter("jpeg_quality", 92)
        self.declare_parameter("depth_max_m", 1.50)

        self.output_dir = Path(str(self.get_parameter("output_dir").value)).expanduser()
        self.frames_dir = self.output_dir / str(self.get_parameter("frames_subdir").value)
        self.status_file = self.output_dir / str(self.get_parameter("status_file").value)
        self.max_bundles = int(self.get_parameter("max_bundles").value)
        self.save_period_sec = float(self.get_parameter("save_period_sec").value)
        self.jpeg_quality = int(self.get_parameter("jpeg_quality").value)
        self.depth_max_m = float(self.get_parameter("depth_max_m").value)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.frames_dir.mkdir(parents=True, exist_ok=True)

        self.bridge = CvBridge()
        self.latest_color: FrameData | None = None
        self.latest_depth: FrameData | None = None
        self.last_saved_at = 0.0
        self.bundle_index = 0
        self.last_center_depth_m: float | None = None

        self.create_subscription(
            Image,
            str(self.get_parameter("color_topic").value),
            self._on_color,
            10,
        )
        self.create_subscription(
            Image,
            str(self.get_parameter("depth_topic").value),
            self._on_depth,
            10,
        )

        self._write_status(
            state="waiting",
            message="Waiting for both RGB and depth frames before recording bundles.",
        )
        self.get_logger().info(f"Rolling RGBD recorder writing into {self.frames_dir}")

    def _on_color(self, msg: Image) -> None:
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        self.latest_color = FrameData(
            image=image,
            frame_id=msg.header.frame_id,
            stamp_sec=int(msg.header.stamp.sec),
            stamp_nanosec=int(msg.header.stamp.nanosec),
        )
        self._maybe_record(trigger="color")

    def _on_depth(self, msg: Image) -> None:
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="32FC1")
        self.latest_depth = FrameData(
            image=image,
            frame_id=msg.header.frame_id,
            stamp_sec=int(msg.header.stamp.sec),
            stamp_nanosec=int(msg.header.stamp.nanosec),
        )
        self._maybe_record(trigger="depth")

    def _maybe_record(self, trigger: str) -> None:
        if self.latest_color is None or self.latest_depth is None:
            self._write_status(
                state="waiting",
                message=f"Received {trigger} frame. Waiting for paired RGB/depth stream.",
            )
            return

        latest_stamp = max(self.latest_color.stamp_float, self.latest_depth.stamp_float)
        if latest_stamp - self.last_saved_at < self.save_period_sec:
            self._write_status(
                state="streaming",
                message="Receiving frames. Waiting for next recorder interval.",
                latest_trigger=trigger,
            )
            return

        self.last_saved_at = latest_stamp
        self.bundle_index += 1
        self._record_bundle(trigger=trigger)

    def _record_bundle(self, trigger: str) -> None:
        assert self.latest_color is not None
        assert self.latest_depth is not None

        bundle_name = f"{self.bundle_index:05d}_{max(self.latest_color.stamp_label, self.latest_depth.stamp_label)}"
        bundle_dir = self.frames_dir / bundle_name
        bundle_dir.mkdir(parents=True, exist_ok=True)

        rgb_image = self.latest_color.image.copy()
        depth_image = self.latest_depth.image.copy()
        center_depth_m = self._depth_center_value(depth_image)
        depth_min_m, depth_max_m = self._depth_min_max(depth_image)
        stamp_delta_ms = abs(self.latest_color.stamp_float - self.latest_depth.stamp_float) * 1000.0

        rgb_path = bundle_dir / "rgb.jpg"
        depth_npy_path = bundle_dir / "depth_m.npy"
        depth_preview_path = bundle_dir / "depth_preview.png"
        compare_path = bundle_dir / "compare_rgb_depth.jpg"
        metadata_path = bundle_dir / "metadata.json"

        cv2.imwrite(str(rgb_path), rgb_image, [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality])
        np.save(depth_npy_path, depth_image)

        depth_preview = self._colorize_depth(depth_image)
        compare_image = self._make_compare_image(
            rgb_image=rgb_image,
            depth_preview=depth_preview,
            center_depth_m=center_depth_m,
            depth_min_m=depth_min_m,
            depth_max_m=depth_max_m,
            stamp_delta_ms=stamp_delta_ms,
        )
        cv2.imwrite(str(depth_preview_path), depth_preview)
        cv2.imwrite(str(compare_path), compare_image, [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality])

        metadata = {
            "bundle_name": bundle_name,
            "trigger": trigger,
            "color": self._frame_metadata(self.latest_color),
            "depth": self._frame_metadata(self.latest_depth),
            "stamp_delta_ms": round(stamp_delta_ms, 3),
            "rgb_shape": [int(v) for v in rgb_image.shape],
            "depth_shape": [int(v) for v in depth_image.shape],
            "center_depth_m": self._rounded_or_none(center_depth_m),
            "depth_min_m": self._rounded_or_none(depth_min_m),
            "depth_max_m": self._rounded_or_none(depth_max_m),
            "previous_center_depth_m": self._rounded_or_none(self.last_center_depth_m),
            "center_depth_delta_m": self._rounded_or_none(
                None if center_depth_m is None or self.last_center_depth_m is None
                else center_depth_m - self.last_center_depth_m
            ),
            "files": {
                "rgb": str(rgb_path),
                "depth_npy": str(depth_npy_path),
                "depth_preview": str(depth_preview_path),
                "compare": str(compare_path),
            },
        }
        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

        self.last_center_depth_m = center_depth_m
        pruned = self._prune_old_bundles()
        self._write_status(
            state="recording",
            message="Saved rolling RGB/depth bundle.",
            latest_trigger=trigger,
            latest_bundle=str(bundle_dir),
            latest_compare_image=str(compare_path),
            latest_metadata=str(metadata_path),
            bundle_count=self._bundle_count(),
            pruned_bundles=pruned,
            center_depth_m=self._rounded_or_none(center_depth_m),
            depth_min_m=self._rounded_or_none(depth_min_m),
            depth_max_m=self._rounded_or_none(depth_max_m),
            stamp_delta_ms=round(stamp_delta_ms, 3),
        )

    def _frame_metadata(self, frame: FrameData) -> dict[str, Any]:
        return {
            "frame_id": frame.frame_id,
            "stamp": {
                "sec": frame.stamp_sec,
                "nanosec": frame.stamp_nanosec,
            },
        }

    def _bundle_count(self) -> int:
        return len([path for path in self.frames_dir.iterdir() if path.is_dir()])

    def _prune_old_bundles(self) -> list[str]:
        # Prune by filesystem modification time, not bundle name.
        # Recorder restarts reset bundle_index, so lexicographic sorting can
        # incorrectly delete the newest bundle immediately.
        bundle_dirs = sorted(
            [path for path in self.frames_dir.iterdir() if path.is_dir()],
            key=lambda path: path.stat().st_mtime,
        )
        removed: list[str] = []
        while len(bundle_dirs) > self.max_bundles:
            oldest = bundle_dirs.pop(0)
            for child in sorted(oldest.iterdir(), reverse=True):
                child.unlink()
            oldest.rmdir()
            removed.append(str(oldest))
        return removed

    def _colorize_depth(self, depth_m: np.ndarray) -> np.ndarray:
        finite_mask = np.isfinite(depth_m) & (depth_m > 0.0)
        preview = np.zeros(depth_m.shape, dtype=np.uint8)
        if np.any(finite_mask):
            clipped = np.clip(depth_m[finite_mask], 0.0, self.depth_max_m)
            normalized = np.zeros_like(clipped, dtype=np.float32)
            if self.depth_max_m > 0.0:
                normalized = clipped / self.depth_max_m
            preview_values = np.uint8((1.0 - normalized) * 255.0)
            preview[finite_mask] = preview_values
        colorized = cv2.applyColorMap(preview, cv2.COLORMAP_TURBO)
        colorized[~finite_mask] = (0, 0, 0)
        self._draw_crosshair(colorized)
        return colorized

    def _make_compare_image(
        self,
        rgb_image: np.ndarray,
        depth_preview: np.ndarray,
        center_depth_m: float | None,
        depth_min_m: float | None,
        depth_max_m: float | None,
        stamp_delta_ms: float,
    ) -> np.ndarray:
        rgb_copy = rgb_image.copy()
        self._draw_crosshair(rgb_copy)
        if depth_preview.shape[:2] != rgb_copy.shape[:2]:
            depth_preview = cv2.resize(depth_preview, (rgb_copy.shape[1], rgb_copy.shape[0]))
        compare = np.hstack([rgb_copy, depth_preview])
        footer = np.full((72, compare.shape[1], 3), 24, dtype=np.uint8)
        lines = [
            "Left: RGB | Right: depth preview (warm = near, dark = invalid/far)",
            (
                f"center_depth_m={self._rounded_or_none(center_depth_m)} "
                f"min={self._rounded_or_none(depth_min_m)} "
                f"max={self._rounded_or_none(depth_max_m)} "
                f"stamp_delta_ms={round(stamp_delta_ms, 2)}"
            ),
        ]
        y = 28
        for line in lines:
            cv2.putText(footer, line, (16, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (230, 230, 230), 1, cv2.LINE_AA)
            y += 26
        return np.vstack([compare, footer])

    def _draw_crosshair(self, image: np.ndarray) -> None:
        center_u = image.shape[1] // 2
        center_v = image.shape[0] // 2
        cv2.drawMarker(
            image,
            (center_u, center_v),
            color=(255, 255, 255),
            markerType=cv2.MARKER_CROSS,
            markerSize=20,
            thickness=1,
            line_type=cv2.LINE_AA,
        )

    def _depth_center_value(self, depth_m: np.ndarray) -> float | None:
        value = float(depth_m[depth_m.shape[0] // 2, depth_m.shape[1] // 2])
        return value if math.isfinite(value) and value > 0.0 else None

    def _depth_min_max(self, depth_m: np.ndarray) -> tuple[float | None, float | None]:
        finite = depth_m[np.isfinite(depth_m) & (depth_m > 0.0)]
        if finite.size == 0:
            return None, None
        return float(np.min(finite)), float(np.max(finite))

    def _rounded_or_none(self, value: float | None) -> float | None:
        if value is None:
            return None
        return round(float(value), 4)

    def _write_status(self, **payload: Any) -> None:
        payload.setdefault(
            "topics",
            {
                "color": str(self.get_parameter("color_topic").value),
                "depth": str(self.get_parameter("depth_topic").value),
            },
        )
        payload.setdefault("output_dir", str(self.output_dir))
        payload.setdefault("frames_dir", str(self.frames_dir))
        payload.setdefault("max_bundles", self.max_bundles)
        payload.setdefault("save_period_sec", self.save_period_sec)
        payload.setdefault("bundle_count", self._bundle_count())
        self.status_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(args=None) -> None:
    node = None
    try:
        with rclpy.init(args=args):
            node = RollingRgbdRecorder()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if node is not None:
            node.destroy_node()


if __name__ == "__main__":
    main()
