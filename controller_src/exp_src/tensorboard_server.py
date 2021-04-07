#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from google.protobuf.any_pb2 import Any
from google.protobuf.timestamp_pb2 import Timestamp

from exp_src.sctp_server import SctpServer
from exp_src.socket_conn_handler import ConnListener
from proto_py.scalar_report_pb2 import scalar

TENSORBOARD_SERVER_PORT = 4003


class TBClientListener(ConnListener):
    def __init__(self, conn, logger):
        ConnListener.__init__(self, 'TBClientListener', conn)
        self.logger = logger

    def process_data(self, data):
        t = scalar()
        any = Any()
        any.ParseFromString(data)
        if any.Is(t.DESCRIPTOR):
            any.Unpack(t)
            self.logger.add_scalar(t.name, t.value, t.tti, float(t.timestamp.ToMicroseconds()) / 1e6)


class TBServer(SctpServer):
    def __init__(self, server_bind_ip, server_bind_port, logger):
        SctpServer.__init__(self, 'TBServer', server_bind_ip, server_bind_port, 100)
        self.logger = logger
        self.tb_client_listener_thread_list = []

    def connection_handler(self, conn):
        print('TBServer get conn from', conn)
        c = TBClientListener(conn, self.logger)
        c.start()
        self.tb_client_listener_thread_list.append(c)


if __name__ == '__main__':
    from sim_src.tb_logger import GLOBAL_LOGGER

    GLOBAL_LOGGER.set_log_path('/tmp/aaaaa/', 'test_tensor_board_server', 'test_tensor_board_server')

    t = scalar()
    t.tti = 1213
    t.name = 'hello'
    ts = Timestamp()
    t.timestamp.seconds = 10
    t.timestamp.nanos = 112310
    print(t.timestamp.ToMicroseconds())
    print(t.name)
    print(t.timestamp)
    print(t.tti)
    print(t.value)

    server = TBServer(server_bind_ip='127.0.1.100', server_bind_port=TENSORBOARD_SERVER_PORT,
                      logger=GLOBAL_LOGGER.get_tb_logger())
    server.start()
