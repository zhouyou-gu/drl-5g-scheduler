#
# Created on 18/9/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
file(GLOB SOURCES "*.cc")
add_library(ddrl_agent_base STATIC ${SOURCES})