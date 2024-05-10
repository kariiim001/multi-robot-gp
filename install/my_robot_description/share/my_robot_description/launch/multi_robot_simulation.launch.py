import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    # Declare launch arguments for robot names
    robot1_name_arg = DeclareLaunchArgument(
        name='robot1_name',
        default_value=os.path.join(get_package_share_directory("my_robot_description"), "urdf", "robot_description.urdf.xacro"),
        description='robot 1'
    )

    robot2_name_arg = DeclareLaunchArgument(
        name='robot2_name',
        default_value=os.path.join(get_package_share_directory("my_robot_description"), "urdf", "robot_description2.urdf.xacro"),
        description='robot 2'
    )

    # Include the launch files for each robot with specified namespaces and parameters
    robot1_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory("my_robot_description"), "launch", "gazebo.launch.py")),
        launch_arguments={
            'namespace': 'robot1',
            'robot_description': LaunchConfiguration('robot1_name'),
            'tf_prefix': 'robot1'
        }.items(),
    )

    robot2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory("my_robot_description"), "launch", "gazebo2.launch.py")),
        launch_arguments={
            'namespace': 'robot2',
            'robot_description': LaunchConfiguration('robot2_name'),
            'tf_prefix': 'robot2'
        }.items(),
    )

    return LaunchDescription([
        robot1_name_arg,
        robot2_name_arg,
        robot1_launch,
        robot2_launch
    ])