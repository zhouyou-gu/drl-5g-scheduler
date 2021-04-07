//
// Created on 13/11/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "ops_global_sync.h"
std::thread::id ops_global_sync::last_ops_output_acquired_thread_id;
pthread_mutex_t ops_global_sync::mutex;
std::map<std::thread::id, struct timeval> ops_global_sync::phy_tx_time_map;
std::mutex ops_global_sync::phy_tx_time_mutex;