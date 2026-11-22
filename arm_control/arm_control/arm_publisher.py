import rclpy
from rclpy.node import Node 
from std_msgs.msg import Float64MultiArray

ARM_POSITION = [0.3, 0.4, 0.0]

PUBLISH_PERIOD = 0.1 

class ArmPublisher(Node):
    def __init__(self):
        super().__init__('arm_publisher')

        self.arm_pub = self.create_publisher(
            Float64MultiArray, 'arm_controller/commands', 10) 
        self.timer = self.create_timer(PUBLISH_PERIOD, self.publish_command)

    def publish_command(self):
        msg = Float64MultiArray()
        msg.data = ARM_POSITION
        self.arm_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ArmPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()