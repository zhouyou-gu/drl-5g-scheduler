#
# Created on 12/10/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
file(GLOB SOURCES "*.cc")
add_library(ops_async_agent STATIC ${SOURCES})
target_link_libraries(ops_async_agent ddrl_ops_async_scheduler)