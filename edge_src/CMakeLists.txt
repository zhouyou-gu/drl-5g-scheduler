#
# Created on 2/09/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(edge)
option(BUILD_DDRL    "Build DDRL in srsLTE"                  ON)

if(BUILD_DDRL)
	message(STATUS "Building with DDRL")
	add_definitions(-DENABLE_DDRL)

	set(TORCH_DIR "${PROJECT_SOURCE_DIR}/libtorch/share/cmake/Torch" )
	find_package(${TORCH_DIR}/Torch REQUIRED)
	message(TORCH_LIBRARIES: ${TORCH_LIBRARIES})
	message(TORCH_INCLUDE_DIRS: ${TORCH_INCLUDE_DIRS})
	include_directories(${TORCH_INCLUDE_DIRS})
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

	include(FindProtobuf)
	find_package(Protobuf REQUIRED)

	if (TARGET proto)
		message(proto is defined)
		link_libraries(proto)
	else(TARGET proto)
		message("proto not is defined, find proto in ./proto_c")
		find_library(DDRL_PROTO
				NAMES libproto.a
				HINTS ${PROJECT_SOURCE_DIR}/proto_c)
		link_libraries(${DDRL_PROTO})
		include_directories(proto_c)
	endif()
	include_directories(ddrl/hdr)
	include_directories(ops/hdr)
	include_directories(scheduler)
	include_directories(${PROJECT_BINARY_DIR}/srsLTE/lib/include)
	include_directories(${PROJECT_SOURCE_DIR}/srsLTE/lib/include)

	include_directories(srsLTE_extension/hdr)
	file(GLOB_RECURSE SRSLTE_EXT_SOURCE ${PROJECT_SOURCE_DIR}/srsLTE_extension/srslte_ext/*.cc)
	file(GLOB_RECURSE SRSENB_EXT_SOURCE ${PROJECT_SOURCE_DIR}/srsLTE_extension/srsenb_ext/*.cc)

	add_subdirectory(ddrl)
	add_subdirectory(ops)
	add_subdirectory(scheduler)
	add_subdirectory(test)
	link_libraries(ddrl_util protobuf ops_global_sync)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-comment -Wno-reorder -Wno-unused-but-set-variable -Wno-unused-variable -Wtype-limits -std=c++11")

else(BUILD_DDRL)
	message(STATUS "DDRL build disabled")
endif(BUILD_DDRL)



add_subdirectory(srsLTE)