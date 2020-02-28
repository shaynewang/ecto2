#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64

class BTController(Node):
  def __init__(self):
    super().__init__("BTController")
    self.steering_pub = self.create_publisher(Float64, 'ecto2/steering', 1) 
    self.throttle_pub = self.create_publisher(Float64, 'ecto2/throttle', 1) 
    self.breaking_pub = self.create_publisher(Float64, 'ecto2/breaking', 1) 
    self.joy_sub = self.create_subscription(Joy, "joy", self.joyCallback)

  def joyCallback(self, joy_msg):
    print(joy_msg)
    steering_cmd = joy_msg.axes[self.get_parameter("LEFT_JOY_LR").value]
    self.steering_pub.publish(steering_cmd)
    throttle_cmd = joy_msg.axes[self.get_parameter("LEFT_JOY_UD").value]
    self.throttle_pub.publish(throttle_cmd)
    breaking_cmd= joy_msg.buttons[self.get_parameter("B").value]
    self.breaking_pub.publish(breaking_cmd)

def main(args=None):
  rclpy.init(args=args)
  btcontroller = BTController()
  rclpy.spin(btcontroller)

if __name__ == '__main__':
  main()
