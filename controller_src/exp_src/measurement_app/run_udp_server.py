#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import argparse

parser = argparse.ArgumentParser(description='set udp sink config.')
parser.add_argument('port', type=int)
parser.add_argument('tb_server_ip', type=str)
args = parser.parse_args()
print(args)

from exp_src.measurement_app.udp_sink import *

sink = UdpSink(args.port, args.tb_server_ip, TENSORBOARD_SERVER_PORT)
sink.start()
