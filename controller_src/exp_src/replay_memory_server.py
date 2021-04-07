#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import numpy as np
from google.protobuf.any_pb2 import Any

from exp_src.sctp_server import SctpServer
from exp_src.socket_conn_handler import ConnListener
from proto_py.transition_pb2 import enb_transition


class TransitionLister(ConnListener):
    def __init__(self, conn, replay_memory, logger):
        ConnListener.__init__(self, 'TransitionLister', conn)
        self.logger = logger
        self.replay_memory = replay_memory

    def process_data(self, data):
        t = enb_transition()
        any = Any()
        any.ParseFromString(data)
        if any.Is(t.DESCRIPTOR):
            any.Unpack(t)
            self.log_transition(t)

            state = []
            for u in t.transition:
                state.append(u.state[0])
            for u in t.transition:
                state.append(u.state[1])

            state = np.array(state, dtype=float)

            next_state = []
            for u in t.transition:
                next_state.append(u.next_state[0])
            for u in t.transition:
                next_state.append(u.next_state[1])
            next_state = np.array(next_state, dtype=float)

            action = []
            for u in t.transition:
                action.append(u.action[0])
            action = np.array(action, dtype=float)

            reward = []
            for u in t.transition:
                reward.append(u.reward)
            reward = np.array(reward, dtype=float)

            if self.replay_memory:
                self.replay_memory.save_step(state, action, reward, next_state, 0, asynchronization=True)
            else:
                print("Warning ---- ReplayMemoryServer: replay_memory is None")
            return

    def log_transition(self, t):
        total_rwd = 0.
        u_id = 0
        for u in t.transition:
            print(t.tti,u.__str__().replace('\n', ''))
            if u.state[0] > 0.:
                self.logger.get_tb_logger().add_scalar('rwd.' + str(u_id), u.reward, t.tti,
                                                       float(t.timestamp.ToMicroseconds()) / 1e6)
                self.logger.get_tb_logger().add_scalar('hol.' + str(u_id), u.state[0], t.tti,
                                                       float(t.timestamp.ToMicroseconds()) / 1e6)
                self.logger.get_tb_logger().add_scalar('cqi.' + str(u_id), u.state[1], t.tti,
                                                       float(t.timestamp.ToMicroseconds()) / 1e6)
                self.logger.get_tb_logger().add_scalar('act.' + str(u_id), u.action[0], t.tti,
                                                       float(t.timestamp.ToMicroseconds()) / 1e6)
            total_rwd += u.reward
            u_id += 1

        self.logger.get_tb_logger().add_scalar('ENB_rwd', total_rwd, t.tti,
                                               float(t.timestamp.ToMicroseconds()) / 1e6)


class ReplayMemoryServer(SctpServer):
    def __init__(self, server_bind_ip, server_bind_port, replay_memory, logger):
        SctpServer.__init__(self, 'ReplayMemoryServer', server_bind_ip, server_bind_port, 10)
        self.replay_memory = replay_memory
        self.logger = logger
        self.transition_listener_thread_list = []

    def connection_handler(self, conn):
        print('ReplayMemoryServer get conn from', conn)
        c = TransitionLister(conn, self.replay_memory, self.logger)
        c.start()
        self.transition_listener_thread_list.append(c)


if __name__ == '__main__':
    t = enb_transition()
    t.tti = 1
    t.timestamp.seconds = 10
    t.timestamp.nanos = 112310
    u = t.transition.add()
    u.rnti = 47
    u.id = 1
    u.reward = 129.
    u.state.append(5)
    u.action.append(6)
    u.next_state.append(7)
    u = t.transition.add()

    print(t)
