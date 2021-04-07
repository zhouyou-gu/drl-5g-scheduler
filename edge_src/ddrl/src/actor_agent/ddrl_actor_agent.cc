//
// Created on 26/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include <google/protobuf/any.pb.h>

#include "ddrl_log.h"
#include "ddrl_actor_agent.h"

using namespace google;
using namespace protobuf;

static ddrl_log this_log("ddrl_actor_agent.log",true);

ddrl_actor_agent::ddrl_actor_agent(): device(torch::kCPU)
{
	std::lock_guard<std::mutex> lock(agent_mutex);
	actor_updating = std::make_shared<Net>();
	actor_running = std::make_shared<Net>();
	actor_ready = std::make_shared<Net>();

	actor_updating->to(device);
	actor_running->to(device);
	actor_ready->to(device);
	
	actor_updating->eval();
	actor_running->eval();
	actor_ready->eval();
	
	m_nn_config.Clear();
	torch::set_num_threads(1);
	
}


int ddrl_actor_agent::process_packet(uint8_t * buffer , int packet_size) {
	if(packet_size <= 0 )
		return -1;
	
	this_log.debug("ddrl_actor_agent get message\n");
	
	Any msg;
	msg.ParseFromArray(buffer,packet_size);
	if(msg.Is<ddrl::nn_config>()){
		ddrl::nn_config c;
		msg.UnpackTo(&c);
		process_nn_config(c);
	} else if (msg.Is<ddrl::update_model_weight>()){
		ddrl::update_model_weight c;
		msg.UnpackTo(&c);
		process_update_weight(c);
	}
	return 0;
}
bool ddrl_actor_agent::wait_for_setup(){
	this_log.debug("ddrl_actor_agent wait for setup\n");
	uint8_t tmp_buffer[MAX_BUF_SIZE];
	bzero(tmp_buffer, sizeof(uint8_t)*MAX_BUF_SIZE);

	while(!is_setup()){
		size_t  buflen = MAX_BUF_SIZE;
		bzero(tmp_buffer, sizeof(uint8_t)*MAX_BUF_SIZE);
		ssize_t n_recv = recv(socket_fd, tmp_buffer, MAX_BUF_SIZE, 0);
		if (n_recv <= 0) {
			controller_connected = false;
			this_log.error("Error: controller disconnected.\n");
			connect_controller();
			continue;
		}
		process_packet(tmp_buffer, n_recv);
	}
	return true;
}
bool ddrl_actor_agent::is_setup(){
	return is_nn_w_inited and is_nn_configed;
}

int ddrl_actor_agent::process_nn_config(ddrl::nn_config c){
	std::lock_guard<std::mutex> lock(agent_mutex);
	if (!is_nn_configed){
		actor_updating->init(c);
		actor_ready->init(c);
		actor_running->init(c);
		m_nn_config.CopyFrom(c);
	}
	is_nn_configed = true;
	return 0;
}

int ddrl_actor_agent::process_update_weight(ddrl::update_model_weight c){
	if(is_nn_configed){
		actor_updating->update_model_weight(c);
		n_node_updated += c.weight_size();
		if(n_node_updated >= (int) actor_updating->parameters().size()){
			is_nn_w_inited = true;
			n_node_updated = 0;
			update_net();
		}
		return  0;
	}
	else{
		this_log.error("Fatal Error:process_update_weight is not configured .\n");
		return  -1;
	}
}

int ddrl_actor_agent::update_net() {
	torch::NoGradGuard no_grad;
	for (size_t i = 0; i < actor_updating->parameters().size(); i++) {
		actor_ready->parameters()[i].copy_(actor_updating->parameters()[i]);
	}
	return swap_running_ready();
}

int ddrl_actor_agent::swap_running_ready() {
	std::lock_guard<std::mutex> lock(agent_mutex);
	std::shared_ptr<Net>  temp = nullptr;
	this_log.debug("ddrl_actor_agent::swap_running_ready\n");
	this_log.debug("ddrl_actor_agent::swap_running_ready BEFORE swap actor_running at %p\n", actor_running.get());
	this_log.debug("ddrl_actor_agent::swap_running_ready BEFORE swap actor_ready at %p\n", actor_ready.get());
	this_log.debug("ddrl_actor_agent::swap_running_ready BEFORE swap actor_updating at %p\n", actor_updating.get());
	
	temp = actor_running;
	actor_running = actor_ready;
	actor_ready = temp;
	
	this_log.debug("ddrl_actor_agent::swap_running_ready AFTER swap actor_running at %p\n", actor_running.get());
	this_log.debug("ddrl_actor_agent::swap_running_ready AFTER swap actor_ready at %p\n", actor_ready.get());
	this_log.debug("ddrl_actor_agent::swap_running_ready AFTER swap actor_updating at %p\n", actor_updating.get());
	return 0;
}
std::vector<float> ddrl_actor_agent::get_action(std::vector<float> state){
	std::lock_guard<std::mutex> lock(agent_mutex);
	torch::Tensor torchState = torch::tensor(state, torch::dtype(at::kFloat)).to(device);
	auto action = actor_running->forward(torchState);
	std::vector<float> v (action.data_ptr<float>(), action.data_ptr<float>() + action.numel());
	return v;
}

int ddrl_actor_agent::get_actor_input_dim(){
	std::lock_guard<std::mutex> lock(agent_mutex);
	if(m_nn_config.nn_arch_size() <= 0)
		return 0;
	
	return m_nn_config.nn_arch(0);
}

int ddrl_actor_agent::get_actor_output_dim(){
	std::lock_guard<std::mutex> lock(agent_mutex);
	if(m_nn_config.nn_arch_size() <= 0)
		return 0;
	
	return m_nn_config.nn_arch(m_nn_config.nn_arch_size()-1);
}
