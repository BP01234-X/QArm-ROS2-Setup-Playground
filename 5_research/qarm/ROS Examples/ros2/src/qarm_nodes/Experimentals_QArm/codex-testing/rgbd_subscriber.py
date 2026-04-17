#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import Image


class ExperimentalRgbdSubscriber(Node):
    def __init__(self) -> None:
        super().__init__('experimental_rgbd_subscriber')
        self.declare_parameter('output_dir', str(Path.cwd()))
        self.declare_parameter('status_file', 'camera_status.json')
        self.declare_parameter('color_topic', 'qarm_camera/color')
        self.declare_parameter('depth_topic', 'qarm_camera/depth')
        self.declare_parameter('ir_left_topic', 'qarm_camera/ir_left')
        self.declare_parameter('ir_right_topic', 'qarm_camera/ir_right')

        self.output_dir = Path(str(self.get_parameter('output_dir').value)).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.status_file = self.output_dir / str(self.get_parameter('status_file').value)
        self.bridge = CvBridge()

        self.latest: dict[str, dict[str, Any]] = {}

        self.create_subscription(
            Image,
            str(self.get_parameter('color_topic').value),
            self._on_color,
            10,
        )
        self.create_subscription(
            Image,
            str(self.get_parameter('depth_topic').value),
            self._on_depth,
            10,
        )
        self.create_subscription(
            Image,
            str(self.get_parameter('ir_left_topic').value),
            self._on_ir_left,
            10,
        )
        self.create_subscription(
            Image,
            str(self.get_parameter('ir_right_topic').value),
            self._on_ir_right,
            10,
        )

        self._write_status(
            state='waiting',
            message='Waiting for color/depth frames. IR is optional and will appear only if published.',
        )
        self.get_logger().info('Experimental RGBD subscriber started')

    def _stamp_to_dict(self, msg: Image) -> dict[str, int]:
        return {
            'sec': int(msg.header.stamp.sec),
            'nanosec': int(msg.header.stamp.nanosec),
        }

    def _write_status(self, **payload: Any) -> None:
        payload.setdefault('topics', {
            'color': str(self.get_parameter('color_topic').value),
            'depth': str(self.get_parameter('depth_topic').value),
            'ir_left': str(self.get_parameter('ir_left_topic').value),
            'ir_right': str(self.get_parameter('ir_right_topic').value),
        })
        payload.setdefault('frames', self.latest)
        self.status_file.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')

    def _on_color(self, msg: Image) -> None:
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        mean_bgr = image.mean(axis=(0, 1))
        center_pixel = image[image.shape[0] // 2, image.shape[1] // 2].tolist()
        self.latest['color'] = {
            'frame_id': msg.header.frame_id,
            'stamp': self._stamp_to_dict(msg),
            'shape': [int(v) for v in image.shape],
            'center_pixel_bgr': [int(v) for v in center_pixel],
            'mean_bgr': [round(float(v), 2) for v in mean_bgr],
        }
        self._write_status(
            state='streaming',
            message='Received color frame.',
        )

    def _on_depth(self, msg: Image) -> None:
        depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='32FC1')
        center_value = float(depth[depth.shape[0] // 2, depth.shape[1] // 2])
        finite_depth = depth[np.isfinite(depth)]
        min_depth = float(np.min(finite_depth)) if finite_depth.size else None
        max_depth = float(np.max(finite_depth)) if finite_depth.size else None
        self.latest['depth'] = {
            'frame_id': msg.header.frame_id,
            'stamp': self._stamp_to_dict(msg),
            'shape': [int(v) for v in depth.shape],
            'center_depth_m': round(center_value, 4) if np.isfinite(center_value) else None,
            'min_depth_m': round(min_depth, 4) if min_depth is not None else None,
            'max_depth_m': round(max_depth, 4) if max_depth is not None else None,
        }
        self._write_status(
            state='streaming',
            message='Received depth frame.',
        )

    def _on_ir_left(self, msg: Image) -> None:
        self.latest['ir_left'] = self._summarize_ir(msg, stream_name='ir_left')
        self._write_status(
            state='streaming',
            message='Received left IR frame.',
        )

    def _on_ir_right(self, msg: Image) -> None:
        self.latest['ir_right'] = self._summarize_ir(msg, stream_name='ir_right')
        self._write_status(
            state='streaming',
            message='Received right IR frame.',
        )

    def _summarize_ir(self, msg: Image, stream_name: str) -> dict[str, Any]:
        try:
            image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        except Exception:
            image = self.bridge.imgmsg_to_cv2(msg)

        if image.ndim == 3:
            grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            grayscale = image

        center_value = float(grayscale[grayscale.shape[0] // 2, grayscale.shape[1] // 2])
        return {
            'frame_id': msg.header.frame_id,
            'stamp': self._stamp_to_dict(msg),
            'shape': [int(v) for v in grayscale.shape],
            'center_intensity': round(center_value, 2),
            'mean_intensity': round(float(np.mean(grayscale)), 2),
            'stream': stream_name,
        }


def main(args=None) -> None:
    node = None
    try:
        with rclpy.init(args=args):
            node = ExperimentalRgbdSubscriber()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if node is not None:
            node.destroy_node()


if __name__ == '__main__':
    main()
