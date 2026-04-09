#!/usr/bin/env python3

import os
import select
import sys
import termios
import tty

import numpy as np
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

lib_repo = os.environ.get('LIB_REPO')
if lib_repo:
    preferred_python = os.path.join(lib_repo, '0_libraries', 'python')
    if os.path.isdir(preferred_python) and preferred_python not in sys.path:
        sys.path.insert(0, preferred_python)

from hal.products.qarm import QArmUtilities
from pal.products.qarm import QArm

JOINT_POSITION_CMD_TOPIC = '/qarm/joint_position_cmd'
JOINT_STATES_TOPIC = '/qarm/joint_states'


class TerminalKeyboardAdapter:
    def __init__(self):
        self.tty_stream = None
        self.closed = False
        if sys.stdin.isatty():
            self.tty_stream = sys.stdin
        else:
            self.tty_stream = open('/dev/tty', 'r', encoding='utf-8', buffering=1)
        self.fd = self.tty_stream.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)
        self.reset()

    def reset(self):
        self.k_space = False
        self.k_home = False
        self.k_esc = False
        self.k_w = False
        self.k_s = False
        self.k_d = False
        self.k_a = False
        self.k_x = False
        self.k_y = False
        self.k_z = False
        self.k_g = False
        self.k_f = False
        self.k_r = False
        self.k_t = False
        self.k_0 = False
        self.k_1 = False
        self.k_2 = False
        self.k_3 = False
        self.k_4 = False
        self.k_5 = False
        self.k_6 = False
        self.k_7 = False
        self.k_8 = False
        self.k_9 = False

    def _apply_char(self, char):
        if char == ' ':
            self.k_space = True
        elif char == '\x1b':
            self.k_esc = True
        elif char in '0123456789':
            setattr(self, f'k_{char}', True)
        elif char.lower() in {'w', 's', 'd', 'a', 'x', 'y', 'z', 'g', 'f', 'r', 't'}:
            setattr(self, f'k_{char.lower()}', True)

    def update(self):
        self.reset()
        while True:
            ready, _, _ = select.select([self.tty_stream], [], [], 0.0)
            if not ready:
                break
            char = self.tty_stream.read(1)
            if char == '\x1b':
                self.k_esc = True
            else:
                self._apply_char(char)

    def close(self):
        if self.closed:
            return
        self.closed = True
        try:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
        except termios.error:
            pass
        if self.tty_stream is not None and self.tty_stream is not sys.stdin:
            try:
                self.tty_stream.close()
            except OSError:
                pass


