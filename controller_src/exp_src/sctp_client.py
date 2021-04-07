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

from exp_src.util import *


class Client(Thread):
    def __init__(self, server_ip: str, server_port: int, ):
        Thread.__init__(self)
        self.server = (server_ip, server_port)
        self.connected = False
        self.connect_server()
        self.buffer = []

    def run(self):
        while True:
            if not self.connected:
                self.connect_server()

    def try_connect(self):
        try:
            self.sock = self.get_socket()
            self.sock.connect(self.server)
            return True
        except:
            return False

    def connect_server(self):
        while not self.try_connect():
            print(self.__class__, 'connection fails, retry in 1 seconds')
            time.sleep(1)
        self.connected = True

    def send(self, str_of_ANY_msg: str):
        if self.connected:
            try:
                return self.sock.send(str_of_ANY_msg)
            except:
                self.connected = False
                return 0
        return 0

    def get_socket(self):
        pass


class SctpClient(Client):
    def get_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)


if __name__ == '__main__':
    c = SctpClient('127.0.1.1', 4003)
    c.start()
