#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import os

from edge_ctrl_src.edge import Edge
from edge_ctrl_src.edge_config import edge_config

e = Edge(0, edge_config)
path = os.path.dirname(os.path.realpath(__file__))

path = os.path.join(path,os.path.pardir)
path = os.path.join(path,os.path.pardir)
path = os.path.abspath(path)
PROJECT_DIR = path

e._create_working_dirs()
e.upload_all_src_file_to_edge(PROJECT_DIR)
