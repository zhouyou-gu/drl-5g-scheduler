//
// Created on 30/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include <google/protobuf/util/time_util.h>

#include "ddrl_log.h"
#include "ddrl_ops_async_scheduler.h"
#include "ops_global_sync.h"

static ddrl_log this_log("ddrl_ops_async_scheduler.log",true);

int ddrl_ops_async_scheduler::init(ops_agent * agent){
	printf("ddrl_ops_async_scheduler::init(ops_agent * agent)");
	m_agent = agent;
	this_log.debug("init ddrl_ops_async_scheduler\n");
	std::string controller_addr(getenv("DDRL_CONTROLLER_IP"));
	actor_agent = std::make_shared<ddrl_actor_agent>();
	transition_agent = std::make_shared<ddrl_transition_agent>();
	actor_agent->init(agent_bind_addr,agent_port,controller_addr,actor_updater_port);
	transition_agent->init(agent_bind_addr,agent_port,controller_addr,replay_memory_port);
	last_input = nullptr;
	last_state.clear();
	last_action.clear();
	last_n_ue = 0;
	
	running= true;
	start(THREAD_PRIO);
	
	return 0;
}


int ddrl_ops_async_scheduler::do_scheduling(){
	if(m_agent == NULL){
		return -1;
	}
	ops::ops_input input = m_agent->get_ops_input();
	
	int state_dim = actor_agent->get_actor_input_dim();
	
	std::vector<float> state(state_dim, 0.0);
	
	auto now  = TTICounter::get_now_timestamp();
	
	/// fill in hol
	for(int u = 0; u < input.ue_input_size() and u < state_dim / 2; u ++){
		const ops::ops_ue_input & ue = input.ue_input(u);
		state[u] = (get_ue_hol_pct(ue,now));
	}
	
	/// fill in channel information
	for(int u = 0; u < input.ue_input_size() and u < state_dim / 2; u ++){
		const ops::ops_ue_input & ue = input.ue_input(u);
		state[u + state_dim / 2] = (get_ue_alp_pct(ue));
	}
	
	/// Actor network forward
	std::vector<float> action = actor_agent->get_action(state);
	
	/// fill in output
	ops::ops_output output;
	output.set_tti(input.tti());
	for(int u = 0; u < input.ue_input_size() and u < action.size(); u ++){
		if((action.at(u) > 0 and state[u] >0) or state[u] >= 1.1){
			auto ue_out = output.add_ue_output();
			ue_out->set_rnti(input.ue_input(u).rnti());
			ue_out->set_tx(true);
		}
	}
	
	do_transition_reporting(input,state);
	
	update_output(output);
	
	update_last(input,state,action);
	
	return  0;
}

bool ddrl_ops_async_scheduler::need_transition_reporting(ops::ops_input& input){
	bool ret = false;
	if(last_input != nullptr){
		if(compare_ue_id(input,*last_input)){
			this_log.debug("need_transition_reporting\n");
			ret = true;
		}
	}
	if(not ret){
		last_state.clear();
		last_action.clear();
		last_input = nullptr;
		last_n_ue = 0;
	}
	return ret;
}


float ddrl_ops_async_scheduler::get_ue_hol_pct(const ops::ops_ue_input & ue_input, google::protobuf::Timestamp * now){
	if(ue_input.hts().seconds() >= 0 and ue_input.hts().nanos() >= 0){
		long hol = (now->seconds() - ue_input.hts().seconds()) * US_IN_S;
		hol += (int) ((now->nanos() - ue_input.hts().nanos()) / NS_IN_US);
		if(hol < 0)
			hol = 0;
		/// this number may be negative but it is right
		long time_to_tx = get_time_to_tx();
		if(hol > 0 and time_to_tx > 0){
			hol += time_to_tx - TX_DELAY_US/2;
//			float hol_f  = ((float) hol)/1000.0;
//			hol = floor(hol_f+0.999999)*1000;
		}
#ifdef SUBCARRIER_SPACING
		float us_per_slot = 1000.0 / (SUBCARRIER_SPACING/15000);
#else
        float us_per_slot = 1000.0;
#endif
		int hol_int = 0;
		if(hol>0){
            hol_int = ceil((hol)/us_per_slot)-1;
        }
		else{
            hol_int = 0;
        }

		float hol_pct = ((float) hol_int) / d_max_slot;
//		if(hol_pct > 1.1)
//			hol_pct = 1.1;
		this_log.debug("rnti:%x, hol:%ld, hol_pct:%f, time_to_tx:%ld\n",ue_input.rnti(),hol,hol_pct,time_to_tx);
		return hol_pct;
		
	}
	return 0.0;
}


float ddrl_ops_async_scheduler::get_ue_alp_pct(const ops::ops_ue_input&ue_input){
	return ue_input.alpha();
}

float ddrl_ops_async_scheduler::get_ue_reward(const ops::ops_ue_input & ue_input){
	if(last_input == nullptr){
		return 0.0;
	}
	int state_dim = actor_agent->get_actor_input_dim();
	for(int u = 0 ; u < last_input->ue_input_size() and u < state_dim / 2 ; u ++ ){
		if(last_input->ue_input(u).rnti() == ue_input.rnti()){
			const ops::ops_ue_input & ue_old = last_input->ue_input(u);
			if(ue_input.hts().seconds() != ue_old.hts().seconds() or
				ue_input.hts().nanos() != ue_old.hts().nanos()){
				float d_min_pct = d_min_slot / d_max_slot;
				if (last_state.at(u) <= 1.0 and last_state.at(u) >= d_min_pct){
					return 5.0;
				}
			}
		}
	}
	return 0.0;
}
int ddrl_ops_async_scheduler::update_last(ops::ops_input& input,std::vector<float>& state, std::vector<float>& action){
	last_state = state;
	last_action = action;
	
	last_input = std::make_shared<ops::ops_input>();
	last_input->CopyFrom(input);
	last_n_ue = last_input->ue_input_size();
	return 0;
}

int ddrl_ops_async_scheduler::do_transition_reporting(ops::ops_input& input, std::vector<float>& state){
	if( not need_transition_reporting(input)){
		return -1;
	}
	int state_dim = actor_agent->get_actor_input_dim();
	
	auto enb_transition = std::make_shared<ddrl::enb_transition>();
	enb_transition->set_tti(input.tti());
	for(int u = 0; u < state_dim / 2; u ++){
		/// add the ue transition
		auto ue_t = enb_transition->add_transition();
		ue_t->set_rnti(0);
		ue_t->set_id(u);
		
		ue_t->set_reward(0.0);
		
		ue_t->add_state(0.0);
		ue_t->add_state(0.0);
		
		ue_t->add_action(0.0);
		
		ue_t->add_next_state(0.0);
		ue_t->add_next_state(0.0);
	}
	
	
	for(int u = 0; u < input.ue_input_size() and u < state_dim / 2; u ++){
		/// add the ue transition and
		auto ue_t = enb_transition->mutable_transition(u);
		auto ue = input.ue_input(u);
		ue_t->set_rnti(input.ue_input(u).rnti());
		ue_t->set_id(u);
		
		ue_t->set_reward(get_ue_reward(ue));
		
		ue_t->set_state(0,last_state.at(u));
		ue_t->set_state(1,last_state.at(state_dim/2 + u));
		
		ue_t->set_action(0,last_action.at(u));
		
		ue_t->set_next_state(0,state.at(u));
		ue_t->set_next_state(1,state.at(state_dim/2 + u));
		this_log.debug("%s\n",ue_t->DebugString().c_str());
		
	}
	
	transition_agent->step(*enb_transition);
	return 0;
}