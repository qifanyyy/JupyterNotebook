# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 18:17:38 2019

@author: Pranit
"""

# k-Nearest Neighbours
# Dataset: glass
# Use knn on short datasets for quicker processing

# import the libraries
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection  import train_test_split
from sklearn import neighbors
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from pandas_ml import ConfusionMatrix
import matplotlib.pyplot as plt

# should be 0.17 or higher. else reinstall with the latest version
# import sklearn
# print(sklearn.__version__)

# read the input file
# ------------------>
path="D:\\Imarticus\\Python\\K-NN & SVM\\glass.csv"
glass = pd.read_csv(path)
glass.head()

# number of rows
# ------------------>
len(glass)

# describe
# ------------------>
glass.describe()

# print the columns
# ------------------>
col = list(glass.columns)
print(col)

# count of Rows and Columns
# ------------------>
glass.shape

# describe the dataset (R,C)
# ------------------------->
glass.dtypes

# drop unwanted columns
# ---------------------->
glass = glass.drop(['id_number'],axis=1)
glass.head(5)

# print the columns
# ------------------>
col = list(glass.columns)
print(col)

# to determine the type of bd. (y = "Type")
# ---------------------------------------->
print(glass['Type'].unique())

# check for NULLS, blanks and zeroes
# --------------------------------->
# fix missing values
# ------------------>

# randomly shuffle the dataset. frac=1 means returns all rows after sorting
glass = glass.sample(frac=1)
glass.head(25)

# standardize the dataset
# ------------------>
glass_scaled = glass.copy(deep=True)
minmax = preprocessing.MinMaxScaler()

scaledvals = minmax.fit_transform(glass_scaled.iloc[:,0:9])
glass_scaled.loc[:,0:9] = scaledvals

glass_scaled.head(10)
glass.head(10)

# split the scaled dataset into X and Y variables. 
# These are numpy array
# --------------------------------------------------------------------->
cols=len(glass_scaled.columns)
X=glass_scaled.values[:,0:cols-1]
Y=glass_scaled.values[:,cols-1]

# split the dataset into train and test
# --------------------------------------

# split the scaled dataset into train and test
# -------------------------------------------->
x_train, x_test, y_train, y_test = train_test_split( X, Y, test_size = 0.3, random_state = 100)

x_train.shape
x_test.shape
y_train.shape
y_test.shape

# cross-validation to select optimum neighbours and folds
# -------------------------------------------------------

# creating a list of nearest neighbours
# -------------------------------------
# nn=list(range(3,50,2))
nn=list(range(3,11,1))
print(nn)
len(nn)

# empty list that will hold cv scores
cv_scores = []

# perform n-fold cross validation
# ---------------------------------
for k in nn:
    knn = neighbors.KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, x_train, y_train, cv=5, scoring='accuracy')
    scores=np.around(scores.astype(np.double),4)
    
    cv_scores.append(scores.mean())
print(cv_scores)


# determining best k
optimal_k = nn[cv_scores.index(max(cv_scores))]
print("The optimal number of neighbors is %d" % optimal_k)

# in case of even neighbours, convert it to odd
# ----------------------------------------------
if (optimal_k%2 == 0):
    print("even number of neighbours {0}".format(optimal_k))
    optimal_k = optimal_k+1
else:
    print("odd number of neighbours {0}".format(optimal_k))

'''
# plot misclassification error vs neighbours
plt.plot(nn, MSE)
plt.xlabel('Number of Neighbors K')
plt.ylabel('Misclassification Error')
plt.show()
'''

# plot right_classifications vs neighbours
plt.plot(nn,cv_scores)
plt.xlabel('Number of Neighbors K')
plt.ylabel('Accurate Classifications')
plt.show()

# knn algorithm call
# ------------------>
clf = neighbors.KNeighborsClassifier(n_neighbors=optimal_k)
fit1 = clf.fit(x_train, y_train)
print(fit1)

# predict
# ------------------>
y_pred = fit1.predict(x_test)

# prediction report
# ----------------->
print(metrics.classification_report(y_test, y_pred))

y_train==5

##### interpretation of results
# recall
# -------
# measure of model completeness
# numbers indicate % of results are relevant
# avg/total : indicate % of results that are relevant overall

# high precision + low recall --> few results

# for i in range(50):
#    print("Actual value = {}, Predicted value = {}".format(y_test[i], y_pred[i]))

# print the accuracy
# -----------------
print("Test Accuracy  :: ", accuracy_score(y_test, y_pred))

len(y_test[y_test==1])
len(y_pred[y_pred==1])

# confusion matrix
# -------------------------------------
cm=ConfusionMatrix(y_test,y_pred)
# -------------------------------------
print(cm)
cm.plot()
cm.print_stats()

for i in range(8):
    print('class = {0}, length = {1}'.format(i, len(y_test[y_test==i])))



###############################################################
    
# without standardization
    
    

# split the scaled dataset into X and Y variables. 
# These are numpy array
# --------------------------------------------------------------------->
cols=len(glass.columns)
X=glass.values[:,0:cols-1]
Y=glass.values[:,cols-1]

# split the dataset into train and test
# --------------------------------------

# split the scaled dataset into train and test
# -------------------------------------------->
x_train, x_test, y_train, y_test = train_test_split( X, Y, test_size = 0.3, random_state = 100)

x_train.shape
x_test.shape
y_train.shape
y_test.shape

# cross-validation to select optimum neighbours and folds
# -------------------------------------------------------

# creating a list of nearest neighbours
# -------------------------------------
# nn=list(range(3,50,2))
nn=list(range(3,11,1))
print(nn)
len(nn)

# empty list that will hold cv scores
cv_scores = []

# perform n-fold cross validation
# ---------------------------------
for k in nn:
    knn = neighbors.KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, x_train, y_train, cv=5, scoring='accuracy')
    scores=np.around(scores.astype(np.double),4)
    
    cv_scores.append(scores.mean())
print(cv_scores)


# determining best k
optimal_k = nn[cv_scores.index(max(cv_scores))]
print("The optimal number of neighbors is %d" % optimal_k)

# in case of even neighbours, convert it to odd
# ----------------------------------------------
if (optimal_k%2 == 0):
    print("even number of neighbours {0}".format(optimal_k))
    optimal_k = optimal_k+1
else:
    print("odd number of neighbours {0}".format(optimal_k))

'''
# plot misclassification error vs neighbours
plt.plot(nn, MSE)
plt.xlabel('Number of Neighbors K')
plt.ylabel('Misclassification Error')
plt.show()
'''

# plot right_classifications vs neighbours
plt.plot(nn,cv_scores)
plt.xlabel('Number of Neighbors K')
plt.ylabel('Accurate Classifications')
plt.show()

# knn algorithm call
# ------------------>
clf = neighbors.KNeighborsClassifier(n_neighbors=optimal_k)
fit1 = clf.fit(x_train, y_train)
print(fit1)

# predict
# ------------------>
y_pred = fit1.predict(x_test)

# prediction report
# ----------------->
print(metrics.classification_report(y_test, y_pred))

y_train==5

##### interpretation of results
# recall
# -------
# measure of model completeness
# numbers indicate % of results are relevant
# avg/total : indicate % of results that are relevant overall

# high precision + low recall --> few results

# for i in range(50):
#    print("Actual value = {}, Predicted value = {}".format(y_test[i], y_pred[i]))

# print the accuracy
# -----------------
print("Test Accuracy  :: ", accuracy_score(y_test, y_pred))

len(y_test[y_test==1])
len(y_pred[y_pred==1])

# confusion matrix
# -------------------------------------
cm=ConfusionMatrix(y_test,y_pred)
# -------------------------------------
print(cm)
cm.plot()
cm.print_stats()

for i in range(8):
    print('class = {0}, length = {1}'.format(i, len(y_test[y_test==i])))
    