#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from adafruit_servokit import ServoKit
from std_msgs.msg import Float64

def mapToOutputRange(x, x_min, x_max, y_min, y_max):
  """ Map values from x to y """
  if x > x_max or x < x_main:
    raise("not in range")
  return y_min + (x - x_min) * ((y_max - y_min)/(x_max - x_min))

class Actuator(Node):
  def __init__(self):
    super().__init__("Actuator")
    print(self._parameters.keys())
    ppp = [parameter for parameter in self._parameters.values()]
    for p in ppp:
        print(p)
    control_num_channels = self.get_parameter("num_channels").value
    steering_servo_ch = self.get_parameter("steering_servo_ch").value
    esc_ch = self.get_parameter("esc_ch").value
    kit = ServoKit(channels=control_num_channels)
    self.steering_servo = kit.servo[steering_servo_ch]
    self.esc = kit.continuous_servo[esc_ch]
    self.steering_min = self.get_parameter("steering_min").value
    self.steering_max = self.get_parameter("steering_max").value
    self.steering_center = self.get_parameter("steering_center").value
    self.steering_sub = self.create_subscription(Float64, "ecto2/steering", self.steeringCallBack)
    self.throttle_sub = self.create_subscription(Float64, "ecto2/throttle", self.throttleCallBack)
    self.breaking_sub = self.create_subscription(Float64, "ecto2/breaking", self.breakingCallBack)

  def steeringCallBack(self, steering):
    if steering == 0.0:
      angle = self.steering_center
    else:
      angle = mapToOutputRange(steering, -1.0, 1.0, self.steering_min, self.steering_max)
    self.steering_servo.angle = angle
    pass
    
  def throttleCallBack(self, throttle):
    pass

  def breakingCallBack(self, breaking):
    pass

def main(args=None):
  rclpy.init(args=args)
  actuator = Actuator()
  rclpy.spin(actuator)
  actuator.destory_node()
  rclpy.shutdown()

if __name__ == "__main__":
    main()
