"""

# -*- coding: utf-8 -*-
Created on          17 May 2019 at 5:58 PM
Author:             Arvind Sachidev Chilkoor  
Created using:      PyCharm
Name of Project:    To Breast Cancer using Machine Learning

Description:  
This project is an attempt to predict if a cell in the human breast is cancerous or not. The dataset has been borrowed
from University of California - Irvine - Machine Learning Repository.
The key decider attribute is CLASS, which has rating of 2 or 4, where 2 is Benign and 4 is Malignant
The program displays the results in Histograms and Scatter Matrices.
The script uses K-Nearest Neighbours (KNN) Algorithm by using Support Vector Machine (SVM) to make the predictions.
"""

import numpy as np
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn import model_selection
from sklearn.metrics import classification_report, accuracy_score
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd


# Loading the dataset from source --> UCI - University of California - Irvine - Machine Learning Repository
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data"

#Attribute Names Initialization based on the dataset
names = ['ID', 'Clump_Thickness', 'Uniform_Cell_Size', 'Uniform_Cell_Shape',
       'Marginal_Adhesion', 'Single_Epithelial_Size', 'Bare_Nuclei',
       'Bland_Chromatin', 'Normal_Nucleoli', 'Mitoses', 'Class']

# Dataframe initialization, panda read as csv, passing url and names as parameters
df = pd.read_csv(url,names=names)


# Preprocessing the data
# Replacing empty spaces with a -999999
df.replace('?',-999999, inplace = True)
print(df.axes)

# Dropping or removing the 'ID_Numb', as it will not help in machine learning analysis, since it is just a serial no.
df.drop(['ID'], 1, inplace = True)

# Print the shape of the dataset
print(df.shape)

# Dataset Visualizations
print(df.loc[0])
# prints additional factors for analysis
print(df.describe())

# Plotting Histograms for each attribute.
df.hist(figsize=(15,15), color = 'gray')

# gcf() - Get current figure
fig1 = plt.gcf()
# Display Figure
plt.show()
# Just to redraw the figure incase any changes to it has been made during display
plt.draw()
# Saving the image
fig1.savefig('Breast_Cancer_Detection_Histogram Plot.jpg', dpi=100)


# To display the attributes in scatter matrix
ax = pd.plotting.scatter_matrix(df, figsize= [20,20], color = 'green')

# A For loop is initiated here since plt.show() cannot work on all axis at once a iteration is used using ravel()

# y labels ha = horizontal axis, va = vertical axis
[plt.setp(item.yaxis.get_label(), rotation = 0, ha = 'right', va = 'baseline', fontsize = 7, rotation_mode = 'anchor') for item in ax.ravel()]
# x labels
[plt.setp(item.xaxis.get_label(), rotation = 18, ha = 'right', va = 'baseline', fontsize = 7, rotation_mode = 'anchor') for item in ax.ravel()]

# gcf() - Get current figure
fig2 = plt.gcf()
# Display Figure
plt.show()
# Just to redraw the figure incase any changes to it has been made during display
plt.draw()
# Saving the image
fig2.savefig('Breast_Cancer_Detection_Scatter_Matrix_Plot.jpg', dpi=100)


# To create X and Y datasets for training.

# In the X - Axis the "Class" column is dropped and shifted to Y - Axis
X = np.array(df.drop(['Class'],1))

# Y - Axis "Class" Column
Y = np.array(df['Class'])

X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.2)


# To specify the testing options
seed = 8
scoring = 'accuracy'


# Here we define the models to train
models = []

# Appending the K - Nearest Neighbours to models
models.append(('KNN', KNeighborsClassifier(n_neighbors = 5)))
# Appending C-Support Vector Classification
models.append(('SVM',SVC()))


# To evaluate each model in-turn
results = []
names = []

# Running them in For Loop:

for name, model in models:
       """
       Here we use the KFold cross-validator,
       Provides train/test indices to split data in train/test sets. Split dataset into k consecutive folds 
       (without shuffling by default). Each fold is then used once as a validation while the k - 1 remaining 
       folds form the training set.
       """
       kfold = model_selection.KFold(n_splits=10, random_state = seed)

       # Using cross_val_score to validate the results
       cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv= kfold, scoring = scoring)

       results.append(cv_results)
       names.append(name)
       msg = "%s: %f (%f)" %(name, cv_results.mean(), cv_results.std())
       print("\n")
       print("---------------------------------------------------\n")
       print(msg)

# To make predictions on a validation dataset

for name, model in models:
       # Training the model
       model.fit(X_train, Y_train)
       # Making the predictions based on the training set.
       predictions = model.predict(X_test)
       print("\n")
       print("---------------")
       print("***************")
       print(name)

       # Here accuracy_score predicts the subset accuracy for the predictions
       print(accuracy_score(Y_test,predictions))
       # Classification_report is display the classification metrics in text format
       print(classification_report(Y_test, predictions))
