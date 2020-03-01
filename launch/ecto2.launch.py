import os
import pathlib
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    parameters_file_path = str(pathlib.Path(__file__).parents[1])

    return LaunchDescription([
        Node(
            package='joy',
            node_executable='joy_node',
            node_name='joy_node',
            output="screen",
        ),
        Node(
            package='ecto2',
            node_executable='bt_controller',
            node_name='bt_controller',
            parameters=[
              parameters_file_path + "/ecto2/xboxOneJoy.yaml"
            ],
            output="screen",
        ),
        Node(
            package='ecto2',
            node_executable='actuator',
            node_name='actuator',
            parameters=[
            ],
            output="screen",
        ),
    ])
