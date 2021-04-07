#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import math

import numpy as np
from scipy.stats import norm

MAX_NUM_RB = 100


def channel_dispersion(snr: float):
    x = 1 + snr
    x = x * x
    x = 1 / x
    x = 1 - x
    return float(x)


def polyanskiy_model_part1(T_f_s, rb_bw_Hz, snr_dec: float, n_rb):
    x = 1 + snr_dec
    x = math.log(x)
    x = x / math.log(2)
    x = x * T_f_s * rb_bw_Hz * n_rb
    return x


def polyanskiy_model_part2(T_f_s, rb_bw_Hz, snr_dec, n_rb):
    x = channel_dispersion(snr_dec)
    x = x * T_f_s * rb_bw_Hz * n_rb
    x = math.sqrt(x)
    x = x / math.log(2)
    return x


def tx_error_rate_for_n_bytes(n_byte, n_rb, snr_dec, T_f_s, rb_bw_Hz) -> float:
    n_bit = n_byte * 8
    x = n_bit - polyanskiy_model_part1(T_f_s, rb_bw_Hz, snr_dec, n_rb)
    x = -x
    x = x / polyanskiy_model_part2(T_f_s, rb_bw_Hz, snr_dec, n_rb)
    return norm.sf(x)


def distance_to_snr(distance_m, tx_power_dbm, noise_power_dbm) -> float:
    if distance_m < 1:
        return tx_power_dbm - 45 - noise_power_dbm
    x = 10 * math.log10(distance_m)
    x = x * 3
    x = 45 + x
    return (tx_power_dbm - x) - noise_power_dbm


def p_true(probability_of_true):
    return np.random.choice([True, False], p=[probability_of_true, 1 - probability_of_true])


def dec_to_db(dec: float) -> float:
    return 10 * math.log10(dec)


def db_to_dec(db: float) -> float:
    return 10 ** (db / 10)


if __name__ == '__main__':
    print(distance_to_snr(200, 20, -90))
