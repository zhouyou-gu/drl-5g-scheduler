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

tb_server_ip = '192.168.1.100'


class OneWayLatencyLTEEdge(Edge):
    def __init__(self, id, config):
        super(OneWayLatencyLTEEdge, self).__init__(id, config)

    def downlink_one_way_latency(self):
        t_list = []
        for u in range(len(self.ues)):
            t = Thread(target=sudo_run_oneway_latency_server, args=(
            self.ues[u], self.config.ue_config_list[u].password, self.config.ue_config_list[u].working_dir, 9000 + u,
            tb_server_ip))
            t.start()
            t_list.append(t)
        time.sleep(3)
        for u in range(len(self.ues)):
            t = Thread(target=sudo_run_oneway_latency_client, args=(
            self.epc, self.config.epc_config.password, self.config.epc_config.working_dir, '172.16.0.10' + str(u + 1),
            9000 + u))
            t.start()
            t_list.append(t)

        for t in t_list:
            t.join()

    def uplink_one_way_latency(self):
        t_list = []
        for u in range(len(self.ues)):
            t = Thread(target=run_oneway_latency_server,
                       args=(self.epc, self.config.epc_config.working_dir, 9000 + u, tb_server_ip))
            t.start()
            t_list.append(t)

        time.sleep(3)
        for u in range(len(self.ues)):
            t = Thread(target=run_oneway_latency_client,
                       args=(self.ues[u], self.config.ue_config_list[u].working_dir, '172.16.0.1', 9000 + u))
            t.start()
            t_list.append(t)

        for t in t_list:
            t.join()


e = OneWayLatencyLTEEdge(0, edge_config)
e.downlink_one_way_latency()
time.sleep(10)
# e.uplink_one_way_latency()
