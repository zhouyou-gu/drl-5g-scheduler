#
# Created on 14/10/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
file(GLOB SOURCES "*.cc")
add_library(ops_sync_agent STATIC ${SOURCES})
