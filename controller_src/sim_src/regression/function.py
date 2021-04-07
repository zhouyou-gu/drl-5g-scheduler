#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from sim_src import StatusObject
from sim_src.sim_env.math_models import *

PCT_LEVELS = 16


def get_a_rb_pct(size=5, out_of_range_pr=0.2):
    out_of_range = np.random.choice([0, 1], size, p=[out_of_range_pr, 1 - out_of_range_pr])
    a = np.random.choice(PCT_LEVELS, size)
    a = np.multiply(a, out_of_range)
    a = np.negative(a)
    a = np.add(a, PCT_LEVELS)
    return a / PCT_LEVELS


def get_a_hol_pct(size=5, empty_pr=0.2):
    empty = np.random.choice([0, 1], size, p=[empty_pr, 1 - empty_pr])
    hol = np.random.choice(PCT_LEVELS, size)
    return np.multiply(empty, hol) / PCT_LEVELS


def rb_to_snr(rb):
    ret = -5
    for x in range(-5, 31):
        e = tx_error_rate_for_n_bytes(32, rb, db_to_dec(float(x)), 1e-4, 180e3)
        if e < 1e-5:
            return e
        ret = e

    return ret


class Function(StatusObject):
    def get_a_batch(self, batch_size):
        pass

    def forward(self, x: np.ndarray) -> np.ndarray:
        pass


class EDFSchedulerFuncion(Function):
    def __init__(self, in_dim, out_dim, d_min_pct):
        self.input_history = np.array([]).reshape((0, in_dim))
        self.output_history = np.array([]).reshape((0, out_dim))

        self.in_dim = in_dim
        self.out_dim = out_dim

        self.d_min_pct = d_min_pct

    def forward(self, x: np.ndarray) -> np.ndarray:
        sum_pct = 0
        input_cp = np.copy(x)
        output_vector = np.zeros(self.out_dim)
        for u in range(0, self.out_dim):
            hol_temp = 0
            index = 0
            for uu in range(0, self.out_dim):
                if input_cp[uu] >= hol_temp:
                    index = uu
                    hol_temp = input_cp[uu]
            if hol_temp >= self.d_min_pct:
                sum_pct += x[index + self.out_dim]
                if sum_pct >= 1:
                    break
                output_vector[index] = x[index + self.out_dim]
                input_cp[index] = 0

        if sum_pct > 0:
            output_vector = output_vector * (1 / float(sum_pct))

        output_vector[output_vector > 0.] = 1
        output_vector = output_vector * 2. - 1.
        return output_vector

    def _get_random_input(self) -> np.ndarray:
        ret = np.zeros(self.in_dim)

        ret[0:int(self.in_dim / 2)] = get_a_hol_pct(size=int(self.out_dim))
        ret[int(self.in_dim / 2):self.in_dim] = get_a_rb_pct(size=int(self.out_dim))

        return ret

    def get_a_batch(self, batch_size):
        input_mat = np.array([]).reshape(0, self.in_dim)
        output_mat = np.array([]).reshape(0, self.out_dim)
        for i in range(batch_size):
            in_v = self._get_random_input()
            out_v = self.forward(in_v)
            input_mat = np.vstack((input_mat, in_v))
            output_mat = np.vstack((output_mat, out_v))
        return input_mat, output_mat


