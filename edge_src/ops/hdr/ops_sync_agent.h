//
// Created on 14/10/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef OPS_SYNC_AGENT_H
#define OPS_SYNC_AGENT_H

#include "ops_agent.h"
#include "ops_scheduler.h"

class ops_sync_agent:
public ops_agent
{
public:
	int init_agent() = 0;
	virtual int do_scheduling() = 0;
	virtual ops::ops_input get_ops_input() = 0;

protected:
	std::shared_ptr<ops_scheduler> ops_sync_scheduler_interface;
	int test_function();
};

#endif //OPS_SYNC_AGENT_H
