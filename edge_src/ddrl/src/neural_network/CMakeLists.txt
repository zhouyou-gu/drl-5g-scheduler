#
# Created on 24/9/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
file(GLOB SOURCES "*.cc")
add_library(ddrl_nn STATIC ${SOURCES})