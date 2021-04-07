//
// Created on 17/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include <iostream>
#include <stdio.h>

#include "ddrl_log.h"

#include "srsenb/hdr/stack/mac/scheduler.h"


using namespace srsenb;

static ddrl_log this_log("ops_agent_ext.log",true);


//int sched::test_function() {
//	std::map<uint16_t, sched_ue>::iterator it;
//	for(it = ue_db.begin(); it != ue_db.end(); it ++){
//		if(it->second.get_head_of_line()>0){
//			this_log.debug("rnti=%x, hol=%ld\n", it->first, it->second.get_head_of_line());
//		}
//	}
//	return 0;
//}

int sched::do_scheduling() {
	for (auto& ue_pair : ue_db) {
		ue_pair.second.temp_output.Clear();
	}
	auto output = ops_async_scheduler_interface->get_ops_output();
	for(int u = 0; u < output.ue_output_size(); u ++){
		uint16_t rnti = output.ue_output(u).rnti();
		if(ue_db.count(rnti)){
			ue_db[rnti].temp_output.CopyFrom(output.ue_output(u));
		}
	}
	return 0;
}

ops::ops_input sched::get_ops_input(){
	auto input =  new ops::ops_input;
	input->set_tti(TTICounter::get_current_dl_tti());
	
	for (auto& ue_pair : ue_db) {
		input->add_ue_input()->CopyFrom(*ue_pair.second.get_ops_ue_input());
	}
	return *input;
}

ops::ops_cell_conf sched::get_cell_config(){
    auto cell_config = new ops::ops_cell_conf;
    cell_config->set_cell_id(cfg.cell.id);
    cell_config->set_n_prb(cfg.cell.nof_prb);

#ifdef SUBCARRIER_SPACING
    cell_config->set_tti_duration((uint32_t)SUBCARRIER_SPACING/15000);
#else
    cell_config->set_tti_duration(1);
#endif
    return *cell_config;
}

