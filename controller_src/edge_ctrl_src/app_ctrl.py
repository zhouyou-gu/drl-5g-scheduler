#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from edge_ctrl_src.util import *

DEFAULT_PACKET_SIZE = 150
DEFAULT_PACKET_INTERVAL = 10
DEFAULT_PACKET_PER_TEST = 100


def run_oneway_latency_server(ssh_client: paramiko.client.SSHClient, working_dir: str, listen_port=8888,
                              tb_server_ip='0.0.0.0'):
    ip, port = ssh_client.get_transport().getpeername()

    p_to_dir = os.path.join(working_dir, 'controller_src')
    p_to_script = os.path.join(working_dir, 'controller_src/exp_src/measurement_app/run_udp_server.py')
    cmd = 'PYTHONPATH=' + p_to_dir + ' python3 ' + p_to_script + ' ' + str(listen_port) + ' ' + tb_server_ip

    ch, stdin, stdout, stderr = no_sudo_exec(ssh_client, cmd)
    print_stdout_blocking(stdout, "run_oneway_latency_server", ip, port)
    print_stderr_blocking(stderr, "run_oneway_latency_server", ip, port)
    return


def run_oneway_latency_client(ssh_client: paramiko.client.SSHClient, working_dir: str, server_ip: str,
                              listen_port=8888):
    ip, port = ssh_client.get_transport().getpeername()

    p_to_dir = os.path.join(working_dir, 'controller_src')
    p_to_script = os.path.join(working_dir, 'controller_src/exp_src/measurement_app/run_udp_client.py')
    cmd = 'PYTHONPATH=' + p_to_dir + ' python3 ' + p_to_script + ' ' + server_ip + ' ' + str(listen_port) + ' ' + str(
        DEFAULT_PACKET_SIZE) + ' ' + str(DEFAULT_PACKET_INTERVAL) + ' ' + str(DEFAULT_PACKET_PER_TEST)

    ch, stdin, stdout, stderr = no_sudo_exec(ssh_client, cmd)
    print_stdout_blocking(stdout, "run_oneway_latency_client", ip, port)
    print_stderr_blocking(stderr, "run_oneway_latency_client", ip, port)
    return


def sudo_run_oneway_latency_server(ssh_client: paramiko.client.SSHClient, pw, working_dir: str, listen_port=8888,
                                   tb_server_ip='0.0.0.0'):
    ip, port = ssh_client.get_transport().getpeername()

    p_to_dir = os.path.join(working_dir, 'controller_src')
    p_to_script = os.path.join(working_dir, 'controller_src/exp_src/measurement_app/run_udp_server.py')
    cmd = 'PYTHONPATH=' + p_to_dir + ' python3 ' + p_to_script + ' ' + str(listen_port) + ' ' + tb_server_ip
    cmd = 'sudo -S -p " " ' + cmd
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, pw)
    print_stdout_blocking(stdout, "run_oneway_latency_server", ip, port)
    print_stderr_blocking(stderr, "run_oneway_latency_server", ip, port)
    return


def sudo_run_oneway_latency_client(ssh_client: paramiko.client.SSHClient, pw, working_dir: str, server_ip: str,
                                   listen_port=8888):
    ip, port = ssh_client.get_transport().getpeername()

    p_to_dir = os.path.join(working_dir, 'controller_src')
    p_to_script = os.path.join(working_dir, 'controller_src/exp_src/measurement_app/run_udp_client.py')
    cmd = 'PYTHONPATH=' + p_to_dir + ' python3 ' + p_to_script + ' ' + server_ip + ' ' + str(listen_port) + ' ' + str(
        DEFAULT_PACKET_SIZE) + ' ' + str(DEFAULT_PACKET_INTERVAL) + ' ' + str(DEFAULT_PACKET_PER_TEST)
    cmd = 'sudo -S -p " " ' + cmd
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, pw)
    print_stdout_blocking(stdout, "run_oneway_latency_client", ip, port)
    print_stderr_blocking(stderr, "run_oneway_latency_client", ip, port)
    return


def run_ping(ssh_client: paramiko.client.SSHClient, dst_ip: str, ping_count=10):
    ip, port = ssh_client.get_transport().getpeername()
    cmd = 'ping -c ' + str(ping_count) + ' ' + dst_ip
    ch, stdin, stdout, stderr = no_sudo_exec(ssh_client, cmd)
    print_stdout_blocking(stdout, "ping to " + dst_ip, ip, port)
    print_stderr_blocking(stderr, "ping to " + dst_ip, ip, port)
    return


def run_tb_server(ssh_client: paramiko.client.SSHClient, working_dir: str):
    ip, port = ssh_client.get_transport().getpeername()
    p_to_dir = os.path.join(working_dir, 'controller_src')
    p_to_script = os.path.join(working_dir, 'controller_src/exp_src/measurement_app/run_tb_server.py')
    cmd = 'PYTHONPATH=' + p_to_dir + ' python3 ' + p_to_script

    ch, stdin, stdout, stderr = no_sudo_exec(ssh_client, cmd)
    print_stdout_blocking(stdout, "run_tb_server", ip, port)
    print_stderr_blocking(stderr, "run_tb_server", ip, port)
    return
