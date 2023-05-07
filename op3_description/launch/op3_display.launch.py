import os
from launch.conditions import UnlessCondition
import yaml

from ament_index_python import get_package_share_path
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

import launch
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
    launch_arguments = []

    def add_launch_arg(name: str, default_value=None, description=None):
        arg = DeclareLaunchArgument(name, default_value=default_value, description=description)
        launch_arguments.append(arg)

    model_path = os.path.join(get_package_share_path('op3_description'), 'urdf', 'robotis_op3.urdf.xacro')
    rviz_config = os.path.join(get_package_share_path('op3_description'), 'rviz', 'op3.rviz')

    add_launch_arg('rviz', rviz_config, 'rviz config')
    add_launch_arg('model', model_path, 'urdf path')
    add_launch_arg('gui', 'false', 'gui config')

    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]), value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        condition=UnlessCondition(LaunchConfiguration('gui'))
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', LaunchConfiguration('rviz')]
    )

    return launch.LaunchDescription(
        launch_arguments +
        [
            joint_state_publisher_node,
            robot_state_publisher_node,
            rviz_node
        ]
    )