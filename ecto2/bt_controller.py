#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
from std_msgs.msg import Int32

class BTController(Node):
  def __init__(self):
    super().__init__(
            "BTController",
            automatically_declare_parameters_from_overrides=True,
    )
    self.joy_sub = self.create_subscription(Joy, "joy", self.joyCallback, 1)
    self.steering_pub = self.create_publisher(Float64, 'ecto2/steering', 1) 
    self.throttle_pub = self.create_publisher(Float64, 'ecto2/throttle', 1) 
    self.breaking_pub = self.create_publisher(Float64, 'ecto2/breaking', 1) 

  def joyCallback(self, joy_msg):
    msg = Float64()
    button_msg = Int32()

    steering_cmd = joy_msg.axes[self.get_parameter("LEFT_JOY_LR").value]
    msg.data = steering_cmd
    self.get_logger().info('Publishing: "%s"' % msg.data)
    self.steering_pub.publish(msg)

    throttle_cmd = joy_msg.axes[self.get_parameter("LEFT_JOY_UD").value]
    msg.data = throttle_cmd
    self.get_logger().info('Publishing: "%s"' % msg.data)
    self.throttle_pub.publish(msg)

    breaking_cmd= joy_msg.buttons[self.get_parameter("B").value]
    button_msg.data = breaking_cmd
    self.get_logger().info('Publishing: "%s"' % msg.data)
    self.breaking_pub.publish(msg)

def main(args=None):
  rclpy.init(args=args)
  btcontroller = BTController()
  rclpy.spin(btcontroller)

if __name__ == '__main__':
  main()
