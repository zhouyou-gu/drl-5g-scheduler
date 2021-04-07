//
// Created on 16/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "ddrl_util.h"
/// init TTICounter
int TTICounter::dl_tti_counter = 0;
std::mutex TTICounter::tti_muted;
std::vector<tic_time> TTICounter::ticed_time;


int TTICounter::tic(std::string msg) {
	ticed_time.push_back(tic_time(msg,get_now_timeval()));
}


int TTICounter::tac() {
	auto now = get_now_timeval();
	if(!ticed_time.empty()) {
		auto a = ticed_time.back();
		int ret = (int) calculate_time_interval_usec(a.second,now);
		fprintf(stdout,"time (us) of %s:%d\n",a.first.c_str(),ret);
		ticed_time.pop_back();
		return ret;
	}
	return -1;
}

