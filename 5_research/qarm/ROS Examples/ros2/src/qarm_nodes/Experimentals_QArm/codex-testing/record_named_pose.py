#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import JointState

from hal.products.qarm import QArmUtilities


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + '.tmp')
    tmp_path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    tmp_path.replace(path)


def load_json_or_default(path: Path, default: dict) -> dict:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return default


class NamedPoseRecorder(Node):
    def __init__(self, pose_name: str, poses_file: Path, gripper: float | None) -> None:
        super().__init__('named_pose_recorder')
        self.pose_name = pose_name
        self.poses_file = poses_file
        self.gripper = gripper
        self.arm_util = QArmUtilities()
        self.subscription = self.create_subscription(
            JointState,
            '/qarm/joint_states',
            self._joint_state_cb,
            10,
        )
        self.recorded = False

    def _joint_state_cb(self, msg: JointState) -> None:
        if self.recorded:
            return
        if len(msg.position) < 4:
            self.get_logger().warning('Received JointState with fewer than 4 joint positions.')
            return

        phi = list(msg.position[:4])
        position, _ = self.arm_util.forward_kinematics(phi)
        goal_pose = [round(float(v), 6) for v in [position[0], position[1], position[2], phi[3]]]

        payload = load_json_or_default(self.poses_file, {'poses': {}})
        poses = payload.setdefault('poses', {})
        pose_record = {
            'goal_pose': goal_pose,
            'recorded_at': utc_now_iso(),
            'joint_positions': [round(float(v), 6) for v in phi],
            'source_topic': '/qarm/joint_states',
        }
        if self.gripper is not None:
            pose_record['gripper'] = round(float(self.gripper), 6)

        poses[self.pose_name] = pose_record
        atomic_write_json(self.poses_file, payload)
        self.get_logger().info(
            f"Recorded pose '{self.pose_name}' as goal_pose={goal_pose}"
            + (f", gripper={pose_record['gripper']}" if 'gripper' in pose_record else '')
        )
        self.recorded = True
        self.destroy_node()


def main(args=None) -> None:
    parser = argparse.ArgumentParser(
        description='Record the current QArm task-space pose from /qarm/joint_states into saved_poses.json.'
    )
    parser.add_argument('name', help='Name to save for this pose.')
    parser.add_argument(
        '--poses-file',
        default=str(Path(__file__).with_name('saved_poses.json')),
        help='Path to the JSON pose registry file.',
    )
    parser.add_argument(
        '--gripper',
        type=float,
        default=None,
        help='Optional gripper value to store alongside the pose.',
    )
    parsed = parser.parse_args(args=args)

    try:
        with rclpy.init(args=None):
            node = NamedPoseRecorder(
                pose_name=parsed.name,
                poses_file=Path(parsed.poses_file).expanduser(),
                gripper=parsed.gripper,
            )
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
