#!/usr/bin/env python3

import numpy as np
import rclpy
from rclpy.action import ActionServer, CancelResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

from qarm_interfaces.action import MoveQArm
from hal.products.qarm import QArmUtilities
from pal.products.qarm import QArm

JOINT_POSITION_CMD_TOPIC = '/qarm/joint_position_cmd'
LED_CMD_TOPIC = '/qarm/led_cmd'
JOINT_STATES_TOPIC = '/qarm/joint_states'

class QArmActionServer(Node):
  #Definition of what is the qarm hardware
    def __init__(self, name):
        super().__init__(name)

        # Initialize QArm Util
        self.myArmUtil = QArmUtilities()

        # Create publisher for QArm commands
        self.joint_pub_ = self.create_publisher(
            Float64MultiArray,
            JOINT_POSITION_CMD_TOPIC,
            10
        )

        self.led_pub_ = self.create_publisher(
            Float64MultiArray,
            LED_CMD_TOPIC,
            10
        )

        # Create subscriber for QArm states
        self.joint_state_sub_ = self.create_subscription(
            JointState,
            JOINT_STATES_TOPIC,
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
        self.joint_state_received = False
        self.prev_phi = np.zeros(4, dtype=np.float64)
        self.threshhold = 0.04
        self.control_rate_hz = 50.0
        self.control_dt = 1.0 / self.control_rate_hz
        self.feedback_sync_tolerance = 1e-3

        self.action_name_ = name
        self.action_server_ = ActionServer(
            self,
            MoveQArm,
            self.action_name_,
            execute_callback=self.execute_cb,
            cancel_callback=self.cancel_cb,
            callback_group = ReentrantCallbackGroup()
        )
        self.rate = self.create_rate(self.control_rate_hz)
        self.get_logger().info("Move Arm Action server started")
        
        #Tunable Variables for singularity handling
        self.cond_treshold = 35.0
        self.lambda_max = 0.20
        self.k_task = 1.0 # Gain for task space control and speed.
        self.dt = self.control_dt
        
        

    def joint_sub_cb(self,joint_state:JointState):
        if len(joint_state.position) >= 4:
            positions = np.zeros(5, dtype=np.float64)
            limit = min(len(joint_state.position), len(positions))
            positions[:limit] = np.asarray(joint_state.position[:limit], dtype=np.float64)
            self.latest_joint_positions = positions
            self.joint_state_received = True

    def _wait_for_joint_state(self, goal_handle: ServerGoalHandle):
        while rclpy.ok() and not self.joint_state_received:
            if goal_handle.is_cancel_requested:
                self.result_.success = False
                self.result_.message = 'Goal canceled before joint state was received.'
                goal_handle.canceled()
                return False
            self.rate.sleep()
        return rclpy.ok()

    def _pose_matches_solution(self, joint_cmd, pose_cmd):
        joint_cmd = np.asarray(joint_cmd, dtype=np.float64)
        if np.isnan(joint_cmd).any() or self.myArmUtil._check_joint_limits(joint_cmd):
            return False

        current_p, _ = self.myArmUtil.forward_kinematics(joint_cmd)
        position_error = np.linalg.norm(current_p - pose_cmd[:3])
        orientation_error = np.abs(pose_cmd[3] - joint_cmd[3])
        return position_error + orientation_error <= self.threshhold

    def _publish_led(self, rgb_values):
        led_cmd_msg = Float64MultiArray()
        led_cmd_msg.data = np.asarray(rgb_values, dtype=np.float64)
        self.led_pub_.publish(led_cmd_msg)

    def _clip_joint_command(self, joint_cmd):
        return np.clip(
            np.asarray(joint_cmd, dtype=np.float64),
            QArm.LIMITS_MIN[:4],
            QArm.LIMITS_MAX[:4],
        )

    def _get_current_phi(self):
        return np.asarray(self.latest_joint_positions[0:4], dtype=np.float64)


# Execution mode decision block
    def execute_cb(self, goal_handle: ServerGoalHandle):
        
        success = False
        reached = False

        goal = goal_handle.request
        pose_cmd = np.array(goal.task_space_pose, dtype=np.float64)

        if not self._wait_for_joint_state(goal_handle):
            return self.result_
        
        if goal.mode == MoveQArm.Goal.GOAL_TASK:
            return self.execute_goal_Task(goal_handle, pose_cmd)
        if goal.mode == MoveQArm.Goal.CONTINOUS_CONTROL:
            return self.Continous_Control_movement(goal_handle, pose_cmd)
        
        self.result_.success = False
        self.result_.message = f"Invalid mode: {goal.mode}"
        goal_handle.abort()
        return self.result_
    
#Goal_pose block based on IK
    def execute_goal_Task(self, goal_handle: ServerGoalHandle, pose_cmd):
        self.get_logger().info("Moving QArm to goal")
        success = False
        reached = False
        
        phi, phiOptimal = self.myArmUtil.inverse_kinematics(pose_cmd[:3], pose_cmd[3], self.latest_joint_positions[0:4])
        outsideLimit = not self._pose_matches_solution(phiOptimal, pose_cmd)
        if outsideLimit: # inv kin return [0,0,0,0] when the goal is outside of the joint limits
            success = False
            reached = True
            self.get_logger().warn(f"Goal pose {pose_cmd} is outside of joint limits")
            self._publish_led([1, 0, 0])
        else:
            joint_cmd_msg = Float64MultiArray()
            joint_cmd_msg.data = self._clip_joint_command(phiOptimal).tolist()
            self.joint_pub_.publish(joint_cmd_msg)

            self._publish_led([0, 1, 0])

        while not reached:
            if goal_handle.is_cancel_requested:
                self.result_.success = False
                self.result_.message = 'Goal canceled.'
                goal_handle.canceled()
                return self.result_
            if not rclpy.ok():
                break

            current_p, current_r = self.myArmUtil.forward_kinematics(self.latest_joint_positions[0:4])
            position_error_norm = np.linalg.norm(current_p - pose_cmd[:3])
            orientation_error = np.abs(pose_cmd[3]-self.latest_joint_positions[3])
            total_error = position_error_norm + orientation_error
            if total_error <= self.threshhold:
                reached = True
                success = True

            # Publish feedback
            self.feedback_.position_error_norm = position_error_norm
            self.feedback_.orientation_error = orientation_error
            goal_handle.publish_feedback(self.feedback_)

            self.rate .sleep()

        self.result_.success = success
        if success:
            self.result_.message = 'QArm has reached the target pose.'
            self.get_logger().info(f'{self.action_name_}: Succeeded')
            self._publish_led([0, 1, 0])
            goal_handle.succeed()
        else:
            self.result_.message = 'QArm failed to reached the target pose.'
            self.get_logger().info(f'{self.action_name_}: Failed')
            self._publish_led([1, 0, 0])
            goal_handle.abort()
        return self.result_
    
    def cancel_cb(self,goal_handle:ServerGoalHandle):

        self.get_logger().info('Received cancel request')
        self.get_logger().info('Moving arm to previous time step')
        joint_cmd_msg = Float64MultiArray()
        joint_cmd_msg.data = self.latest_joint_positions[:4]
        self.joint_pub_.publish(joint_cmd_msg)

        self._publish_led([1, 1, 0])

        return CancelResponse.ACCEPT

# Iterative control or movement based on Differential Kinematics - made by BP01234-X
# Version: 1.0 - Initial testing Implementation
    def Continous_Control_movement(self, goal_handle: ServerGoalHandle, pose_cmd):
        success = False
        reached = False
        self._publish_led([0, 0, 1])
        command_phi = self._clip_joint_command(self._get_current_phi())
        last_measured_phi = command_phi.copy()
        
        while rclpy.ok() and not reached:
            if goal_handle.is_cancel_requested:
                self.result_.success = False
                self.result_.message = 'Goal canceled.'
                self._publish_led([1, 1, 0])
                goal_handle.canceled()
                return self.result_

            measured_phi = self._clip_joint_command(self._get_current_phi())
            if np.linalg.norm(measured_phi - last_measured_phi) > self.feedback_sync_tolerance:
                command_phi = measured_phi.copy()
            last_measured_phi = measured_phi.copy()
            phi = command_phi.copy()
            
            current_p, current_r = self.myArmUtil.forward_kinematics(phi)
            position_error = pose_cmd[:3] - current_p
            orientation_error = pose_cmd[3] - phi[3]
            
            total_error = np.linalg.norm(position_error) + np.abs(orientation_error)
            if total_error <= self.threshhold:
                reached = True
                success = True
                break

            
            task_error = np.array([
                position_error[0],
                position_error[1],
                position_error[2],
                orientation_error
            ], dtype=np.float64)

            V = self.k_task * task_error
            
            # Compute joint velocity command using differential kinematics.
            # Support both HAL signatures: (J, c, r) and legacy (J, c, r, J_inv).
            dk_result = self.myArmUtil.differential_kinematics(phi)
            J, c, r = dk_result[0], dk_result[1], dk_result[2]
            
            near_singularity = (r == 4 and c > self.cond_treshold)
            hard_singularity = (r < 4)
            
            #Singularity Detector
            if near_singularity or hard_singularity:
                alpha = max (0.2, min(1.0, self.cond_treshold / max(c,1e-9)))
                V_eff = alpha * V
                if hard_singularity:
                    lam = self.lambda_max
                    self.get_logger().warn(f"Singularity detected! Applying damping. \n cond(J)={c:.3f}, lambda={lam:.3f}"  )
                else:
                    lam = self.lambda_max * (1 - self.cond_treshold/c)
                    self.get_logger().warn(f"Near singularity detected! Scaling down velocity. \n rank(J)={r}, cond(J)={c:.3f}" )
                I= np.eye(4)
                q_dot = J.T @ np.linalg.solve(J @ J.T + (lam**2) * I, V_eff)
            else:
                q_dot = np.linalg.lstsq(J, V, rcond=None)[0]

            if not np.isfinite(q_dot).all():
                self.get_logger().error('Continuous control produced a non-finite joint velocity command.')
                break
            
            q_next = self._clip_joint_command(phi + q_dot * self.dt)
            command_phi = q_next.copy()
            
            joint_cmd_msg = Float64MultiArray()
            joint_cmd_msg.data = q_next.tolist()
            self.joint_pub_.publish(joint_cmd_msg)
            self.rate.sleep()
            
        self.result_.success = success
        if success:
            self.result_.message = 'QArm has reached the target pose.'
            self.get_logger().info(f'{self.action_name_}: Succeeded')
            self._publish_led([0, 1, 0])
            goal_handle.succeed()
        else:
            self.result_.message = 'QArm failed to reached the target pose.'
            self.get_logger().info(f'{self.action_name_}: Failed')
            self._publish_led([1, 0, 0])
            goal_handle.abort()
        return self.result_




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
