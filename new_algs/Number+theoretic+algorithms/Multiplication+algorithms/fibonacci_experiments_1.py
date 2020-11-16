# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 14:55:57 2019

@author: DSU
"""

"""
Increases n by one each time
Shows how this changes the function time
"""
import sys
sys.path.append("..")

from tqdm import trange
from stopwatch import stopwatch
from scipy.optimize import curve_fit
import fibonacci.fibonacci_strings as fibonacci
import pandas as pd
import matplotlib.pyplot as plt

MAX_INT = 1000

# timing and data
clock = stopwatch()
df = pd.DataFrame()

# run experiment
for i in trange(MAX_INT):
    # the row
    record = dict()
    
    # calculate for each algorithm
    for algo in fibonacci.algorithms:
        clock.start()
        algo(i)
        record[algo.__name__] = clock.time()
    
    # add to dataframe
    df = df.append(pd.Series(record, name=i))

# curve fitting functions
def exp_fit(x, a, b, c):
    return x ** a + x * b + c

# linear curve fit function
def lin_fit(x, a, b):
    return x * a + b

# exponential functions
for algo in fibonacci.algorithms[:2]:
    args = curve_fit(exp_fit, df.index, df[algo.__name__])
    df[algo.__name__+'_predict'] = df.index.map(lambda x: exp_fit(x, *args[0]))

# linear functions
for algo in fibonacci.algorithms[2:]:
    args = curve_fit(exp_fit, df.index, df[algo.__name__])
    df[algo.__name__+'_predict'] = df.index.map(lambda x: exp_fit(x, *args[0]))

# print graph of each
df.plot()
plt.show()

# calculate ratios
for col in df:
    df[col+'_change'] = df[col].pct_change().add(1)

# print table
print(df)
