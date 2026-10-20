from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch_ros.substitutions import FindPackageShare
from launch.actions import ExecuteProcess


def generate_launch_description():

    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='robot_a',
        description='Namespace for the robot'
    )
    
    record_arg = DeclareLaunchArgument(
        'record',
        default_value='false',
        description='Enable MCAP recording'
    )
    
    subscriber_reliability_arg = DeclareLaunchArgument(
        'subscriber_reliability',
        default_value='best_effort',
        description='QoS reliability for subscriber'
    )

    # получение значений аргументов
    namespace = LaunchConfiguration('namespace')
    record    = LaunchConfiguration('record')

    # ros2 run patrol pose_relay --ros-args -r pose:=/turtle1/pose -r __ns:=/robot_a
    pose_relay_node = Node(
        package='patrol',
        executable='pose_relay',
        namespace=namespace,
        remappings=[
            ('pose', '/turtle1/pose')
        ],
        output='screen'
    )

    # куда сохраняем
    bag_output_path = PathJoinSubstitution([
        FindPackageShare('course_bringup'),
        '..', '..',
        'evidence', 'pr05', 'bag'
    ])

    # ros2 bag record -s mcap -o /home/danya/ros2_ws/evidence/pr05/bag --topics /robot_a/sensor_pose
    recorder_process = ExecuteProcess(
        cmd=[
            'ros2', 'bag', 'record',
            '-s', 'mcap',
            '-o', bag_output_path,
            '--topics',
            PathJoinSubstitution(['/', namespace, 'sensor_pose'])
        ],
        condition=IfCondition(record),
        output='screen'
    )
    
    
    return LaunchDescription([
        namespace_arg,
        record_arg,
        subscriber_reliability_arg,
        pose_relay_node,
        recorder_process,
    ])