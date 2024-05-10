import os
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    # Robot Names
    robot_names = ['robot1', 'robot2']  # Add more names for more robots

    launch_description = []

    # Declare robot model path
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(get_package_share_directory("my_robot_description"), "urdf", "robot_description.urdf.xacro"),
        description="Absolute path to robot URDF file"
    )
    launch_description.append(model_arg)

    env_var = SetEnvironmentVariable("GAZEBO_MODEL_PATH", os.path.join(get_package_prefix("my_robot_description"), "share"))
    launch_description.append(env_var)

    # Start Gazebo server and client
    start_gazebo_server = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gzserver.launch.py")))
    start_gazebo_client = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gzclient.launch.py")))
    launch_description.extend([start_gazebo_server, start_gazebo_client])

    for robot_name in robot_names:
        # Generate unique robot_description parameter
        robot_description = ParameterValue(Command(["xacro ", LaunchConfiguration("model")]), value_type=str)

        # Robot state publisher per robot
        robot_state_publisher = Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            namespace=robot_name,
            parameters=[{"robot_description": robot_description, "use_sim_time": True, "tf_prefix": robot_name}],
            output="screen"
        )
        launch_description.append(robot_state_publisher)

        # Spawn each robot at different locations
        spawn_robot = Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            arguments=["-entity", robot_name, "-topic", "robot_description", "-x", str(2 * robot_names.index(robot_name)), "-y", "0", "-z", "0"],
            output="screen"
        )
        launch_description.append(spawn_robot)

    # RViz2 node (common)
    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen"
    )
    launch_description.append(rviz2_node)

    return LaunchDescription(launch_description)
