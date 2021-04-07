#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from threading import Thread

from edge_ctrl_src.app_ctrl import *
from edge_ctrl_src.edge import Edge
from edge_ctrl_src.edge_config import edge_config


class TBServerAtEpc(Edge):
    def __init__(self, id, config):
        Edge.__init__(self, id, config)

    def run_tb_server_at_epc(self):
        t = Thread(target=run_tb_server,
                   args=(self.epc, self.config.epc_config.working_dir))
        t.start()
        t.join()


e = TBServerAtEpc(0, edge_config)
e.run_tb_server_at_epc()
