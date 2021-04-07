//
// Created on 30/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef DDRL_OPS_ASYNC_SCHEDULER_H
#define DDRL_OPS_ASYNC_SCHEDULER_H

#include "ops_async_scheduler.h"
#include "ddrl_actor_agent.h"
#include "ddrl_transition_agent.h"
#include "ddrl_scalar_agent.h"

class ddrl_ops_async_scheduler
: public ops_async_scheduler
{
public:
	int init(ops_agent* agent);
	static inline bool compare_ue_id(ops::ops_input& input_a, ops::ops_input& input_b){
		if(input_a.ue_input_size() != input_b.ue_input_size())
			return false;
		
		for(int u = 0 ; u < input_a.ue_input_size() ; u ++ ){
			if(input_a.ue_input(u).rnti() != input_b.ue_input(u).rnti()){
				return false;
			}
		}
		return true;
	}

protected:
	int do_scheduling();
	
	std::shared_ptr<ddrl_actor_agent> 	actor_agent;
	std::shared_ptr<ddrl_transition_agent> 	transition_agent;
	
	std::shared_ptr<ops::ops_input> last_input = nullptr;
	int last_n_ue = 0;
	
	std::vector<float> last_state;
	std::vector<float> last_action;
	
	const float d_max_slot = 6;
	const float d_min_slot = 5;
	
	
	bool need_transition_reporting(ops::ops_input& input);
	int do_transition_reporting(ops::ops_input& input, std::vector<float>& state);
	
	float get_ue_hol_pct(const ops::ops_ue_input& ue_input, google::protobuf::Timestamp * now);
	float get_ue_alp_pct(const ops::ops_ue_input& ue_input);
	float get_ue_reward(const ops::ops_ue_input& ue_input);
	
	int update_last(ops::ops_input& input,std::vector<float>& state, std::vector<float>& action);
	
	std::string agent_bind_addr = "0.0.0.0";
	int agent_port = 0;
	int actor_updater_port = 4000;
	int replay_memory_port = 4001;
	
};

#endif //DDRL_OPS_ASYNC_SCHEDULER_H
