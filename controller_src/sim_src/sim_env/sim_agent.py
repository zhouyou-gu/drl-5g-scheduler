#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

# TODO: add support for parameter space noise
import math
from collections import namedtuple
from threading import Lock

from sim_src.sim_env import StatusObject
from sim_src.sim_env.action_noise import OUActionNoise, OU_ACTION_NOISE_CONFIG
from sim_src.tb_logger import GLOBAL_LOGGER
from sim_src.util import *


class EnvToAgentInterface:
    """
    The interface from Env to Agent
    """

    def set_env_id(self, env_id):
        pass

    def get_action(self, state: np.ndarray) -> np.ndarray:
        pass

    def save_step(self, state, action, reward, next_state, done, asynchronization=False):
        pass


class ControllerToAgentInterface:
    """
    The interface from Controller to Agent
    """

    def update_actor(self, actor):
        pass

    def get_id(self):
        pass

    def set_replay_memory(self, replay_memory):
        pass


SIM_AGENT_CONFIG = namedtuple("SIM_AGENT_CONFIG", ['noise_config', 'noise_attenuation'])


class SimAgent(StatusObject, EnvToAgentInterface, ControllerToAgentInterface):
    def __init__(self, id, config, replay_memory, scheduler_function=None):
        StatusObject.__init__(self)
        self.id = id
        self.env_id = None
        self.replay_memory = replay_memory
        self.actor = None
        self.actor_lock = Lock()
        self.config = config

        self.scheduler_function = scheduler_function

        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("AGENT_CONFIG", self.config)
        if isinstance(self.config.noise_config, OU_ACTION_NOISE_CONFIG):
            self.action_noise = OUActionNoise(self.id, self.config.noise_config)
        else:
            self.action_noise = None

    # env to agent interface
    @counted
    def get_action(self, state):
        """
        Get the action from the actor
        :param state: env state in np
        :return: action in np
        """

        # if logic is present, the agent will use logic as the actor
        with self.actor_lock:
            if self.scheduler_function is None:
                state = to_tensor(state)
                ret = self.actor.forward(state)
                ret = to_numpy(ret)
            else:
                ret = self.scheduler_function.forward(state)

            noise_factor = math.exp(-self.n_step * self.config.noise_attenuation)
            if self.action_noise:
                GLOBAL_LOGGER.get_tb_logger().add_scalar("NOISE_FACTOR", noise_factor, self.n_step)
                ret = self.action_noise.add_noise(ret, noise_factor)
            for a in range(len(ret)):
                GLOBAL_LOGGER.get_tb_logger().add_scalar("ACTION_" + str(a), ret[a], self.n_step)
        return ret

    def set_env_id(self, env_id):
        self.env_id = env_id

    def save_step(self, state, action, reward, next_state, done, asynchronization=False):
        self.replay_memory.save_step(state, action, reward, next_state, done, asynchronization=asynchronization)

    # controller to agent interface
    def update_actor(self, actor):
        with self.actor_lock:
            if self.actor is None:
                self.actor = actor
                return
            # update actor network
            else:
                self.actor = actor
                return

    def get_id(self):
        return self.id

    def set_replay_memory(self, replay_memory):
        self.replay_memory = replay_memory


if __name__ == '__main__':
    print(np.array([1]).__class__)
