#
# Created on 2/10/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
file(GLOB SOURCES "*.cc")
add_library(ddrl_util STATIC ${SOURCES})