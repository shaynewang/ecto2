cmake_minimum_required(VERSION 2.8.3)
project(ecto2)

find_package(catkin REQUIRED COMPONENTS message_generation rospy roscpp)
find_package(nodelet REQUIRED)
catkin_package()
