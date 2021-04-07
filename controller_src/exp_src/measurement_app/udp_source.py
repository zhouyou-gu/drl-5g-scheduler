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

from exp_src.measurement_app.util import *
from exp_src.util import *

PACKER = struct.pack


def run_udp_source(server_ip, server_port, n_per_test, length_generator: MeasurementLengthGenerator,
                   interval_generator: MeasurementIntervalGenerator):
    import os
    os.nice(-20)
    total_seq = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = (server_ip, server_port)
    while True:
        i = interval_generator.generate_a_interval_ms()
        i = float(i) / 1e3
        time.sleep(i)

        l = length_generator.generate_a_length_byte()
        p = "x" * (l - MEASUREMENT_HEADER_SIZE + 1)
        p_bytes = p.encode('utf-8')

        test_id = int(total_seq / n_per_test)
        tot = n_per_test
        seq = int(total_seq - test_id * n_per_test)

        seq_bytes = PACKER('!III', seq, tot, test_id)
        ns = read_time_ns()
        s, ns = ns_to_seconds_nanos(ns)
        time_bytes = PACKER('!QI', s, ns)

        sock.sendto(time_bytes + seq_bytes + p_bytes, server)

        total_seq += 1
    # if total_seq % n_per_test == 0:
    # 	time.sleep(1)


class UdpSource(Thread):
    def __init__(self, server_ip, server_port, n_per_test, length_generator: MeasurementLengthGenerator,
                 interval_generator: MeasurementIntervalGenerator):
        Thread.__init__(self)
        self.length_generator = length_generator
        self.interval_generator = interval_generator

        self.n_per_test = n_per_test
        self.server = (server_ip, server_port)

        self.q = Queue()

        self.sink_process = Process(target=run_udp_source,
                                    args=(server_ip, server_port, n_per_test, length_generator, interval_generator))

    def run(self):
        self.sink_process.start()
        self.sink_process.join()


if __name__ == '__main__':
    from exp_src.measurement_app.util import ConstantSizeLG, PoissonIG

    lg = ConstantSizeLG(500)
    ig = PoissonIG(100)

    source = UdpSource('0.0.0.0', 4010, 100, lg, ig)
    source.start()

# p = MeasurementPacket()
# p.timestamp.seconds, p.timestamp.nanos = ns_to_seconds_nanos(read_time_ns())
# from pprint import pprint
# pprint(vars(p.timestamp))
#
# socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server = ('0.0.0.0', 9000)
# socket.connect(server)
# socket.sendall(p.pack_to_bytes())
