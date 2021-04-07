#
# Created on 23/9/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
file(GLOB SOURCES "*.cc")
add_library(ddrl_actor_agent STATIC ${SOURCES})
