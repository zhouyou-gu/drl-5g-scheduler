//
// Created on 25/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef DDRL_DDRL_TRANSITION_AGENT_H
#define DDRL_DDRL_TRANSITION_AGENT_H
#include <google/protobuf/any.pb.h>
#include <google/protobuf/timestamp.pb.h>

#include "transition.pb.h"

#include "ddrl_agent_base.h"
#include "ddrl_util.h"

using namespace google;
using namespace protobuf;


class ddrl_transition_agent: public ddrl_agent_base {
public:
	inline int step(ddrl::enb_transition t){
		if(!controller_connected) {
			return -1;
		}
		t.set_allocated_timestamp(TTICounter::get_now_timestamp());
		auto * any =  new Any;
		any->PackFrom(t);
		auto s = any->SerializeAsString();
		send(socket_fd, s.c_str(), s.size(),  MSG_DONTWAIT);
		return 0;
	}
};

#endif //DDRL_DDRL_TRANSITION_AGENT_H
