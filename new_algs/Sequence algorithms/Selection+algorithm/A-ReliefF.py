#https://medium.com/@yashdagli98/feature-selection-using-relief-algorithms-with-python-example-3c2006e18f83

from ReliefF import ReliefF
import numpy as np
from sklearn import datasets
import pandas as pd

#example of 2 class problem
data = np.array([[9,2,2],
                 [5,1,0],
                 [9,3,2],
                 [8,3,1],
                 [6,0,0]]
                 )
target = np.array([0,
                   0,
                   1,
                   1,
                   1])

fs = ReliefF(n_neighbors=1, n_features_to_keep=2)
X_train = fs.fit_transform(data, target)
print(X_train)
print("--------------")
print("(No. of tuples, No. of Columns before ReliefF) : "+str(data.shape)+
      "\n(No. of tuples , No. of Columns after ReliefF) : "+str(X_train.shape))


#example of multi class problem
iris = datasets.load_iris()
#print(iris)

X = iris.data
Y = iris.target

fs = ReliefF(n_neighbors=20, n_features_to_keep=2)
X_train = fs.fit_transform(X, Y)
print("(No. of tuples, No. of Columns before ReliefF) : "+str(iris.data.shape)+
      "\n(No. of tuples, No. of Columns after ReliefF) : "+str(X_train.shape))
