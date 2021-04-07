#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import os
import select
import time
from collections import deque

import paramiko

from edge_ctrl_src.app_ctrl import no_sudo_exec
from edge_ctrl_src.edge import PC_ACCESS_CONFIG

controller_config = PC_ACCESS_CONFIG(name='deep', ip='0.0.0.0', port=22, username='deep', password='deep',
                                     working_dir='~/')

controller = paramiko.SSHClient()
controller.set_missing_host_key_policy(paramiko.AutoAddPolicy)
controller.connect(controller_config.ip,
                   port=controller_config.port,
                   username=controller_config.username,
                   password=controller_config.password)


class Experiment():
    def __init__(self, cmd, env):
        self.started = False
        self.p = None
        self.out = None
        self.command = cmd
        self.env = env.copy()
        self.out_queue = deque(maxlen=10)

    def toggle_run(self):
        if not self.started and self.p is None:
            self.out_queue.clear()
            self.p, stdin, self.out, stderr = no_sudo_exec(controller, cmd=self.command)
            self.started = True
        else:
            self.started = False
            if self.p is not None:
                self.p.close()
                self.p = None

    def readlines(self):
        if self.started and self.p is not None:
            if self.out.channel.recv_ready():
                rl, wl, xl = select.select([self.out.channel], [], [], 0.)
                if len(rl) > 0:
                    self.out_queue.append(self.out.channel.recv(1024).decode("utf-8"))
            ret = ''
            for t in self.out_queue:
                ret = ret + t
            return ret
        return ''


EDGE_CTRL_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
CONTROLLER_SRC = os.path.abspath(os.path.join(EDGE_CTRL_SCRIPT_PATH, os.pardir))

env = os.environ.copy()
PATH_TO_SCRIPT = os.path.join(EDGE_CTRL_SCRIPT_PATH, "edge_ptp_sync.py")
run_sync = Experiment("PYTHONPATH=" + CONTROLLER_SRC + " python3 " + PATH_TO_SCRIPT, env)

PATH_TO_SCRIPT = os.path.join(CONTROLLER_SRC, "exp_script_example/run_rt_controller.py")
run_controller = Experiment("PYTHONPATH=" + CONTROLLER_SRC + " python3 " + PATH_TO_SCRIPT, env)

PATH_TO_SCRIPT = os.path.join(EDGE_CTRL_SCRIPT_PATH, "edge_run.py")
edge_run = Experiment("PYTHONPATH=" + CONTROLLER_SRC + " python3 " + PATH_TO_SCRIPT, env)

PATH_TO_SCRIPT = os.path.join(EDGE_CTRL_SCRIPT_PATH, "test/edge_ping.py")
edge_ping = Experiment("PYTHONPATH=" + CONTROLLER_SRC + " python3 " + PATH_TO_SCRIPT, env)

PATH_TO_SCRIPT = os.path.join(EDGE_CTRL_SCRIPT_PATH, "ctrl_web_interface/edge_one_way_latency_lte.py")
edge_one_way_latency_lte = Experiment("PYTHONPATH=" + CONTROLLER_SRC + " python3 " + PATH_TO_SCRIPT, env)

if __name__ == '__main__':
    run_controller.toggle_run()
    while True:
        print(run_controller.readlines().strip())
        time.sleep(1)