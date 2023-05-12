def hol_is_in_range(hol, d_min, d_max) -> bool:
    if hol >= d_min and hol <= d_max:
        return True
    else:
        return False


def hol_flat_reward(hol, d_min, d_max) -> float:
    if not hol_is_in_range(hol, d_min, d_max):
        return 0.
    else:
        return 1.


if __name__ == '__main__':
    #  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

    a = hol_is_in_range(7, 4, 6)
    print(a)

    a = hol_flat_reward(2, 4, 60)
    print(a)
