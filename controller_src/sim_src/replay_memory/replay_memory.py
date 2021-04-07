#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import random
from collections import namedtuple, deque
from threading import Lock

import numpy as np

from sim_src import StatusObject
from sim_src.tb_logger import GLOBAL_LOGGER


class ReplayMemory(StatusObject):
    def save_step(self, state, action, reward, next_state, done, asynchronization=False):
        """Add a new experience to memory.
        :param asynchronization:
        """
        pass

    def sample(self, asynchronization=False):
        """Randomly sample a batch of experiences from memory.
        :param asynchronization:
        """
        pass

    def get_id(self):
        pass

    def get_size(self):
        """Return the current size of internal memory."""
        pass

    def training_info(self, batch, training_info):
        pass


SIM_REPLAY_MEMORY_CONFIG = namedtuple("SIM_REPLAY_MEMORY_CONFIG", ["batch_size", "buffer_size", "seed"])


class SimReplayMemory(ReplayMemory):
    """Fixed-size buffer to store experience tuples."""

    def __init__(self, id, config):
        """Initialize a ReplayBuffer object.
        Params
        ======
            buffer_size (int): maximum size of buffer
            batch_size (int): size of each training batch
        """
        self.id = id
        self.config = config

        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("REPLAY_MEMORY_CONFIG", self.config)

        self.memory = deque(maxlen=self.config.buffer_size)  # internal memory (deque)
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
        self.seed = random.seed(self.config.seed)
        self.step_lock = Lock()
        self.sample_lock = Lock()
        self.sample_lock.acquire()  # allow save_step first

    def save_step(self, state, action, reward, next_state, done, asynchronization=False):
        """Add a new experience to memory.
        :param asynchronization:
        """
        if not asynchronization:
            self.step_lock.acquire()

        # self._print("step")
        self.async_save_step(state, action, reward, next_state, done)

        if not asynchronization:
            self.sample_lock.release()

    def sample(self, asynchronization=False):
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
        return len(self.memory)

    def status(self):
        print("len of memory", len(self.memory), "max size of memory", self.memory.maxlen)

    def async_sample(self):
        if self.get_size() < self.config.batch_size * 10 and self.get_size() < self.config.buffer_size:
            ret = None
        else:
            experiences = random.sample(self.memory, k=self.config.batch_size)
            states = np.vstack([e.state for e in experiences if e is not None])
            actions = np.vstack([e.action for e in experiences if e is not None])
            rewards = np.vstack([e.reward for e in experiences if e is not None])
            next_states = np.vstack([e.next_state for e in experiences if e is not None])
            dones = np.vstack([e.done for e in experiences if e is not None])

            ret = (states, actions, rewards, next_states, dones)
        return ret

    def async_save_step(self, state, action, reward, next_state, done):
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)


if __name__ == '__main__':
    print("test  deque dropout when maxlen is reached")
    deque_size = 5
    test_memory = deque(maxlen=deque_size)
    for i in range(deque_size + 5):
        test_memory.append(i)
        print(test_memory)
    experiences = random.sample(test_memory, k=int(deque_size / 2))
    print(experiences)
    print(test_memory.maxlen)
    print((1, 2))


    class TestReplayMemory(ReplayMemory):
        """Fixed-size buffer to store experience tuples."""

        def __init__(self, id, batch_size, buffer_size, seed):
            """Initialize a ReplayBuffer object.
            Params
            ======
                buffer_size (int): maximum size of buffer
                batch_size (int): size of each training batch
            """
            self.id = id
            self.batch_size = batch_size
            self.memory = deque(maxlen=buffer_size)  # internal memory (deque)
            self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
            self.seed = random.seed(seed)
            self.step_lock = Lock()
            self.sample_lock = Lock()
            self.sample_lock.acquire()  # allow save_step first

        def step(self, state, action, reward, next_state, done):
            """Add a new experience to memory."""
            self.step_lock.acquire()

            print("save_step")

            self.sample_lock.release()

        def sample(self):
            """Randomly sample a batch of experiences from memory."""

            self.sample_lock.acquire()

            print("sample")

            self.step_lock.release()

        def get_id(self):
            return self.id

        def get_size(self):
            """Return the current size of internal memory."""
            return len(self.memory)

        def status(self):
            print("len of memory", len(self.memory), "max size of memory", self.memory.maxlen)


    test_memory = TestReplayMemory(id=1, batch_size=5, buffer_size=5, seed=0)


    def step():
        while True:
            i = 1
            test_memory.step(1, 1, 1, 1, 1)
        # print("save_step")


    def sample():
        while True:
            i = 1
            test_memory.sample()
        # print("sample")


    from threading import Thread

    Thread_a = Thread(None, step)
    Thread_b = Thread(None, sample)

    Thread_a.start()
    Thread_b.start()
