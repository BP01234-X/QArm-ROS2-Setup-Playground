from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    qarm_share = Path(get_package_share_directory('qarm'))
    urdf_path = qarm_share / 'urdf' / 'QARM.urdf'

    robot_description = {
        'robot_description': urdf_path.read_text(encoding='utf-8')
    }

    use_joint_state_gui = DeclareLaunchArgument(
        'use_joint_state_gui',
        default_value='false',
        description='Launch joint_state_publisher_gui for manual RViz control.',
    )
    use_hardware = DeclareLaunchArgument(
        'use_hardware',
        default_value='false',
        description='Launch qarm_hardware and mirror the real arm into RViz TF.',
    )
    device_id = DeclareLaunchArgument(
        'device_id',
        default_value='0',
        description='QArm device ID for qarm_hardware.',
    )

    return LaunchDescription([
        use_joint_state_gui,
        use_hardware,
        device_id,
        Node(
            package='qarm_nodes',
            executable='qarm_hardware',
            name='qarm_hardware',
            output='screen',
            parameters=[{'device_id': LaunchConfiguration('device_id')}],
            condition=IfCondition(LaunchConfiguration('use_hardware')),
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[robot_description],
            remappings=[('joint_states', '/qarm/joint_states')],
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
            parameters=[robot_description],
            remappings=[('joint_states', '/qarm/joint_states')],
            condition=IfCondition(LaunchConfiguration('use_joint_state_gui')),
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
        )
    ])
