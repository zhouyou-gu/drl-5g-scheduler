//
// Created on 18/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#include "ddrl_log.h"
#include "ddrl_util.h"
static ddrl_log this_log("test_logging.log",true);
int main(){
	long int t1 = TTICounter::get_current_dl_tti();
	long int t2 = TTICounter::step_dl_tti();
	long int t3 = TTICounter::step_dl_tti();
	long int t4 = TTICounter::step_dl_tti();
	this_log.debug("hello %ld %ld %ld %ld \n", t1, t2, t3, t4);
}