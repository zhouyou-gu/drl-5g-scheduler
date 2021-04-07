#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

# TODO: add support for different af at the last layer (currently is only for tanh [-1,1])
from collections import namedtuple
from threading import Thread

from sim_src.sim_env import EnvObject, StatusObject
from sim_src.sim_env.sim_agent import SimAgent
from sim_src.sim_env.user_equipment import UeRb, UeRbBinaryModelFree, UE_RB_ACTION
from sim_src.tb_logger import GLOBAL_LOGGER
from sim_src.util import *

SIM_ENV_CONFIG = namedtuple("SIM_ENV_CONFIG", ['n_ue', 'n_episode', 'n_step', 'ue_config', 'action_conversion_f'])


class SimEnv(EnvObject):
    def __init__(self, id, config, agent):
        StatusObject.__init__(self)
        self.id = id
        self.agent = agent
        self.config = config
        self.ue_list = None
        self.tmp_state = []

    def init_env(self):
        pass

    def get_state(self):
        pass

    def step(self, action):
        pass


class SimEnvTxBinary(SimEnv, Thread):
    def __init__(self, id, config, agent):
        Thread.__init__(self)
        SimEnv.__init__(self, id, config, agent)
        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("ENV_CONFIG", self.config)

    def init_env(self):
        self.ue_list = []
        for u in range(self.config.n_ue):
            self.ue_list.append(UeRb(u, self.config.ue_config))
        self.tmp_state = []

    def get_state(self):
        self.tmp_state = []
        for u in range(self.config.n_ue):
            self.tmp_state.append(self.ue_list[u].get_state())

        state_number = []
        for u in range(self.config.n_ue):
            pct = float(self.tmp_state[u].hol) / float(self.config.ue_config.rlc.d_max)
            state_number.append(pct)

        for u in range(self.config.n_ue):
            pct = float(self.tmp_state[u].n_rb) / float(self.config.ue_config.channel.total_n_rb)
            state_number.append(pct)

        state = np.array(state_number, dtype=float)
        return state

    @counted
    def step(self, action):
        total_reward = 0.0
        rewards = []
        total_rb = 0.0
        for u in range(self.config.n_ue):
            a_n_rb = self.tmp_state[u].n_rb
            GLOBAL_LOGGER.get_tb_logger().add_scalar('required_n_rb.' + str(u), a_n_rb, self.n_step)
            if action[u] == 1 and self.tmp_state[u].q_length:
                total_rb += a_n_rb
        if total_rb <= self.config.ue_config.channel.total_n_rb:
            total_rb = self.config.ue_config.channel.total_n_rb

        for u in range(self.config.n_ue):
            if action[u] == 1 and self.tmp_state[u].q_length > 0:
                n_rb = round(float(self.tmp_state[u].n_rb) / total_rb * self.config.ue_config.channel.total_n_rb)
                GLOBAL_LOGGER.get_tb_logger().add_scalar('A_NRB_' + str(u), n_rb, self.n_step)
                r = self.ue_list[u].step(UE_RB_ACTION(n_rb))
                total_reward += r
                GLOBAL_LOGGER.get_tb_logger().add_scalar('UE_REWARD_' + str(u), r, self.n_step)
            else:
                self.ue_list[u].step(UE_RB_ACTION(0))
                r = 0
                GLOBAL_LOGGER.get_tb_logger().add_scalar('UE_REWARD_' + str(u), 0, self.n_step)

            rewards.append(r)

        GLOBAL_LOGGER.get_tb_logger().add_scalar('ENV_REWARD', total_reward, self.n_step)
        return np.array(rewards, dtype=float)

    def run(self):
        rewards_his = np.zeros(self.config.n_ue)
        total_reward_his = 0
        for e in range(self.config.n_episode):
            self.init_env()
            for t in range(self.config.n_step):
                state = self.get_state()
                action = self.agent.get_action(state)
                action_ = np.copy(action)
                if self.config.action_conversion_f is None:
                    action_[action_ > 0.] = 1
                    action_[action_ <= 0.] = 0
                else:
                    action_ = self.config.action_conversion_f(action_)
                rewards = self.step(action_)

                rewards_his = 0.99 * rewards_his + 0.01 * rewards
                for i in range(self.config.n_ue):
                    GLOBAL_LOGGER.get_tb_logger().add_scalar('UE_REWARD.moving_avg.' + str(i), rewards_his[i],
                                                             self.n_step)

                total_reward = np.sum(rewards)
                total_reward_his = 0.99 * total_reward_his + 0.01 * total_reward

                GLOBAL_LOGGER.get_tb_logger().add_scalar('ENV_REWARD.moving_avg', total_reward_his, self.n_step)

                next_state = self.get_state()
                done = 0
                if t == self.config.n_step - 1:
                    done = 1
                self.agent.save_step(state, action, rewards, next_state, done)


