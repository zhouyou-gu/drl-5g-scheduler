//
// Created on 23/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//
#include "ddrl_log.h"
#include "ddrl_agent_base.h"

static ddrl_log this_log("ddrl_agent_base.log",true);

ddrl_agent_base::ddrl_agent_base(): thread("DDRL_AGENT"){
	bzero(buffer, sizeof(uint8_t)*MAX_BUF_SIZE);
}

ddrl_agent_base::~ddrl_agent_base(){
	stop();
}
int ddrl_agent_base::init(std::string agent_bind_addr_, int agent_port_, std::string controller_addr_, int controller_port_) {
	this_log.debug("init ddrl_agent_base\n");
	agent_port = agent_port_;
	agent_bind_ipaddr = agent_bind_addr_;
	controller_port = controller_port_;
	controller_ipaddr = controller_addr_;
	running = true;
	connect_controller();
	wait_for_setup();
	start(THREAD_PRIO);
	return 0;
}
void ddrl_agent_base::stop()
{
	if(running) {
		running = false;
		thread_cancel();
		wait_thread_finish();
	}
	
	if(close(socket_fd) == -1) {
		this_log.error("Failed to close TCP socket\n");
	}
}

void ddrl_agent_base::run_thread(){
	while(running) {
		bzero(buffer, sizeof(uint8_t)*MAX_BUF_SIZE);
		ssize_t n_recv = recv(socket_fd, buffer, MAX_BUF_SIZE, 0);
		if (n_recv <= 0) {
			controller_connected = false;
			this_log.error("Error: controller disconnected.\n");
			connect_controller();
			continue;
		}
		process_packet(buffer,n_recv);
	}
	running = false;
}
bool ddrl_agent_base::connect_controller() {

	while(running && !try_connect()) {
		this_log.error("Failed to connect to controller - retrying in 5 seconds\n");
		sleep(5);
	}
	controller_connected = true;
	return true;
}

bool ddrl_agent_base::try_connect() {
	socket_fd = 0;
	if((socket_fd = socket(ADDR_FAMILY, SOCK_TYPE, IPPROTO_SCTP)) == -1) {
		this_log.error("Failed to create ddrl_agent_base socket\n");
		return false;
	}
	int enable = 1;
//	if (setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int)) < 0)
//		this_log.error("setsockopt(SO_REUSEADDR) failed\n");
//	if (setsockopt(socket_fd, SOL_SOCKET, SO_REUSEPORT, &enable, sizeof(int)) < 0)
//		this_log.error("setsockopt(SO_REUSEPORT) failed\n");
	this_log.debug("Connecting to controller %s:%d\n", controller_ipaddr.c_str(), controller_port);
	// Bind to the local address
	struct sockaddr_in local_addr;
	memset(&local_addr, 0, sizeof(struct sockaddr_in));
	local_addr.sin_family = ADDR_FAMILY;
	local_addr.sin_port = agent_port;
	if(inet_pton(AF_INET, agent_bind_ipaddr.c_str(), &(local_addr.sin_addr)) != 1) {
		this_log.error("Error converting IP address (%s) to sockaddr_in structure\n", agent_bind_ipaddr.c_str());
		return false;
	}
	if (bind(socket_fd, (struct sockaddr *)&local_addr, sizeof(local_addr)) != 0) {
		this_log.error("Failed to bind on address %s: %s errno %d\n", agent_bind_ipaddr.c_str(), strerror(errno), errno);
		return false;
	}
	
	memset(&con_addr, 0, sizeof(struct sockaddr_in));
	con_addr.sin_family = ADDR_FAMILY;
	con_addr.sin_port = htons(controller_port);
	if(inet_pton(AF_INET, controller_ipaddr.c_str(), &(con_addr.sin_addr)) != 1) {
		this_log.error("Error converting IP address (%s) to sockaddr_in structure\n", controller_ipaddr.c_str());
		return false;
	}
	if(connect(socket_fd, (struct sockaddr*)&con_addr, sizeof(con_addr)) == -1) {
		this_log.error("Failed to establish socket connection to DDRL Controller\n");
		return false;
	}
	this_log.debug("DDRL ddrl_agent_base socket established with DDRL controller\n");
	return true;
}

int ddrl_agent_base::process_packet(uint8_t * buffer, int packet_size) {
	this_log.error("AGENT process_packet FUNCTION SHOULD BE overwrited\n");
	return 0;
}
bool ddrl_agent_base::wait_for_setup() {
	this_log.error("AGENT wait_for_setup FUNCTION SHOULD BE overwrited\n");
	return true;
}
int ddrl_agent_base::test_function() {
	wait_for_setup();
	return 0;
}