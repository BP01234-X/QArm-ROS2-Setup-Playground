import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import ExternalShutdownException
from cv_bridge import CvBridge
from sensor_msgs.msg import CameraInfo, Image

from pal.products.qarm import QArmRealSense

class QArmCamera(Node):
    def __init__(self):
        super().__init__('qarm_camera')
        
        # Declare camera parameters
        self.declare_parameter('color_width', 640)
        self.declare_parameter('color_height', 480)
        self.declare_parameter('depth_width', 640)
        self.declare_parameter('depth_height', 480)
        self.declare_parameter('fps', 30.0)
        self.declare_parameter('depth_fx', 592.451)
        self.declare_parameter('depth_fy', 592.451)
        self.declare_parameter('depth_ppx', 318.592)
        self.declare_parameter('depth_ppy', 249.341)

        # Set up camera
        self.color_width = self.get_parameter('color_width').get_parameter_value().integer_value
        self.color_height = self.get_parameter('color_height').get_parameter_value().integer_value
        self.depth_width = self.get_parameter('depth_width').get_parameter_value().integer_value
        self.depth_height = self.get_parameter('depth_height').get_parameter_value().integer_value
        self.fps = self.get_parameter('fps').get_parameter_value().double_value
        self.depth_fx = self.get_parameter('depth_fx').get_parameter_value().double_value
        self.depth_fy = self.get_parameter('depth_fy').get_parameter_value().double_value
        self.depth_ppx = self.get_parameter('depth_ppx').get_parameter_value().double_value
        self.depth_ppy = self.get_parameter('depth_ppy').get_parameter_value().double_value
        self.camera = QArmRealSense(            
            hardware = 1,
            mode='RGB&DEPTH',
            frameWidthRGB=self.color_width,
            frameHeightRGB=self.color_height,
            frameRateRGB=self.fps,
            frameWidthDepth=self.depth_width,
            frameHeightDepth=self.depth_height,
            frameRateDepth=self.fps,
            )
        
        self.bridge = CvBridge()
        qos = QoSProfile(depth=10)
        
        # Publishers
        self.color_pub = self.create_publisher(Image, 'qarm_camera/color', qos)
        self.depth_pub = self.create_publisher(Image, 'qarm_camera/depth', qos)
        self.depth_rect_pub = self.create_publisher(Image, '/camera/depth/image_rect_raw', qos)
        self.depth_info_pub = self.create_publisher(CameraInfo, '/camera/depth/camera_info', qos)

        # Timer
        period = 1.0 / self.fps
        self.timer = self.create_timer(
            period, 
            self.camera_publish_cb, 
            callback_group=ReentrantCallbackGroup())
        
        self.get_logger().info("RGBD camera initialized")

    def _make_depth_camera_info(self, stamp):
        msg = CameraInfo()
        msg.header.stamp = stamp
        msg.header.frame_id = 'left_ir_optical_frame'
        msg.width = self.depth_width
        msg.height = self.depth_height
        # First-pass rectified depth intrinsics provided by user.
        msg.distortion_model = 'plumb_bob'
        msg.d = [0.0, 0.0, 0.0, 0.0, 0.0]
        msg.k = [
            self.depth_fx, 0.0, self.depth_ppx,
            0.0, self.depth_fy, self.depth_ppy,
            0.0, 0.0, 1.0,
        ]
        msg.r = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
        ]
        msg.p = [
            self.depth_fx, 0.0, self.depth_ppx, 0.0,
            0.0, self.depth_fy, self.depth_ppy, 0.0,
            0.0, 0.0, 1.0, 0.0,
        ]
        return msg

    def camera_publish_cb(self):
        new = self.camera.read_RGB()
        if new == -1:
            self.get_logger().warn("Failed to capture color frame")
            return
        new = self.camera.read_depth(dataMode='M')
        if new == -1:
            self.get_logger().warn("Failed to capture depth frame")
            return
        stamp = self.get_clock().now().to_msg()
        color_msg = self.bridge.cv2_to_imgmsg(self.camera.imageBufferRGB,"bgr8")
        color_msg.header.stamp = stamp
        color_msg.header.frame_id = 'camera_color'
        self.color_pub.publish(color_msg)
        depth_msg = self.bridge.cv2_to_imgmsg(self.camera.imageBufferDepthM,'32FC1')
        depth_msg.header.stamp = stamp
        depth_msg.header.frame_id = 'left_ir_optical_frame'
        self.depth_pub.publish(depth_msg)
        self.depth_rect_pub.publish(depth_msg)
        self.depth_info_pub.publish(self._make_depth_camera_info(stamp))
    
    def destroy_node(self):
        self.camera.terminate()
        super().destroy_node()

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = QArmCamera()
            rclpy.spin(node)

    except (KeyboardInterrupt,ExternalShutdownException):
        pass

    finally:
        node.destroy_node()
        
if __name__ == '__main__':
    main()
