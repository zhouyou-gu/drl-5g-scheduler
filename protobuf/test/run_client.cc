//
// Created on 20/9/19.
// Author: Zhouyou Gu <guzhouyou@gmail.com>.
//


#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <wait.h>
#include <iostream>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>

#include "transition.pb.h"


using namespace std;
#define PORT 8000           // the port users will be connecting to
#define MAXDATASIZE 4096    // max number of bytes we can send at once
#define BACKLOG 10          // how many pending connections queue will hold
#define HOSTNAME "localhost"
/* simple little function to write an error string and exit */
static void err(const char* s) {
	perror(s);
	exit(EXIT_FAILURE);
}

int main(int argc, char** argv) {
	int fd;
	int numbytes;
	char buf[MAXDATASIZE];
	struct hostent *he;
	struct sockaddr_in server;
	
	if ((he = gethostbyname(HOSTNAME)) == NULL) {
		err("gethostbyname");
	}
	
	if ((fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
		err("socket");
	}
	
	bzero(&server, sizeof(server));
	server.sin_family = AF_INET;
	server.sin_port = htons(PORT);
	server.sin_addr = *((struct in_addr *)he->h_addr);
	
	if (connect(fd, (struct sockaddr *)&server, sizeof(struct sockaddr)) == -1) {
		err("connect");
	}
	
	string msg;
	ddrl::ue_transition to;
	to.set_rnti(19);
	to.set_id(8);
	to.SerializeToString(&msg);
	sprintf(buf, "%s", msg.c_str());
	send(fd, buf, sizeof(buf), 0);
	
	numbytes = recv(fd, buf, MAXDATASIZE, 0);
	buf[numbytes] = '\0';
	string data = buf;
	ddrl::ue_transition p;
	p.ParseFromString(data);
	cout << "People:\t" << endl;
	cout << "Name:\t" << p.rnti() << endl;
	cout << "ID:\t" << p.id() << endl;
	
	close(fd);
	return 0;
}
