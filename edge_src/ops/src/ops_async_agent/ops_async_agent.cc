//
// Created on 2/10/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#include "ops_async_agent.h"
#include "ddrl_ops_async_scheduler/ddrl_ops_async_scheduler.h"

int ops_async_agent::init_agent() {
	ops_async_scheduler_interface = std::make_shared<ddrl_ops_async_scheduler>();
	ops_async_scheduler_interface->init(this);
	return 0;
}
int ops_async_agent::test_function() {
	printf("ops_async_agent:test_function\n");
	return 0;
}