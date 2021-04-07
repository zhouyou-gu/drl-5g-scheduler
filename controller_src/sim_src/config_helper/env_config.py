#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from sim_src.sim_env.action_noise import *
from sim_src.sim_env.channel import CHANNEL_CONFIG
from sim_src.sim_env.reward_functions import *
from sim_src.sim_env.rlc import RLC_CONFIG
from sim_src.sim_env.sim_agent import SIM_AGENT_CONFIG
from sim_src.sim_env.sim_env import SIM_ENV_CONFIG
from sim_src.sim_env.user_equipment import UE_CONFIG


class env_config_helper():
    def __init__(self):
        np.random.seed(int(time()))
        self.N_UE = 5
        self.N_EPISODE = 1000
        self.N_STEP = 200  # gamma 0.9 thus reward at 50 slots later will be 5e-3

        self.ERROR_RATE = 1e-5
        self.PACKET_SIZE = 32
        self.p = 0.1
        self.D_MIN = 5
        self.D_MAX = 6

        self.TOTAL_N_RB = 50

        self.T_f = 1.25e-4
        self.rb_bw = 180e3

        assert self.D_MIN <= self.D_MAX

        self.D_MIN_to_D_MAX_pct = float(self.D_MIN) / float(self.D_MAX)

    def reload_config(self):
        self.rlc_config = RLC_CONFIG(packet_size=self.PACKET_SIZE,
                                     max_size=100,
                                     packet_p=self.p,
                                     d_min=self.D_MIN,
                                     d_max=self.D_MAX,
                                     hol_reward_f=hol_flat_reward)

        # max=100-200 is a reasonable range
        self.channel_config = CHANNEL_CONFIG(max_dis=100,
                                             step_dis=5,
                                             move_p=1e-4,
                                             tx_power=20,
                                             noise_power=-90,
                                             T_f=self.T_f,
                                             rb_bw=self.rb_bw,
                                             total_n_rb=self.TOTAL_N_RB)

        self.ue_config = UE_CONFIG(channel=self.channel_config,
                                   rlc=self.rlc_config,
                                   error_rate=self.ERROR_RATE)

        self.sim_env_config = SIM_ENV_CONFIG(n_ue=self.N_UE,
                                             n_episode=self.N_EPISODE,
                                             n_step=self.N_STEP,
                                             ue_config=self.ue_config,
                                             action_conversion_f=None)

        self.noise_config = OU_ACTION_NOISE_CONFIG(mu=0., n_action=self.N_UE, theta=1, sigma=0.4)

        self.agent_config = SIM_AGENT_CONFIG(noise_config=self.noise_config, noise_attenuation=0.)
