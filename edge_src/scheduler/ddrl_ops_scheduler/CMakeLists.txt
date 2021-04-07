#
# Created on 2/10/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
file(GLOB HEADERS "*.h")
file(GLOB SOURCES "*.cc")
add_library(ddrl_ops_scheduler STATIC ${SOURCES})
target_link_libraries(ddrl_ops_scheduler ddrl_actor_agent ddrl_scalar_agent ddrl_agent_base ddrl_nn ${TORCH_LIBRARIES})
