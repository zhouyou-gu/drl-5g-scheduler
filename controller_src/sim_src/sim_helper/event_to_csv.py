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
from multiprocessing import Process

from sim_src.tb_logger import TBScalarToCSV


def export_event_to_csv(path_to_dir, scalar_list):
    a = TBScalarToCSV(path_to_dir, path_to_dir, scalar_list)


class EventToCsvHandler():
    def __init__(self, event_dir=None, dir_pattern=None, scalar_list=None):
        assert isinstance(event_dir, list)
        assert isinstance(dir_pattern, str)
        assert isinstance(scalar_list, list)

        self.proc_list = []
        for sim in event_dir:
            for path, dirs, files in os.walk(sim):
                for d in dirs:
                    if fnmatch.fnmatch(d, dir_pattern):
                        path_to_dir = os.path.join(path, d)
                        print('export event', path_to_dir)
                        proc = Process(target=export_event_to_csv, args=(path_to_dir, scalar_list,))
                        self.proc_list.append(proc)

        for proc in self.proc_list:
            proc.start()

        for proc in self.proc_list:
            proc.join()
