# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:58:03 2019

@author: DSU
"""

import sys
sys.path.append("..")

import fibonacci.fibonacci_cpp as cpp
import fibonacci.fibonacci_python as python
import fibonacci.fibonacci_strings as strings

from tqdm import trange
from stopwatch import stopwatch
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

CAP = 1e9
TRIALS = 1
MAX_I = 10000

df = pd.DataFrame()
clock = stopwatch()
universe = cpp.algorithms + python.algorithms + strings.algorithms
keys = [algo.__name__ + '_cpp' for algo in cpp.algorithms] + \
       [algo.__name__ + '_python' for algo in python.algorithms] + \
       [algo.__name__ + '_string' for algo in strings.algorithms]
skip_algo = [False] * len(universe)
for i in trange(MAX_I):
    record = pd.Series(name=i)
    f = [python.FibMatrix(i)]
    f.append(str(f[0]))
    for num, (algo, skip, key) in enumerate(zip(universe, skip_algo, keys)):
        if skip: continue
        try:
            clock.start()
            for _ in range(TRIALS):
                ans = algo(i)
                if clock.time() > CAP:
                    print(f'\nSkipping {key} at {i} due to time taken.')
                    skip_algo[num] = True
                    break
            time = clock.time() / TRIALS
            if ans not in f:
                print(f'\nSkipping {key} at {i} due to wrong answer.')
                skip_algo[num] = True
                continue
            record[key] = time
            
        except:
            print(f'\nSkipping {key} at {i} due to exception.')
            skip_algo[num] = True
    
    df = df.append(record)