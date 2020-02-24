#!/usr/bin/env python

import rospy
from adafruit_servokit import ServoKit
from std_msgs.msg import Float64

def mapToOutputRange(x, x_min, x_max, y_min, y_max):
  """ Map values from x to y """
  if x > x_max or x < x_main:
    raise("not in range")
  return y_min + (x - x_min) * ((y_max - y_min)/(x_max - x_min))

class Actuator():
  def __init__(self):
    control_num_channels = get_param("/ecto2/pca9685/num_channels")
    steering_servo_ch = get_param("/ecto2/pca9685/steering_servo_ch")
    esc_ch = get_param("/ecto2/pca9685/esc_ch")
    kit = ServoKit(channels=control_num_channels)
    self.steering_servo = kit.servo[steering_servo_ch]
    self.esc = kit.continuous_servo[esc_ch]
    self.steering_min = get_param("/ecto2/pca9685/steering_min")
    self.steering_max = get_param("/ecto2/pca9685/steering_max")
    self.steering_center = get_param("/ecto2/pca9685/steering_center")
    self.steering_sub = rospy.Subscriber("ecto2/steering", Float64, self.steeringCallBack)
    self.throttle_sub = rospy.Subscriber("ecto2/throttle", Float64, self.throttleCallBack)
    self.breaking_sub = rospy.Subscriber("ecto2/breaking", Float64, self.breakingCallBack)

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

if __name__ == "__main__":
  rospy.init_node('actuator')
  Actuator()
  rospy.spin()
