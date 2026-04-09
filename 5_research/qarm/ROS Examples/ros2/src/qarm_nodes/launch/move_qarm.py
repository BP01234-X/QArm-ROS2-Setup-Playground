# This is the launch file that starts up the basic QArm nodes for move arm action

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():

    # Declare launch arguments with default values
    declare_args = [
        DeclareLaunchArgument('goal_pose', default_value='[0.45,0.0,0.5,0.0]'),
        DeclareLaunchArgument('mode', default_value='GOAL_TASK'),
        DeclareLaunchArgument('controller', default_value='action'),
        DeclareLaunchArgument('keyboard_mode', default_value='joint'),
    ]  # Default goal pose is [x, y, z, gripper_radians]

    action_controller = PythonExpression(["'", LaunchConfiguration('controller'), "' == 'action'"])
    keyboard_controller = PythonExpression(["'", LaunchConfiguration('controller'), "' == 'keyboard'"])

    hardware = Node(
            package='qarm_nodes',
            executable='qarm_hardware',
            name='Hardware'
        )
    
    move_server = Node(
            package='qarm_nodes',
            executable='move_qarm_server',
            name='Move_Server',
            condition=IfCondition(action_controller)
        )
    
    move_client = Node(
            package='qarm_nodes',
            executable='move_qarm_client',
            name='Move_Client',
            condition=IfCondition(action_controller),
            parameters=[{
                'goal_pose': LaunchConfiguration("goal_pose"),
                'mode': LaunchConfiguration("mode"),
            }]
        )

    keyboard_control = Node(
            package='qarm_nodes',
            executable='qarm_keyboard_control',
            name='Keyboard_Control',
            condition=IfCondition(keyboard_controller),
            parameters=[{
                'mode': LaunchConfiguration('keyboard_mode'),
            }]
        )
    realsense_camera_node = Node(
            package='qarm_nodes',
            executable='rgbd',
            name='Camera'
    )

    
    return LaunchDescription(
        declare_args+[
        hardware,
        realsense_camera_node,
        move_server,
        move_client,
        keyboard_control,
    ])
