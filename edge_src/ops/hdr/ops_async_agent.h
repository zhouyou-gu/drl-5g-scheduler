//
// Created on 14/10/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef OPS_ASYNC_AGENT_H
#define OPS_ASYNC_AGENT_H

#include "ops_agent.h"
#include "ops_async_scheduler.h"

class ops_async_agent:
public ops_agent
{
public:
	int init_agent();
	virtual int do_scheduling() = 0;
	virtual ops::ops_input get_ops_input() = 0;
    virtual ops::ops_cell_conf get_cell_config() = 0;

protected:
	std::shared_ptr<ops_async_scheduler> ops_async_scheduler_interface;
	int test_function();
};



#endif //OPS_ASYNC_AGENT_H
