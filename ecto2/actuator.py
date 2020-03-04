#!/usr/bin/env python

import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray
from ecto2.ecto_serial import EctoSerial

def mapToOutputRange(x, x_min, x_max, y_min, y_max):
  """ Map values from x to y """
  if x > x_max or x < x_main:
    raise("not in range")
  return y_min + (x - x_min) * ((y_max - y_min)/(x_max - x_min))

class Actuator(Node):
  comm = {
          "steering": 0,
          "throttle": 1,
          } 

  def __init__(self):
    super().__init__(
            "Actuator", 
            automatically_declare_parameters_from_overrides=True,
    )
    # Initialize publiser and subscriber
    self.steering_sub = self.create_subscription(Int32MultiArray, "ecto2/command", self.commandCallBack)
    self.breaking_sub = self.create_subscription(Int32, "ecto2/breaking", self.breakingCallBack)

    self.serial = EctoSerial(port='/dev/ttyUSB0', baudrate=115200)

  def commandCallBack(self, command):
    msg = (command.data[0], command.data[1])
    self.serial.send(msg)
    time.sleep(0.05)

  def breakingCallBack(self, breaking):
    msg = (0, 0)
    self.serial.send(msg)
    time.sleep(0.01)

def main(args=None):
  rclpy.init(args=args)
  actuator = Actuator()
  rclpy.spin(actuator)
  actuator.destory_node()
  rclpy.shutdown()

if __name__ == "__main__":
    main()
