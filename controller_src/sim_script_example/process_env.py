#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import os
from multiprocessing import Process

from sim_src.tb_logger import TBScalarToCSV

path = os.path.dirname(os.path.realpath(__file__))
path_data = os.path.join(path,'tb-data')
dirs = next(os.walk(path_data))[1]

scalar_list = []
scalar = 'TX_DELAY_'
scalar_list.append(scalar)

scalar = 'N_RLCTX_'
scalar_list.append(scalar)

scalar = 'N_DISCARD_'
scalar_list.append(scalar)

scalar = 'RLC_REWARD_'
scalar_list.append(scalar)

scalar = 'N_CH_TX_OK_'
scalar_list.append(scalar)

scalar = 'UE_REWARD_'
scalar_list.append(scalar)


def process_env(path,dir):
    p = os.path.join(path, dir)
    TBScalarToCSV(p, p, scalar_list)


p_list = []
for d in dirs:
    p = Process(target=process_env, args=(path_data,d,))
    p_list.append(p)

for p in p_list:
    p.start()

for p in p_list:
    p.join()
