#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from sim_src.config_helper.ddpg_config import *


class exp_drl_config(ddpg_config_helper):
    def __init__(self, n_ue=5, n_step=500):
        ddpg_config_helper.__init__(self, n_ue, n_step)
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

        self.critic_nn_arch = [self.N_UE * self.N_UE_INPUT + self.N_UE * self.N_UE_OUTPUT,
                               (self.N_UE * self.N_UE_INPUT + self.N_UE * self.N_UE_OUTPUT) * self.N_NODE_MUL_PER_LAYER,
                               (self.N_UE * self.N_UE_INPUT + self.N_UE * self.N_UE_OUTPUT) * self.N_NODE_MUL_PER_LAYER,
                               self.N_UE]

        self.critic_af_config = [None,
                                 nn.modules.ReLU(),
                                 nn.modules.ReLU(),
                                 None]

        self.critic_w_config = [None,
                                None,
                                3e-3]

        self.reload_config()
