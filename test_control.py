import rospy
from sensor_msgs.msg import Joy
from actionlib_msgs.msg import GoalID

def callback(data):
  print(data)

def start():
  global pub
  pub = rospy.Publisher('ecto2/controller', GoalID)
  rospy.Subscriber("joy", Joy, callback)
  rospy.init_node('Ecto2')
  rospy.spin()

if __name__ == '__main__':
  start()
