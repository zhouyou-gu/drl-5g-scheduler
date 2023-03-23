#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from edge_ctrl_src.edge import PC_ACCESS_CONFIG, EDGE_ACCESS_CONFIG


ue_config_list = []
# SSH access to edge
ue1 = PC_ACCESS_CONFIG(name='ue1', ip='192.168.1.101', port='22', username='ue1', password='sdr123!ue1',
                       working_dir='~/drl-5g-scheduler/')
ue2 = PC_ACCESS_CONFIG(name='ue2', ip='192.168.1.102', port='22', username='ue2', password='sdr123!ue2',
                       working_dir='~/drl-5g-scheduler/')
ue_config_list.append(ue1)
ue_config_list.append(ue2)

enb = PC_ACCESS_CONFIG(name='enb', ip='192.168.1.100', port='22', username='enb', password='sdr123!enb',
                       working_dir='~/drl-5g-scheduler/')
epc = enb

edge_config = EDGE_ACCESS_CONFIG(epc_config=epc, enb_config=enb, ue_config_list=ue_config_list)

# the ip for controller
CONTROLLER_IP = "192.168.1.200"
