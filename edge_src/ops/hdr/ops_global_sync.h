//
// Created on 13/11/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef OPS_GLOBAL_SYNC_H
#define OPS_GLOBAL_SYNC_H

#include <thread>
#include <pthread.h>
#include <iostream>
#include <map>
#include <mutex>
#include <sys/time.h>
#ifdef SUBCARRIER_SPACING
#define TX_DELAY_US 4000/(SUBCARRIER_SPACING/15000)
#else
#define TX_DELAY_US 4000
#endif

// TODO: sync using pthread_mutex_lock seems has limitation, try to condition_wait
class ops_global_sync {
public:
	static inline long ops_output_acquired(){
		pthread_mutex_lock(&mutex);
		last_ops_output_acquired_thread_id = std::this_thread::get_id();
		return ops_get_phy_tx_time(last_ops_output_acquired_thread_id);
	}
	
	static inline void ops_output_processed(){
		if(std::this_thread::get_id() == last_ops_output_acquired_thread_id)
			pthread_mutex_unlock(&mutex);
	}
	
	static inline void wait_ops_output_processed(){
		pthread_mutex_lock(&mutex);
	}
	
	static inline void ops_output_ready(){
		pthread_mutex_unlock(&mutex);
	}
	
	static inline void ops_report_phy_rx(){
		std::lock_guard<std::mutex> lock(phy_tx_time_mutex);
		struct timeval now;
		gettimeofday(&now, NULL);
        struct timeval tx_delay{0,TX_DELAY_US*3/4};
        timeradd(&now,&tx_delay,&now);
		phy_tx_time_map[std::this_thread::get_id()] = now;
	}
	
	static inline long ops_get_phy_tx_time(std::thread::id th_id){
		std::lock_guard<std::mutex> lock(phy_tx_time_mutex);
		struct timeval now;
		gettimeofday(&now, NULL);
		if(phy_tx_time_map.count(th_id)){
			auto tx_time = phy_tx_time_map[std::this_thread::get_id()];
            long sec =  tx_time.tv_sec - now.tv_sec;
			long usec =  tx_time.tv_usec - now.tv_usec;
			if (usec < 0) {
				sec--;
				usec += 1000000;
			}
			return (sec * 1000000 + usec);
		} else {
			return  0;
		}
	}
	
	static std::thread::id last_ops_output_acquired_thread_id;
	static pthread_mutex_t mutex;
	
	static std::map<std::thread::id,struct timeval> phy_tx_time_map;
	static std::mutex phy_tx_time_mutex;
	
};


#endif //OPS_GLOBAL_SYNC_H
