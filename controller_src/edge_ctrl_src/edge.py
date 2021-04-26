#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from collections import namedtuple
from threading import Thread

from edge_ctrl_src.ptp_ctrl import *
from edge_ctrl_src.srslte_ctrl import *

PC_ACCESS_CONFIG = namedtuple('PC_ACCESS_CONFIG', ['name', 'ip', 'port', 'username', 'password', 'working_dir'])
EDGE_ACCESS_CONFIG = namedtuple('EDGE_ACCESS_CONFIG', ['epc_config', 'enb_config', 'ue_config_list'])


class Edge():
    def __init__(self, id, config):
        self.id = id
        self.config = config

        self.epc = None
        self.enb = None
        self.ues = []
        self._connect()

        self.t_epc = None
        self.t_enb = None
        self.t_ues = []

        self._ddrl_enabled = True

    def run_edge(self, time_s):
        '''
		:param time_s:
		:return:
		'''
        self._run_epc(time_s)
        self._run_enb(time_s)
        self._run_ues(time_s)

    # self.t_enb.join()
    # for u in range(len(self.t_ues)):
    # 	self.t_ues[u].join()
    # self.t_epc.join()

    def run_app(self):
        pass

    def _connect(self):
        self._connect_epc()
        self._connect_enb()
        self._connect_ues()
        return

    def _connect_epc(self):
        self.epc = paramiko.SSHClient()
        self.epc.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.epc.connect(self.config.epc_config.ip,
                         port=self.config.epc_config.port,
                         username=self.config.epc_config.username,
                         password=self.config.epc_config.password)

    def _connect_enb(self):
        self.enb = paramiko.SSHClient()
        self.enb.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.enb.connect(self.config.enb_config.ip,
                         port=self.config.enb_config.port,
                         username=self.config.enb_config.username,
                         password=self.config.enb_config.password)

    def _connect_ues(self):
        self.ues = []
        for x in self.config.ue_config_list:
            u = paramiko.SSHClient()
            u.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            u.connect(x.ip,
                      port=x.port,
                      username=x.username,
                      password=x.password)
            self.ues.append(u)

    def ptp_sync(self):
        # Warning: only EPC and UE need to be sync

        # run ptp4l
        t = Thread(target=run_ptp4l, args=(self.epc, self.config.epc_config.password, True))
        t.start()
        t = Thread(target=run_phc2sys, args=(self.epc, self.config.epc_config.password, True))
        t.start()
        for u in range(len(self.ues)):
            t = Thread(target=run_ptp4l, args=(self.ues[u], self.config.ue_config_list[u].password, False))
            t.start()
            t = Thread(target=run_phc2sys, args=(self.ues[u], self.config.ue_config_list[u].password, False))
            t.start()

    def sync_global_time(self):
        t = Thread(target=sync_eth_with_right_time, args=(self.epc, self.config.epc_config.password))
        t.start()
        for u in range(len(self.ues)):
            t = Thread(target=sync_eth_with_right_time, args=(self.ues[u], self.config.ue_config_list[u].password))
            t.start()

    def compile(self):
        self._compile_epc()
        self._compile_enb()
        self._compile_ues()

    # TODO: wait compile finish

    def clean_compilation(self):
        clean_srs(self.epc, os.path.join(self.config.epc_config.working_dir , 'edge_src/'), self.config.epc_config.password)
        clean_srs(self.enb, os.path.join(self.config.enb_config.working_dir , 'edge_src/'), self.config.enb_config.password)
        for u in range(len(self.ues)):
            clean_srs(self.ues[u], os.path.join(self.config.ue_config_list[u].working_dir , 'edge_src/'),
                      self.config.ue_config_list[u].password)

    def _compile_epc(self):
        pass

    # compile_srs(self.epc, self.config.epc_config.working_dir + 'edge_src/', self.config.epc_config.password,as_original_srslte=True)

    def _compile_enb(self):
        compile_srs(self.enb, os.path.join(self.config.enb_config.working_dir , 'edge_src/'), self.config.enb_config.password,
                    ddrl_enabled=self._ddrl_enabled)

    def _compile_ues(self):
        for u in range(len(self.ues)):
            compile_srs(self.ues[u], os.path.join(self.config.ue_config_list[u].working_dir , 'edge_src/'),
                        self.config.ue_config_list[u].password, ddrl_enabled=self._ddrl_enabled)

    def _run_epc(self, time_s):
        t = Thread(target=run_srsepc, args=(
            self.epc, os.path.join(self.config.epc_config.working_dir , 'edge_src/build/srsLTE/srsepc/src/srsepc'),
            self.config.epc_config.password, time_s,))
        t.start()
        self.t_epc = t

    def _run_enb(self, time_s):
        t = Thread(target=run_srsenb, args=(
            self.enb, os.path.join(self.config.enb_config.working_dir , 'edge_src/build/srsLTE/srsenb/src/srsenb'),
            self.config.enb_config.password, time_s,))
        t.start()
        self.t_enb = t

    def _run_ues(self, time_s):
        self.t_ues = []
        for u in range(len(self.ues)):
            # ue idx start for 1
            t = Thread(target=run_srsue, args=(
                u + 1, self.ues[u], os.path.join(self.config.ue_config_list[u].working_dir , 'edge_src/build/srsLTE/srsue/src/srsue'),
                self.config.ue_config_list[u].password, time_s,))
            t.start()
            self.t_ues.append(t)

    def run_one_sudo_command(self, cmd):
        run_one_sudo_cmd(self.epc, cmd, self.config.epc_config.password)
        run_one_sudo_cmd(self.enb, cmd, self.config.enb_config.password)
        for u in range(len(self.ues)):
            run_one_sudo_cmd(self.ues[u], cmd, self.config.ue_config_list[u].password)

    def run_one_no_sudo_command(self, cmd):
        run_one_no_sudo_cmd(self.epc, cmd)
        run_one_no_sudo_cmd(self.enb, cmd)
        for u in range(len(self.ues)):
            run_one_no_sudo_cmd(self.ues[u], cmd)

    def reboot(self):
        try:
            reboot_pc(self.epc, self.config.epc_config.password)
            reboot_pc(self.enb, self.config.enb_config.password)
        except:
            print('reboot enb/epc error')
        for u in range(len(self.ues)):
            try:
                reboot_pc(self.ues[u], self.config.ue_config_list[u].password)
            except:
                print('reboot ue', u + 1, 'error')

    def upload_all_src_file_to_edge(self, path_to_project):

        upload_file(self.epc, path_to_project, self.config.epc_config.working_dir)

        upload_file(self.enb, path_to_project, self.config.enb_config.working_dir)

        for u in range(len(self.ues)):
            upload_file(self.ues[u], path_to_project, self.config.ue_config_list[u].working_dir)

    def _create_working_dirs(self):

        run_one_no_sudo_cmd(self.epc, 'mkdir ' + self.config.epc_config.working_dir)

        run_one_no_sudo_cmd(self.enb, 'mkdir ' + self.config.enb_config.working_dir)

        for u in range(len(self.ues)):
            run_one_no_sudo_cmd(self.ues[u], 'mkdir ' + self.config.enb_config.working_dir)
