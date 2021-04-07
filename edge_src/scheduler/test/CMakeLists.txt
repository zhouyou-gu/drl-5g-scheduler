#
# Created on 2/10/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
add_executable(				test_ops_scheduler test_ops_scheduler.cc)
target_link_libraries(		test_ops_scheduler ddrl_scalar_agent ddrl_actor_agent ddrl_nn ddrl_common srslte_common proto protobuf ${TORCH_LIBRARIES})