//
// Created on 30/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef OPS_AGENT_H
#define OPS_AGENT_H

#include "ops_interface.pb.h"

class ops_agent{
public:
	virtual int init_agent() = 0;
	virtual int do_scheduling() = 0;
	virtual ops::ops_input get_ops_input() = 0;
    virtual ops::ops_cell_conf get_cell_config() = 0;
protected:
	virtual int test_function() = 0;
	
};

class ops_agent_ue{
public:
	virtual ops::ops_ue_input * get_ops_ue_input() = 0;
	
	ops::ops_ue_output temp_output;
};
#endif //OPS_AGENT_H
