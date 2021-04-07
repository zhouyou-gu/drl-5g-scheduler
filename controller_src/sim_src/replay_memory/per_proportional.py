#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

# The code in this file is originally from https://github.com/rlcode/per
# TODO: validate beta incrementation

import random
from collections import namedtuple
from threading import Lock

import numpy as np

from sim_src.replay_memory.replay_memory import ReplayMemory
from sim_src.replay_memory.sum_tree import SumTree
from sim_src.tb_logger import GLOBAL_LOGGER

PER_PROPORTIONAL_REPLAY_MEMORY_CONFIG = namedtuple("PER_PROPORTIONAL_REPLAY_MEMORY_CONFIG",
                                                   ["batch_size", "buffer_size", "seed", "alpha", "total_step"])

EPSILON = 1e-16


class PERProportional(ReplayMemory):
    """ The class represents prioritized experience replay buffer.
    The class has functions: store samples, pick samples with
    probability in proportion to sample's priority, update
    each sample's priority, reset alpha.
    see https://arxiv.org/pdf/1511.05952.pdf .
    """

    def __init__(self, id, config):
        """
        Prioritized experience replay buffer initialization.
        """

        self.id = id
        self.config = config
        self.tree = SumTree(self.config.buffer_size)
        self.buffer_size = self.config.buffer_size
        self.batch_size = self.config.batch_size
        self.alpha = self.config.alpha

        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
        self.seed = random.seed(self.config.seed)
        self.step_lock = Lock()
        self.sample_lock = Lock()
        self.sample_lock.acquire()  # allow save_step first

        self.eps = EPSILON
        self.beta = 0.6

        self.beta_increment_per_sampling = 2. / float(self.config.total_step)

        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("PER_REPLAY_MEMORY_CONFIG", self.config)

    def save_step(self, state, action, reward, next_state, done, asynchronization=False):
        """Add a new experience to memory.
        :param async:
        """
        if not asynchronization:
            self.step_lock.acquire()

        # self._print("step")
        self.async_save_step(state, action, reward, next_state, done)

        if not asynchronization:
            self.sample_lock.release()

    def sample(self, asynchronization=False):
        # TODO: handle asynchronization sample
        """Randomly sample a batch of experiences from memory.
        :param asynchronization:
        """
        if not asynchronization:
            self.sample_lock.acquire()

        # self._print("sample")
        ret = self.async_sample()

        if not asynchronization:
            self.step_lock.release()
        return ret

    def get_id(self):
        return self.id

    def get_size(self):
        """Return the current size of internal memory."""
        return self.tree.get_size()

    def training_info(self, batch, errors):
        for i, e in zip(batch[6], errors):
            p = self._get_priority(e)
            self.tree.update(i, p)

    def _select(self):
        batch = []
        idxs = []
        segment = self.tree.total() / self.batch_size
        priorities = []

        self.beta = np.min([1., self.beta + self.beta_increment_per_sampling])

        for i in range(self.batch_size):
            a = segment * i
            b = segment * (i + 1)

            s = random.uniform(a, b)
            (idx, p, data) = self.tree.get(s)
            if isinstance(data, int) or isinstance(data, type(None)):
                continue
            priorities.append(p)
            batch.append(data)
            idxs.append(idx)
        sampling_probabilities = np.array(priorities) / self.tree.total() + self.eps
        is_weight = np.power(self.tree.n_entries * sampling_probabilities, -self.beta)
        is_weight /= is_weight.max()

        return batch, is_weight, idxs

    def _get_priority(self, error):
        return (np.abs(error) + self.eps) ** self.config.alpha

    def async_sample(self):
        if self.get_size() < self.config.batch_size * 10 and self.get_size() < self.config.buffer_size:
            ret = None
        else:
            experiences, weight, indices = self._select()
            states = np.vstack([e.state for e in experiences if e is not None])
            actions = np.vstack([e.action for e in experiences if e is not None])
            rewards = np.vstack([e.reward for e in experiences if e is not None])
            next_states = np.vstack([e.next_state for e in experiences if e is not None])
            dones = np.vstack([e.done for e in experiences if e is not None])
            weights = np.vstack([w for w in weight if w is not None])
            ret = (states, actions, rewards, next_states, dones, weights, indices)
        return ret

    def async_save_step(self, state, action, reward, next_state, done):
        exp = self.experience(state, action, reward, next_state, done)
        p = self.tree.get_max_priority()
        p += self.eps
        self.tree.add(exp, p)


if __name__ == '__main__':
    rm_config = PER_PROPORTIONAL_REPLAY_MEMORY_CONFIG(batch_size=1, buffer_size=5, seed=0, alpha=1, total_step=100)
    rm = PERProportional(0, rm_config)


    def save_loop():
        for x in range(10):
            rm.save_step(x, x, x, x, x)


    def sample_loop():
        for x in range(10):
            print(x)
            ret = rm.sample()
            print(ret)
            print("tree", rm.tree.tree)
            if ret:
                rm.training_info(ret, [random.random()])

            print("updated_tree", rm.tree.tree)


    from threading import Thread

    Thread_a = Thread(None, save_loop)
    Thread_b = Thread(None, sample_loop)

    Thread_a.start()
    Thread_b.start()

    Thread_a.join()
    Thread_b.join()
