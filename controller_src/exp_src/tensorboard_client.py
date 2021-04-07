#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from google.protobuf.any_pb2 import Any

from exp_src.sctp_client import SctpClient
from exp_src.tensorboard_server import TENSORBOARD_SERVER_PORT
from exp_src.util import *
from proto_py.scalar_report_pb2 import scalar


class TBClient(SctpClient):
    def __init__(self, server_ip: str, server_port: int):
        SctpClient.__init__(self, server_ip, server_port)

    def send_scalar(self, name: str, time_step: int, value: float):
        s = scalar()
        s.name = name

        s.tti = time_step

        ns = read_time_ns()
        s.timestamp.seconds, s.timestamp.nanos = ns_to_seconds_nanos(ns)

        s.value = value

        any = Any()
        any.Pack(s)

        self.send(any.SerializeToString())


if __name__ == '__main__':
    c = TBClient("127.0.1.1", TENSORBOARD_SERVER_PORT)

    i = 0
    while True:
        c.send_scalar("TBScalarReporter", i, i)
        i += 1
        time.sleep(0.01)
