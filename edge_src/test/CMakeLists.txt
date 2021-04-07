#
# Created on 2/09/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#
add_executable(test_nn_forward_latency test_nn_forward_latency.cc)
target_link_libraries(test_nn_forward_latency ${TORCH_LIBRARIES})