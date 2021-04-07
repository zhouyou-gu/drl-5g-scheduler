#
# Created on 18/9/19.
# Author: Zhouyou Gu <guzhouyou@gmail.com>.
#

add_executable(				test_logging test_logging.cc)
target_link_libraries(		test_logging ddrl_util ddrl_agent_base srslte_common)

add_executable(				test_torch test_torch.cc)
target_link_libraries(		test_torch ddrl_nn ddrl_util ddrl_agent_base ddrl_actor_agent srslte_common protobuf ${TORCH_LIBRARIES})

add_executable(				test_proto test_proto.cc)
target_link_libraries(		test_proto ddrl_nn ddrl_util ddrl_agent_base ddrl_actor_agent srslte_common protobuf  ${TORCH_LIBRARIES})

add_executable(				test_agent test_agent.cc)
target_link_libraries(		test_agent ddrl_actor_agent ddrl_nn ddrl_util ddrl_agent_base  srslte_common protobuf  ${TORCH_LIBRARIES})

add_executable(				test_scalar_agent test_scalar_agent.cc)
target_link_libraries(		test_scalar_agent ddrl_scalar_agent ddrl_actor_agent ddrl_nn ddrl_util ddrl_agent_base srslte_common protobuf  ${TORCH_LIBRARIES})

add_executable(				test_any_message_delimitation test_any_message_delimitation.cc)
target_link_libraries(		test_any_message_delimitation)

