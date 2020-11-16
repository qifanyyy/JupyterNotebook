# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 13:15:19 2019

@author: Tazrin
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import accuracy_score

#5 Fold Cross Validation
def kfold(df):
    df['DailySummary'] = data['DailySummary']
    classLabel = data.DailySummary.unique()
    classList = []
    for i in classLabel:
        classList.append(df[data['DailySummary']==i])
 #splitting into 5 folds       
    for i in range(5):
          classList[i] = np.array_split(classList[i], 5)
    
    folds = []
    for i in range(5):
        folds.append(pd.DataFrame())
        for j in classList:
            folds[i] = folds[i].append(j[i], ignore_index=True, verify_integrity=True)
    accuracyFold = []
    #Random Forest is used for measuring performance
    clf = RandomForestClassifier(n_estimators = 50, random_state = 42, max_features = 'auto')  
      
    for i in range(5):
        X_train = pd.DataFrame()       
        Y_train = pd.DataFrame()       
        X_test = folds[i].iloc[:,:-1]
        Y_test = folds[i].iloc[:,-1]
        for j in range(5):
            if j !=i:
                X_train = X_train.append(folds[j].iloc[:,:-1], ignore_index=True, verify_integrity=True)
                #Y_train = Y_train.append(x = folds[j].iloc[:,-1])  #['DailySummary'] = ytr
                Y_train = pd.concat([Y_train, folds[j].iloc[:,-1]], ignore_index=True, verify_integrity=True)
        clf.fit(X_train, Y_train)
        y_pred = clf.predict(X_test)
        #accuracy = correctly predicted values/total predicted values
        accurate =0
        for a in range(len(y_pred)):
            if y_pred[a] == Y_test[a]:
                accurate = accurate+1
        accuracy = accurate/len(y_pred)
        accuracyFold.append(accuracy)
    return np.mean(accuracyFold)


data = pd.read_csv("data3.csv")
import warnings
warnings.filterwarnings("ignore")
allFeatures = data.iloc[:,:-1]
newFeatures = pd.DataFrame()
#y = data.iloc[:,-1 ]

#clf = RandomForestClassifier(n_estimators = 100, random_state = 42, max_features = 'auto')
modelAccuracy = 0
for iter in range(len(allFeatures.columns)):
    accuracyList = []
    for i in allFeatures.columns.values:
        if i not in newFeatures.columns:
            newFeatures[i] = allFeatures[i]
            #x = newFeatures.iloc[:,:]
            #X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
            #clf.fit(X_train, y_train)
            #y_pred = clf.predict(X_test)
            acc = kfold(newFeatures)	#returns average accuracy of k fold
            accuracyList.append([acc,i])
            newFeatures = newFeatures.iloc[:, :-2]
        
    maxAccIdx = np.argmax([i[0] for i in accuracyList])
    maxAccuracy = accuracyList[maxAccIdx][0]
    if maxAccuracy>modelAccuracy:
        newFeatures[accuracyList[maxAccIdx][1]] = allFeatures[accuracyList[maxAccIdx][1]]
        modelAccuracy = maxAccuracy
    else:
        break

    
print('Selected Features are: ', newFeatures.columns.values)
print('Accuracy = ', modelAccuracy)


