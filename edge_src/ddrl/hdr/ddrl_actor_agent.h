//
// Created on 23/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef DDRL_ACTOR_AGENT_H
#define DDRL_ACTOR_AGENT_H
#include "nn_config.pb.h"
#include "update_weight.pb.h"
#include "transition.pb.h"

#include "ddrl_util.h"
#include "ddrl_agent_base.h"
#include "ddrl_nn.h"

class ddrl_actor_agent
	: public ddrl_agent_base{
public:
	ddrl_actor_agent();
	int process_packet(uint8_t * buffer , int packet_size);
	bool wait_for_setup();
	bool is_setup();
	int process_nn_config(ddrl::nn_config c);
	int process_update_weight(ddrl::update_model_weight c);
	int update_net();
	
	int swap_running_ready();
	
	std::vector<float> get_action(std::vector<float> state);
	
	int get_actor_input_dim();
	int get_actor_output_dim();

protected:
	torch::Device device;
	
	bool is_nn_configed = false;
	bool is_nn_w_inited = false;
	
	int n_node_updated = 0;
	
	ddrl::nn_config m_nn_config;
	
	std::shared_ptr<Net> actor_running;
	std::shared_ptr<Net> actor_ready;
	std::shared_ptr<Net> actor_updating;
	
};
#endif //DDRL_ACTOR_AGENT_H
