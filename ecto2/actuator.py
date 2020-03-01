#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

def mapToOutputRange(x, x_min, x_max, y_min, y_max):
  """ Map values from x to y """
  if x > x_max or x < x_main:
    raise("not in range")
  return y_min + (x - x_min) * ((y_max - y_min)/(x_max - x_min))

class Actuator(Node):
  def __init__(self):
    super().__init__(
            "Actuator", 
            automatically_declare_parameters_from_overrides=True,
    )
    # Initialize publiser and subscriber
    self.steering_sub = self.create_subscription(Float64, "ecto2/steering", self.steeringCallBack)
    self.throttle_sub = self.create_subscription(Float64, "ecto2/throttle", self.throttleCallBack)
    self.breaking_sub = self.create_subscription(Float64, "ecto2/breaking", self.breakingCallBack)

  def steeringCallBack(self, steering):
    print("Steering: " + str(steering))
    
  def throttleCallBack(self, throttle):
    print("Throttle: " + str(throttle))

  def breakingCallBack(self, breaking):
    print("Breaking: " + str(breaking))

def main(args=None):
  rclpy.init(args=args)
  actuator = Actuator()
  rclpy.spin(actuator)
  actuator.destory_node()
  rclpy.shutdown()

if __name__ == "__main__":
    main()
