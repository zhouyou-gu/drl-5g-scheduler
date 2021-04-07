//
// Created on 12/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef DDRL_UTIL_H
#define DDRL_UTIL_H

#include <sys/time.h>
#include <mutex>
#include <google/protobuf/timestamp.pb.h>

#define LTE_TX_DELAY 4
#define NS_IN_S 1000000000
#define NS_IN_MS 1000000
#define NS_IN_US 1000
#define US_IN_S 1000000


typedef std::pair<std::string, struct timeval> tic_time;


class TTICounter {
public:
	static inline long step_dl_tti(){
		std::lock_guard<std::mutex> lock(tti_muted);
		dl_tti_counter ++;
		return dl_tti_counter;
	}
	
	static inline long get_current_dl_tti(){
		std::lock_guard<std::mutex> lock(tti_muted);
		return dl_tti_counter;
	}
	
	static inline long get_current_ul_tti(){
		std::lock_guard<std::mutex> lock(tti_muted);
		return dl_tti_counter + LTE_TX_DELAY;
	}
	
	static inline google::protobuf::Timestamp * get_now_timestamp(){
		auto * ts =  new google::protobuf::Timestamp;
		struct timeval tv;
		gettimeofday(&tv, NULL);
		ts->set_seconds(tv.tv_sec);
		ts->set_nanos(tv.tv_usec * 1000);
		return ts;
	}
	
	static inline struct timeval get_now_timeval(){
		struct timeval tv;
		gettimeofday(&tv, NULL);
		return tv;
	}
	
	static long calculate_time_interval_usec(struct timeval & start, struct timeval & end) {
		long sec = end.tv_sec - start.tv_sec;
		long usec = end.tv_usec - start.tv_usec;
		if (usec < 0) {
			sec--;
			usec += 1000000;
		}
		return sec * 1000000 + usec;
	}
	static bool timestamp_is_valid(struct timeval & t){
		if(t.tv_sec>=0 and t.tv_usec>=0){
			return true;
		}
		return false;
	}
	static struct timeval get_a_invalid_time(){
		struct timeval invalid_time {-1,-1};
		return invalid_time;
	}
	
	///TODO: tic tac in different thread will fail
	static int tic(std::string msg);
	static int tac();
	
	
	static std::vector<tic_time> ticed_time;
	
	static int dl_tti_counter;
	static std::mutex tti_muted;
};

#endif //DDRL_UTIL_H
