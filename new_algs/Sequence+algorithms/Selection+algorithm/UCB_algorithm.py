# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 17:40:56 2019

@author: DARA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as alt

datasat = pd.read_csv('Ads_CTR_Optimisation.csv') 

 
#Implementing UCB
import math
N= 10000
d = 10
ads_selected=[0]
numbers_of_selections =[0]* d
sums_of_rewards = [0]* d
for n in range(0,N):
    ad = 0
    max_upper_bound = 0
    for i in range (0,d):
        if(numbers_of_selections[i]>0):
            average_reward = sums_of_rewards[i]/ numbers_of_selections[i]
            delta_i = math.sqrt(3/2 * math.log(n+1)/ numbers_of_selections[i])
            upper_bound = average_reward + delta_i
        else:
            upper_bound = 1e400
            
        if upper_bound > max_upper_bound:
            max_upper_bound = upper_bound
            ad = i
            
    ads_selected.append(ad)
    numbers_of_selections[ad] = numbers_of_selections[ad]+1
    reward = datasat.values[n,ad]
    sums_of_rewards[ad]= sums_of_rewards[ad] + reward
    
      
            
                
            
            
        