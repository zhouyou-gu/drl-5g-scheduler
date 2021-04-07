#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import torch.nn as nn
import torch.optim.optimizer

from sim_src.controller import PY_SIM_CONTROLLER_CONFIG
from sim_src.model.ddpg import DDPG_CONFIG, ACTOR_CONFIG, CRITIC_CONFIG, UPDATE_CONFIG, RL_CONFIG
from sim_src.replay_memory.replay_memory import SIM_REPLAY_MEMORY_CONFIG


class ddpg_config_helper():
    def __init__(self, n_ue=5, n_step=500):
        self.N_STEP = n_step

        self.no_update = False
        self.is_soft = True
        self.tau = 1e-3
        self.C_STEP = int(5000)
        self.BATCH_SIZE = 20
        self.SEED = 0
        self.BUFFER_SIZE = int(1e4)

        self.GAMMA = 0.9

        self.N_UE = n_ue
        self.N_UE_INPUT = 2
        self.N_UE_OUTPUT = 1

        self.N_NODE_MUL_PER_LAYER = 10

        self.actor_lr = 1e-3
        self.actor_optim = torch.optim.Adam

        self.actor_nn_arch = [self.N_UE * self.N_UE_INPUT,
                              self.N_UE * self.N_UE_INPUT * self.N_NODE_MUL_PER_LAYER,
                              self.N_UE * self.N_UE_INPUT * self.N_NODE_MUL_PER_LAYER,
                              self.N_UE * self.N_UE_OUTPUT]

        self.actor_af_config = [None,
                                nn.modules.ReLU(),
                                nn.modules.ReLU(),
                                nn.modules.Tanh()]

        self.actor_w_config = [None,
                               None,
                               3e-3]

        self.actor_load_path = None

        self.critic_lr = 1e-3
        self.critic_optim = torch.optim.Adam

        self.critic_nn_arch = [self.N_UE * self.N_UE_INPUT + self.N_UE * self.N_UE_OUTPUT,
                               (self.N_UE * self.N_UE_INPUT + self.N_UE * self.N_UE_OUTPUT) * self.N_NODE_MUL_PER_LAYER,
                               (self.N_UE * self.N_UE_INPUT + self.N_UE * self.N_UE_OUTPUT) * self.N_NODE_MUL_PER_LAYER,
                               # (self.N_UE * self.N_UE_INPUT + self.N_UE * self.N_UE_OUTPUT) * self.N_NODE_MUL_PER_LAYER,
                               self.N_UE]

        self.critic_af_config = [None,
                                 nn.modules.ReLU(),
                                 nn.modules.ReLU(),
                                 # nn.modules.ReLU(),
                                 None]

        self.critic_w_config = [None,
                                None,
                                # None,
                                3e-3]

        self.critic_load_path = None

        self.reload_config()

    def reload_config(self):
        self.actor_config = ACTOR_CONFIG(self.actor_nn_arch, self.actor_af_config, self.actor_w_config, self.actor_lr,
                                         self.actor_optim, self.actor_load_path)

        self.critic_config = CRITIC_CONFIG(self.critic_nn_arch, self.critic_af_config, self.critic_w_config,
                                           self.critic_lr, self.critic_optim, self.critic_load_path)

        self.rl_config = RL_CONFIG(gamma=self.GAMMA)

        self.update_config = UPDATE_CONFIG(is_soft=self.is_soft, tau=self.tau, c_step=self.C_STEP,
                                           no_update=self.no_update)

        self.ddpg_config = DDPG_CONFIG(actor_config=self.actor_config,
                                       critic_config=self.critic_config,
                                       update_config=self.update_config,
                                       rl_config=self.rl_config)

        self.replay_memory_config = SIM_REPLAY_MEMORY_CONFIG(batch_size=self.BATCH_SIZE,
                                                             buffer_size=self.BUFFER_SIZE,
                                                             seed=self.SEED)

        self.controller_config = PY_SIM_CONTROLLER_CONFIG(c_step=self.C_STEP,
                                                          total_step=self.N_STEP)


if __name__ == '__main__':
    c = ddpg_config_helper()
