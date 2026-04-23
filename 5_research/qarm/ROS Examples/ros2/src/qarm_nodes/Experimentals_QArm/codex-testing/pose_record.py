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

try:
    import yaml
except ImportError:  # pragma: no cover - optional until observer update is requested
    yaml = None


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


def load_yaml_or_default(path: Path, default: dict) -> dict:
    if yaml is None:
        raise RuntimeError('PyYAML is required when updating observer_pose.yaml')
    try:
        payload = yaml.safe_load(path.read_text(encoding='utf-8'))
    except OSError:
        payload = None
    if isinstance(payload, dict):
        return payload
    return default


def atomic_write_yaml(path: Path, payload: dict) -> None:
    if yaml is None:
        raise RuntimeError('PyYAML is required when updating observer_pose.yaml')
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + '.tmp')
    tmp_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')
    tmp_path.replace(path)


def update_observer_pose_config(
    observer_config: Path,
    observer_name: str,
    goal_pose: list[float],
    source_pose_name: str,
) -> None:
    payload = load_yaml_or_default(observer_config, {})
    candidates = payload.setdefault('observer_pose_candidates', {})
    observer_xyz = [round(float(v), 6) for v in goal_pose[:3]]
    observer_rpy = [0.0, 0.0, round(float(goal_pose[3]), 6)]

    candidates[observer_name] = {
        'observer_world_xyz': observer_xyz,
        'observer_rpy': observer_rpy,
        'note': (
            f"Captured from pose_record hold-startup flow using saved pose "
            f"'{source_pose_name}' on {utc_now_iso()}."
        ),
        'evaluation_focus': (
            'Manual recorder-tuned chess observer pose captured from the live bridge '
            'hold workflow.'
        ),
    }
    payload['default_observer_pose'] = observer_name
    payload['observer_pose_name'] = observer_name
    payload['observer_world_xyz'] = observer_xyz
    payload['observer_rpy'] = observer_rpy
    atomic_write_yaml(observer_config, payload)


class StartupPoseCapture(Node):
    def __init__(
        self,
        pose_name: str,
        poses_file: Path,
        observer_config: Path | None = None,
        observer_name: str | None = None,
    ) -> None:
        super().__init__('startup_pose_capture')
        self.pose_name = pose_name
        self.poses_file = poses_file
        self.observer_config = observer_config
        self.observer_name = observer_name
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
        if self.observer_config is not None and self.observer_name is not None:
            update_observer_pose_config(
                observer_config=self.observer_config,
                observer_name=self.observer_name,
                goal_pose=goal_pose,
                source_pose_name=self.pose_name,
            )
            self.get_logger().info(
                f"Updated observer pose config '{self.observer_name}' in {self.observer_config}"
            )
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
        description='Start QArm hardware in hold-current mode and save the startup pose by name.'
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
    parser.add_argument(
        '--update-chess-observer',
        action='store_true',
        help='Also update the Phase 3 observer_pose.yaml active chess observer fields.',
    )
    parser.add_argument(
        '--observer-config',
        default=str(
            Path(__file__).resolve().parent / 'chess-logic' / 'config' / 'observer_pose.yaml'
        ),
        help='Path to the Phase 3 observer_pose.yaml file.',
    )
    parser.add_argument(
        '--observer-name',
        default='chess_observer_manual',
        help='Observer pose candidate name to create/update inside observer_pose.yaml.',
    )
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    poses_file = Path(args.poses_file).expanduser().resolve()
    bridge_dir = Path(args.bridge_dir).expanduser().resolve()
    observer_config = Path(args.observer_config).expanduser().resolve()
    hold_helper = bridge_dir / 'start_qarm_hardware_hold.py'

    processes: list[subprocess.Popen] = []
    try:
        processes.append(
            start_process(
                ['python3', str(hold_helper)],
                workspace,
            )
        )
        time.sleep(1.0)

        with rclpy.init(args=None):
            node = StartupPoseCapture(
                pose_name=args.name,
                poses_file=poses_file,
                observer_config=observer_config if args.update_chess_observer else None,
                observer_name=args.observer_name if args.update_chess_observer else None,
            )
            start_time = time.time()
            while rclpy.ok() and not node.captured:
                rclpy.spin_once(node, timeout_sec=0.2)
                if time.time() - start_time > 10.0:
                    raise RuntimeError('Timed out waiting for /qarm/joint_states to capture startup pose.')

        print(f"Started hold-current qarm_hardware and saved pose '{args.name}'.")
        if args.update_chess_observer:
            print(
                f"Updated observer pose '{args.observer_name}' in {observer_config} "
                "and made it the active chess observer pose."
            )
        print('Processes remain running until you press Ctrl+C.')
        while True:
            time.sleep(1.0)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        terminate_processes(processes)


if __name__ == '__main__':
    main()
