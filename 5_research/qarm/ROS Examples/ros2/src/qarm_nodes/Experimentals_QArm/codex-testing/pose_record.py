#!/usr/bin/env python3

import argparse
import json
import signal
import subprocess
import sys
import time
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


class StartupPoseCapture(Node):
    def __init__(self, pose_name: str, poses_file: Path) -> None:
        super().__init__('startup_pose_capture')
        self.pose_name = pose_name
        self.poses_file = poses_file
        self.arm_util = QArmUtilities()
        self.captured = False
        self.subscription = self.create_subscription(
            JointState,
            '/qarm/joint_states',
            self._joint_state_cb,
            10,
        )

    def _joint_state_cb(self, msg: JointState) -> None:
        if self.captured or len(msg.position) < 4:
            return

        phi = list(msg.position[:4])
        position, _ = self.arm_util.forward_kinematics(phi)
        goal_pose = [round(float(v), 6) for v in [position[0], position[1], position[2], phi[3]]]

        payload = load_json_or_default(self.poses_file, {'poses': {}})
        payload.setdefault('poses', {})[self.pose_name] = {
            'goal_pose': goal_pose,
            'joint_positions': [round(float(v), 6) for v in phi],
            'recorded_at': utc_now_iso(),
            'source': 'pose_record startup capture',
            'note': 'Captured immediately after starting qarm_hardware in hold-startup-pose mode.',
        }
        atomic_write_json(self.poses_file, payload)
        self.get_logger().info(f"Captured startup pose '{self.pose_name}' as {goal_pose}")
        self.captured = True
        self.destroy_node()


def start_process(cmd: list[str], cwd: Path) -> subprocess.Popen:
    return subprocess.Popen(cmd, cwd=str(cwd))


def terminate_processes(processes: list[subprocess.Popen]) -> None:
    for proc in processes:
        if proc.poll() is None:
            proc.send_signal(signal.SIGINT)
    deadline = time.time() + 5.0
    for proc in processes:
        if proc.poll() is None:
            timeout = max(0.0, deadline - time.time())
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill()


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Start QArm hold-current hardware, move_qarm server, and bridge; save the startup pose by name.'
    )
    parser.add_argument('name', help='Name to store for the startup pose.')
    parser.add_argument(
        '--workspace',
        default='.',
        help='ROS workspace root containing src/ and install/.',
    )
    parser.add_argument(
        '--poses-file',
        default=str(Path(__file__).with_name('saved_poses.json')),
        help='Path to the JSON pose registry file.',
    )
    parser.add_argument(
        '--bridge-dir',
        default=str(Path(__file__).resolve().parent),
        help='Path to the codex-testing bridge directory.',
    )
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    poses_file = Path(args.poses_file).expanduser().resolve()
    bridge_dir = Path(args.bridge_dir).expanduser().resolve()

    processes: list[subprocess.Popen] = []
    try:
        processes.append(
            start_process(
                [
                    'python3',
                    '-m',
                    'qarm_nodes.qarm_hardware',
                    '--ros-args',
                    '-p',
                    'hold_startup_pose:=true',
                ],
                workspace,
            )
        )
        time.sleep(1.0)
        processes.append(
            start_process(
                ['python3', '-m', 'qarm_nodes.move_qarm_server'],
                workspace,
            )
        )
        processes.append(
            start_process(
                [
                    'python3',
                    str(bridge_dir / 'bridge_commander.py'),
                    '--ros-args',
                    '-p',
                    f'bridge_dir:={bridge_dir}',
                ],
                workspace,
            )
        )

        with rclpy.init(args=None):
            node = StartupPoseCapture(args.name, poses_file)
            start_time = time.time()
            while rclpy.ok() and not node.captured:
                rclpy.spin_once(node, timeout_sec=0.2)
                if time.time() - start_time > 10.0:
                    raise RuntimeError('Timed out waiting for /qarm/joint_states to capture startup pose.')

        print(f"Started hold-current qarm_hardware + move_qarm_server + bridge and saved pose '{args.name}'.")
        print('Processes remain running until you press Ctrl+C.')
        while True:
            time.sleep(1.0)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        terminate_processes(processes)


if __name__ == '__main__':
    main()
