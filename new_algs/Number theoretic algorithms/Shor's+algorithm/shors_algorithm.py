from numpy import sqrt, log
import sympy, progressbar, plot
from numpy.random import randint
from math import gcd
from time import time
import numpy as np
import matplotlib.pyplot as plt


def periodFind(x, N):
    bar = progressbar.ProgressBar()
    for i in bar(range(1, N)):
        f = (x**i) % N
        if f == 1:
            print(i)
            print(x)
            return i
    print('here1')


def factor(N, fail_count):
    x = randint(2, sqrt(N)+1)
    d = gcd(N,x)
    if d != 1:
        return N//d, d, fail_count

    i = periodFind(x, N)
    if i % 2 != 0:
        fail_count += 1
        # print('fail')
        return factor(N, fail_count)
    
    f1, f2 = (x**(i//2)-1), (x**(i//2)+1)
    f1, f2 = gcd(f1, N), gcd(f2, N)
    
    if f2 == 1 or f2 == N:
        fail_count += 1
        # print('fail')
        return factor(N, fail_count)

    if not abs(int(N/f1) - N/f1) < 1e-10:
        fail_count += 1
        # print('fail')
        return factor(N, fail_count)
    
    return f2, f1, fail_count


def main(N):
    # print('N = %s' % N)
    if abs(int(sqrt(N))-sqrt(N)) < 1e-10:
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
            N = randint(2**i, 2**(i+1))
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
        N = 2*(randint(2**2, 2**16))+1
        x = randint(2, sqrt(N) + 1)
        time_start = time()
        periodFind(x, N)
        time_end = time()
        find_times.append(time_end-time_start), nums.append(N)
    # np.save('results_period.npy', [nums, find_times])
    # plot.graph_period()
main(301)