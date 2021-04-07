#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from collections import namedtuple

from sim_src.sim_env import EnvObject
from sim_src.sim_env.channel import ChannelUnknownErr, ChannelUnknownErrBinaryReward, CHANNEL_UNKNOWN_ERROR_ACTION
from sim_src.sim_env.math_models import *
from sim_src.sim_env.rlc import RlcBinaryTx, RLC_BINARY_TX_ACTION

UE_CONFIG = namedtuple("UE_CONFIG", ['channel', 'rlc', 'error_rate'])


class UserEquipement(EnvObject):
    def __init__(self, id, config):
        self.id = id
        self.config = config
        self.channel = None
        self.rlc = None

    def step(self, action):
        pass

    def get_state(self):
        pass


UE_RB_ACTION = namedtuple("UE_RB_ACTION", ['n_rb'])
UE_RB_STATE = namedtuple("UE_RB_STATE", ['n_rb', 'hol', 'q_length'])


class UeRb(UserEquipement):
    """
    the UE object:
        Action : the number of rb allocated to this UE
        State: the channel and rlc queue state
    """

    def __init__(self, id, config):
        super(UeRb, self).__init__(id, config)
        self.channel = ChannelUnknownErr(id, config.channel)
        self.rlc = RlcBinaryTx(id, config.rlc)

    def step(self, action):
        channel_action = CHANNEL_UNKNOWN_ERROR_ACTION(action.n_rb, self.config.rlc.packet_size)
        channel_reward = self.channel.step(channel_action)
        rlc_action = RLC_BINARY_TX_ACTION(action.n_rb > 0)
        hol_reward = self.rlc.step(rlc_action)
        return channel_reward * hol_reward

    def get_state(self):
        channel_state = self.channel.get_state()
        rlc_state = self.rlc.get_state()
        packet_size = self.config.rlc.packet_size
        n_rb = 0
        for x in range(MAX_NUM_RB):
            n_rb = x + 1
            e = tx_error_rate_for_n_bytes(packet_size,
                                          n_rb,
                                          db_to_dec(channel_state.snr_db),
                                          self.config.channel.T_f,
                                          self.config.channel.rb_bw)

            if e <= self.config.error_rate:
                break

        return UE_RB_STATE(n_rb, rlc_state.hol, rlc_state.n_byte)


UE_RB_MODEL_FREE_STATE = namedtuple("UE_RB_STATE", ['snr_db', 'hol', 'q_length'])


class UeRbBinaryModelFree(UeRb):
    """
    channel reward is binary
    """

    def __init__(self, id, config):
        super(UeRbBinaryModelFree, self).__init__(id, config)
        self.channel = ChannelUnknownErrBinaryReward(id, config.channel)

    def get_state(self):
        channel_state = self.channel.get_state()
        rlc_state = self.rlc.get_state()

        return UE_RB_MODEL_FREE_STATE(channel_state.snr_db, rlc_state.hol, rlc_state.n_byte)


if __name__ == '__main__':
    p_tx_s = 'a' if 1 > 0 else 'b'
    print(p_tx_s)
