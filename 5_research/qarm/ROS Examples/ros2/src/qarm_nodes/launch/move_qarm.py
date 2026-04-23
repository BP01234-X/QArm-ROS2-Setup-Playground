# This is the launch file that starts up the basic QArm nodes for move arm action

from pathlib import Path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def _python_node_or_installed(
    workspace_script: Path,
    package: str,
    executable: str,
    node_name: str,
):
    """Prefer launching the source Python file directly inside this workspace."""

    if workspace_script.exists():
        return ExecuteProcess(
            cmd=[
                'python3',
                str(workspace_script),
                '--ros-args',
                '-r',
                f'__node:={node_name}',
            ],
            output='screen',
        )
    return Node(package=package, executable=executable, name=node_name)


def generate_launch_description():
    workspace_src_dir = Path.cwd() / 'src' / 'qarm_nodes' / 'qarm_nodes'
    workspace_bridge_dir = Path.cwd() / 'src' / 'qarm_nodes' / 'Experimentals_QArm' / 'codex-testing'
    if workspace_bridge_dir.exists():
        bridge_dir = workspace_bridge_dir
    else:
        package_share = Path(get_package_share_directory('qarm_nodes'))
        bridge_dir = package_share / 'Experimentals_QArm' / 'codex-testing'
    image_recorder_dir = bridge_dir / 'image-recorder'
    bridge_script = bridge_dir / 'bridge_commander.py'
    kinematics_monitor_script = bridge_dir / 'bridge_kinematics_monitor.py'
    camera_observer_script = bridge_dir / 'rgbd_subscriber.py'
    gripper_cycle_script = bridge_dir / 'gripper_cycle.py'
    image_recorder_script = image_recorder_dir / 'rolling_rgbd_recorder.py'

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
    enable_image_recorder = DeclareLaunchArgument(
        'enable_image_recorder',
        default_value='true',
        description='Run the rolling experimental RGBD image recorder under codex-testing/image-recorder.',
    )
    enable_kinematics_helper = DeclareLaunchArgument(
        'enable_kinematics_helper',
        default_value='true',
        description='Run the bridge-aware observer kinematics monitor that writes kinematics_status.json.',
    )
    image_recorder_max_bundles = DeclareLaunchArgument(
        'image_recorder_max_bundles',
        default_value='30',
        description='Maximum saved RGB/depth snapshot bundles kept by the experimental image recorder.',
    )
    image_recorder_save_period_sec = DeclareLaunchArgument(
        'image_recorder_save_period_sec',
        default_value='0.5',
        description='Seconds between saved RGB/depth snapshot bundles in the experimental image recorder.',
    )
    kinematics_top_candidates = DeclareLaunchArgument(
        'kinematics_top_candidates',
        default_value='8',
        description='How many top observer-pose candidates to keep in kinematics_status.json.',
    )
    kinematics_period_sec = DeclareLaunchArgument(
        'kinematics_period_sec',
        default_value='1.0',
        description='Seconds between bridge kinematics status refreshes.',
    )

    hardware = _python_node_or_installed(
        workspace_script=workspace_src_dir / 'qarm_hardware.py',
        package='qarm_nodes',
        executable='qarm_hardware',
        node_name='Hardware',
    )

    move_server = _python_node_or_installed(
        workspace_script=workspace_src_dir / 'move_qarm_server.py',
        package='qarm_nodes',
        executable='move_qarm_server',
        node_name='Move_Server',
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

    image_recorder = ExecuteProcess(
            cmd=[
                'python3',
                str(image_recorder_script),
                '--ros-args',
                '-p',
                f'output_dir:={image_recorder_dir}',
                '-p',
                ['max_bundles:=', LaunchConfiguration('image_recorder_max_bundles')],
                '-p',
                ['save_period_sec:=', LaunchConfiguration('image_recorder_save_period_sec')],
            ],
            output='screen',
            condition=IfCondition(LaunchConfiguration('enable_image_recorder'))
    )

    kinematics_helper = ExecuteProcess(
            cmd=[
                'python3',
                str(kinematics_monitor_script),
                '--bridge-dir',
                str(bridge_dir),
                '--config-dir',
                str(bridge_dir / 'chess-logic' / 'config'),
                '--output-file',
                str(bridge_dir / 'kinematics_status.json'),
                '--top',
                LaunchConfiguration('kinematics_top_candidates'),
                '--period-sec',
                LaunchConfiguration('kinematics_period_sec'),
                '--seed-source',
                'bridge',
            ],
            output='screen',
            condition=IfCondition(LaunchConfiguration('enable_kinematics_helper'))
    )

    realsense_camera_node = _python_node_or_installed(
        workspace_script=workspace_src_dir / 'rgbd.py',
        package='qarm_nodes',
        executable='rgbd',
        node_name='Camera',
    )

    
    return LaunchDescription(
        [
        enable_camera_observer,
        enable_gripper_cycle,
        enable_image_recorder,
        enable_kinematics_helper,
        image_recorder_max_bundles,
        image_recorder_save_period_sec,
        kinematics_top_candidates,
        kinematics_period_sec,
        hardware,
        realsense_camera_node,
        move_server,
        bridge_commander,
        camera_observer,
        gripper_cycle,
        image_recorder,
        kinematics_helper,
    ])
