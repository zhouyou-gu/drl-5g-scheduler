#
# Created on 12/10/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
file(GLOB SOURCES "*.cc")
add_library(ops_async_scheduler STATIC ${SOURCES})