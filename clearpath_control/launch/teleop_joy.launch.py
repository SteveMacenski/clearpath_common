from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    lc = LaunchContext()
    ld = LaunchDescription()

    # Launch Arguments
    arg_platform_model = DeclareLaunchArgument(
        'platform_model',
        choices=['a200', 'j100'],
        default_value='a200'
    )

    arg_joy_type = DeclareLaunchArgument(
        'joy_type',
        choices=['logitech', 'ps4'],
        default_value='ps4'
    )

    # Launch Configurations
    platform_model = LaunchConfiguration('platform_model')
    joy_type = EnvironmentVariable('CPR_JOY_TYPE', default_value='ps4')

    # Packages
    pkg_clearpath_control = FindPackageShare('clearpath_control')

    # Paths
    dir_robot_config = PathJoinSubstitution([
        pkg_clearpath_control, 'config', platform_model])
    
    file_config_joy = 'teleop_' + joy_type.perform(lc) + '.yaml'

    filepath_config_joy = PathJoinSubstitution([
        dir_robot_config,
        file_config_joy]
    )

    node_joy = Node(
        namespace='joy_teleop',
        package='joy_linux',
        executable='joy_linux_node',
        output='screen',
        name='joy_node',
        parameters=[filepath_config_joy]
    )

    node_teleop_twist_joy = Node(
        namespace='joy_teleop',
        package='teleop_twist_joy',
        executable='teleop_node',
        output='screen',
        name='teleop_twist_joy_node',
        parameters=[filepath_config_joy]
    )


    ld.add_action(arg_platform_model)
    ld.add_action(arg_joy_type)
    ld.add_action(node_joy)
    ld.add_action(node_teleop_twist_joy)
    return ld
