#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import socket
import struct
from multiprocessing import Process, Queue
from threading import Thread

from exp_src.tensorboard_client import TBClient
from exp_src.tensorboard_server import TENSORBOARD_SERVER_PORT
from exp_src.util import *

UNPACKER = struct.unpack


def run_udp_sink(udp_sink_port, queue):
    import os
    os.nice(-20)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(('0.0.0.0', udp_sink_port))

    while True:
        data = sock.recv(4096)
        now = read_time_ns()
        p = UNPACKER('!QIIII', data[0:24])
        queue.put((p, now))


class UdpSink(Thread):
    def __init__(self, udp_sink_port, tb_server_ip, tb_server_port):
        Thread.__init__(self)
        self.current_test_id = 0
        self.current_test_total_packet = 0
        self.current_test_received_packet = 0

        self.timeliness_current_test_received_packet = 0

        self.total_received = 0

        self.ns_now = 0

        self.tb_client = TBClient(tb_server_ip, tb_server_port)
        self.q = Queue()

        self.sink_process = Process(target=run_udp_sink, args=(udp_sink_port, self.q))

        self.average_delay = 0.

    def run(self):
        print('udp_sink running')
        self.tb_client.start()
        self.sink_process.start()
        while True:
            (p, rx_time) = self.q.get()
            self.log_packet(p[2], p[3], p[4], int(p[0] * 1e9 + p[1]), rx_time)

        self.sink_process.join()

    def log_packet(self, seq, tot, test_id, tx_time, rx_time):
        d = rx_time - tx_time
        if d <= 0:
            print('ERROR: latency', d, '<=0')
        else:
            self.average_delay = 0.99 * self.average_delay + 0.01 * ns_to_ms(d)
            self.tb_client.send_scalar(socket.gethostname() + '_Latency_ms', self.total_received, ns_to_ms(d))
            if test_id != self.current_test_id:
                self.current_test_id = test_id
                print('average lateny ms', self.average_delay)
                if self.current_test_total_packet > 0:
                    rel = float(self.current_test_received_packet) / float(self.current_test_total_packet)
                    self.tb_client.send_scalar(socket.gethostname() + '.reliability', self.total_received, rel)
                    rel_timeliness = float(self.timeliness_current_test_received_packet) / float(
                        self.current_test_total_packet)
                    self.tb_client.send_scalar(socket.gethostname() + '.reliability.timeliness', self.total_received,
                                               rel_timeliness)
                    print('report reliability', rel, '\t', rel_timeliness)

                self.current_test_received_packet = 0  # reset packet counter
                self.timeliness_current_test_received_packet = 0
                self.receive_one_packet(d)
                self.current_test_total_packet = tot

            else:
                self.receive_one_packet(d)

        self.total_received += 1
        return

    def receive_one_packet(self, delay_ns):
        self.current_test_received_packet += 1

        if delay_ns >= 8e6 and delay_ns <= 12e6:
            self.timeliness_current_test_received_packet += 1


if __name__ == '__main__':
    sink = UdpSink(4010, '127.0.1.100', TENSORBOARD_SERVER_PORT)
    sink.start()
