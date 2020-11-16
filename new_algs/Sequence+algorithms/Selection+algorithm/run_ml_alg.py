# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 15:37:04 2018

@author: Casey
"""

from sklearn import linear_model,svm
from sklearn.model_selection import cross_val_score

def getModelScores(mlAlgorithm,X,y,folds):
    if mlAlgorithm == 'lin_reg':
        myModel = linear_model.LinearRegression()#here call a function that specifies ml model
        return cross_val_score(myModel,X,y,scoring='neg_mean_squared_error',cv=folds)
    elif mlAlgorithm == 'svm':
        y = y.reshape(len(y),)#reshape so svm doesn't complain
        myModel = svm.SVC(gamma='auto',kernel='rbf', decision_function_shape='ovo')#use decision_function_shape arg when using multiclass
        return cross_val_score(myModel, X, y, cv=5)#change cv later
    else:
        print('no match for ML algorithm')
        return 0
    
