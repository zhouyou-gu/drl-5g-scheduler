//
// Created on 24/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include <google/protobuf/any.pb.h>

#include "transition.pb.h"

#include "ddrl_log.h"
#include "ddrl_agent_base.h"
#include "ddrl_actor_agent.h"
#include "ddrl_transition_agent.h"

using namespace google;
using namespace protobuf;

static ddrl_log this_log("test_agent.log",true);

int main() {
	ddrl_agent_base a;
	ddrl_actor_agent b;
	ddrl_transition_agent c;
	a.test_function();

	b.swap_running_ready();
	std::string agent_bind_addr = "127.0.1.100";
	int agent_port = 0;
	std::string controller_addr = "127.0.1.1";
	int controller_port = 4000;
	
	
	b.init(agent_bind_addr,agent_port,controller_addr,controller_port);
	c.init(agent_bind_addr,agent_port,controller_addr,controller_port+1);
	
	
	std::vector<float > s;
	s.push_back(2.5);
	s.push_back(4.6);
	

	
	auto * enb =  new ddrl::enb_transition;
	enb->set_tti(100);
	
	for (int j = 0; j < 5; ++j) {
		auto * ue =  enb->add_transition();
		ue->set_rnti(100*j);
		ue->set_id(100*j+1);
		
		ue->add_state(100*j+3);
		ue->add_state(100*j+4);
		
		
		ue->add_action(100*j+2);
		ue->add_next_state(100*j+3);
		ue->add_next_state(100*j+4);
		ue->set_reward(100*j+5);
	}
	while(true){
		usleep(1000);
		std::vector<float > a = b.get_action(s);
		printf("output:");
		for (int i = 0; i < (int)a.size(); i ++){
			printf("%f ",a.at(i));
		}
		printf("\n");
		enb->set_tti(TTICounter::get_current_dl_tti());
		TTICounter::step_dl_tti();
		c.step(*enb);
	}
	
}