class SimEnvTxBinary_RewardShaping(SimEnvTxBinary):
    phi = np.array([0., 0., 0.25, 0.5, 0.75, 1., 1.])
    gamma = 0.9

    def run(self):
        rewards_his = np.zeros(self.config.n_ue)
        total_reward_his = 0
        for e in range(self.config.n_episode):
            self.init_env()
            for t in range(self.config.n_step):
                state = self.get_state()
                action = self.agent.get_action(state)
                action_ = np.copy(action)
                phi = self.get_phi()

                if self.config.action_conversion_f is None:
                    action_[action_ > 0.] = 1
                    action_[action_ <= 0.] = 0
                else:
                    action_ = self.config.action_conversion_f(action_)
                rewards = self.step(action_)

                rewards_his = 0.99 * rewards_his + 0.01 * rewards
                for i in range(self.config.n_ue):
                    GLOBAL_LOGGER.get_tb_logger().add_scalar('UE_REWARD.moving_avg.' + str(i), rewards_his[i],
                                                             self.n_step)

                total_reward = np.sum(rewards)
                total_reward_his = 0.99 * total_reward_his + 0.01 * total_reward

                GLOBAL_LOGGER.get_tb_logger().add_scalar('ENV_REWARD.moving_avg', total_reward_his, self.n_step)

                next_state = self.get_state()
                phi_next = self.get_phi()
                shaper = - 1. * (phi - self.gamma * phi_next)
                for i in range(self.config.n_ue):
                    GLOBAL_LOGGER.get_tb_logger().add_scalar('shaper.' + str(i), shaper[i],
                                                             self.n_step)

                done = 0
                if t == self.config.n_step - 1:
                    done = 1
                self.agent.save_step(state, action, rewards + shaper, next_state, done)

    def get_phi(self):
        phi_list = []
        for u in range(self.config.n_ue):
            phi_list.append(self.phi[self.tmp_state[u].hol])
        return np.array(phi_list, dtype=float)


class AsyncEnv(SimEnvTxBinary):
    def run(self):
        rewards_his = np.zeros(self.config.n_ue)
        total_reward_his = 0
        for e in range(self.config.n_episode):
            self.init_env()
            for t in range(self.config.n_step):
                state = self.get_state()
                action = self.agent.get_action(state)
                action_ = np.copy(action)
                if self.config.action_conversion_f is None:
                    action_[action_ > 0.] = 1
                    action_[action_ <= 0.] = 0
                else:
                    action_ = self.config.action_conversion_f(action_)
                rewards = self.step(action_)

                rewards_his = 0.99 * rewards_his + 0.01 * rewards
                for i in range(self.config.n_ue):
                    GLOBAL_LOGGER.get_tb_logger().add_scalar('UE_REWARD.moving_avg.' + str(i), rewards_his[i],
                                                             self.n_step)

                total_reward = np.sum(rewards)
                total_reward_his = 0.99 * total_reward_his + 0.01 * total_reward

                GLOBAL_LOGGER.get_tb_logger().add_scalar('ENV_REWARD.moving_avg', total_reward_his, self.n_step)

                next_state = self.get_state()
                done = 0
                if t == self.config.n_step - 1:
                    done = 1
                self.agent.save_step(state, action, rewards, next_state, done, asynchronization=True)


