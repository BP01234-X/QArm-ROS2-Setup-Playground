cmake_minimum_required(VERSION 3.8)

project(qarm)

find_package(ament_cmake REQUIRED)

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}
		DESTINATION share/${PROJECT_NAME}
		OPTIONAL)
endforeach(dir)

ament_package()
