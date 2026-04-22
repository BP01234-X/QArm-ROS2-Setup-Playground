import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.executors import ExternalShutdownException
from rclpy.time import Time
from std_msgs.msg import Float64, Float64MultiArray
from sensor_msgs.msg import JointState
import numpy as np
from pal.products.qarm import QArm
from qarm_interfaces.msg import QArmDiagnostics

class QarmHardware(Node):
    def __init__(self):
        super().__init__('qarm_hardware')

		# Initialize QArm
        #self.myArm = QArm() NORMAL WAY TO CALL 1 QARM
        #TESTING FOR 2 QARMS CALL ON ROS2
        self.declare_parameter('device_id', 0)
        self.declare_parameter('hold_startup_pose', True)
        device_id = int(self.get_parameter('device_id').value)
        hold_startup_pose = bool(self.get_parameter('hold_startup_pose').value)
        self.myArm = QArm(deviceId=device_id)
        #END OF TESTING FOR 2 QARMS CALL ON ROS2

        self.last_cmd_time = self.get_clock().now()
        self.cmd_timeout_sec = 0.5

		# Initialize buffers
        self.joint_command = np.zeros(4, dtype=np.float64)
        #self.gripper_command = np.zeros(1, dtype=np.float64) Bug BY Quanser feeding an array instead of direct scalar.
        self.gripper_command = 0.1
        self.LED_command = np.zeros(3, dtype=np.float64)
        self.startup_pose_latched = False

        if self.myArm.status and hold_startup_pose:
            self.myArm.read_std()
            self.joint_command[:] = self.myArm.measJointPosition[:4]
            self.startup_pose_latched = True
            self.get_logger().info(
                f'Latched startup pose as hold command: {self.joint_command.tolist()}'
            )

        # QoS profile for publisher/subscriber
        qos_profile = QoSProfile(depth=10)

        # Publisher (state)
        self.joint_state_pub_ = self.create_publisher(
            msg_type = JointState, 
            topic = '/qarm/joint_states', 
            qos_profile = qos_profile
        )

        self.diag_pub_ = self.create_publisher(
            msg_type = QArmDiagnostics,
            topic = 'qarm/diagnostics',
            qos_profile = qos_profile
        )

        # Subscriber (commands) 
        self.joint_cmd_sub = self.create_subscription(
            Float64MultiArray,
            '/qarm/joint_position_cmd',
            self.joint_cmd_cb,
            qos_profile
        )

        self.gripper_cmd_sub = self.create_subscription(
            Float64,
            '/qarm/gripper_cmd',
            self.gripper_cmd_cb,
            qos_profile
        )

        self.led_cmd_sub = self.create_subscription(
            Float64MultiArray,
            '/qarm/led_cmd',
            self.led_cmd_cb,
            qos_profile
        )

        # Timer for 200 Hz control loop
        self.timer = self.create_timer(
            timer_period_sec=1/200.0, 
            callback = self.write_arm_and_pub_states
        )
    
    def joint_cmd_cb(self, msg: Float64MultiArray):
        if len(msg.data) >= 4:
            self.joint_command[:] = msg.data[:4]

    def gripper_cmd_cb(self, msg: Float64):
        self.gripper_command = float(msg.data)

    def led_cmd_cb(self, msg: Float64MultiArray):
        if len(msg.data) == 3:
            self.LED_command[:] = msg.data

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
        msg.name = ['YAW', 'SHOULDER', 'ELBOW', 'WRIST']
        msg.position = list(self.myArm.measJointPosition[:4])
        msg.velocity = list(self.myArm.measJointSpeed[:4])
        msg.effort = list(self.myArm.measJointCurrent[:4]) # TODO: estimation of joint force from current

        self.joint_state_pub_.publish(msg)

        diag_msg = QArmDiagnostics()
        diag_msg.joint_names = msg.name
        diag_msg.header.stamp = msg.header.stamp
        diag_msg.joint_currents = self.myArm.measJointCurrent
        diag_msg.joint_pwms = self.myArm.measJointPWM
        diag_msg.joint_temperatures = self.myArm.measJointTemperature

        self.diag_pub_.publish(diag_msg)
    
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
