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

import numpy as np

from sim_src.sim_helper.csv_to_result import CsvToResultHandler

n_ue = 5
n_step = 1000
n_episode = 200
path = os.path.dirname(os.path.realpath(__file__))
path_data = os.path.join(path,'tb-data')
dirs = next(os.walk(path_data))[1]

n_average_step = 10000

def process_csv(path,d):
    p = os.path.join(path, d)
    res_dir = os.path.join(p, "res")
    try:
        os.mkdir(res_dir)
    except:
        pass
    o = CsvToResultHandler(p, n_ue=n_ue, n_step=n_step, n_episode=n_episode)
    for k in range(n_ue):
        out = o.get_ue_average_reward(k, n_average_step)
        np.savetxt(os.path.join(res_dir, "ue." + str(k) + ".average_reward.csv"), out)
        out = o.get_ue_packet_loss(k, n_average_step)
        np.savetxt(os.path.join(res_dir, "ue." + str(k) + ".loss_rate.csv"), out)
    out = o.get_min_ue_average_reward(n_average_step)
    np.savetxt(os.path.join(res_dir, "min.average_reward.csv"), out)


p_list = []
for d in dirs:
    p = Process(target=process_csv, args=(path_data,d,))
    p_list.append(p)

for p in p_list:
    p.start()

for p in p_list:
    p.join()
