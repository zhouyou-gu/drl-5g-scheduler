//
// Created on 13/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#include <sys/time.h>
#include "srsenb/hdr/stack/mac/scheduler_ue.h"
using namespace srsenb;

int sched_ue_ext::set_qci(uint8_t lc_id, uint8_t qci) {
	std::lock_guard<std::mutex> lock(ext_mutex);
	int ret = 0;
	qci_map[lc_id] = qci;
	return ret;
}

int sched_ue_ext::set_head_of_line(uint8_t lc_id, long hol) {
	std::lock_guard<std::mutex> lock(ext_mutex);
	int ret = 0;
	hol_map[lc_id] = hol;
	return ret;
}

int sched_ue_ext::set_head_timestamp(uint8_t lc_id, struct timeval hts) {
	std::lock_guard<std::mutex> lock(ext_mutex);
	int ret = 0;
	hts_map[lc_id] = hts;
	return ret;
}


uint8_t sched_ue_ext::get_qci(uint8_t lc_id){
	std::lock_guard<std::mutex> lock(ext_mutex);
	uint8_t ret = 0;
	if (qci_map.count(lc_id)) {
		ret = qci_map[lc_id];
	} else {
		ret = 0;
	}
	return ret;
}

long sched_ue_ext::get_head_of_line_of_a_lc(uint8_t lc_id){
	std::lock_guard<std::mutex> lock(ext_mutex);
	long ret = 0;
	if (hts_map.count(lc_id)) {
		struct timeval temp;
		gettimeofday(&temp, NULL);
		ret = TTICounter::calculate_time_interval_usec(hts_map[lc_id],temp);
	} else {
		ret = 0;
	}
	return ret;
}

long sched_ue_ext::get_head_of_line(){
	std::lock_guard<std::mutex> lock(ext_mutex);
	long ret = 0;
	for(auto it = hts_map.begin(); it != hts_map.end() ; it++){
		if(TTICounter::timestamp_is_valid(it->second)){
			struct timeval temp;
			gettimeofday(&temp, NULL);
			long temp_hol = TTICounter::calculate_time_interval_usec(it->second,temp);
			if(temp_hol > ret){
				ret = temp_hol;
			}
		}
	}
	return ret;
}

google::protobuf::Timestamp *  sched_ue_ext::get_hts(){
	std::lock_guard<std::mutex> lock(ext_mutex);
	long ret = 0;
	auto * t = new google::protobuf::Timestamp;
	t->set_seconds(-1);
	t->set_nanos(-1);
	for(auto it = hts_map.begin(); it != hts_map.end() ; it++){
		if(TTICounter::timestamp_is_valid(it->second)){
			struct timeval temp;
			gettimeofday(&temp, NULL);
			long temp_hol = TTICounter::calculate_time_interval_usec(it->second,temp);
			if(temp_hol > ret){
				ret = temp_hol;
				t->set_seconds(it->second.tv_sec);
				t->set_nanos(it->second.tv_usec*1000);
			}
		}
	}
	return t;
}

ops::ops_ue_input * sched_ue::get_ops_ue_input(){
	auto ue_input = new ops::ops_ue_input;
	ue_input->set_rnti(rnti);
	ue_input->set_allocated_hts(get_hts());
	int n_prb = get_required_prb_dl(PACKET_SIZE, 3)*1.2;
	ue_input->set_alpha((float) n_prb / cell.nof_prb);
	return ue_input;
}

uint32_t sched_ue::get_dl_lc_buffer_size(uint8_t lc_id){
	std::lock_guard<std::mutex> lock(mutex);
	if (lc_id >= sched_interface::MAX_LC)
		return 0;
	if (bearer_is_dl(&lch[lc_id])) {
		return  lch[lc_id].buf_retx + lch[lc_id].buf_tx;
	}
	return 0;
}