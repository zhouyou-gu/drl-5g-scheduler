#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from pprint import pprint

import torch

DEBUG = True


class StatusObject:
    n_step = 0
    n_debug_step = 1000

    def status(self):
        if DEBUG:
            pprint(vars(self))

    def _print(self, *args, **kwargs):
        if DEBUG and (
                self.n_step % self.n_debug_step == 0 or self.n_step % self.n_debug_step == 1 or self.n_step % self.n_debug_step == 2):
            print(*args, **kwargs)


if __name__ == '__main__':
    s = StatusObject()
    s._print(3, 2, 'asdf')

    print("Total number of threads can be used is", torch.get_num_threads())
