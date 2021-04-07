
#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import sys
assert sys.version_info[0] == 3, "Please run with Python 3"
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
[sys.path.append(os.path.join(dir_path, name)) for name in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, name))]
[print('system path:',p) for p in sys.path]
