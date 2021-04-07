#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from collections import deque
from collections import namedtuple

from sim_src import StatusObject
from sim_src.sim_env import EnvObject
from sim_src.sim_env.math_models import *
from sim_src.tb_logger import GLOBAL_LOGGER
from sim_src.util import *

RLC_CONFIG = namedtuple("RLC_CONFIG", ['packet_size', 'max_size', 'packet_p', 'd_min', 'd_max', 'hol_reward_f'])
RLC_STATE = namedtuple("RLC_STATE", ['n_packet', 'hol', 'n_byte'])


class Rlc(EnvObject):
    def __init__(self, id, config):
        self.id = id
        self.config = config
        self.packet = namedtuple("Packet", ['time', 'packet_size'])
        self.queue = deque(maxlen=config.max_size)
        self.time_step = 0

        self.n_packet = 0

    def get_state(self):
        return RLC_STATE(n_packet=len(self.queue),
                         hol=self.get_hol(),
                         n_byte=self.get_n_byte_total())

    def step(self, action):
        pass

    def get_hol(self):
        if self.queue:
            return self.time_step - self.queue[0].time
        else:
            return 0

    def get_hol_packet_size(self):
        if self.queue:
            return self.queue[0].packet_size
        else:
            return 0

    def pop(self):
        if self.queue:
            self.queue.popleft()

    def push(self):
        """
        :return: the number of packet is discard
        """
        if p_true(self.config.packet_p):
            self.n_packet += 1
            if len(self.queue) == self.queue.maxlen:
                return 1
            else:
                self.queue.append(self.packet(self.time_step, self.config.packet_size))
                return 0
        return 0

    def discard(self):
        n_discard = 0
        while self.queue and self.get_hol() > self.config.d_max:
            self.queue.popleft()
            n_discard += 1
        return n_discard

    def get_n_byte_total(self):
        ret = 0
        for x in range(len(self.queue)):
            ret += self.queue[x].packet_size

        return ret


RLC_BINARY_TX_ACTION = namedtuple("RLC_BINARY_TX_ACTION", ['tx'])


class RlcBinaryTx(Rlc):
    def __init__(self, id, config):
        super(RlcBinaryTx, self).__init__(id, config)
        StatusObject.__init__(self)

    @counted
    def step(self, action):
        ret = 0.
        n_txed = 0
        if action.tx:
            ret = self.get_hol_reward()
            if self.queue:
                GLOBAL_LOGGER.get_tb_logger().add_scalar('TX_DELAY_' + str(self.id), self.get_hol(), self.n_step)
                n_txed = 1
            self.pop()
        GLOBAL_LOGGER.get_tb_logger().add_scalar('N_RLCTX_' + str(self.id), n_txed, self.n_step)

        n_discard = self.push()
        GLOBAL_LOGGER.get_tb_logger().add_scalar('N_PACKET_' + str(self.id), self.n_packet, self.n_step)

        # assuming packet is arrived at the end of the last TTI
        self.time_step += 1

        n_discard += self.discard()

        GLOBAL_LOGGER.get_tb_logger().add_scalar('N_DISCARD_' + str(self.id), n_discard, self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('RLC_REWARD_' + str(self.id), ret, self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('HOL_' + str(self.id), self.get_hol(), self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('Qsize_' + str(self.id), self.get_n_byte_total(), self.n_step)
        return ret

    def get_hol_reward(self):
        if self.config.hol_reward_f is None:
            if self.queue and self.get_hol() <= self.config.d_max and self.get_hol() >= self.config.d_min:
                return 1.
            else:
                return 0.
        else:
            if self.queue:
                return self.config.hol_reward_f(self.get_hol(), self.config.d_min, self.config.d_max)
            else:
                return 0.


if __name__ == '__main__':
    q = deque(maxlen=5)
    for x in range(7):
        q.append(x)
        print(q)

# config = RLC_CONFIG(packet_size=100,max_size=5,packet_p=0.6,d_min=10,d_max=20)
# a = RlcBinaryTx(0,config)
# b = RlcBinaryTx(1,config)
# GLOBAL_LOGGER.set_log_path("/tmp/","hello_test/","rlc_test")
# GLOBAL_LOGGER.get_tb_logger().add_scalar('test',0, 0)
# for s in range(100000):
# 	print(a.get_state())
# 	action = RLC_BINARY_TX_ACTION(True)
# 	print(a.step(action),a.n_step)
# 	print(b.get_state())
# 	action = RLC_BINARY_TX_ACTION(True)
# 	print(b.step(action),b.n_step)
#
# GLOBAL_LOGGER.close_logger()
