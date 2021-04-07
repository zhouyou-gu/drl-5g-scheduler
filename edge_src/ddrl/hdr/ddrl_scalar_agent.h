//
// Created on 26/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef DDRL_DDRL_SCALAR_AGENT_H
#define DDRL_DDRL_SCALAR_AGENT_H
#include <google/protobuf/any.pb.h>
#include <google/protobuf/timestamp.pb.h>

#include "scalar_report.pb.h"


using namespace google;
using namespace protobuf;

#include "ddrl_agent_base.h"
#include "ddrl_util.h"

class ddrl_scalar_agent
: public ddrl_agent_base{
public:
	int report_scalar(std::string name, float value){
		if(!controller_connected) {
			return -1;
		}
		auto * r =  new ddrl::scalar;
		r->set_tti(TTICounter::get_current_dl_tti());
		r->set_name(name);
		r->set_value(value);
		r->set_allocated_timestamp(TTICounter::get_now_timestamp());
		auto * any =  new Any;
		any->PackFrom(*r);
		auto ss = any->SerializeAsString();
		return send(socket_fd, ss.c_str(), ss.size(),  MSG_EOR);
		
	}
};

class GlobalSalarReporter{

public:
	static int init(std::string agent_ip, std::string controller_ip){
		if(is_report_inited or reporter != nullptr) {
			printf("repeated init for GlobalSalarReporter!!!!!!!!!!!!!\n");
			return -1;
		}
		reporter = std::make_shared<ddrl_scalar_agent>();
		is_report_inited = true;
		reporter->init(agent_ip,0,controller_ip,controller_scalar_server_port);
		return 0;
	}
	static int report_scalar(std::string name, float value){
		if(is_report_inited and reporter != nullptr) {
			return reporter->report_scalar(name,value);
		}
		printf("GlobalSalarReporter is not inited yet !!!!!!!!!!!!!\n");
		return -1;

	}
	const static int controller_scalar_server_port = 4003;
	static std::shared_ptr<ddrl_scalar_agent>  reporter;
protected:
	static bool is_report_inited;

};


#endif //DDRL_DDRL_SCALAR_AGENT_H
