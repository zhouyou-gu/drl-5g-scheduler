//
// Created on 23/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//

#ifndef DDRL_DDRL_AGENT_BASE_H
#define DDRL_DDRL_AGENT_BASE_H
#include <mutex>
#include <sstream>



#include <google/protobuf/any.pb.h>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/io/zero_copy_stream.h>

#include "srslte/common/threads.h"
#include "srslte/common/common.h"

#define MAX_BUF_SIZE 5000

class ddrl_agent_base
: public thread
{
public:;
	ddrl_agent_base();
	~ddrl_agent_base();
	int init( std::string agent_bind_addr_,int agent_port_, std::string controller_addr_, int controller_port_);
	void stop();
	void run_thread();

	virtual int process_packet(uint8_t * buffer , int packet_size);
	virtual bool wait_for_setup();
	int test_function();
	
protected:
	
	bool connect_controller();
	bool try_connect();
	
	static const int THREAD_PRIO = 65;
	static const int ADDR_FAMILY      = AF_INET;
	static const int SOCK_TYPE        = SOCK_STREAM;

	bool running = false;
	bool controller_connected = false;
	
	int agent_port;
	int controller_port;
	std::string                  agent_bind_ipaddr;
	std::string                  controller_ipaddr;
	
	int       socket_fd;
	struct    sockaddr_in con_addr;   // controller address
	
	uint8_t buffer[MAX_BUF_SIZE];
	std::mutex agent_mutex;
	
};


#endif //DDRL_DDRL_AGENT_BASE_H
