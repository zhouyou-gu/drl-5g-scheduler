#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import os

from sim_src.sim_helper.event_to_csv import EventToCsvHandler

n_ue = 2
scalar_list = []
for k in range(n_ue):
    scalar = 'ue' + str(k + 1) + '_Latency_ms'
    scalar_list.append(scalar)

event = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'online')]
e = EventToCsvHandler(event_dir=event, dir_pattern='*', scalar_list=scalar_list)
