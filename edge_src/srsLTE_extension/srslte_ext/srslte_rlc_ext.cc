//
// Created on 16/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "srslte/upper/rlc.h"
#include "srslte/upper/rlc_tm.h"
#include "srslte/upper/rlc_am.h"
#include "srslte/upper/rlc_um.h"
long srslte::rlc::get_head_of_line(uint8_t lc_id){
	if (valid_lcid(lc_id)) {
		return rlc_array.at(lc_id)->get_head_of_line();
	} else {
		return 0;
	}
}

struct timeval srslte::rlc::get_head_timestamp(uint8_t lc_id) {
	if (valid_lcid(lc_id)) {
		return rlc_array.at(lc_id)->get_head_timestamp();
	} else {
		return TTICounter::get_a_invalid_time();
	}
}


long srslte::rlc_tm::get_head_of_line(){
	if(!ul_queue.is_empty()){
		return ul_queue.get_hol();
	} else {
		return 0;
	}
}

struct timeval srslte::rlc_tm::get_head_timestamp() {
	if(!ul_queue.is_empty()){
		return ul_queue.get_hts();
	} else {
		return TTICounter::get_a_invalid_time();
	}
}
long srslte::rlc_am::rlc_am_tx::get_head_of_line(){
	if(tx_sdu != NULL){
		return tx_sdu->get_latency_us();
	}
	else if (!tx_sdu_queue.is_empty()){
		return tx_sdu_queue.get_hol();
	} else {
		return 0;
	}
}

struct timeval srslte::rlc_am::rlc_am_tx::get_head_timestamp() {
	if(tx_sdu != NULL){
		return tx_sdu->get_timestamp();
	}
	else if (!tx_sdu_queue.is_empty()){
		return tx_sdu_queue.get_hts();
	} else {
		return TTICounter::get_a_invalid_time();
	}
}

long srslte::rlc_am::get_head_of_line(){
	return tx.get_head_of_line();
}

struct timeval srslte::rlc_am::get_head_timestamp() {
	return tx.get_head_timestamp();
}

long srslte::rlc_um::rlc_um_tx::get_head_of_line(){
	if(tx_sdu != NULL){
		return tx_sdu->get_latency_us();
	}
	else if (!tx_sdu_queue.is_empty()){
		return tx_sdu_queue.get_hol();
	} else {
		return 0;
	}
}

struct timeval srslte::rlc_um::rlc_um_tx::get_head_timestamp() {
	if(tx_sdu != NULL){
		return tx_sdu->get_timestamp();
	}
	else if (!tx_sdu_queue.is_empty()){
		return tx_sdu_queue.get_hts();
	} else {
		return TTICounter::get_a_invalid_time();
	}
}

long srslte::rlc_um::get_head_of_line(){
	return tx.get_head_of_line();

}

struct timeval srslte::rlc_um::get_head_timestamp() {
	return tx.get_head_timestamp();
}

