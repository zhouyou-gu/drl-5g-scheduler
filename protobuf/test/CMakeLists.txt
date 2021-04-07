#
# Created on 20/9/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
include_directories(proto_c)
INCLUDE(FindProtobuf)
find_package(Protobuf REQUIRED)

add_executable(run_server run_server.cc)
target_link_libraries(run_server proto protobuf)

add_executable(run_client run_client.cc)
target_link_libraries(run_client proto protobuf)