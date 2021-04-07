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


def sync_eth_with_right_time(ssh_client: paramiko.client.SSHClient, password: str):
    ip, port = ssh_client.get_transport().getpeername()

    # wall time must be in the same second before ptp start
    # enable ntp first
    cmd = 'sudo -S -p " " timedatectl set-ntp 1'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "disable_ntp", ip, port)
    print_stderr_blocking(stderr, "disable_ntp", ip, port)

    time.sleep(1)

    cmd = 'sudo -S -p " " timedatectl set-local-rtc 1'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "sync_eth_with_right_time", ip, port)
    print_stderr_blocking(stderr, "sync_eth_with_right_time", ip, port)

    time.sleep(1)

    cmd = 'sudo -S -p " " timedatectl set-local-rtc 0'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "sync_eth_with_right_time", ip, port)
    print_stderr_blocking(stderr, "sync_eth_with_right_time", ip, port)
    return


def run_ptp4l(ssh_client: paramiko.client.SSHClient, password: str, is_master: bool):
    ip, port = ssh_client.get_transport().getpeername()
    if is_master:
        cmd = 'sudo -S -p " " ptp4l -i ' + '$(' + GET_DEAULT_ETH_CMD + ') -m'
    else:
        cmd = 'sudo -S -p " " ptp4l -i ' + '$(' + GET_DEAULT_ETH_CMD + ')' + ' -s -m'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "run_ptp4l", ip, port)
    print_stderr_blocking(stderr, "run_ptp4l", ip, port)
    return


def run_phc2sys(ssh_client: paramiko.client.SSHClient, password: str, is_master: bool):
    ip, port = ssh_client.get_transport().getpeername()

    # wall time must be in the same second before ptp start
    # enable ntp first
    cmd = 'sudo -S -p " " timedatectl set-ntp 1'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "disable_ntp", ip, port)
    print_stderr_blocking(stderr, "disable_ntp", ip, port)

    time.sleep(1)

    # disable ntp in order to prevent affect to ptp
    cmd = 'sudo -S -p " " timedatectl set-ntp 0'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "disable_ntp", ip, port)
    print_stderr_blocking(stderr, "disable_ntp", ip, port)
    if is_master:
        cmd = 'sudo -S -p " " phc2sys -s CLOCK_REALTIME' + ' -c $(' + GET_DEAULT_ETH_CMD + ') -w -m'
        ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
        print_stdout_blocking(stdout, "run_phc2sys_master", ip, port)
        print_stderr_blocking(stderr, "run_phc2sys", ip, port)
    else:
        cmd = 'sudo -S -p " " phc2sys -s ' + '$(' + GET_DEAULT_ETH_CMD + ') -c CLOCK_REALTIME -w -m'
        ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
        print_stdout_blocking(stdout, "run_phc2sys_slave", ip, port)
        print_stderr_blocking(stderr, "run_phc2sys", ip, port)
    return
