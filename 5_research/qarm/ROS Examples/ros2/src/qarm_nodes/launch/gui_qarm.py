from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _python_node_or_installed(
    workspace_script: Path,
    package: str,
    executable: str,
    node_name: str,
    *,
    condition=None,
    parameters: list | None = None,
):
    """Prefer launching the source Python file directly inside this workspace."""

    if workspace_script.exists():
        cmd = [
            'python3',
            str(workspace_script),
            '--ros-args',
            '-r',
            f'__node:={node_name}',
        ]
        for parameter in parameters or []:
            for key, value in parameter.items():
                cmd.extend(['-p', f'{key}:={value}'])
        return ExecuteProcess(cmd=cmd, output='screen', condition=condition)

    return Node(
        package=package,
        executable=executable,
        name=node_name,
        output='screen',
        parameters=parameters,
        condition=condition,
    )


def _launch_setup(context, plain_urdf_path: Path):
    workspace_root = Path.cwd()
    workspace_src_dir = workspace_root / 'src' / 'qarm_nodes' / 'qarm_nodes'
    workspace_chess_logic_dir = (
        workspace_root
        / 'src'
        / 'qarm_nodes'
        / 'Experimentals_QArm'
        / 'codex-testing'
        / 'chess-logic'
    )
    package_share = Path(get_package_share_directory('qarm_nodes'))
    package_chess_logic_dir = package_share / 'Experimentals_QArm' / 'codex-testing' / 'chess-logic'
    chess_logic_dir = workspace_chess_logic_dir if workspace_chess_logic_dir.exists() else package_chess_logic_dir
    chess_debug_script = chess_logic_dir / 'chess_rviz_debug_node.py'
    marker_topic_value = LaunchConfiguration('chess_debug_marker_topic').perform(context).strip()
    fixed_frame_value = LaunchConfiguration('chess_debug_fixed_frame').perform(context).strip()
    color_topic_value = LaunchConfiguration('chess_debug_color_topic').perform(context).strip()
    depth_topic_value = LaunchConfiguration('chess_debug_depth_topic').perform(context).strip()
    observer_only_value = LaunchConfiguration('chess_debug_observer_only').perform(context).strip()
    device_id_value = LaunchConfiguration('device_id').perform(context).strip()
    robot_description = {
        'robot_description': plain_urdf_path.read_text(encoding='utf-8')
    }
    rviz_config = LaunchConfiguration('rviz_config').perform(context).strip()
    rviz_arguments = ['-d', rviz_config] if rviz_config else []
    chess_debug_process = ExecuteProcess(
        cmd=[
            'python3',
            str(chess_debug_script),
            '--ros-args',
            '-r',
            '__node:=chess_rviz_debug',
            '-p',
            f'marker_topic:={marker_topic_value}',
            '-p',
            f'fixed_frame:={fixed_frame_value}',
            '-p',
            f'color_topic:={color_topic_value}',
            '-p',
            f'depth_topic:={depth_topic_value}',
            '-p',
            f'observer_only:={observer_only_value}',
        ],
        output='screen',
        condition=IfCondition(LaunchConfiguration('enable_chess_debug_markers')),
    )
    return [
        _python_node_or_installed(
            workspace_script=workspace_src_dir / 'qarm_hardware.py',
            package='qarm_nodes',
            executable='qarm_hardware',
            node_name='qarm_hardware',
            parameters=[{'device_id': device_id_value}],
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
        _python_node_or_installed(
            workspace_script=workspace_src_dir / 'rgbd.py',
            package='qarm_nodes',
            executable='rgbd',
            node_name='qarm_camera',
            condition=IfCondition(LaunchConfiguration('use_camera')),
        ),
        Node(
            package='depth_image_proc',
            executable='point_cloud_xyz_node',
            name='depth_point_cloud_xyz',
            output='screen',
            remappings=[
                ('image_rect', '/camera/depth/image_rect_raw'),
                ('camera_info', '/camera/depth/camera_info'),
                ('points', '/camera/depth/points'),
            ],
            condition=IfCondition(LaunchConfiguration('use_depth_point_cloud')),
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=rviz_arguments,
        ),
        chess_debug_process,
    ]


def generate_launch_description():
    qarm_share = Path(get_package_share_directory('qarm'))

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
    use_camera = DeclareLaunchArgument(
        'use_camera',
        default_value='false',
        description='Launch the QArm depth camera publisher.',
    )
    use_depth_point_cloud = DeclareLaunchArgument(
        'use_depth_point_cloud',
        default_value='true',
        description='Launch depth_image_proc XYZ point cloud generation.',
    )
    enable_chess_debug_markers = DeclareLaunchArgument(
        'enable_chess_debug_markers',
        default_value='false',
        description='Launch Phase 4 chessboard debug MarkerArray publisher.',
    )
    chess_debug_marker_topic = DeclareLaunchArgument(
        'chess_debug_marker_topic',
        default_value='/chess/debug/markers',
        description='MarkerArray topic used by chess debug visualization.',
    )
    chess_debug_fixed_frame = DeclareLaunchArgument(
        'chess_debug_fixed_frame',
        default_value='world',
        description='Fixed frame for chess debug markers.',
    )
    chess_debug_color_topic = DeclareLaunchArgument(
        'chess_debug_color_topic',
        default_value='qarm_camera/color',
        description='RGB topic consumed by chess debug observer pipeline.',
    )
    chess_debug_depth_topic = DeclareLaunchArgument(
        'chess_debug_depth_topic',
        default_value='qarm_camera/depth',
        description='Depth topic consumed by chess debug observer pipeline.',
    )
    chess_debug_observer_only = DeclareLaunchArgument(
        'chess_debug_observer_only',
        default_value='false',
        description='If true, refresh markers only when status_file reports observer pose; otherwise update continuously.',
    )
    chess_debug_status_file = DeclareLaunchArgument(
        'chess_debug_status_file',
        default_value='',
        description='Optional status.json path for observer-only gating; empty falls back to chess-logic default.',
    )
    rviz_config = DeclareLaunchArgument(
        'rviz_config',
        default_value='/home/bp02-ubuntu/Documents/GitHub/QArm-ROS2-Setup-Playground/5_research/qarm/ROS Examples/ros2/bridge/QArm-gui-observer-config.rviz',
        description='Optional absolute path to an RViz2 .rviz config file.',
    )

    plain_urdf_path = qarm_share / 'urdf' / 'QARM.urdf'

    return LaunchDescription([
        use_joint_state_gui,
        use_hardware,
        device_id,
        use_camera,
        use_depth_point_cloud,
        enable_chess_debug_markers,
        chess_debug_marker_topic,
        chess_debug_fixed_frame,
        chess_debug_color_topic,
        chess_debug_depth_topic,
        chess_debug_observer_only,
        chess_debug_status_file,
        rviz_config,
        OpaqueFunction(
            function=lambda context: _launch_setup(
                context,
                plain_urdf_path=plain_urdf_path,
            )
        ),
    ])
