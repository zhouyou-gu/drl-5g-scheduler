#
# Created on 26/9/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
file(GLOB SOURCES "*.cc")
add_library(ddrl_scalar_agent STATIC ${SOURCES})