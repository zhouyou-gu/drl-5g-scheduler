//
// Created on 26/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "ddrl_log.h"
#include "ddrl_scalar_agent.h"
using namespace google;
using namespace protobuf;

static ddrl_log this_log("ddrl_scalar_agent.log",true);

bool GlobalSalarReporter::is_report_inited = false;
std::shared_ptr<ddrl_scalar_agent> GlobalSalarReporter::reporter = nullptr;