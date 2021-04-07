#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import time
from collections import namedtuple
from threading import Thread

from sim_src import StatusObject
from sim_src.tb_logger import GLOBAL_LOGGER

PY_SIM_CONTROLLER_CONFIG = namedtuple("PY_SIM_CONTROLLER_CONFIG", ['c_step', 'total_step'])


class PySimController(StatusObject, Thread):
    def __init__(self, id, config, agent, learning_model, replay_memory):
        Thread.__init__(self)
        self.id = id
        self.config = config
        GLOBAL_LOGGER.get_tb_logger().add_text_of_object("CONTROLLER_CONFIG", config)

        self.agent = agent
        self.model = learning_model
        self.replay_memory = replay_memory

        self.agent.update_actor(self.model.get_actor())
        if isinstance(self.agent, Thread):
            print("agent as a thread start it")
            self.agent.start()
        self.step = 0

    def run(self):
        for x in range(self.config.total_step):
            batch = self.replay_memory.sample()
            if batch is not None:
                training_info = self.model.step(batch)
                if training_info is not None:
                    self.replay_memory.training_info(batch, training_info)
                self.agent.update_actor(self.model.get_actor())

            if x % 5000 == 0:
                output_file_path = GLOBAL_LOGGER.get_log_path()
                self.model.save(output_file_path, str(x))
                GLOBAL_LOGGER.reset_event_file()

        output_file_path = GLOBAL_LOGGER.get_log_path()

        self.model.save(output_file_path, 'final')


class ExpController(PySimController):
    def run(self):
        for x in range(self.config.total_step):
            t1 = time.time()
            batch = self.replay_memory.sample(asynchronization=True)
            if batch is not None:
                training_info = self.model.step(batch)
                if training_info is not None:
                    self.replay_memory.training_info(batch, training_info)
                self.agent.update_actor(self.model.get_actor())
                GLOBAL_LOGGER.get_tb_logger().add_scalar("training_time", time.time() - t1, x)
            else:
                time.sleep(0.01)

            if x % 5000 == 0:
                output_file_path = GLOBAL_LOGGER.get_log_path()
                self.model.save(output_file_path, str(x))
                GLOBAL_LOGGER.reset_event_file()

        output_file_path = GLOBAL_LOGGER.get_log_path()

        self.model.save(output_file_path, 'final')


if __name__ == '__main__':
    class A(Thread):
        pass


    a = A();
    if (isinstance(a, Thread)):
        print("a is thread")
