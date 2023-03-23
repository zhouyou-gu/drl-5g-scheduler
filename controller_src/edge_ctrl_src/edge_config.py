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
ue1 = PC_ACCESS_CONFIG(name='ue1', ip='IP-TO-UE1', port='PORT-TO-UE1', username='USERNAME-OF-UE1', password='PASSWORD-TO-UE1',
                       working_dir='~/drl-5g-scheduler/')
ue2 = PC_ACCESS_CONFIG(name='ue2', ip='IP-TO-UE2', port='PORT-TO-UE2', username='USERNAME-OF-UE2', password='PASSWORD-TO-UE2',
                       working_dir='~/drl-5g-scheduler/')
ue_config_list.append(ue1)
ue_config_list.append(ue2)

enb = PC_ACCESS_CONFIG(name='enb', ip='IP-TO-ENB', port='PORT-TO-ENB', username='USERNAME-OF-ENB', password='PASSWORD-TO-ENB',
                       working_dir='~/drl-5g-scheduler/')
epc = enb

edge_config = EDGE_ACCESS_CONFIG(epc_config=epc, enb_config=enb, ue_config_list=ue_config_list)

# the ip for controller
CONTROLLER_IP = "IP-TO-EDGE-CONTROLLER-SERVER"
