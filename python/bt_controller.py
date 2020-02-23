#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
from actionlib_msgs.msg import GoalID

class BTController():
  def __init__(self):
    joy_sub = rospy.Subscriber("joy", Joy, self.joyCallback)
    self.steering_pub = rospy.Publisher('ecto2/steering', Float64, queue_size=1) 
    self.throttle_pub = rospy.Publisher('ecto2/throttle', Float64, queue_size=1) 
    self.breaking_pub = rospy.Publisher('ecto2/breaking', Float64, queue_size=1) 

  def joyCallback(self, joy_msg):
    steering_cmd = joy_msg.axes[rospy.get_param("~LEFT_JOY_LR")]
    self.steering_pub.publish(steering_cmd)
    throttle_cmd = joy_msg.axes[rospy.get_param("~LEFT_JOY_UD")]
    self.throttle_pub.publish(throttle_cmd)
    breaking_cmd= joy_msg.buttons[rospy.get_param("~B")]
    self.breaking_pub.publish(breaking_cmd)

def start():
  rospy.init_node('bt_controller')
  BTController()
  rospy.spin()

if __name__ == '__main__':
  start()
