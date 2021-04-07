//
// Created on 11/10/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#include "ddrl_util.h"
#include "ops_global_sync.h"
#include "ops_async_scheduler.h"
#include <thread>
#include <iostream>

ops_async_scheduler::ops_async_scheduler(): thread("ops_async_scheduler") {
	m_agent = NULL;
	output.Clear();
	output_pending = false;
}
ops_async_scheduler::~ops_async_scheduler(){
	stop();
}

int ops_async_scheduler::init(ops_agent *agent) {
	printf("ops_async_scheduler::init(ops_agent *agent) virtual function need to be overridden\n");
	return 0;
}
void ops_async_scheduler::stop() {
	if(running) {
		running = false;
		thread_cancel();
		wait_thread_finish();
	}
}
void ops_async_scheduler::run_thread() {
	while(running){
		if(is_output_pending()){
			continue;
		}
		ops_global_sync::wait_ops_output_processed();
		auto t1 = TTICounter::get_now_timeval();
		do_scheduling();
		auto t2 = TTICounter::get_now_timeval();
		int d = TTICounter::calculate_time_interval_usec(t1,t2);
//		if(d > 0)
//			usleep(MIN_ITERATION_TIME_US-(d%MIN_ITERATION_TIME_US));
	}
}
int ops_async_scheduler::do_scheduling() {
	printf("virtual function need to be overridden\n");
}
ops::ops_output ops_async_scheduler::get_ops_output() {
	std::lock_guard<std::mutex> lock(scheduler_mutex);
	ops::ops_output ret;
	if(output_pending){
		ret.CopyFrom(output);
		output.Clear();
		output_pending = false;
		time_to_tx_us = ops_global_sync::ops_output_acquired();
	}
	return ret;
}

int ops_async_scheduler::update_output(ops::ops_output new_output){
	std::lock_guard<std::mutex> lock(scheduler_mutex);
	output_pending = true;
	output.CopyFrom(new_output);
	ops_global_sync::ops_output_ready();
	return 0;
}

bool ops_async_scheduler::is_output_pending() {
	std::lock_guard<std::mutex> lock(scheduler_mutex);
	return output_pending;
}

long ops_async_scheduler::get_time_to_tx() {
	std::lock_guard<std::mutex> lock(scheduler_mutex);
	/// the time_to_tx of the next thread consumer
	return time_to_tx_us;
}