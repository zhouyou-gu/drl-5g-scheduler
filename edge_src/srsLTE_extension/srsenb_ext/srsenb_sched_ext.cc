//
// Created on 13/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "srsenb/hdr/stack/mac/scheduler.h"
using namespace srsenb;

int sched::set_qci(uint16_t rnti, uint8_t lc_id, uint8_t qci) {
	int ret = 0;
	pthread_rwlock_rdlock(&rwlock);
	if (ue_db.count(rnti)) {
		ue_db[rnti].set_qci(lc_id,qci);
	} else {
		log_h->error("User rnti=0x%x not found\n", rnti);
		ret = -1;
	}
	pthread_rwlock_unlock(&rwlock);
	return ret;
}

int sched::set_head_of_line(uint16_t rnti, uint8_t lc_id, long hol) {
	int ret = 0;
	pthread_rwlock_rdlock(&rwlock);
	if (ue_db.count(rnti)) {
		ue_db[rnti].set_head_of_line(lc_id,hol);
	} else {
		log_h->error("User rnti=0x%x not found\n", rnti);
		ret = -1;
	}
	pthread_rwlock_unlock(&rwlock);
	return ret;
}

int sched::set_head_timestamp(uint16_t rnti, uint8_t lc_id, struct timeval hts) {
	int ret = 0;
	pthread_rwlock_rdlock(&rwlock);
	if (ue_db.count(rnti)) {
		ue_db[rnti].set_head_timestamp(lc_id,hts);
	} else {
		log_h->error("User rnti=0x%x not found\n", rnti);
		ret = -1;
	}
	pthread_rwlock_unlock(&rwlock);
	return ret;
}