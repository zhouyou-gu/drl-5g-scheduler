//
// Created on 11/10/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef OPS_ASYNC_SCHEDULER_H
#define OPS_ASYNC_SCHEDULER_H

#include <mutex>
#include "srslte/common/threads.h"
#include "srslte/common/threads.h"
#include "ops_interface.pb.h"
#include "ops_agent.h"
class ops_async_scheduler:
public thread
{
public:
	ops_async_scheduler();
	~ops_async_scheduler();
	virtual int init(ops_agent* agent);
	ops::ops_output get_ops_output();
	void stop();
	void run_thread();
	
protected:
	ops_agent* m_agent = NULL;
	
	virtual int do_scheduling();
	int update_output(ops::ops_output new_output);
	bool is_output_pending();
	long get_time_to_tx();
	
	ops::ops_output output;
	bool output_pending;
	
	long time_to_tx_us = 0;
	
	bool running = false;
	static const int THREAD_PRIO = 2;
	static const int MIN_ITERATION_TIME_US = 1000;
	
	std::mutex scheduler_mutex;
	
};


#endif //OPS_ASYNC_SCHEDULER_H
