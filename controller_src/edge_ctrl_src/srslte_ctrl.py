#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import time

from edge_ctrl_src.util import *
from sim_src.util import get_current_time_str

time_advance_nsample = 64


def compile_srs(ssh_client: paramiko.client.SSHClient, path_to_srs: str, password: str, ddrl_enabled=True):
    ip, port = ssh_client.get_transport().getpeername()

    if ddrl_enabled:
        cmd = 'cd ' + path_to_srs + '; mkdir build; cd build; cmake ../  -DBUILD_DDRL=ON ; make'
    else:
        cmd = 'cd ' + path_to_srs + '; mkdir build; cd build; cmake ../  -DBUILD_DDRL=OFF ; make'

    ch, stdin, stdout, stderr = no_sudo_exec(ssh_client, cmd)
    print_stdout_blocking(stdout, "compile_srs", ip, port)
    print_stderr_blocking(stderr, "compile_srs", ip, port)

    cmd = 'cd ' + path_to_srs + '; cd build; sudo -S -p " " make install'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "install_srs", ip, port)
    print_stderr_blocking(stderr, "install_srs", ip, port)

    cmd = 'sudo -S -p " " ldconfig'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "load_so_srs", ip, port)
    print_stderr_blocking(stderr, "load_so_srs", ip, port)

    cmd = 'cd ' + path_to_srs + '; cd build/srsLTE; sudo -S -p " " srslte_install_configs.sh service'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "config_srs", ip, port)
    print_stderr_blocking(stderr, "config_srs", ip, port)

    return


def clean_srs(ssh_client: paramiko.client.SSHClient, path_to_srs: str, password: str):
    ip, port = ssh_client.get_transport().getpeername()
    cmd = 'cd ' + path_to_srs + '; sudo -S -p " " rm -rf build'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "compile_srs", ip, port)
    print_stderr_blocking(stderr, "compile_srs", ip, port)
    return


def run_srsepc(ssh_client: paramiko.client.SSHClient, path_to_binary: str, password: str, time_to_run=20):
    ip, port = ssh_client.get_transport().getpeername()
    cmd = 'sudo -S -p " " ' + path_to_binary
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    start_time = int(time.time())
    print('start srsepc at time', get_current_time_str())
    while int(time.time()) - start_time < time_to_run:
        time.sleep(0.5)
        print_stdout_no_blocking(stdout, "run_srsepc", ip, port)
        print_stderr_no_blocking(stderr, "run_srsepc", ip, port)
    ch.close()
    print('stop srsepc at time', get_current_time_str())
    return


def run_srsenb(ssh_client: paramiko.client.SSHClient, path_to_binary: str, password: str, time_to_run=20):
    ip, port = ssh_client.get_transport().getpeername()
    from edge_ctrl_src.edge_config import CONTROLLER_IP
    cmd = 'sudo DDRL_CONTROLLER_IP=' + CONTROLLER_IP + ' -S -p " " ' + path_to_binary + ' --log.all_level debug'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    start_time = int(time.time())
    print('start srsenb at time', get_current_time_str())
    while int(time.time()) - start_time < time_to_run:
        time.sleep(0.5)
        print_stdout_no_blocking(stdout, "run_srsenb", ip, port)
        print_stderr_no_blocking(stderr, "run_srsenb", ip, port)
    ch.close()
    print('stop srsenb at time', get_current_time_str())
    return


MAX_UE = 5


# TODO: merge MAX UE here with the one in simulation
def run_srsue(ue_id, ssh_client: paramiko.client.SSHClient, path_to_binary: str, password: str, time_to_run=20):
    if ue_id > MAX_UE:
        print('Warning: UE', ue_id, 'is not running')
        print('Warning: Maximum number of UE is', MAX_UE)
        return
    ip, port = ssh_client.get_transport().getpeername()
    cmd = 'sudo -S -p " " ' + path_to_binary + ' --usim.imsi=' + '01234567890000' + str(ue_id)
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    start_time = int(time.time())
    print('start srsue', ue_id, 'at time', get_current_time_str())
    while int(time.time()) - start_time < time_to_run:
        time.sleep(0.5)
        print_stdout_no_blocking(stdout, "run_srsue", ip, port)
        print_stderr_no_blocking(stderr, "run_srsue", ip, port)
    ch.close()
    print('stop srsue', ue_id, 'at time', get_current_time_str())
    return
