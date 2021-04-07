#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import fnmatch
import os

import numpy as np


class CsvToResultHandler():
    def __init__(self, c_dir: str, n_ue: int, n_step: int, n_episode: int):
        self.n_ue = n_ue
        self.n_step = n_step
        self.n_episode = n_episode

        self.TX_DELAY_ = []
        self.N_RLCTX_ = []
        self.N_DISCARD_ = []
        self.RLC_REWARD_ = []
        self.N_CH_TX_OK_ = []
        self.UE_REWARD_ = []

        for path, dirs, files in os.walk(c_dir):
            for d in dirs:
                if fnmatch.fnmatch(d, 'csv'):
                    self.c_dir = os.path.join(path, d)
                    print('load csv dir:', self.c_dir)
                    self._load()
                    return

    def _load(self):
        for k in range(self.n_ue):
            postfix = str(k) + '.csv'

            fn = os.path.join(self.c_dir, 'TX_DELAY_' + postfix)
            self.TX_DELAY_.append(np.genfromtxt(fn, delimiter=","))

            fn = os.path.join(self.c_dir, 'N_RLCTX_' + postfix)
            self.N_RLCTX_.append(np.genfromtxt(fn, delimiter=","))

            fn = os.path.join(self.c_dir, 'N_DISCARD_' + postfix)
            self.N_DISCARD_.append(np.genfromtxt(fn, delimiter=","))

            fn = os.path.join(self.c_dir, 'RLC_REWARD_' + postfix)
            self.RLC_REWARD_.append(np.genfromtxt(fn, delimiter=","))

            fn = os.path.join(self.c_dir, 'N_CH_TX_OK_' + postfix)
            self.N_CH_TX_OK_.append(np.genfromtxt(fn, delimiter=","))

            fn = os.path.join(self.c_dir, 'UE_REWARD_' + postfix)
            self.UE_REWARD_.append(np.genfromtxt(fn, delimiter=","))

    def get_ue_average_reward(self, ue_id, n_average_step=1000):
        out = np.array([]).reshape((0, 3))
        i = 0

        while i < self.UE_REWARD_[ue_id].shape[0] and (i + n_average_step) <= self.UE_REWARD_[ue_id].shape[0]:
            index_low = i
            index_high = i + n_average_step
            average = np.sum(self.UE_REWARD_[ue_id][index_low:index_high, 2].astype(np.float)) / float(n_average_step)
            step = np.array(
                [self.UE_REWARD_[ue_id][index_high - 1, 0], self.UE_REWARD_[ue_id][index_high - 1, 1], average])
            out = np.vstack((out, step))
            i = i + n_average_step

        return out

    def get_ue_packet_loss(self, ue_id, n_average_step=1000):
        out = np.array([]).reshape((0, 3))
        i = 0

        while i < self.UE_REWARD_[ue_id].shape[0] and (i + n_average_step) <= self.UE_REWARD_[ue_id].shape[0]:
            index_low = i
            index_high = i + n_average_step

            this_ue_total = 0
            this_ue_total += np.sum(self.N_RLCTX_[ue_id][index_low:index_high, 2].astype(int))
            this_ue_total += np.sum(self.N_DISCARD_[ue_id][index_low:index_high, 2].astype(int))

            v = np.multiply(self.RLC_REWARD_[ue_id][index_low:index_high, 2].astype(int),
                            self.N_CH_TX_OK_[ue_id][index_low:index_high, 2].astype(int))

            this_ue_s_txed = np.sum(v)

            success_rate = float(this_ue_s_txed) / float(this_ue_total)

            step = np.array([self.UE_REWARD_[ue_id][index_high - 1, 0], self.UE_REWARD_[ue_id][index_high - 1, 1],
                             1 - success_rate])
            out = np.vstack((out, step))
            i = i + n_average_step

        return out

    def get_min_ue_average_reward(self, n_average_step=1000):
        out = np.array([]).reshape((0, 2))
        out = []
        for i in range(int(self.n_episode * self.n_step / n_average_step)):
            index_low = i * n_average_step
            index_high = i * n_average_step + n_average_step
            average_min = float('inf')
            for ue_id in range(self.n_ue):
                average = np.sum(self.UE_REWARD_[ue_id][index_low:index_high, 2].astype(np.float)) / float(
                    n_average_step)
                if average <= average_min:
                    average_min = average
            out.append(average_min)

        out = np.array(out).reshape(int(self.n_episode * self.n_step / n_average_step), 1)
        return out
