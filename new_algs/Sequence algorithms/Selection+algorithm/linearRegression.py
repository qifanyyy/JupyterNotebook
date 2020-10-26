import numpy as np 
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

def learnAndPrintResults(dataSet):
    (m, n) = data.shape
    X = dataSet.data
    y = dataSet.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    ypred = linreg.predict(X_test)

    absoluteErr = metrics.mean_absolute_error(y_test, ypred)
    #squaredErr = metrics.mean_square_error(y_test, ypred)
    #rootErr = np.sqrt(squaredErr)
    print(absoluteErr
