#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray

class BTController(Node):
  def __init__(self):
    super().__init__(
            "BTController",
            automatically_declare_parameters_from_overrides=True,
    )
    self.joy_sub = self.create_subscription(Joy, "joy", self.joyCallback, 1)

    self.command_pub = self.create_publisher(Int32MultiArray, 'ecto2/command', 1) 
    self.breaking_pub = self.create_publisher(Int32, 'ecto2/breaking', 1) 

  def joyCallback(self, joy_msg):
    com_data = [0, 0]
    button_msg = Int32()

    steering_cmd = joy_msg.axes[self.get_parameter("LEFT_JOY_LR").value]
    com_data[0] = int(100*(steering_cmd))

    lt_val = joy_msg.axes[self.get_parameter("LT").value]
    rt_val = joy_msg.axes[self.get_parameter("RT").value]
    com_data[1] = int(100*(lt_val - rt_val))
    msg = Int32MultiArray(data=com_data)
    self.command_pub.publish(msg)

    breaking_cmd= joy_msg.buttons[self.get_parameter("B").value]
    button_msg.data = breaking_cmd
    #self.get_logger().info('Publishing: "%s"' % msg.data)
    self.breaking_pub.publish(button_msg)

def main(args=None):
  rclpy.init(args=args)
  btcontroller = BTController()
  rclpy.spin(btcontroller)

if __name__ == '__main__':
  main()
