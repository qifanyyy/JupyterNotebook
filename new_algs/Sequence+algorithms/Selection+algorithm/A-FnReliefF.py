#https://medium.com/@yashdagli98/feature-selection-using-relief-algorithms-with-python-example-3c2006e18f83

from ReliefF import ReliefF
import numpy as np
from sklearn import datasets
import pandas as pd


#example of multi class problem
iris = datasets.load_iris()

X = iris.data
Y = iris.target

fs = ReliefF(n_neighbors=20, n_features_to_keep=2)
X_train = fs.fit_transform(X, Y)
print("(No. of tuples, No. of Columns before ReliefF) : "+str(iris.data.shape))
print("(No. of tuples, No. of Columns after ReliefF) : "+str(X_train.shape))

print("\nDataFrame\n")
print(pd.DataFrame.from_records(X_train))