#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

# TODO: develop the action noise process
# TODO: epsilon greedy algorithm should take the action space as input

from collections import namedtuple

from sim_src.sim_env import StatusObject
from sim_src.util import *


class ActionNoise(StatusObject):
    """
    The base object for action noise
    """

    def __init__(self):
        StatusObject.__init__(self)

    def reset(self):
        pass

    def add_noise(self, action, noise_factor=1.):
        pass


OU_ACTION_NOISE_CONFIG = namedtuple("OU_ACTION_NOISE_CONFIG", ['mu', 'n_action', 'sigma', 'theta'])


class OUActionNoise(ActionNoise):
    """
    Noise object for Ornstein-Uhlenbeck Noise

    """

    def __init__(self, id, config):
        ActionNoise.__init__(self)

        self.id = id
        self.config = config

        self.mu = self.config.mu
        self.n_action = self.config.n_action
        self.sigma = self.config.sigma
        self.theta = self.config.theta

        self.noise_state = np.ones(self.n_action) * self.mu + np.random.randn(self.n_action)
        self.reset()

    def reset(self):
        self.noise_state = np.ones(self.n_action) * self.mu

    def get_noise(self):
        x = self.noise_state
        dx = self.theta * (self.mu - x) + self.sigma * np.random.randn(self.n_action)
        self.noise_state = x + dx
        return self.noise_state

    def add_noise(self, action, noise_factor=1.):
        action = action.astype(float)

        ret = action + self.get_noise() * noise_factor

        return ret


if __name__ == '__main__':

    n_action = 1
    ou_noise_config = OU_ACTION_NOISE_CONFIG(mu=0.2, n_action=n_action, sigma=0.3, theta=1)
    n = OUActionNoise(0, ou_noise_config)

    a = np.zeros(n_action)
    states = []
    for i in range(100):
        states.append(n.add_noise(a))
    import matplotlib.pyplot as plt

    plt.plot(states)
    plt.show()

    print(a)
