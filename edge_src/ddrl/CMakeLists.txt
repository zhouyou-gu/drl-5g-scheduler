#
# Created on 12/9/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

project(ddrl_ext)

include_directories(
		${PROJECT_SOURCE_DIR}
		${CMAKE_SOURCE_DIR}
		${TORCH_INCLUDE_DIRS}
)

add_subdirectory(src)
add_subdirectory(test)