from numpy import sqrt, log, log2, concatenate, reshape, exp, pi
import sympy, progressbar, plot
from fractions import Fraction
from numpy.random import randint, shuffle
from numpy.linalg import eig
from math import gcd
from time import time
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


def periodFind(x, N):
    mat_size = int(2 ** np.ceil(log2(N)))
    j_new_mat = np.array(())

    U = np.zeros((mat_size, mat_size))
    for i in range(0, mat_size):
        if i >= N:
            U[i][i] = 1
        else:
            U[int((i * x) % N)][i] = 1
    for j_val in range(0, mat_size):
        j = np.zeros((1, mat_size))
        j[:, j_val] = 1

        j_new = j*U
        j_new = reshape(j_new[:, j_val], (1, mat_size))
        if j_new_mat.shape[0] == 0:
            j_new_mat = j_new
        else:
            j_new_mat = concatenate([j_new_mat, j_new], axis=0)
    j_new_mat = j_new_mat.T
    # print(U)
    eig_val = eig(U)[0][randint(0, len(eig(U)[0]))]
    print(eig_val)
    r = Fraction(float((log(eig_val) / (1j * 2 * pi)))).limit_denominator().denominator
    return r


def factor(N, fail_count):
    x = randint(2, sqrt(N) + 1)
    d = gcd(N, x)
    if d != 1:
        return N // d, d, fail_count

    r = periodFind(x, N)
    if r % 2 != 0:
        fail_count += 1
        return factor(N, fail_count)
    f1, f2 = (x ** (r // 2) - 1), (x ** (r // 2) + 1)
    f1, f2 = gcd(f1, N), gcd(f2, N)

    if f2 == 1 or f2 == N:
        fail_count += 1
        return factor(N, fail_count)

    if not abs(int(N / f1) - N / f1) < 1e-10:
        fail_count += 1
        return factor(N, fail_count)

    return f2, f1, fail_count


def main(N):
    # print('N = %s' % N)
    if abs(int(sqrt(N)) - sqrt(N)) < 1e-10:
        f1, f2, fail_count = int(sqrt(N)), int(sqrt(N)), 0
    elif not sympy.isprime(N):
        f1, f2, fail_count = factor(N, 0)
    else:
        # print('Prime number detected. Stopping...')
        return False
    print('%s can be factored by %s and %s' % (f1*f2, f1, f2))
    print('Fails:\t%s' % fail_count)

    return fail_count


def analyze_fails():
    numbers_avg, fail_counts_avg = [], []
    nums, find_times = [], []
    bar = progressbar.ProgressBar()

    for i in bar(range(2, 16)):
        numbers, fail_counts = [], []
        for j in range(0, 1000):
            start_time = time()
            N = randint(2 ** i, 2 ** (i + 1))
            f_count = main(N)
            end_time = time()
            if f_count is not False:
                numbers.append(log(N))
                fail_counts.append(f_count)
        numbers_avg.append(np.mean(numbers)), fail_counts_avg.append(np.mean(fail_counts))
    print('Time elapsed:\t%s seconds' % str(end_time - start_time))
    np.save('results.npy', [numbers_avg, fail_counts_avg])
    plot.graph_fails()


def analyze_periods():
    find_times, nums = [], []
    bar = progressbar.ProgressBar()
    for i in bar(range(0, 100)):
        N = 2 * (randint(2 ** 2, 2 ** 16)) + 1
        N = 71405
        x = randint(2, sqrt(N) + 1)
        x = 245
        time_start = time()
        periodFind(x, N)
        time_end = time()
        find_times.append(time_end - time_start), nums.append(N)
        # np.save('results_period.npy', [nums, find_times])
        # plot.graph_period()


# periodFind(7, 153)
if __name__ == "main":
    main(15)
