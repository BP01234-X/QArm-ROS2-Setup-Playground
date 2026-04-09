import os
import sys

import numpy as np
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64, Float64MultiArray

lib_repo = os.environ.get('LIB_REPO')
if lib_repo:
    preferred_python = os.path.join(lib_repo, '0_libraries', 'python')
    if os.path.isdir(preferred_python) and preferred_python not in sys.path:
        sys.path.insert(0, preferred_python)

from pal.products.qarm import QArm
from qarm_interfaces.msg import QArmDiagnostics

JOINT_STATES_TOPIC = '/qarm/joint_states'
DIAGNOSTICS_TOPIC = '/qarm/diagnostics'
JOINT_POSITION_CMD_TOPIC = '/qarm/joint_position_cmd'
GRIPPER_CMD_TOPIC = '/qarm/gripper_cmd'
LED_CMD_TOPIC = '/qarm/led_cmd'

class QarmHardware(Node):
    def __init__(self):
        super().__init__('qarm_hardware')

        # Initialize QArm
        self.myArm = QArm(readMode=1, frequency=200)
        self.get_logger().info(f'Using QArm library: {QArm.__module__} ({sys.modules[QArm.__module__].__file__})')

        self.last_cmd_time = self.get_clock().now()
        self.cmd_timeout_sec = 0.5

        # Initialize buffers
        self.joint_command = np.zeros(4, dtype=np.float64)
        #self.gripper_command = np.zeros(1, dtype=np.float64) Bug BY Quanser feeding an array instead of direct scalar.
        self.gripper_command = 0.1
        self.LED_command = np.zeros(3, dtype=np.float64)
        self.state_publish_count = 0
        self.last_logged_joint_command = None

        # QoS profile for publisher/subscriber
        qos_profile = QoSProfile(depth=10)

        # Publisher (state)
        self.joint_state_pub_ = self.create_publisher(
            msg_type = JointState, 
            topic = JOINT_STATES_TOPIC, 
            qos_profile = qos_profile
        )

        self.diag_pub_ = self.create_publisher(
            msg_type = QArmDiagnostics,
            topic = DIAGNOSTICS_TOPIC,
            qos_profile = qos_profile
        )

        # Subscriber (commands) 
        self.joint_cmd_sub = self.create_subscription(
            Float64MultiArray,
            JOINT_POSITION_CMD_TOPIC,
            self.joint_cmd_cb,
            qos_profile
        )

        self.gripper_cmd_sub = self.create_subscription(
            Float64,
            GRIPPER_CMD_TOPIC,
            self.gripper_cmd_cb,
            qos_profile
        )

        self.led_cmd_sub = self.create_subscription(
            Float64MultiArray,
            LED_CMD_TOPIC,
            self.led_cmd_cb,
            qos_profile
        )

        # Timer for 200 Hz control loop
        self.timer = self.create_timer(
            timer_period_sec=1/200.0, 
            callback = self.write_arm_and_pub_states
        )

        if self.myArm.status:
            self.myArm.read_write_std(
                phiCMD=self.joint_command,
                gprCMD=float(self.gripper_command),
                baseLED=self.LED_command,
            )
            self.get_logger().info(
                f'Initial joint state: {np.asarray(self.myArm.measJointPosition).tolist()}'
            )
    
    def joint_cmd_cb(self, msg: Float64MultiArray):
        if len(msg.data) >= 4:
            self.joint_command[:] = msg.data[:4]
            self.last_cmd_time = self.get_clock().now()
            if self.last_logged_joint_command is None or not np.allclose(
                self.joint_command,
                self.last_logged_joint_command,
                atol=1e-6,
            ):
                self.get_logger().info(f'Received joint command: {self.joint_command.tolist()}')
                self.last_logged_joint_command = self.joint_command.copy()

    def gripper_cmd_cb(self, msg: Float64):
        self.gripper_command = float(msg.data)
        self.last_cmd_time = self.get_clock().now()

    def led_cmd_cb(self, msg: Float64MultiArray):
        if len(msg.data) == 3:
            self.LED_command[:] = msg.data
            self.last_cmd_time = self.get_clock().now()

    def write_arm_and_pub_states(self):
        if not self.myArm.status:
            self.get_logger().error('QArm not initialized properly.')
            return
        # Write them to the arm
        self.myArm.read_write_std(
            phiCMD=self.joint_command, 
            gprCMD=float(self.gripper_command),  #Fix for bug BY Quanser 
            baseLED=self.LED_command)
        
        # ---- Publish joint state ----
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = [
            'base_joint',
            'shoulder_joint',
            'arm_joint',
            'wrist_joint',
            'gripper_joint'
        ]

        msg.position = list(self.myArm.measJointPosition)
        msg.velocity = list(self.myArm.measJointSpeed)
        msg.effort = list(self.myArm.measJointCurrent) # TODO: estimation of joint force from current

        self.joint_state_pub_.publish(msg)

        diag_msg = QArmDiagnostics()
        diag_msg.joint_names = msg.name
        diag_msg.header.stamp = msg.header.stamp
        diag_msg.joint_currents = list(self.myArm.measJointCurrent)
        diag_msg.joint_pwms = list(self.myArm.measJointPWM)
        diag_msg.joint_temperatures = list(self.myArm.measJointTemperature)

        self.diag_pub_.publish(diag_msg)
        self.state_publish_count += 1
        if self.state_publish_count == 1:
            self.get_logger().info(
                f'Published first joint state: position={msg.position}, velocity={msg.velocity}, effort={msg.effort}'
            )
    
    def destroy_node(self):
        self.myArm.terminate()
        super().destroy_node()

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = QarmHardware()
            rclpy.spin(node)

    except (KeyboardInterrupt,ExternalShutdownException):
            pass

    finally:        
        node.destroy_node()

if __name__ == '__main__':
    main()
