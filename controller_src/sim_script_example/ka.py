#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from sim_src.config_helper.ddpg_config import *
from sim_src.config_helper.env_config import *
from sim_src.controller import PySimController
from sim_src.model.ddpg import MultiHeadCriticDDPG_NEW_PER
from sim_src.replay_memory.per_proportional import PER_PROPORTIONAL_REPLAY_MEMORY_CONFIG, PERProportional
from sim_src.sim_env.sim_agent import SimAgent
from sim_src.sim_env.sim_env import SimEnvTxBinary_RewardShaping
from sim_src.tb_logger import GLOBAL_LOGGER

env_c = env_config_helper()
drl_c = ddpg_config_helper(env_c.N_UE, env_c.N_STEP * env_c.N_EPISODE)

env_c.reload_config()
drl_c.reload_config()

import os

log_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
folder_name = "tb-data"
experiment_name = "ka"
GLOBAL_LOGGER.set_log_path(log_path, folder_name, experiment_name)
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
GLOBAL_LOGGER.get_tb_logger().set_scalar_filter(scalar_list)
rm_config = PER_PROPORTIONAL_REPLAY_MEMORY_CONFIG(batch_size=drl_c.BATCH_SIZE, buffer_size=drl_c.BUFFER_SIZE,
                                                  seed=drl_c.SEED, alpha=0.7, total_step=env_c.N_EPISODE * env_c.N_STEP)
rm = PERProportional(0, rm_config)

agent = SimAgent(0, env_c.agent_config, rm)

env = SimEnvTxBinary_RewardShaping(0, env_c.sim_env_config, agent)

ddpg = MultiHeadCriticDDPG_NEW_PER(0, drl_c.ddpg_config)
ddpg.threshold = env_c.D_MIN_to_D_MAX_pct

controller = PySimController(0, drl_c.controller_config, agent, ddpg, rm)

env.start()
controller.start()

env.join()
controller.join()
GLOBAL_LOGGER.close_logger()