class QArmKeyboardControl(Node):
    def __init__(self):
        super().__init__('qarm_keyboard_control')

        self.declare_parameter('mode', 'joint')
        self.declare_parameter('publish_rate_hz', 30.0)
        self.declare_parameter('joint_speed', float(np.pi / 12.0))
        self.declare_parameter('task_speed', 0.02)

        self.mode = str(self.get_parameter('mode').value).lower()
        self.publish_rate_hz = float(self.get_parameter('publish_rate_hz').value)
        self.joint_speed = float(self.get_parameter('joint_speed').value)
        self.task_speed = float(self.get_parameter('task_speed').value)
        self.dt = 1.0 / max(self.publish_rate_hz, 1.0)

        self.arm_util = QArmUtilities()
        self.keyboard = None
        self.keyboard = TerminalKeyboardAdapter()
        self.joint_state_received = False
        self.current_joint_pose = QArm.HOME_POSE.copy()
        self.selected_joint = 0
        self.selected_task_axis = 'x'
        self.last_command = self.current_joint_pose.copy()
        self.shutdown_requested = False

        self.joint_pub_ = self.create_publisher(Float64MultiArray, JOINT_POSITION_CMD_TOPIC, 10)
        self.joint_state_sub_ = self.create_subscription(
            JointState,
            JOINT_STATES_TOPIC,
            self.joint_state_cb,
            10,
        )
        self.timer = self.create_timer(self.dt, self.publish_command)

        self._print_controls()

    def _print_controls(self):
        self.get_logger().info('Keyboard control is reading from the launch terminal.')
        if self.mode == 'task':
            self.get_logger().info('Task mode: x/y/z/g select axis, w positive, s negative, 0 home, Esc exit.')
        else:
            self.get_logger().info('Joint mode: 1/2/3/4 select joint, w positive, s negative, 0 home, Esc exit.')

    def joint_state_cb(self, joint_state: JointState):
        if len(joint_state.position) >= 4 and not self.joint_state_received:
            initial_pose = np.asarray(joint_state.position[:4], dtype=np.float64)
            self.current_joint_pose = initial_pose.copy()
            self.last_command = initial_pose.copy()
            self.joint_state_received = True
            self.get_logger().info(f'Initialized keyboard control from joint state {initial_pose.tolist()}')

    def _update_selection(self):
        if self.keyboard.k_1:
            self.selected_joint = 0
        elif self.keyboard.k_2:
            self.selected_joint = 1
        elif self.keyboard.k_3:
            self.selected_joint = 2
        elif self.keyboard.k_4:
            self.selected_joint = 3

        if self.keyboard.k_x:
            self.selected_task_axis = 'x'
        elif self.keyboard.k_y:
            self.selected_task_axis = 'y'
        elif self.keyboard.k_z:
            self.selected_task_axis = 'z'
        elif self.keyboard.k_g:
            self.selected_task_axis = 'g'

    def _step_input(self, speed):
        if self.keyboard.k_w:
            return speed
        if self.keyboard.k_s:
            return -speed
        return 0.0

    def _next_joint_command(self):
        step = self._step_input(self.joint_speed * self.dt)
        joint_cmd = self.current_joint_pose.copy()
        if step != 0.0:
            joint_cmd[self.selected_joint] += step
        return np.clip(joint_cmd, QArm.LIMITS_MIN[:4], QArm.LIMITS_MAX[:4])

    def _next_task_command(self):
        step = self._step_input(self.task_speed)
        joint_cmd = self.current_joint_pose.copy()
        if step == 0.0:
            return joint_cmd

        position, _ = self.arm_util.forward_kinematics(joint_cmd)
        goal_position = np.asarray(position, dtype=np.float64).copy()
        goal_gamma = float(joint_cmd[3])

        if self.selected_task_axis == 'x':
            goal_position[0] += step
        elif self.selected_task_axis == 'y':
            goal_position[1] += step
        elif self.selected_task_axis == 'z':
            goal_position[2] += step
        elif self.selected_task_axis == 'g':
            goal_gamma = float(np.clip(goal_gamma + 10.0 * step, QArm.LIMITS_MIN[3], QArm.LIMITS_MAX[3]))

        _, phi_optimal = self.arm_util.inverse_kinematics(goal_position, goal_gamma, joint_cmd)
        phi_optimal = np.asarray(phi_optimal, dtype=np.float64)
        if np.isnan(phi_optimal).any() or self.arm_util._check_joint_limits(phi_optimal):
            self.get_logger().warn('Ignoring keyboard task command outside valid IK workspace.')
            return joint_cmd
        return np.clip(phi_optimal, QArm.LIMITS_MIN[:4], QArm.LIMITS_MAX[:4])

    def publish_command(self):
        self.keyboard.update()
        self._update_selection()

        if self.keyboard.k_esc:
            self.get_logger().info('Escape pressed, shutting down keyboard control.')
            self.shutdown_requested = True
            rclpy.shutdown()
            return

        if self.keyboard.k_home or self.keyboard.k_0:
            home_pose = QArm.HOME_POSE.copy()
            self.current_joint_pose = home_pose.copy()
            self.last_command = home_pose.copy()
            self.get_logger().info('Reset keyboard command pose to HOME.')

        if self.mode == 'task':
            joint_cmd = self._next_task_command()
        else:
            joint_cmd = self._next_joint_command()

        joint_cmd = np.clip(np.asarray(joint_cmd, dtype=np.float64), QArm.LIMITS_MIN[:4], QArm.LIMITS_MAX[:4])
        self.current_joint_pose = joint_cmd.copy()

        msg = Float64MultiArray()
        msg.data = joint_cmd.tolist()
        self.joint_pub_.publish(msg)

        if not np.allclose(joint_cmd, self.last_command, atol=1e-6):
            self.get_logger().info(f'Publishing keyboard joint target: {joint_cmd.tolist()}')
            self.last_command = joint_cmd.copy()

    def destroy_node(self):
        if self.keyboard is not None:
            self.keyboard.close()
        super().destroy_node()


def main(args=None):
    node = None
    try:
        with rclpy.init(args=args):
            node = QArmKeyboardControl()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if node is not None:
            node.destroy_node()


if __name__ == '__main__':
    main()
