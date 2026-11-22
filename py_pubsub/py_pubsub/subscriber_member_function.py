import rclpy
import numpy as np
import math
from rclpy.node import Node

from geometry_msgs.msg import Quaternion


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Quaternion,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        w = msg.w 
        x = msg.x
        y = msg.y
        z = msg.z
        norm = math.sqrt(w*w + x*x + y*y + z*z)
        w, x, y, z = w/norm, x/norm, y/norm, z/norm
        roll =  np.degrees(math.atan2(2*((w*x)+(y*z)), 1 - 2*((x*x) + (y*y))))
        pitch = np.degrees(math.asin(2*((w*y) - (z*x))))
        yaw = np.degrees(math.atan2(2*((w*z)+(x*y)), 1 - 2*((y*y) + (z*z))))
        self.get_logger().info(f"roll: {roll}, pitch: {pitch}, yaw: {yaw}")

        if abs(roll) > 45 or abs(pitch) > 45:
            action = "STOP (robot terlalu miring)"
        elif yaw > 10:
            action = "TURN LEFT (ccw)"
        elif yaw < -10:
            action = "TURN RIGHT (cw)"
        else:
            action = "MOVE FORWARD"
        self.get_logger().info(f"robot response: {action}")


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()