# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 17:13:39 2019

@author: DSU
"""

import sys
sys.path.append("..")

from tqdm import trange
from stopwatch import stopwatch
from random import randrange
import bigint.bigint as bigint
import pandas as pd
import matplotlib.pyplot as plt

# helper variables
TRIALS = 1000
MAX_MAG = 8

# timing and data
clock = stopwatch()
df = pd.DataFrame()

# experiments
for i in trange(MAX_MAG):
    # lower bound for variables
    i = 2**i
    
    # create lists of factors to use
    factors = [tuple(str(randrange(10**(i-1), 10**i)) for _ in range(2))\
               for _ in range(TRIALS)]
    
    # multiplication trials
    clock.start()
    for a, b in factors:
        bigint.MyBigIntegers(a) * bigint.MyBigIntegers(b)
    time_mul = clock.time() / TRIALS
    
    # addition trials
    clock.start()
    for a, b in factors:
        bigint.MyBigIntegers(a) + bigint.MyBigIntegers(b)
    time_add = clock.time() / TRIALS
    
    # add data to dataframe
    df = df.append(pd.Series({'mul':time_mul, 'add':time_add}, name=i))


# plot each times 
# takes first 300 to prevent convert to float error
df['add'].plot()
plt.show()
df['mul'].plot()
plt.show()

# add ratios
df['add_ratio'] = df['add'].pct_change().add(1)
df['mul_ratio'] = df['add'].pct_change().add(1)

# show table
print(df)