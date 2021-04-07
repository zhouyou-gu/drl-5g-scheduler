#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import fnmatch
import os
import select

import paramiko
import scp

GET_DEAULT_ETH_CMD = " route | grep '^default' | grep -o '[^ ]*$' "


def no_sudo_exec(ssh_client: paramiko.client.SSHClient, cmd: str, block=True):
    ch = ssh_client.get_transport().open_session()
    if block:
        ch.get_pty()
    ch.exec_command(cmd)
    stdin = ch.makefile_stdin("wb", -1)
    stdout = ch.makefile("r", -1)
    stderr = ch.makefile_stderr("r", -1)
    return ch, stdin, stdout, stderr


def sudo_exec(ssh_client: paramiko.client.SSHClient, cmd: str, password: str, block=True):
    ch = ssh_client.get_transport().open_session()
    if block:
        ch.get_pty()
    ch.exec_command(cmd)
    stdin = ch.makefile_stdin("wb", -1)
    stdin.write(password + '\n')
    stdin.flush()
    stdout = ch.makefile("r", -1)
    stderr = ch.makefile_stderr("r", -1)
    stdout.readline()
    stdout.readline()
    return ch, stdin, stdout, stderr


def print_stdout_blocking(stdout, tag, ip, port):
    for x in iter(stdout.readline, ''):
        print(tag + ':OUT', ip, port, x, end='')


def print_stderr_blocking(stderr, tag, ip, port):
    for x in iter(stderr.readline, ''):
        print(tag + ':ERR', ip, port, x, end='')


def print_stdout_no_blocking(stdout, tag, ip, port):
    if stdout.channel.recv_ready():
        rl, wl, xl = select.select([stdout.channel], [], [], 0.)
        if len(rl) > 0:
            print(tag + ':OUT', ip, port, stdout.channel.recv(1024).decode("utf-8"), end='')


def print_stderr_no_blocking(stderr, tag, ip, port):
    if stderr.channel.recv_ready():
        rl, wl, xl = select.select([stderr.channel], [], [], 0.)
        if len(rl) > 0:
            print(tag + ':ERR', ip, port, stderr.channel.recv(1024).decode("utf-8"), end='')


def reboot_pc(ssh_client: paramiko.client.SSHClient, password: str):
    ip, port = ssh_client.get_transport().getpeername()
    cmd = 'sudo -S -p " " reboot'
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd, password)
    print_stdout_blocking(stdout, "reboot_pc", ip, port)
    print_stderr_blocking(stderr, "reboot_pc", ip, port)
    return


def run_one_sudo_cmd(ssh_client: paramiko.client.SSHClient, cmd: str, password: str):
    ip, port = ssh_client.get_transport().getpeername()
    cmd_s = 'sudo -S -p " " ' + cmd
    ch, stdin, stdout, stderr = sudo_exec(ssh_client, cmd_s, password)
    print_stdout_blocking(stdout, "run_one_sudo_cmd", ip, port)
    print_stderr_blocking(stderr, "run_one_sudo_cmd", ip, port)
    return


def run_one_no_sudo_cmd(ssh_client: paramiko.client.SSHClient, cmd: str):
    ip, port = ssh_client.get_transport().getpeername()
    ch, stdin, stdout, stderr = no_sudo_exec(ssh_client, cmd)
    print_stdout_blocking(stdout, "run_one_no_sudo_cmd", ip, port)
    print_stderr_blocking(stderr, "run_one_no_sudo_cmd", ip, port)
    return


def upload_file(ssh_client: paramiko.client.SSHClient, local_path, remote_path):
    def print_progress(filename, size, sent, trans):
        print(trans, "%s\'s progress: %.2f%%   \r" % (filename, float(sent) / float(size) * 100))

    scp_client = scp.SCPClient(ssh_client.get_transport(), progress4=print_progress)

    def fnmatch_list(fn, l):
        for n in l:
            if fnmatch.fnmatch(fn, n):
                return True
        return False

    ex_list = ['.svn', '.cvs', '.idea', '.DS_Store', '.git', '.hg', '.hprof', '*.pyc', 'build', '*-build-*',
               '__pycache__', 'events*', '*.pt']

    for path, dirs, files in os.walk(local_path, topdown=True):
        dirs[:] = [d for d in dirs if not fnmatch_list(d, ex_list)]
        for d in dirs:
            local_p_to_d = os.path.join(path, d)
            relative_p_to_d = os.path.relpath(local_p_to_d, local_path)
            remote_p_to_d = os.path.join(remote_path, relative_p_to_d)
            print('cp from:	', relative_p_to_d)
            print('cp to:	', remote_p_to_d, scp_client.peername)
            run_one_no_sudo_cmd(ssh_client, 'mkdir ' + remote_p_to_d)

        for filename in files:
            if fnmatch_list(filename, ex_list):
                continue
            local_p_to_f = os.path.join(path, filename)
            relative_p_to_f = os.path.relpath(local_p_to_f, local_path)
            remote_p_to_f = os.path.join(remote_path, relative_p_to_f)
            print('local file', local_p_to_f)
            print('remote file', remote_p_to_f)

            print(scp_client.put(local_p_to_f, remote_path=remote_p_to_f, preserve_times=False))

    return


if __name__ == '__main__':
    pass
