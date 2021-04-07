#
# Created on 13/11/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
file(GLOB SOURCES "*.cc")
add_library(ops_global_sync STATIC ${SOURCES})