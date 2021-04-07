#
# Created on 2/09/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#


cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(ddrl)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-comment -Wno-reorder -Wno-unused-but-set-variable -Wno-unused-variable -Wtype-limits -std=c++11")

#set the protobuf python files install directory
set(PROTO_PY_DIR "${PROJECT_SOURCE_DIR}/controller_src/proto_py" )
set(PROTO_LIB_DIR "${PROJECT_SOURCE_DIR}/edge_src/proto_c" )
add_subdirectory(protobuf)
message(PROTO_HEADER_INCLUDE_DIR: ${PROTO_HEADER_INCLUDE_DIR})
include_directories(${PROTO_HEADER_INCLUDE_DIR})
