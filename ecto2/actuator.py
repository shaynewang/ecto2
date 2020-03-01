#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from ecto2.ecto_serial import EctoSerial

def mapToOutputRange(x, x_min, x_max, y_min, y_max):
  """ Map values from x to y """
  if x > x_max or x < x_main:
    raise("not in range")
  return y_min + (x - x_min) * ((y_max - y_min)/(x_max - x_min))

class Actuator(Node):
  comm = {
          "steering": chr(1),
          "throttle": chr(2),
          } 

  def __init__(self):
    super().__init__(
            "Actuator", 
            automatically_declare_parameters_from_overrides=True,
    )
    # Initialize publiser and subscriber
    self.steering_sub = self.create_subscription(Int32, "ecto2/steering", self.steeringCallBack)
    self.throttle_sub = self.create_subscription(Int32, "ecto2/throttle", self.throttleCallBack)
    self.breaking_sub = self.create_subscription(Int32, "ecto2/breaking", self.breakingCallBack)

    self.serial = EctoSerial(port='/dev/ttyUSB0', baudrate=115200)

  def steeringCallBack(self, steering):
    print("Steering: " + str(steering))
    msg = [{self.comm["steering"]: steering.data}]
    self.serial.send(msg)
    
  def throttleCallBack(self, throttle):
    print("Throttle: " + str(throttle))
    msg = [{self.comm["throttle"]: throttle.data}]
    self.serial.send(msg)

  def breakingCallBack(self, breaking):
    print("Breaking: " + str(breaking))
    msg = [{self.comm["throttle"]: 0},
           {self.comm["steering"]: 0}]
    self.serial.send(msg)

def main(args=None):
  rclpy.init(args=args)
  actuator = Actuator()
  rclpy.spin(actuator)
  actuator.destory_node()
  rclpy.shutdown()

if __name__ == "__main__":
    main()
