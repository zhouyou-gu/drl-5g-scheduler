#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from collections import namedtuple

import numpy as np
import torch.nn as nn

NN_CONFIG = namedtuple("NN_CONFIG", ['nn_arch', 'af_config', 'init_w', 'lr', 'optim', 'load_path'])


class Net(nn.Module):
    def __init__(self, nn_arch=None, af_config=None, init_w=None):
        super(Net, self).__init__()
        assert len(nn_arch) >= 2, "At least 2 layer NN is required"
        assert len(af_config) == len(nn_arch), "af_config size %s should equals nn_arch _size %s!!" % (
            af_config, nn_arch)
        assert len(init_w) == len(nn_arch) - 1, "init_w size %s should equals nn_arch _size - 1 %s!!" % (
            init_w, nn_arch)

        # self.bn = torch.nn.BatchNorm1d(nn_config[0])

        self.fc = nn.ModuleList()
        for x in range(0, len(af_config) - 1):
            if af_config[x] is not None:
                self.fc.append(af_config[x])
            self.fc.append(nn.Linear(nn_arch[x], nn_arch[x + 1]))
            if init_w[x] is not None:
                self.fc[-1].weight.data.uniform_(-init_w[x], init_w[x])
            else:
                s = self.fc[-1].weight.data.size()[0]
                s = 1. / np.sqrt(s)
                self.fc[-1].weight.data.uniform_(-s, s)

        if af_config[len(af_config) - 1] is not None:
            self.fc.append(af_config[len(af_config) - 1])

    def forward(self, x):
        for f in range(0, len(self.fc)):
            x = self.fc[f](x)
        return x


if __name__ == '__main__':
    nc = NN_CONFIG(nn_arch=[10, 100, 10], af_config=[None, nn.modules.ReLU(), nn.modules.ReLU()], init_w=[None, None],
                   lr=0.1, optim=None, load_path=None)

    nn = Net(nc.nn_arch, nc.af_config, nc.init_w)
    nn.to(torch.cuda.current_device())
    print(next(nn.parameters()).device)
