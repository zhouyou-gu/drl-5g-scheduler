#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from collections import namedtuple

import torch.nn.functional as F

from sim_src.model import LearningModel
from sim_src.nn.neural_network import Net, NN_CONFIG
from sim_src.tb_logger import GLOBAL_LOGGER
from sim_src.util import *

ACTOR_CONFIG = NN_CONFIG
CRITIC_CONFIG = NN_CONFIG
UPDATE_CONFIG = namedtuple("UPDATE_CONFIG", ['is_soft', 'tau', 'c_step', 'no_update'])
RL_CONFIG = namedtuple("RL_CONFIG", ['gamma'])
DDPG_CONFIG = namedtuple("DDPG_CONFIG", ['actor_config', 'critic_config', 'update_config', 'rl_config'])


class DDPG(LearningModel):
    def __init__(self, id, config):
        LearningModel.__init__(self)
        self.id = id
        self.config = config
        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("DDPG_CONFIG", self.config)

        self.actor = None
        self.actor_optim = None

        self.critic = None
        self.critic_optim = None

        self.actor_target = None

        self.critic_target = None

        self.init_model()
        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("actor_target_arch", self.actor_target)
        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("critic_target_arch", self.critic_target)

        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("actor_arch", self.actor)
        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("critic_arch", self.critic)

        self.step_counter = 0

        if USE_CUDA:
            self.move_nn_to_gpu()

    def move_nn_to_gpu(self):
        self.actor.to(torch.cuda.current_device())
        self.actor_target.to(torch.cuda.current_device())
        self.critic.to(torch.cuda.current_device())
        self.critic_target.to(torch.cuda.current_device())

    def setup_actor(self):
        if self.config.actor_config.load_path is not None:
            self.actor = self._load(self.config.actor_config.load_path)
        else:
            self.actor = Net(self.config.actor_config.nn_arch,
                             self.config.actor_config.af_config,
                             self.config.actor_config.init_w)

        self.actor_optim = self.config.actor_config.optim(self.actor.parameters(),
                                                          lr=self.config.actor_config.lr)

        self.actor_target = Net(self.config.actor_config.nn_arch,
                                self.config.actor_config.af_config,
                                self.config.actor_config.init_w)

        hard_update_inplace(self.actor_target, self.actor)

    def setup_critic(self):
        if self.config.critic_config.load_path is not None:
            self.critic = self._load(self.config.critic_config.load_path)
        else:
            self.critic = Net(self.config.critic_config.nn_arch,
                              self.config.critic_config.af_config,
                              self.config.critic_config.init_w)

        self.critic_optim = self.config.critic_config.optim(self.critic.parameters(),
                                                            lr=self.config.critic_config.lr)

        self.critic_target = Net(self.config.critic_config.nn_arch,
                                 self.config.critic_config.af_config,
                                 self.config.critic_config.init_w)

        hard_update_inplace(self.critic_target, self.critic)

    def init_model(self):
        self.setup_actor()
        self.setup_critic()

    def set_actor_target(self, path):
        self.actor_target = self._load(path)

    def set_critic_target(self, path):
        self.critic_target = self._load(path)

    def _load(self, path):
        if USE_CUDA:
            return torch.load(path)
        else:
            return torch.load(path, map_location=torch.device('cpu'))

    def _reward(self, reward, states):
        return reward

    def _action_match(self, action):
        action[action > 0] = 1.
        action[action <= 0] = -1.
        return action

    @counted
    def step(self, batch):
        self._print("learn")
        states = to_tensor(batch[0])
        actions = to_tensor(batch[1])
        rewards = self._reward(to_tensor(batch[2]), states)
        next_states = to_tensor(batch[3])
        done = to_tensor(batch[4])

        a = self.actor_target.forward(next_states)
        a = self._action_match(a)
        s_a = torch.cat((next_states, a), dim=1)
        q = self.critic_target.forward(s_a)
        y = torch.mul(q, self.config.rl_config.gamma)
        self._print("gamma", self.config.rl_config.gamma)
        self._print("rewards", rewards)
        self._print("q", q)

        y = torch.add(rewards, y).detach()
        self._print("y", y)

        actions = self._action_match(actions)
        s_a = torch.cat((states, actions), dim=1)
        q = self.critic.forward(s_a)
        l_critic = F.smooth_l1_loss(q, y, reduction='none')
        self._print("loss", l_critic)

        l_critic_per_batch = torch.sum(l_critic, dim=1, keepdim=True)
        ret_per_e = to_numpy(l_critic_per_batch)
        self._print('l_critic_per_batch', ret_per_e)

        if len(batch) > 5:
            weights = to_tensor(batch[5])
            self._print("weights", weights)
            l_critic = torch.mul(l_critic_per_batch, weights)
            self._print("w_l_critic", l_critic)

        l_critic = torch.mean(l_critic)

        self.critic_optim.zero_grad()
        l_critic.backward()
        self.critic_optim.step()

        a = self.actor.forward(states)
        s_a = torch.cat((states, a), dim=1)
        l_actor = self.critic.forward(s_a)

        l_actor_per_batch = torch.sum(l_actor, dim=1, keepdim=True)
        if len(batch) > 5:
            weights = to_tensor(batch[5])
            self._print("weights", weights)
            l_actor = torch.mul(l_actor_per_batch, weights)
            self._print("w_l_actor", l_actor)

        l_actor = torch.mean(torch.neg(l_actor))

        self.actor_optim.zero_grad()
        l_actor.backward()
        self.actor_optim.step()

        GLOBAL_LOGGER.get_tb_logger().add_scalar('DDPG.loss_actor', to_numpy(l_actor), self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('DDPG.loss_critic', to_numpy(l_critic), self.n_step)

        self.update_nn()

        self.step_counter += 1

        return ret_per_e

    def update_nn(self):
        if self.config.update_config.no_update:
            return
        if self.config.update_config.is_soft:
            soft_update_inplace(self.actor_target, self.actor, self.config.update_config.tau)
            soft_update_inplace(self.critic_target, self.critic, self.config.update_config.tau)
        elif self.step_counter % self.config.update_config.c_step == 0:
            hard_update_inplace(self.actor_target, self.actor)
            hard_update_inplace(self.critic_target, self.critic)

    def get_actor(self):
        return self.actor_target

    def save(self, path: str, postfix: str):
        torch.save(self.actor, path + "actor_" + postfix + ".pt")
        torch.save(self.actor_target, path + "actor_target_" + postfix + ".pt")

        torch.save(self.critic, path + "critic_" + postfix + ".pt")
        torch.save(self.critic_target, path + "critic_target_" + postfix + ".pt")

    def start_eval(self):
        self.actor.eval()
        self.actor_target.eval()
        self.critic.eval()
        self.critic_target.eval()

    def start_train(self):
        self.actor.train()
        self.actor_target.train()
        self.critic.train()
        self.critic_target.train()


class MultiHeadCriticDDPG(DDPG):
    def _reward(self, reward, state):
        return reward


class SingleHeadCriticDDPG(DDPG):
    def _reward(self, reward, state):
        return torch.sum(reward, dim=1, keepdim=True)


class MultiHeadCriticDDPG_NEW_PER(MultiHeadCriticDDPG):
    threshold = 0.

    def _per_w_multiplier(self, batch):
        ret = np.ones(batch[2].shape, dtype=float)
        n_ue = batch[4].shape[1]
        for d in range(batch[4].shape[0]):
            for u in range(n_ue):
                if batch[0][d][u] > 0. and batch[0][d][u] < self.threshold and batch[1][d][u] > 0:
                    ret[d][u] += 1.
                elif batch[0][d][u] >= self.threshold:
                    ret[d][u] += 1.

        self._print(ret)
        return ret

    @counted
    def step(self, batch):
        self._print("learn")
        states = to_tensor(batch[0])
        actions = to_tensor(batch[1])
        rewards = self._reward(to_tensor(batch[2]), states)
        next_states = to_tensor(batch[3])
        done = to_tensor(batch[4])
        self._print("states", batch[0])
        self._print("actions", batch[1])

        a = self.actor_target.forward(next_states)
        a = self._action_match(a)
        s_a = torch.cat((next_states, a), dim=1)
        q = self.critic_target.forward(s_a)
        y = torch.mul(q, self.config.rl_config.gamma)
        self._print("gamma", self.config.rl_config.gamma)
        self._print("rewards", rewards)
        self._print("q", q)

        y = torch.add(rewards, y).detach()
        self._print("y", y)

        actions = self._action_match(actions)
        s_a = torch.cat((states, actions), dim=1)
        q = self.critic.forward(s_a)
        l_critic = F.smooth_l1_loss(q, y, reduction='none')
        self._print("loss", l_critic)

        l_critic_per_batch = torch.sum(l_critic, dim=1, keepdim=True)
        self._print('l_critic_per_batch', l_critic_per_batch)
        ret_per_e = to_numpy(l_critic)
        ret_per_e = ret_per_e * self._per_w_multiplier(batch)
        self._print('ret_per_e_full', ret_per_e)
        ret_per_e = np.sum(ret_per_e, axis=1, keepdims=True)
        self._print('ret_per_e', ret_per_e)

        if len(batch) > 5:
            weights = to_tensor(batch[5])
            self._print("weights", weights)
            l_critic = torch.mul(l_critic_per_batch, weights)
            self._print("w_l_critic", l_critic)

        l_critic = torch.mean(l_critic)

        self.critic_optim.zero_grad()
        l_critic.backward()
        self.critic_optim.step()

        a = self.actor.forward(states)
        s_a = torch.cat((states, a), dim=1)
        l_actor = self.critic.forward(s_a)

        l_actor_per_batch = torch.sum(l_actor, dim=1, keepdim=True)
        if len(batch) > 5:
            weights = to_tensor(batch[5])
            self._print("weights", weights)
            l_actor = torch.mul(l_actor_per_batch, weights)
            self._print("w_l_actor", l_actor)

        l_actor = torch.mean(torch.neg(l_actor))

        self.actor_optim.zero_grad()
        l_actor.backward()
        self.actor_optim.step()

        GLOBAL_LOGGER.get_tb_logger().add_scalar('DDPG.loss_actor', to_numpy(l_actor), self.n_step)
        GLOBAL_LOGGER.get_tb_logger().add_scalar('DDPG.loss_critic', to_numpy(l_critic), self.n_step)

        self.update_nn()
        self.step_counter += 1

        return ret_per_e


if __name__ == '__main__':
    # for x in range(50000):
    # 	gamma = 0.9 * (1 - math.exp(- float(x)/10000))
    # 	print(gamma)

    print(to_tensor(np.zeros(1)))
    a = torch.Tensor([[3, 5], [1, 2]])
    print(a)
    print(torch.mean(a))
