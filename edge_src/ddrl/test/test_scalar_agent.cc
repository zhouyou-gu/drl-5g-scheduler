//
// Created on 26/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#include "ddrl_log.h"
#include "ddrl_scalar_agent.h"

using namespace google;
using namespace protobuf;
static ddrl_log this_log("test_scalar_agent.log",true);

int main() {
	GlobalSalarReporter::init("127.0.1.1", "127.0.1.100");
	while(true){
		usleep(1000);
		GlobalSalarReporter::report_scalar("hello",TTICounter::get_current_dl_tti());
		TTICounter::step_dl_tti();
	}
	return 0;
}