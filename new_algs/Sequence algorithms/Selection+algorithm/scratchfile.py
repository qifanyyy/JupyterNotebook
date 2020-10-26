# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 14:29:17 2018

@author: Casey
file for testing code
"""


import pandas as pd
import numpy as np
from process_data import *
from sklearn import svm,linear_model
from sklearn.model_selection import cross_val_score
'''
def readFile(_inputColNums, _outputColNums, relativeFilename):
    inputData = pd.read_csv(relativeFilename,
                            sep=',',
                            usecols=_inputColNums,
                            header=0)
    outputData = pd.read_csv(relativeFilename,
                             sep=',',
                             usecols=_outputColNums,
                             header=0)

    tempAllX = np.array(inputData, dtype="float")
    
    #minmax scaling
    for index in range(tempAllX.shape[1]):
        avgOfX = np.average(tempAllX[:, index])

        tempAllX[:, index] = (tempAllX[:, index] - avgOfX)/(np.max(tempAllX[:, index] - np.min(tempAllX[:, index])))
 
    #only use a subset for speed reasons
    return tempAllX, np.array(outputData, dtype="float"), inputData.head(0).columns.values
   # return tempAllX[:100], np.array(outputData, dtype="float")[:100], inputData.head(0).columns.values

'''
def main():
   ''' 
    X,y,features=readAllFeatures('./datasets/kc_house_data/kc_house_data_X.csv','./datasets/kc_house_data/kc_house_data_y_regression.csv')
    print(features)
    '''
    '''
    myModel = linear_model.LinearRegression()
    scores = cross_val_score(myModel,X,y,scoring='neg_mean_squared_error', cv=10)
    print(scores.mean())#take the mean score of all cross val runs
    print(features)'''
    '''#svm run
    filename = "./datasets/kc_house_data/kc_house_data.csv"
    X, y, features = readFile([8,11,12,13,14,17],[2],filename)

    y = pd.read_csv('./datasets/kc_house_data/kc_house_data_y_classification_3_class.csv',
                    sep=',',
                    usecols=[0],
                    header=0)
    
    
    y = np.array(y)
    y = y.reshape(len(y),)#reshape so svm doesn't complain
   
    clf = svm.SVC(gamma='auto',kernel='rbf', decision_function_shape='ovo')#use decision_function_shape arg when using multiclass
   # clf.fit(X,y)
    
    # print(clf.predict([[1,1,1,1]]))
   # row = 1149#min7252#max
    #row = 7252
    #row = 156
    scores = cross_val_score(clf, X, y, cv=5)
    print(scores)
    print(scores.mean())
   # print(clf.predict([[X[row][0],X[row][1],X[row][2],X[row][3],X[row][4],X[row][5]]])) 
   
    print(features)
    
    
    '''
    
'''
    
    classList = []
    
    for i in range(len(y)):
        if y[i] <0:
            print('breaking')
            break
        elif y[i] < 500000:
            classList.append('average')
        #elif y[i] < 800000:
         #   classList.append('pricey')
        else:
            classList.append('expensive')
        
    print(classList[0])
    dataDict = {'price_class': classList}
    
    df = pd.DataFrame(data=dataDict)
    df.to_csv('./datasets/kc_house_data/kc_house_data_y_classification_2_class.csv',encoding='utf-8',index=False)
    
    '''
    
main()