#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import math
import os

from torch import nn

from exp_src.exp_config import exp_drl_config
from exp_src.rt_agent import RTAgent
from sim_src.controller import ExpController
from sim_src.model.ddpg import MultiHeadCriticDDPG
from sim_src.replay_memory.replay_memory import SimReplayMemory
from sim_src.sim_env.action_noise import *
from sim_src.tb_logger import GLOBAL_LOGGER

drl_c = exp_drl_config(2, int(1e9))
drl_c.actor_lr = 1e-4
drl_c.critic_lr = 1e-4
dir = os.path.dirname(os.path.abspath(__file__))
dir = os.path.join(dir, 'example_nn')
drl_c.actor_load_path = os.path.join(dir, 'actor_0.pt')
drl_c.critic_load_path = os.path.join(dir, 'critic_0.pt')

drl_c.reload_config()

assert isinstance(drl_c.actor_config.af_config[-1], nn.modules.Tanh)

log_path = os.path.dirname(os.path.realpath(__file__))
folder_name = "online/"
experiment_name = "online_example"
GLOBAL_LOGGER.set_log_path(log_path, folder_name, experiment_name)

rm = SimReplayMemory(0, drl_c.replay_memory_config)

nf = None
# def noise_f(p, t_now, t_start):
#     return p + 0.1 * p * np.random.randn() * math.exp(- (t_now - t_start) / 60)
#
# nf = noise_f

rt_agent = RTAgent(0, None, '0.0.0.0', 4000, drl_c.actor_config, GLOBAL_LOGGER, nf)
rt_agent.set_replay_memory(rm)

ddpg = MultiHeadCriticDDPG(0, drl_c.ddpg_config)

ddpg.set_actor_target(os.path.join(dir, 'actor_target_0.pt'))
ddpg.set_critic_target(os.path.join(dir, 'critic_target_0.pt'))

controller = ExpController(0, drl_c.controller_config, rt_agent, ddpg, rm)

controller.start()
controller.join()

rt_agent.join()