class MTSchedulerFuncion(Function):
    def __init__(self, in_dim, out_dim, d_min_pct):
        self.input_history = np.array([]).reshape((0, in_dim))
        self.output_history = np.array([]).reshape((0, out_dim))

        self.in_dim = in_dim
        self.out_dim = out_dim

        self.d_min_pct = d_min_pct

    def forward(self, x: np.ndarray) -> np.ndarray:
        sum_pct = 0
        input_cp = np.copy(x)
        output_vector = np.zeros(self.out_dim)

        idxs = []
        for u in range(0, self.out_dim):
            if input_cp[u] >= self.d_min_pct:
                idxs.append(u)

        for i in range(self.out_dim):
            n_rb_min = 1.
            uuu = None
            for uu in idxs:
                if input_cp[uu + self.out_dim] <= n_rb_min and output_vector[uu] == 0:
                    n_rb_min = input_cp[uu + self.out_dim]
                    uuu = uu
            if uuu is not None:
                sum_pct += x[uuu + self.out_dim]
                if sum_pct >= 1:
                    break
                output_vector[uuu] = 1.

        output_vector[output_vector > 0.] = 1.
        output_vector[output_vector <= 0.] = -1.
        return output_vector

    def _get_random_input(self) -> np.ndarray:
        ret = np.zeros(self.in_dim)

        ret[0:int(self.in_dim / 2)] = get_a_hol_pct(size=int(self.out_dim))
        ret[int(self.in_dim / 2):self.in_dim] = get_a_rb_pct(size=int(self.out_dim))

        return ret

    def get_a_batch(self, batch_size):
        input_mat = np.array([]).reshape(0, self.in_dim)
        output_mat = np.array([]).reshape(0, self.out_dim)
        for i in range(batch_size):
            in_v = self._get_random_input()
            out_v = self.forward(in_v)
            input_mat = np.vstack((input_mat, in_v))
            output_mat = np.vstack((output_mat, out_v))
        return input_mat, output_mat


class RRSchedulerFuncion(Function):
    def __init__(self, in_dim, out_dim, d_min_pct):
        self.input_history = np.array([]).reshape((0, in_dim))
        self.output_history = np.array([]).reshape((0, out_dim))

        self.in_dim = in_dim
        self.out_dim = out_dim

        self.d_min_pct = d_min_pct

        self.last_idx = -1  # start the last idx with -1

    def forward(self, x: np.ndarray) -> np.ndarray:
        sum_pct = 0.
        input_cp = np.copy(x)
        output_vector = np.zeros(self.out_dim)

        idxs = []
        for u in range(0, self.out_dim):
            if input_cp[u] >= self.d_min_pct:
                idxs.append(u)

        i = self.last_idx + 1
        i = (i % self.out_dim)
        while idxs and sum_pct < 1.:
            if (i % self.out_dim) in idxs:
                # do scheduling
                sum_pct += x[i + self.out_dim]
                if sum_pct >= 1.:
                    break
                output_vector[i] = 1.
                idxs.remove(i)
                self.last_idx = i
            else:
                pass
            i = i + 1
            i = (i % self.out_dim)

        output_vector[output_vector > 0.] = 1.
        output_vector[output_vector <= 0.] = -1.
        return output_vector

    def _get_random_input(self) -> np.ndarray:
        ret = np.zeros(self.in_dim)

        ret[0:int(self.in_dim / 2)] = get_a_hol_pct(size=int(self.out_dim))
        ret[int(self.in_dim / 2):self.in_dim] = get_a_rb_pct(size=int(self.out_dim))

        return ret

    def get_a_batch(self, batch_size):
        input_mat = np.array([]).reshape(0, self.in_dim)
        output_mat = np.array([]).reshape(0, self.out_dim)
        for i in range(batch_size):
            in_v = self._get_random_input()
            out_v = self.forward(in_v)
            input_mat = np.vstack((input_mat, in_v))
            output_mat = np.vstack((output_mat, out_v))
        return input_mat, output_mat


if __name__ == '__main__':
    print(np.empty(4))
    print(np.zeros(1))
    a = np.zeros(1)
    a += 7
    print(np.random.choice(100, 10))
    print(get_a_rb_pct())

    a = EDFSchedulerFuncion(in_dim=10, out_dim=5, d_min_pct=0.1)

    i = a._get_random_input()
    print(i)
    o = a.forward(i)
    print(o)
    print((o + 1) / 2.)

    a = RRSchedulerFuncion(in_dim=10, out_dim=5, d_min_pct=0.1)

    for ii in range(10000):
        print("++++++++++++++++++++++++++")
        i = a._get_random_input()
        print(i)
        o = a.forward(i)
        print(o, (o + 1) / 2., a.last_idx)
