#
# Created on 20/9/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#

project(ddrl_proto)
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

#set the place of generated protobuf headers
set(PROTO_HEADER_INCLUDE_DIR ${PROJECT_BINARY_DIR}/src)
set(PROTO_HEADER_INCLUDE_DIR ${PROTO_HEADER_INCLUDE_DIR} PARENT_SCOPE)

#set the test dir for the python genereted files
set(PROTO_PY_DIR_TEST "${PROJECT_SOURCE_DIR}/test/proto_py" )
set(PROTO_LIB_DIR_TEST "${PROJECT_SOURCE_DIR}/test/proto_c" )
add_subdirectory(src)
add_subdirectory(test)
