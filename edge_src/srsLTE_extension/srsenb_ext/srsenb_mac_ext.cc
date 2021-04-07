//
// Created on 16/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "srsenb/hdr/stack/mac/mac.h"
using namespace srsenb;

int mac::set_qci(uint16_t rnti, uint8_t lc_id, uint8_t qci) {
	int ret = 0;
	pthread_rwlock_rdlock(&rwlock);
	ret = scheduler.set_qci(rnti, lc_id, qci);
	pthread_rwlock_unlock(&rwlock);
	return ret;
}

int mac::set_head_of_line(uint16_t rnti, uint8_t lc_id, long hol) {
	int ret = 0;
	pthread_rwlock_rdlock(&rwlock);
	ret = scheduler.set_head_of_line(rnti, lc_id, hol);
	pthread_rwlock_unlock(&rwlock);
	return ret;
}

int mac::set_head_timestamp(uint16_t rnti, uint8_t lc_id, struct timeval hts) {
	int ret = 0;
	pthread_rwlock_rdlock(&rwlock);
	ret = scheduler.set_head_timestamp(rnti, lc_id, hts);
	pthread_rwlock_unlock(&rwlock);
	return ret;
}