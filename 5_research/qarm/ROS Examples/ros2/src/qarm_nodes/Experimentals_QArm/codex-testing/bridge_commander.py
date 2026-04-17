#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Any

import rclpy
from rclpy.action import ActionClient
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64

from qarm_interfaces.action import MoveQArm


class BridgeCommander(Node):
    SAFE_HOME_POSE = [0.45, 0.0, 0.49, 0.0]

    def __init__(self) -> None:
        super().__init__('bridge_commander')
        self.declare_parameter('bridge_dir', str(Path.cwd()))
        self.declare_parameter('target_file', 'target_pose.json')
        self.declare_parameter('status_file', 'status.json')
        self.declare_parameter('poll_period_sec', 0.2)

        self.bridge_dir = Path(str(self.get_parameter('bridge_dir').value)).expanduser()
        self.target_file = self.bridge_dir / str(self.get_parameter('target_file').value)
        self.status_file = self.bridge_dir / str(self.get_parameter('status_file').value)
        self.poll_period = float(self.get_parameter('poll_period_sec').value)

        self.bridge_dir.mkdir(parents=True, exist_ok=True)
        self.target_file.touch(exist_ok=True)
        self.action_client = ActionClient(self, MoveQArm, 'move_qarm')
        self.gripper_pub = self.create_publisher(Float64, '/qarm/gripper_cmd', 10)

        self.last_payload_fingerprint = ''
        self.active_goal_handle = None
        self.active_goal_id: str | None = None
        self.pending_command: dict[str, Any] | None = None
        self.last_executed_signature: str | None = None
        self.last_pose_signature: str | None = None
        self.last_gripper_value: float | None = None

        self._ensure_target_template()
        self._write_status(
            state='idle',
            message='Waiting for target_pose.json updates.',
            active_goal_id=None,
            active_goal_pose=None,
        )
        self.create_timer(self.poll_period, self._poll_target_file)
        self.get_logger().info(f'Watching bridge file {self.target_file}')

    def _ensure_target_template(self) -> None:
        if self.target_file.stat().st_size != 0:
            return
        template = {
            'goal_id': 'initial',
            'goal_pose': self.SAFE_HOME_POSE,
            'gripper': 0.1,
            'enabled': False,
            'note': 'Set enabled=true and change goal_id to send a goal. Gripper is optional.',
        }
        self.target_file.write_text(json.dumps(template, indent=2) + '\n', encoding='utf-8')

    def _write_status(self, **payload: Any) -> None:
        payload.setdefault('bridge_dir', str(self.bridge_dir))
        payload.setdefault('target_file', str(self.target_file))
        payload.setdefault('status_file', str(self.status_file))
        self.status_file.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')

    def _poll_target_file(self) -> None:
        try:
            raw_payload = self.target_file.read_text(encoding='utf-8')
        except OSError as exc:
            self._write_status(state='error', message=f'Failed to read target file: {exc}')
            return

        fingerprint = raw_payload.strip()
        if not fingerprint or fingerprint == self.last_payload_fingerprint:
            return

        try:
            command = json.loads(raw_payload)
        except json.JSONDecodeError as exc:
            self.last_payload_fingerprint = fingerprint
            self._write_status(state='error', message=f'Invalid JSON: {exc}')
            return

        self.last_payload_fingerprint = fingerprint

        if not command.get('enabled', True):
            self._write_status(
                state='idle',
                message='Target file updated but enabled=false, ignoring command.',
                active_goal_id=self.active_goal_id,
                active_goal_pose=None,
                active_gripper=None,
            )
            return

        error = self._validate_command(command)
        if error is not None:
            self._write_status(state='error', message=error, active_goal_id=self.active_goal_id)
            return

        normalized_signature = self._command_signature(command)
        if self.last_executed_signature == normalized_signature and self.active_goal_handle is None:
            self._write_status(
                state='idle',
                message='Ignored duplicate command with identical pose/gripper payload.',
                active_goal_id=self.active_goal_id,
                active_goal_pose=command['goal_pose'],
                active_gripper=command.get('gripper'),
            )
            return

        if self.active_goal_handle is None and self._is_gripper_only_update(command):
            gripper = float(command['gripper'])
            self._publish_gripper(gripper)
            self.last_executed_signature = normalized_signature
            self.last_gripper_value = gripper
            self._write_status(
                state='succeeded',
                message='Applied gripper-only update without resending the same pose goal.',
                active_goal_id=command['goal_id'],
                active_goal_pose=self._normalized_goal_pose(command),
                active_gripper=gripper,
                success=True,
            )
            return

        if self.active_goal_handle is not None:
            self.pending_command = command
            self._write_status(
                state='canceling',
                message='Received a new command while a goal is active. Canceling current goal.',
                active_goal_id=self.active_goal_id,
                active_goal_pose=None,
                active_gripper=None,
                pending_goal_id=command['goal_id'],
                pending_goal_pose=command['goal_pose'],
                pending_gripper=command.get('gripper'),
            )
            self.active_goal_handle.cancel_goal_async().add_done_callback(self._cancel_done_cb)
            return

        self._send_goal(command)

    def _validate_command(self, command: dict[str, Any]) -> str | None:
        goal_pose = command.get('goal_pose')
        if not isinstance(goal_pose, list) or len(goal_pose) != 4:
            return 'goal_pose must be a JSON array with four numbers: [x, y, z, wrist].'
        try:
            [float(value) for value in goal_pose]
        except (TypeError, ValueError):
            return 'goal_pose values must be numeric.'
        if 'gripper' in command:
            try:
                gripper_value = float(command['gripper'])
            except (TypeError, ValueError):
                return 'gripper must be numeric if provided.'
            if gripper_value < 0.1 or gripper_value > 0.9:
                return 'gripper must stay within [0.1, 0.9].'
        if not command.get('goal_id'):
            return 'goal_id must be set so repeated edits are distinguishable.'
        return None

    def _send_goal(self, command: dict[str, Any]) -> None:
        goal_pose = self._normalized_goal_pose(command)
        goal_id = str(command['goal_id'])
        gripper = float(command['gripper']) if 'gripper' in command else None

        command_signature = self._command_signature(command)

        if gripper is not None:
            self._publish_gripper(gripper)

        self._write_status(
            state='waiting_for_server',
            message='Waiting for move_qarm action server.',
            active_goal_id=goal_id,
            active_goal_pose=goal_pose,
            active_gripper=gripper,
        )

        self.action_client.wait_for_server()
        goal_msg = MoveQArm.Goal()
        goal_msg.task_space_pose = goal_pose
        self.active_goal_id = goal_id

        self._write_status(
            state='goal_sent',
            message='Goal sent to move_qarm action server.',
            active_goal_id=goal_id,
            active_goal_pose=goal_pose,
            active_gripper=gripper,
        )

        future = self.action_client.send_goal_async(goal_msg, feedback_callback=self._feedback_cb)
        future.add_done_callback(
            lambda done: self._goal_response_cb(done, goal_id, goal_pose, gripper, command_signature)
        )

    def _goal_response_cb(
        self,
        future,
        goal_id: str,
        goal_pose: list[float],
        gripper: float | None,
        command_signature: str,
    ) -> None:
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.active_goal_handle = None
            self.active_goal_id = None
            self._write_status(
                state='rejected',
                message='Action server rejected the goal.',
                active_goal_id=goal_id,
                active_goal_pose=goal_pose,
                active_gripper=gripper,
            )
            self._flush_pending_command()
            return

        self.active_goal_handle = goal_handle
        self.last_executed_signature = command_signature
        self.last_pose_signature = self._pose_signature(goal_pose)
        self.last_gripper_value = gripper
        self._write_status(
            state='accepted',
            message='Action server accepted the goal.',
            active_goal_id=goal_id,
            active_goal_pose=goal_pose,
            active_gripper=gripper,
        )
        goal_handle.get_result_async().add_done_callback(
            lambda done: self._result_cb(done, goal_id, goal_pose, gripper)
        )

    def _feedback_cb(self, feedback_msg) -> None:
        feedback = feedback_msg.feedback
        self._write_status(
            state='feedback',
            message='Goal is in progress.',
            active_goal_id=self.active_goal_id,
            position_error_norm=feedback.position_error_norm,
            orientation_error=feedback.orientation_error,
        )

    def _result_cb(self, future, goal_id: str, goal_pose: list[float], gripper: float | None) -> None:
        result = future.result().result
        self.active_goal_handle = None
        self.active_goal_id = None
        self._write_status(
            state='succeeded' if result.success else 'failed',
            message=result.message,
            active_goal_id=goal_id,
            active_goal_pose=goal_pose,
            active_gripper=gripper,
            success=result.success,
        )
        self._flush_pending_command()

    def _cancel_done_cb(self, future) -> None:
        cancel_response = future.result()
        if len(cancel_response.goals_canceling) > 0:
            self._write_status(
                state='canceled',
                message='Previous goal canceled. Sending pending goal if present.',
                active_goal_id=self.active_goal_id,
            )
        else:
            self._write_status(
                state='cancel_failed',
                message='Cancel request did not stop the current goal.',
                active_goal_id=self.active_goal_id,
            )
        self.active_goal_handle = None
        self.active_goal_id = None
        self._flush_pending_command()

    def _flush_pending_command(self) -> None:
        if self.pending_command is None:
            return
        pending = self.pending_command
        self.pending_command = None
        self._send_goal(pending)

    def _publish_gripper(self, value: float) -> None:
        msg = Float64()
        msg.data = float(value)
        self.gripper_pub.publish(msg)
        self.get_logger().info(f'Published gripper command: {value:.3f}')

    def _normalized_goal_pose(self, command: dict[str, Any]) -> list[float]:
        goal_pose = [float(value) for value in command['goal_pose']]
        if self._is_home_pose(goal_pose):
            return self.SAFE_HOME_POSE.copy()
        return goal_pose

    def _is_home_pose(self, goal_pose: list[float]) -> bool:
        return abs(goal_pose[0] - 0.45) < 1e-6 and abs(goal_pose[1]) < 1e-6 and abs(goal_pose[3]) < 1e-6 and abs(goal_pose[2] - 0.5) < 0.02

    def _command_signature(self, command: dict[str, Any]) -> str:
        normalized = {
            'goal_pose': self._normalized_goal_pose(command),
            'gripper': float(command['gripper']) if 'gripper' in command else None,
            'enabled': bool(command.get('enabled', True)),
        }
        return json.dumps(normalized, sort_keys=True)

    def _pose_signature(self, goal_pose: list[float]) -> str:
        rounded_pose = [round(float(value), 6) for value in goal_pose]
        return json.dumps(rounded_pose)

    def _is_gripper_only_update(self, command: dict[str, Any]) -> bool:
        if 'gripper' not in command:
            return False
        normalized_pose = self._normalized_goal_pose(command)
        if self.last_pose_signature is None:
            return False
        if self._pose_signature(normalized_pose) != self.last_pose_signature:
            return False
        new_gripper = float(command['gripper'])
        if self.last_gripper_value is None:
            return False
        return abs(new_gripper - self.last_gripper_value) > 1e-6


def main(args=None) -> None:
    node = None
    try:
        with rclpy.init(args=args):
            node = BridgeCommander()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if node is not None:
            node.destroy_node()


if __name__ == '__main__':
    main()
