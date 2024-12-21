cmake_minimum_required(VERSION 3.5)
project(op3_gazebo)

find_package(ament_cmake_auto REQUIRED)
ament_auto_find_build_dependencies()

install(DIRECTORY config launch worlds  
	DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

ament_auto_package()

