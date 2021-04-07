//
// Created on 1/10/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "hdr/ddrl_ops_scheduler.h"

int main(){
	ddrl_ops_scheduler a;
	a.init();
	for(int t = 0; t < 200000; t ++){
		usleep(1000);
		ops::ops_input input;
		input.set_tti(TTICounter::get_current_dl_tti());
		TTICounter::step_dl_tti();
		auto u0 = input.add_ue_input();
		u0->set_rnti(11);
		u0->set_allocated_hts(TTICounter::get_now_timestamp());
		u0->set_alpha(0.5);
		
		auto u1 = input.add_ue_input();
		u1->set_rnti(71);
		u1->set_allocated_hts(TTICounter::get_now_timestamp());
		u1->set_alpha(0.7);
		
		printf("%s\n",input.DebugString().c_str());
		auto output = a.do_ops_scheduling(input);
		printf("%s\n",output.DebugString().c_str());
	}
	
	return 0;
}
