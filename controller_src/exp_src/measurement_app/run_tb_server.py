#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from exp_src.tensorboard_server import *
from sim_src.tb_logger import GLOBAL_LOGGER

log_path = "./"
folder_name = "tb_server_log/"
experiment_name = "tb_server_log"
GLOBAL_LOGGER.set_log_path(log_path, folder_name, experiment_name)
server = TBServer(server_bind_ip='0.0.0.0', server_bind_port=TENSORBOARD_SERVER_PORT,
                  logger=GLOBAL_LOGGER.get_tb_logger())
server.start()
server.join()
