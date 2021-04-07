//
// Created on 13/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef SRS_EXT_H
#define SRS_EXT_H
#include <stdint.h>
#include <mutex>
#include <sys/time.h>
#include <map>

#include <google/protobuf/timestamp.pb.h>

#include "ddrl_util.h"
class rlc_common_ext{
public:
	virtual long get_head_of_line() = 0;
	virtual struct timeval get_head_timestamp() = 0;
};

class ue_rlc_ext{
public:
	virtual long get_head_of_line(uint8_t lc_id) = 0;
	virtual struct timeval get_head_timestamp(uint8_t lc_id) = 0;
};

class rlc_layer_ext{
protected:
	virtual int do_ext_report(uint16_t rnti, uint8_t lc_id) = 0; // run get hol then run set inside
	virtual int report_head_of_line(uint16_t rnti, uint8_t lc_id) = 0; // run get hol then run set inside
	virtual int report_head_timestamp(uint16_t rnti, uint8_t lc_id) = 0; // report -1 sec -1 usec if not packets
};

class sched_ue_ext{
public:
	virtual uint32_t get_dl_lc_buffer_size(uint8_t lc_id) = 0;
	
	int set_qci(uint8_t lc_id, uint8_t qci);
	int set_head_of_line(uint8_t lc_id, long hol);
	int set_head_timestamp(uint8_t lc_id, struct timeval hts);
	
	uint8_t get_qci(uint8_t lc_id);
	long get_head_of_line_of_a_lc(uint8_t lc_id);
	long get_head_of_line();
	google::protobuf::Timestamp * get_hts();
	
	int tti_from_control_txed = -1;
	
	const static int PACKET_SIZE = 200;

protected:
	std::mutex ext_mutex;
	std::map<uint8_t , uint8_t > qci_map;
	std::map<uint8_t , long > hol_map;
	std::map<uint8_t , struct timeval > hts_map;
	
};

class mac_interface_ext{
public:
	virtual int set_qci(uint16_t rnti, uint8_t lc_id, uint8_t qci) = 0;
	virtual int set_head_of_line(uint16_t rnti, uint8_t lc_id, long hol) = 0;
	virtual int set_head_timestamp(uint16_t rnti, uint8_t lc_id, struct timeval hts) = 0;
};



#endif //SRS_EXT_H