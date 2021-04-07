#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import random
from collections import namedtuple

from scipy.stats import rice

from sim_src.sim_env import EnvObject, StatusObject
from sim_src.sim_env.math_models import *
from sim_src.tb_logger import GLOBAL_LOGGER
from sim_src.util import *

CHANNEL_CONFIG = namedtuple("CHANNEL_CONFIG",
                            ['max_dis', 'step_dis', 'move_p', 'tx_power', 'noise_power', 'T_f', 'rb_bw', 'total_n_rb'])
CHANNEL_STATE = namedtuple("CHANNEL_STATE", ['snr_db'])


class Channel(EnvObject):
    def __init__(self, id, config):
        self.id = id
        self.config = config
        self.dis = 0
        self.init_distance()

        self.scale = 0.559
        self.shape = 0.612 / self.scale
        self.small_scale_gain = rice.rvs(self.shape, scale=self.scale)

    def get_state(self):
        return CHANNEL_STATE(self.get_snr_db())

    def step(self, action):
        pass

    def change_position(self):
        if p_true(self.config.move_p):
            if p_true(0.5):
                self.increase_distance()
            else:
                self.decrease_distance()
        # small scale channel gain. 20% to be changed
        if p_true(0.2):
            self.small_scale_gain = rice.rvs(self.shape, scale=self.scale)

    def get_snr_db(self) -> float:
        # large scale channel gain
        snr = distance_to_snr(self.dis, self.config.tx_power, self.config.noise_power)

        snr += dec_to_db(self.small_scale_gain)

        if snr > 20.:
            return 20.
        # TODO: handling out-of-range
        # elif snr < -5.:
        # 	return -5.
        else:
            return snr

    # return distance_to_snr(self.dis,self.config.tx_power,self.config.noise_power)

    def init_distance(self):
        initial_steps = random.randint(0, int(self.config.max_dis / self.config.step_dis))
        for x in range(initial_steps):
            self.increase_distance()

    def increase_distance(self):
        if self.dis + self.config.step_dis <= self.config.max_dis:
            self.dis += self.config.step_dis

    def decrease_distance(self):
        if self.dis - self.config.step_dis >= 0:
            self.dis -= self.config.step_dis


CHANNEL_UNKNOWN_ERROR_ACTION = namedtuple("CHANNEL_UNKNOWN_ERROR_ACTION", ['n_rb', 'n_byte'])


class ChannelUnknownErr(Channel):
    '''
    A channel object
        Action: the number of RB, the number of bytes
        Reward: 1 - tx error rate
    '''

    def __init__(self, id, config):
        super(ChannelUnknownErr, self).__init__(id, config)
        StatusObject.__init__(self)

    @counted
    def step(self, action):
        err = 0.
        if action.n_rb > 0:
            err = tx_error_rate_for_n_bytes(action.n_byte, action.n_rb, db_to_dec(self.get_snr_db()), self.config.T_f,
                                            self.config.rb_bw)

            if action.n_rb >= self.config.total_n_rb and err < 1e-5:
                err = 1e-5
            if err < 1e-5:
                ret = 5.
            else:
                ret = - math.log10(err)
        else:
            ret = 0.

        n_successful_tx = 1
        if p_true(err):
            n_successful_tx = 0

        GLOBAL_LOGGER.get_tb_logger().add_scalar('NRB_' + str(self.id), action.n_rb, self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('SNR_' + str(self.id), self.get_snr_db(), self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('E_' + str(self.id), err, self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('DIS_' + str(self.id), self.dis, self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('CH_REWARD_' + str(self.id), ret, self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('N_CH_TX_OK_' + str(self.id), n_successful_tx, self.n_step)
        self.change_position()

        return ret


class ChannelUnknownErrBinaryReward(Channel):
    '''
    reward is a binary indicator to show whether the packet is transmitted or not
    '''

    def __init__(self, id, config):
        super(ChannelUnknownErrBinaryReward, self).__init__(id, config)
        StatusObject.__init__(self)

    @counted
    def step(self, action):
        err = 0.
        if action.n_rb > 0:
            err = tx_error_rate_for_n_bytes(action.n_byte, action.n_rb, db_to_dec(self.get_snr_db()), self.config.T_f,
                                            self.config.rb_bw)

            if action.n_rb >= self.config.total_n_rb and err < 1e-5:
                err = 1e-5
            if err < 1e-5:
                ret = 5.
            else:
                ret = - math.log10(err)
        else:
            ret = 0.

        n_successful_tx = 1
        if p_true(err):
            n_successful_tx = 0

        GLOBAL_LOGGER.get_tb_logger().add_scalar('NRB_' + str(self.id), action.n_rb, self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('SNR_' + str(self.id), self.get_snr_db(), self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('E_' + str(self.id), err, self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('DIS_' + str(self.id), self.dis, self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('CH_REWARD_' + str(self.id), ret, self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('N_CH_TX_OK_' + str(self.id), n_successful_tx, self.n_step)
        self.change_position()

        return float(n_successful_tx)


if __name__ == '__main__':
    # err = tx_error_rate_for_n_bytes(32, 6, 1.0221785259170593, 0.000125, 180000.0)
    # print(err)

    for x in range(50):
        err = tx_error_rate_for_n_bytes(50., x + 1, db_to_dec(0), 1e-4, 180e3)
        print(err, x)

    from scipy.stats import expon
    import matplotlib.pyplot as plt

    scale = 0.559
    shape = 0.612 / scale
    print(rice.rvs(shape, scale=scale))
    fig, ax = plt.subplots(1, 1)
    x = np.linspace(rice.ppf(0.0001, shape, scale=scale), rice.ppf(0.9999, shape, scale=scale), 10000)
    ax.plot(x, rice.pdf(x, shape, scale=scale), 'r-', label='rice pdf')
    x = np.linspace(expon.ppf(0.01),
                    expon.ppf(0.99), 100)
    ax.plot(x, expon.pdf(x),
            'r-', lw=5, alpha=0.6, label='expon pdf')
    print(rice.rvs(shape, scale=scale))
    plt.show()
