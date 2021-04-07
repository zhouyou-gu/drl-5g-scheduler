#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import numpy as np

"""
measurement packet structure

seconds                         uint64
nanos                           uint32
seq                             uint32
number of packet per test       uint32
current test id                 uint32
padding                         str
"""

MIN_MEASUREMENT_PACKET_SIZE = 25
MEASUREMENT_HEADER_SIZE = 25


class MeasurementLengthGenerator():
    def generate_a_length_byte(self):
        pass


class MeasurementIntervalGenerator():
    def generate_a_interval_ms(self):
        pass


class ConstantSizeLG(MeasurementLengthGenerator):
    def __init__(self, packet_size):
        if (packet_size < MIN_MEASUREMENT_PACKET_SIZE):
            print('ConstantSizePG packet_size', packet_size, 'is larger than min packet_size', self.min_len)
            print('ConstantSizePG use', self.min_len, 'as packet_size')
            self.packet_size = MIN_MEASUREMENT_PACKET_SIZE
        else:
            self.packet_size = packet_size

    def generate_a_length_byte(self):
        return self.packet_size


class PoissonIG(MeasurementIntervalGenerator):
    def __init__(self, mean_ms: float):
        self.mean_ms = mean_ms

    def generate_a_interval_ms(self):
        return np.random.exponential(self.mean_ms)


if __name__ == '__main__':
    pass
