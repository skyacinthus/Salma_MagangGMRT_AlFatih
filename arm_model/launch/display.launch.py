from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    package = FindPackageShare('arm_model')
    urdf_path = PathJoinSubstitution([package, 'urdf', 'arm.urdf'])
    rviz_config_path = PathJoinSubstitution([package, 'config', 'rviz_config.rviz'])

    # joint state publisher node
    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(Command(['cat', urdf_path]), value_type=str)
        }]
    )

    # rviz2 node
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path],
    )

    # add nodes
    node_list = [
        robot_state_publisher_node,
        rviz2_node,
    ]

    return LaunchDescription(node_list)