from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _launch_setup(context, plain_urdf_path: Path, combined_urdf_path: Path):
    use_gripper = LaunchConfiguration('include_gripper').perform(context).lower() == 'true'
    selected_urdf_path = combined_urdf_path if use_gripper else plain_urdf_path
    robot_description = {
        'robot_description': selected_urdf_path.read_text(encoding='utf-8')
    }
    return [
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
            package='qarm_nodes',
            executable='rgbd',
            name='qarm_camera',
            output='screen',
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
        ),
    ]


def generate_launch_description():
    qarm_nodes_share = Path(get_package_share_directory('qarm_nodes'))
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
    include_gripper = DeclareLaunchArgument(
        'include_gripper',
        default_value='true',
        description='Use the combined QArm + gripper observer URDF.',
    )
    use_camera = DeclareLaunchArgument(
        'use_camera',
        default_value='true',
        description='Launch the QArm depth camera publisher.',
    )
    use_depth_point_cloud = DeclareLaunchArgument(
        'use_depth_point_cloud',
        default_value='true',
        description='Launch depth_image_proc XYZ point cloud generation.',
    )

    plain_urdf_path = qarm_share / 'urdf' / 'QARM.urdf'
    combined_urdf_path = qarm_nodes_share / 'urdf' / 'QARM_with_gripper.urdf'

    return LaunchDescription([
        use_joint_state_gui,
        use_hardware,
        device_id,
        include_gripper,
        use_camera,
        use_depth_point_cloud,
        OpaqueFunction(
            function=lambda context: _launch_setup(
                context,
                plain_urdf_path=plain_urdf_path,
                combined_urdf_path=combined_urdf_path,
            )
        ),
    ])
