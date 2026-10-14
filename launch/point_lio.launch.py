"""Evaluation-only Point-LIO launch. Sensor bridge and FAST-LIO are external."""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from go2_dds_ros2_bridge.tf_utils import flatten_rotation_matrix, lidar_pose_in_imu_frame


def _nodes(context):
    translation, rotation = lidar_pose_in_imu_frame()
    return [
        Node(
            package='tf2_ros', executable='static_transform_publisher',
            name='pointlio_origin_attachment', output='screen',
            arguments=['--x', '0', '--y', '0', '--z', '0', '--roll', '0', '--pitch', '0', '--yaw', '0',
                       '--frame-id', 'camera_init_correct', '--child-frame-id', 'pointlio_init'],
        ),
        Node(
            package='point_lio_unilidar', executable='pointlio_mapping',
            name='pointlio_mapping', output='screen',
            parameters=[LaunchConfiguration('config'), {
                'common.lid_topic': LaunchConfiguration('cloud_topic'),
                'common.imu_topic': LaunchConfiguration('imu_topic'),
                'mapping.extrinsic_est_en': False,
                'mapping.extrinsic_T': [float(v) for v in translation],
                'mapping.extrinsic_R': flatten_rotation_matrix(rotation),
                'pcd_save.pcd_save_en': False,
                'runtime_pos_log_enable': False,
            }],
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('config', default_value=PathJoinSubstitution([
            FindPackageShare('point_lio_unilidar'), 'config', 'go2_l2_ros2.yaml'])),
        DeclareLaunchArgument('cloud_topic', default_value='/utlidar/time_corrected/cloud'),
        DeclareLaunchArgument('imu_topic', default_value='/imu/data_fastlio'),
        OpaqueFunction(function=_nodes),
    ])
