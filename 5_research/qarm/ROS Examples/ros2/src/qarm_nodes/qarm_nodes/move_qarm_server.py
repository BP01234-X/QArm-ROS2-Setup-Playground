#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer,CancelResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor,ExternalShutdownException

from sensor_msgs.msg import JointState
from std_msgs.msg import Float64,Float64MultiArray
from qarm_interfaces.action import MoveQArm

import numpy as np
from hal.products.qarm import QArmUtilities

class QArmActionServer(Node):

    def __init__(self, name):
        super().__init__(name)

        # Initialize QArm Util
        self.myArmUtil = QArmUtilities()

        # Create publisher for QArm commands
        self.joint_pub_ = self.create_publisher(
            Float64MultiArray,
            'qarm/joint_position_cmd',
            10
        )

        self.led_pub_ = self.create_publisher(
            Float64MultiArray,
            'qarm/led_cmd',
            10
        )

        # Create subscriber for QArm states
        self.joint_state_sub_ = self.create_subscription(
            JointState,
            'qarm/joint_states',
            self.joint_sub_cb,
            10
        )

        # Create messages for feedback and result
        self.feedback_ = MoveQArm.Feedback()
        self.result_ = MoveQArm.Result()

        # Initialize buffers and other parameters
        self.joint_command = np.zeros(4, dtype=np.float64)
        self.LED_command = np.zeros(3, dtype=np.float64)
        self.latest_joint_positions = np.zeros(5, dtype=np.float64)
        self.prev_phi = np.zeros(4, dtype=np.float64)
        self.declare_parameter('position_tolerance_m', 0.008)
        self.declare_parameter('orientation_tolerance_rad', 0.02)
        self.declare_parameter('goal_timeout_sec', 20.0)
        self.position_tolerance_m = float(self.get_parameter('position_tolerance_m').value)
        self.orientation_tolerance_rad = float(self.get_parameter('orientation_tolerance_rad').value)
        self.goal_timeout_sec = float(self.get_parameter('goal_timeout_sec').value)

        self.action_name_ = name
        self.action_server_ = ActionServer(
            self,
            MoveQArm,
            self.action_name_,
            execute_callback=self.execute_cb,
            cancel_callback=self.cancel_cb,
            callback_group = ReentrantCallbackGroup()
        )
        self.rate = self.create_rate(30) 
        self.get_logger().info(
            "Move Arm Action server started "
            f"(position_tolerance_m={self.position_tolerance_m:.4f}, "
            f"orientation_tolerance_rad={self.orientation_tolerance_rad:.4f}, "
            f"goal_timeout_sec={self.goal_timeout_sec:.1f})"
        )

    def joint_sub_cb(self,joint_state:JointState):
        self.latest_joint_positions = np.array(joint_state.position)

    def _compute_pose_errors(self, pose_cmd, joints):
        current_p, _ = self.myArmUtil.forward_kinematics(joints[:4])
        position_error_norm = float(np.linalg.norm(current_p - pose_cmd[:3]))
        orientation_error = float(np.abs(pose_cmd[3] - joints[3]))
        return position_error_norm, orientation_error

    def _within_goal_tolerance(self, position_error_norm: float, orientation_error: float) -> bool:
        return (
            position_error_norm <= self.position_tolerance_m
            and orientation_error <= self.orientation_tolerance_rad
        )

    def execute_cb(self, goal_handle: ServerGoalHandle):
        
        success = False
        reached = False

        goal = goal_handle.request
        pose_cmd = np.array(goal.task_space_pose, dtype=np.float64)

        self.get_logger().info("Moving QArm to goal")
        
        phi, phiOptimal = self.myArmUtil.inverse_kinematics(pose_cmd[:3], pose_cmd[3], self.latest_joint_positions[0:4])
        candidate_joints = np.array(phiOptimal, dtype=np.float64)
        outsideLimit = all(x == y for x, y in zip(candidate_joints, [0,0,0,0]))
        if not outsideLimit:
            predicted_pos_err, predicted_ori_err = self._compute_pose_errors(pose_cmd, candidate_joints)
            outsideLimit = not self._within_goal_tolerance(predicted_pos_err, predicted_ori_err)
        else:
            predicted_pos_err = float("inf")
            predicted_ori_err = float("inf")
        if outsideLimit: # inv kin return [0,0,0,0] when the goal is outside of the joint limits
            success = False
            reached = True
            self.get_logger().warn(
                f"Goal pose {pose_cmd.tolist()} rejected by IK/tolerance check "
                f"(predicted_pos_err={predicted_pos_err:.4f} m, "
                f"predicted_orientation_err={predicted_ori_err:.4f} rad)"
            )
            led_cmd_msg = Float64MultiArray()
            led_cmd_msg.data = np.array([1,0,0])
            self.led_pub_.publish(led_cmd_msg)
        else:
            joint_cmd_msg = Float64MultiArray()
            joint_cmd_msg.data = candidate_joints
            self.joint_pub_.publish(joint_cmd_msg)

            led_cmd_msg = Float64MultiArray()
            led_cmd_msg.data = np.array([0,1,0])
            self.led_pub_.publish(led_cmd_msg)

        goal_start = time.time()
        while not reached:
            current_joints = np.array(self.latest_joint_positions[:4], dtype=np.float64)
            position_error_norm, orientation_error = self._compute_pose_errors(pose_cmd, current_joints)
            if self._within_goal_tolerance(position_error_norm, orientation_error):
                reached = True
                success = True
            elif (time.time() - goal_start) >= self.goal_timeout_sec:
                reached = True
                success = False
                self.get_logger().warn(
                    f"Goal timeout after {self.goal_timeout_sec:.1f}s "
                    f"(position_error={position_error_norm:.4f} m, "
                    f"orientation_error={orientation_error:.4f} rad)"
                )

            # Publish feedback
            self.feedback_.position_error_norm = position_error_norm
            self.feedback_.orientation_error = orientation_error
            goal_handle.publish_feedback(self.feedback_)

            self.rate .sleep()

        self.result_.success = success
        if success:
            self.result_.message = 'QArm has reached the target pose.'
            self.get_logger().info(f'{self.action_name_}: Succeeded')
            goal_handle.succeed()
        else:
            self.result_.message = 'QArm failed to reached the target pose.'
            self.get_logger().info(f'{self.action_name_}: Failed')
            goal_handle.abort()
        return self.result_
    
    def cancel_cb(self,goal_handle:ServerGoalHandle):

        self.get_logger().info('Received cancel request')
        self.get_logger().info('Moving arm to previous time step')
        joint_cmd_msg = Float64MultiArray()
        joint_cmd_msg.data = self.latest_joint_positions[:4]
        self.joint_pub_.publish(joint_cmd_msg)

        led_cmd_msg = Float64MultiArray()
        led_cmd_msg.data = np.array([1,1,0])
        self.led_pub_.publish(led_cmd_msg)

        return CancelResponse.ACCEPT


def main(args=None):
    try:
        with rclpy.init(args=args):
            qarm_action_server = QArmActionServer('move_qarm')
            executor = MultiThreadedExecutor()
            executor.add_node(qarm_action_server)
            executor.spin()

    except (KeyboardInterrupt,ExternalShutdownException):
        pass

    finally:     
        qarm_action_server.destroy_node()

if __name__ == '__main__':
    main()