class SimEnvModelFree(SimEnv, Thread):
    def __init__(self, id, config, agent):
        Thread.__init__(self)
        SimEnv.__init__(self, id, config, agent)
        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("ENV_CONFIG", self.config)

    def init_env(self):
        self.ue_list = []
        for u in range(self.config.n_ue):
            self.ue_list.append(UeRbBinaryModelFree(u, self.config.ue_config))
        self.tmp_state = []

    def get_state(self):
        self.tmp_state = []
        for u in range(self.config.n_ue):
            self.tmp_state.append(self.ue_list[u].get_state())

        state_number = []
        for u in range(self.config.n_ue):
            pct = float(self.tmp_state[u].hol) / float(self.config.ue_config.rlc.d_max)
            state_number.append(pct)

        for u in range(self.config.n_ue):
            pct = float(self.tmp_state[u].snr_db) / float(30)
            state_number.append(pct)

        state = np.array(state_number, dtype=float)
        return state

    @counted
    def step(self, action):
        '''

        :param action: 0 or 1 for Tx binary,  0~1 for the percentage of RBs
        :return:
        '''
        total_reward = 0.0
        rewards = []
        total_rb_pct = 0.0
        for u in range(self.config.n_ue):
            a_n_rb = action[u] * self.config.ue_config.channel.total_n_rb
            GLOBAL_LOGGER.get_tb_logger().add_scalar('required_n_rb.' + str(u), a_n_rb, self.n_step)
            total_rb_pct += action[u]
        if total_rb_pct < 1.:
            total_rb_pct = 1.
        for u in range(self.config.n_ue):
            if int(action[u] * self.config.ue_config.channel.total_n_rb) > 0 and self.tmp_state[u].q_length > 0:
                n_rb = round(float(action[u]) / total_rb_pct * self.config.ue_config.channel.total_n_rb)
                GLOBAL_LOGGER.get_tb_logger().add_scalar('A_NRB_' + str(u), n_rb, self.n_step)
                r = self.ue_list[u].step(UE_RB_ACTION(n_rb))
                total_reward += r
                GLOBAL_LOGGER.get_tb_logger().add_scalar('UE_REWARD_' + str(u), r, self.n_step)
            else:
                self.ue_list[u].step(UE_RB_ACTION(0))
                r = 0
                GLOBAL_LOGGER.get_tb_logger().add_scalar('UE_REWARD_' + str(u), 0, self.n_step)

            rewards.append(r)

        GLOBAL_LOGGER.get_tb_logger().add_scalar('ENV_REWARD', total_reward, self.n_step)
        return np.array(rewards, dtype=float)

    def run(self):
        rewards_his = np.zeros(self.config.n_ue)
        total_reward_his = 0
        for e in range(self.config.n_episode):
            self.init_env()
            for t in range(self.config.n_step):
                state = self.get_state()
                action = self.agent.get_action(state)
                action_ = np.copy(action)
                if self.config.action_conversion_f is None:
                    for u in range(self.config.n_ue):
                        if (action_[u] > 1.):
                            action_[u] = 1.
                else:
                    action_ = self.config.action_conversion_f(action_)
                rewards = self.step(action_)

                rewards_his = 0.99 * rewards_his + 0.01 * rewards
                for i in range(self.config.n_ue):
                    GLOBAL_LOGGER.get_tb_logger().add_scalar('UE_REWARD.moving_avg.' + str(i), rewards_his[i],
                                                             self.n_step)

                total_reward = np.sum(rewards)
                total_reward_his = 0.99 * total_reward_his + 0.01 * total_reward

                GLOBAL_LOGGER.get_tb_logger().add_scalar('ENV_REWARD.moving_avg', total_reward_his, self.n_step)

                next_state = self.get_state()
                done = 0
                if t == self.config.n_step - 1:
                    done = 1
                self.agent.save_step(state, action, rewards, next_state, done)


if __name__ == '__main__':
    print(SIM_ENV_CONFIG)
    a = SimAgent(0, None, None)
    a.status()
    print(a)
    a = [1, 2, 3, 4]
    print(np.array(a, dtype=float))
