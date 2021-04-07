#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import argparse

parser = argparse.ArgumentParser(description='set udp source config.')
parser.add_argument('ip', type=str)
parser.add_argument('port', type=int)
parser.add_argument('p_size', type=int)
parser.add_argument('mean_interval', type=float)
parser.add_argument('n_per_test', type=int)

args = parser.parse_args()
print(args)

from exp_src.measurement_app.udp_source import *
from exp_src.measurement_app.util import *

lg = ConstantSizeLG(args.p_size)
ig = PoissonIG(args.mean_interval)

source = UdpSource(args.ip, args.port, args.n_per_test, lg, ig)
source.start()
