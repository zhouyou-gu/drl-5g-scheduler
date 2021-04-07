#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import socket

from threading import Thread


class Server(Thread):
    def __init__(self, name: str, bind_ip: str, bind_port: int, max_conn=5):
        Thread.__init__(self)
        self.name = name
        self.sock = self.get_socket()
        self.sock.bind((bind_ip, bind_port))
        try:
            self.sock.listen(max_conn)
        except:
            print("socket no listen")
        self.client_conn = []

    def run(self):
        print("running SctpServer: Name =", self.name)
        while True:
            conn, address = self.sock.accept()
            print('Accepted connection from', address[0], ':', address[1])
            self.connection_handler(conn)
            self.client_conn.append(conn)

    def connection_handler(self, conn):
        print('Need a child function to handle connection: ', conn)
        pass

    def get_socket(self):
        pass


class SctpServer(Server):
    def get_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)


if __name__ == '__main__':
    s = SctpServer('test_server', '127.0.1.1', 4003)
    s.start()
