#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class GripperCycle(Node):
    def __init__(self) -> None:
        super().__init__('gripper_cycle')
        self.declare_parameter('close_value', 0.9)
        self.declare_parameter('open_value', 0.1)
        self.declare_parameter('delay_sec', 3.0)
        self.declare_parameter('topic', '/qarm/gripper_cmd')

        self.close_value = float(self.get_parameter('close_value').value)
        self.open_value = float(self.get_parameter('open_value').value)
        self.delay_sec = float(self.get_parameter('delay_sec').value)
        topic = str(self.get_parameter('topic').value)

        self.publisher = self.create_publisher(Float64, topic, 10)
        self.get_logger().info(
            f'Gripper cycle ready on {topic}: close={self.close_value}, '
            f'open={self.open_value}, delay={self.delay_sec}s'
        )

    def publish_value(self, value: float, label: str) -> None:
        msg = Float64()
        msg.data = float(value)
        self.publisher.publish(msg)
        self.get_logger().info(f'Published gripper {label}: {value:.3f}')

    def run_cycle(self) -> None:
        # Give discovery a moment before the first publish.
        time.sleep(0.5)
        self.publish_value(self.close_value, 'close')
        time.sleep(self.delay_sec)
        self.publish_value(self.open_value, 'open')


def main(args=None) -> None:
    node = None
    try:
        rclpy.init(args=args)
        node = GripperCycle()
        node.run_cycle()
        rclpy.spin_once(node, timeout_sec=0.2)
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
