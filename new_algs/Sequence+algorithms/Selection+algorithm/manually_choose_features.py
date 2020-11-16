# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 10:20:11 2018

@author: Casey

This file just runs whichever features you specify. "Domain expertise"
"""

from process_data import chooseFeatures
from run_ml_alg import getModelScores
from sklearn import linear_model
from sklearn.model_selection import cross_val_score

def enterFeatureIndeces(XFeatures,yFeature,XFile,yFile,mlAlg):
    
    allX,allY,features = chooseFeatures(XFeatures,XFile,yFile)
    scores = getModelScores(mlAlg,allX,allY,10)
    #myModel = linear_model.LinearRegression()
    #scores = cross_val_score(myModel,allX,allY,scoring='neg_mean_squared_error', cv=10)
    print(scores.mean())#take the mean score of all cross val runs
    print(features)