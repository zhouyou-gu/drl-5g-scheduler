//
// Created on 14/10/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "ops_sync_agent.h"
#include "ddrl_ops_scheduler/ddrl_ops_scheduler.h"

int ops_sync_agent::init_agent() {
	ops_sync_scheduler_interface = std::make_shared<ddrl_ops_scheduler>();
	ops_sync_scheduler_interface->init();
	return 0;
}
int ops_sync_agent::test_function() {
	printf("ops_sync_agent:test_function\n");
	return 0;
}
