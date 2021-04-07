#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import time


def read_time_ns():
    return int(time.clock_gettime(time.CLOCK_REALTIME) * 1e9)


def ns_to_seconds_nanos(ns: int):
    sec = int(ns / 1e9)
    nsec = int(ns - sec * int(1e9))
    return sec, nsec


def seconds_nanos_to_ns(seconds: int, nanos: int):
    return int(seconds * 1e9 + nanos)


def ns_to_us(t: float):
    return t / 1e3


def ns_to_ms(t: float):
    return t / 1e6


if __name__ == '__main__':
    print(ns_to_ms(int(1231)))
