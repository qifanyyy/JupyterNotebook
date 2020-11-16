import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression


def checkDistribution(data):
    group0 = data['diagnosis'][data['diagnosis'] == 'M'].count()
    group1 = data['diagnosis'][data['diagnosis'] == 'B'].count()

    target = pd.Series(data = [group0,group1], index=['malignant','benign'])

    return target

def splitData(data):
    y = data['diagnosis']
    features = list(data.columns.values)
    features.remove('diagnosis')
    x = data[features]

    return x,y

def trainTestSplit(data):
    x,y = splitData(data)

    X_train,X_test,y_train,y_test = train_test_split(x,y,random_state=0)

    return X_train,X_test,y_train,y_test

def KNNeighbors(data):
    X_train, X_test, y_train, y_test = trainTestSplit(data)

    Knn = KNeighborsClassifier(n_neighbors= 5)
    Knn.fit(X_train,y_train)
    result = Knn.score(X_test,y_test)

    return result

def LogesticRegression(data):
    X_train, X_test, y_train, y_test = trainTestSplit(data)
    LR = LogisticRegression()
    LR.fit(X_train,y_train)
    result = LR.score(X_test,y_test)

    return result
