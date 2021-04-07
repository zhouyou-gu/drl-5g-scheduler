#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import time
from threading import Thread

from edge_ctrl_src.app_ctrl import *
from edge_ctrl_src.edge import Edge
from edge_ctrl_src.edge_config import edge_config

PING_COUNTER = 1000000


class PingEdge(Edge):
    def __init__(self, id, config):
        super(PingEdge, self).__init__(id, config)

    def downlink_ping(self):
        t_list = []
        for u in range(len(self.ues)):
            t = Thread(target=run_ping, args=(self.epc, '172.16.0.10' + str(u + 1), PING_COUNTER))
            t.start()
            t_list.append(t)

        for t in t_list:
            t.join()

    def uplink_ping(self):
        t_list = []
        for u in range(len(self.ues)):
            t = Thread(target=run_ping, args=(self.ues[u], '172.16.0.1', PING_COUNTER))
            t.start()
            t_list.append(t)

        for t in t_list:
            t.join()


e = PingEdge(0, edge_config)
e.downlink_ping()
time.sleep(10)
e.uplink_ping()
