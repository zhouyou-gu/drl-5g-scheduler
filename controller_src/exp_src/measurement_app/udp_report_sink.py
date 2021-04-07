#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import socket
import time
from collections import deque
from threading import Thread

UDP_REPORT_SINK_PORT = 5000


class udp_report_sink(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.bind(('0.0.0.0', UDP_REPORT_SINK_PORT))
        self.data_queue = {}

    def run(self):
        while True:
            data = self.sock.recv(4096)
            data = data.decode('utf-8')
            d = data.split()
            if d[0] not in self.data_queue:
                self.data_queue[d[0]] = deque(maxlen=100)
            self.data_queue[d[0]].append((time.time(), d[1]))

    def get_report(self):
        return self.data_queue


if __name__ == '__main__':
    u = udp_report_sink()
    u.start()

    while True:
        k = u.get_report()
        if k:
            print(k[0], int(k[1]))
