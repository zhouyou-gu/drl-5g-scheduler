#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import time
from threading import Lock

import numpy as np
import pandas as pd
from google.protobuf.any_pb2 import Any

from exp_src.replay_memory_server import ReplayMemoryServer
from exp_src.sctp_server import SctpServer
from exp_src.socket_conn_handler import ConnSender
from proto_py.update_weight_pb2 import update_model_weight, model_weight
from proto_py.nn_config_pb2 import nn_config
from sim_src.sim_env.sim_agent import ControllerToAgentInterface
from sim_src.util import to_numpy, to_tensor


def nn_config_to_proto_msg(name: str, config):
    import torch.nn as nn
    n = nn_config()
    n.name = name
    n.nn_arch[:] = config.nn_arch
    for af in config.af_config:
        if isinstance(af, nn.ReLU):
            n.af_config.append(nn_config.RELU)
        elif isinstance(af, nn.Tanh):
            n.af_config.append(nn_config.TANH)
        elif isinstance(af, nn.Sigmoid):
            n.af_config.append(nn_config.SIGMOID)
        else:
            n.af_config.append(nn_config.NONE)
    return n


def get_tensor_idx_value_list(net):
    tensor_list = np.array([]).reshape((0, 5))
    tensor_idx = 0
    for xx in net.parameters():
        x = to_numpy(xx)
        df = pd.DataFrame(x)
        df = df.unstack().reset_index()
        df.columns.name = None
        dimensions = np.full((df.values.shape[0], 1), xx.ndim)
        o = df.values
        o = np.hstack((dimensions, o))
        idxs = np.full((o.shape[0], 1), tensor_idx)
        o = np.hstack((idxs, o))
        tensor_list = np.vstack((tensor_list, o))
        tensor_idx += 1

    return tensor_list, tensor_idx


class ActorUpdater(ConnSender):
    def __init__(self, conn, nn_config):
        ConnSender.__init__(self, 'ActorUpdater', conn)
        self.lock = Lock()
        self.nn_config = nn_config

        self.actor = None
        self.weight_idx = 0
        self.total_n_weight = 0
        self.MAX_N_WEIGHT_PER_PACKET = 10

        self.actor_tensor_list = None
        self.actor_n_tensor = 0

        self.start_time = time.time()

        self.param_space_noise_function = None

    def set_param_space_noise_function(self, f):
        self.param_space_noise_function = f

    def do_sending(self):
        self.send_config()

        while self.send_update_weight() > 0:
            pass

        self.conn.close()

    def update_actor(self, actor):
        with self.lock:
            self.actor = actor
            self.total_n_weight = sum(p.numel() for p in self.actor.parameters())
            self.actor_tensor_list, self.actor_n_tensor = get_tensor_idx_value_list(self.actor)

    def send_config(self):
        n = self.get_nn_config()
        any = Any()
        any.Pack(n)
        return self.send(any.SerializeToString())

    def send_update_weight(self):
        u = self.get_update_model_weight()
        if u:
            any = Any()
            any.Pack(u)
            return self.send(any.SerializeToString())
        else:
            return 0

    def get_nn_config(self):
        return nn_config_to_proto_msg('actor', self.nn_config)

    def get_update_model_weight(self):
        w = update_model_weight()
        w.name = 'actor'
        w.nn_config.CopyFrom(self.get_nn_config())
        w.n_tensor_in_model = self.actor_n_tensor
        counter = 0
        while counter < self.MAX_N_WEIGHT_PER_PACKET and self.weight_idx < self.actor_tensor_list.shape[0]:
            p = self.actor_tensor_list[self.weight_idx]
            ww = model_weight()
            ww.tensor_index = int(p[0])
            ww.n_dim = int(p[1])
            ww.x_index = int(p[3])  # p[3] is x index
            ww.y_index = int(p[2])  # p[2] is y index
            if self.param_space_noise_function:
                ww.value = self.param_space_noise_function(float(p[4]), time.time(), self.start_time)
            else:
                ww.value = float(p[4])
            ww.tau = float(1)
            w.weight.append(ww)
            counter += 1
            self.weight_idx += 1

        if self.weight_idx >= self.actor_tensor_list.shape[0]:
            self.weight_idx = 0
        return w


class RTAgent(SctpServer, ControllerToAgentInterface):
    def __init__(self, id, config, server_bind_ip, server_bind_port, nn_config, logger, noise_f=None):
        SctpServer.__init__(self, 'RTController', server_bind_ip, server_bind_port, 10)
        self.id = id
        self.config = config
        self.nn_config = nn_config
        self.logger = logger
        self.actor = None
        self.lock = Lock()
        self.replay_memory = None
        self.replay_memory_server = None
        self.server_bind_ip = server_bind_ip
        self.server_bind_port = server_bind_port
        self.actor_updater = []

        self.noise_f = noise_f

    def connection_handler(self, conn):
        print('RTController get conn from', conn)
        u = ActorUpdater(conn, self.nn_config)
        u.set_param_space_noise_function(self.noise_f)
        u.update_actor(self.actor)
        u.start()
        self.actor_updater.append(u)

    def set_replay_memory(self, replay_memory):
        if self.replay_memory is None or self.replay_memory_server is None:
            self.replay_memory = replay_memory
            rm_port = self.server_bind_port + 1
            print('Binding replay memory at', self.server_bind_ip, rm_port)
            self.replay_memory_server = ReplayMemoryServer(self.server_bind_ip, rm_port, replay_memory, self.logger)
            self.replay_memory_server.start()
        else:
            print('Duplicated setup for replay memory in RT controller')

    def get_id(self):
        return self.id

    def update_actor(self, actor):
        with self.lock:
            self.actor = actor
            for u in self.actor_updater:
                u.update_actor(actor)


if __name__ == '__main__':
    from sim_src.tb_logger import GLOBAL_LOGGER
    from proto_py.nn_config_pb2 import nn_config
    import torch.nn as nn

    GLOBAL_LOGGER.set_log_path('/tmp/test_tb/', 'test_tensor_board_server', 'rt_controller_test')
    GLOBAL_LOGGER.get_tb_logger().add_scalar("hello", 1234)
    n = nn_config()
    n.name = 'actor'
    n.af_config.append(nn_config.NONE)
    n.af_config.append(nn_config.TANH)
    n.af_config.append(nn_config.NONE)
    n.af_config.append(nn_config.NONE)
    n.nn_arch.append(0)

    any = Any()
    any.Pack(n)

    x = nn_config()
    any.Unpack(x)
    print(any)
    print(x)
    print(n)
    t = nn.Tanh()
    assert isinstance(t, nn.Tanh)

    a = np.array([[0.]])[0]
    b = np.array([[0.]])[0]

    print(a, b)
    from sim_src.nn.neural_network import NN_CONFIG
    from sim_src.nn.neural_network import Net

    n_config = NN_CONFIG(nn_arch=[2, 10, 2], af_config=[nn.ReLU(), nn.ReLU(), nn.Tanh()], init_w=[None, None], lr=0,
                         load_path=None, optim=None)
    net = Net(n_config.nn_arch, n_config.af_config, n_config.init_w)
    print(net.parameters())
    controller = RTAgent(0, None, '127.0.1.1', 4000, n_config, GLOBAL_LOGGER.get_tb_logger())
    controller.update_actor(net)
    controller.set_replay_memory(None)
    controller.start()
    while True:
        s = np.array([2.5, 4.6])
        s = to_tensor(s)
        a = net.forward(s)
        a = to_numpy(a)
        print(a)
        time.sleep(0.001)
