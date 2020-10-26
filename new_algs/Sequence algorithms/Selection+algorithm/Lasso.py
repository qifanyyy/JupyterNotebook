# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 13:53:00 2019

@author: Asucan
"""

from sklearn.linear_model import Lasso
from sklearn import preprocessing
import numpy as np
import pandas as pd
class lasso:
    def __init__(self,x,y,feature_num,swim=2,iteration=100):
        self.feature_num = feature_num
        self.x = x
        self.y = y
        self.swim = swim
        self.iteration = iteration
        self.count = 0
    
    def run(self):
        min_max_scaler = preprocessing.MinMaxScaler()
        features = min_max_scaler.fit_transform(self.x)
        #features = np.asarray(features.values)
        #labels = np.transpose(np.asarray(self.y.values.ravel() - 1, dtype=int))
        labels = self.y
        low,now,high = 0,1,1
        indexes = None
        while (indexes==None or len(indexes[0]) > self.feature_num) and (self.count<self.iteration):
            self.count += 1
            lasso = Lasso(alpha=now)
            lasso.fit(features, labels)
            indexes = np.asarray(np.where(lasso.coef_ != 0))
            if  len(indexes[0])>=self.feature_num-self.swim and len(indexes[0])<=self.feature_num+self.swim:
                return indexes[0]
            elif len(indexes[0]) > self.feature_num:
                low = now
                now = hight
                high = high*2
                #print(low,now,high)
            else:
                break
        #print('berak')
        while (not(len(indexes[0])>=self.feature_num-self.swim and len(indexes[0])<=self.feature_num+self.swim)) and (self.count<self.iteration):
            self.count += 1
            if len(indexes[0])<=self.feature_num-self.swim:
                high = now
                now = (high+low)/2
            else:
                low = now
                now = high+low/2
            #print(low,now,high)
            lasso = Lasso(alpha=now)
            lasso.fit(features, labels)
            indexes = np.asarray(np.where(lasso.coef_ != 0))
            #print(len(indexes[0]))
        return indexes[0]

#example：
#from sklearn.datasets import make_friedman1
#x, y = make_friedman1(n_samples=50, n_features=1000, random_state=0)
#print(x.shape)
#slector = lasso(x,y,10)
#slector.run()
