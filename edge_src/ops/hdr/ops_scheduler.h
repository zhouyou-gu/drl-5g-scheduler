//
// Created on 30/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef OPS_SCHEDULER_H
#define OPS_SCHEDULER_H

#include "ops_interface.pb.h"

class ops_scheduler{
public:
	virtual int init() = 0;
	virtual ops::ops_output do_ops_scheduling(ops::ops_input& input) = 0;
};

#endif //OPS_SCHEDULER_H
