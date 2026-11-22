from launch import LaunchDescription 
from launch.substitutions import Command, PathJoinSubstitution 

from launch_ros.actions import Node 
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_share = FindPackageShare('arm_bringup')
    urdf = PathJoinSubstitution([
        FindPackageShare('arm_model'), 'urdf', 'arm.urdf'
    ])

    robot_description = Command(['xacro ', urdf])

    robot_state_publisher_node = Node(
        package= 'robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description}
        ],
    )

    controller_config = PathJoinSubstitution([pkg_share, 'config', 'arm_controllers.yaml'])
    ros2_control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        output='screen',
        parameters=[controller_config],
    )

    controller_spawner_node = Node(
        package='controller_manager',
        executable='spawner',
        name='controller_spawner',
        output='screen',
        arguments=[
            'joint_state_broadcaster',
            'arm_controller',
            '--param-file', controller_config,
        ],
    )

    rviz_config = PathJoinSubstitution([pkg_share, 'config', 'arm.rviz'])
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
    )

    node_list = [
        robot_state_publisher_node,
        ros2_control_node,
        controller_spawner_node,
        rviz2_node,
    ]

    return LaunchDescription(node_list)