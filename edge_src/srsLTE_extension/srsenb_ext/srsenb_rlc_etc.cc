//
// Created on 18/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "ddrl_log.h"
#include "srsenb/hdr/stack/upper/rlc.h"

using namespace std;

static ddrl_log this_log("srs_rlc_ext.log",true);

int srsenb::rlc::do_ext_report(uint16_t rnti, uint8_t lc_id){
	this_log.debug("do_ext_report\n");
	report_head_of_line(rnti,lc_id);
	report_head_timestamp(rnti,lc_id);
	return 0;
}

int srsenb::rlc::report_head_of_line(uint16_t rnti, uint8_t lc_id){
	if (users.count(rnti)) {
		long hol = users[rnti].rlc->get_head_of_line(lc_id);
		mac->set_head_of_line(rnti, lc_id, hol);
		return 0;
	}
	return -1;
}

int srsenb::rlc::report_head_timestamp(uint16_t rnti, uint8_t lc_id) {
	if (users.count(rnti)) {
 		struct timeval hts = users[rnti].rlc->get_head_timestamp(lc_id);
		this_log.debug("report_head_timestamp: %x-%d:%ld:%ld\n", rnti, lc_id, hts.tv_sec, hts.tv_usec);
		mac->set_head_timestamp(rnti, lc_id, hts);
		return 0;
	}
	return -1;
}
