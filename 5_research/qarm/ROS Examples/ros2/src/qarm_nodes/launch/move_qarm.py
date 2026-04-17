# This is the launch file that starts up the basic QArm nodes for move arm action

from pathlib import Path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    workspace_bridge_dir = Path.cwd() / 'src' / 'qarm_nodes' / 'Experimentals_QArm' / 'codex-testing'
    if workspace_bridge_dir.exists():
        bridge_dir = workspace_bridge_dir
    else:
        package_share = Path(get_package_share_directory('qarm_nodes'))
        bridge_dir = package_share / 'Experimentals_QArm' / 'codex-testing'
    bridge_script = bridge_dir / 'bridge_commander.py'
    camera_observer_script = bridge_dir / 'rgbd_subscriber.py'
    gripper_cycle_script = bridge_dir / 'gripper_cycle.py'

    enable_camera_observer = DeclareLaunchArgument(
        'enable_camera_observer',
        default_value='false',
        description='Run the experimental RGBD observer that writes camera_status.json.',
    )
    enable_gripper_cycle = DeclareLaunchArgument(
        'enable_gripper_cycle',
        default_value='false',
        description='Run the experimental gripper close/open cycle helper.',
    )

    hardware = Node(
            package='qarm_nodes',
            executable='qarm_hardware',
            name='Hardware'
        )
    
    move_server = Node(
            package='qarm_nodes',
            executable='move_qarm_server',
            name='Move_Server'
        )

    bridge_commander = ExecuteProcess(
            cmd=[
                'python3',
                str(bridge_script),
                '--ros-args',
                '-p',
                f'bridge_dir:={bridge_dir}',
            ],
            output='screen'
    )

    camera_observer = ExecuteProcess(
            cmd=[
                'python3',
                str(camera_observer_script),
                '--ros-args',
                '-p',
                f'output_dir:={bridge_dir}',
            ],
            output='screen',
            condition=IfCondition(LaunchConfiguration('enable_camera_observer'))
    )

    gripper_cycle = ExecuteProcess(
            cmd=[
                'python3',
                str(gripper_cycle_script),
            ],
            output='screen',
            condition=IfCondition(LaunchConfiguration('enable_gripper_cycle'))
    )

    realsense_camera_node = Node(
            package='qarm_nodes',
            executable='rgbd',
            name='Camera'
    )

    
    return LaunchDescription(
        [
        enable_camera_observer,
        enable_gripper_cycle,
        hardware,
        realsense_camera_node,
        move_server,
        bridge_commander,
        camera_observer,
        gripper_cycle,
    ])
