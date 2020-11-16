import common as cm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.linear_model import Perceptron
# import xgboost as xgb


names = [
		"Perceptron",
		# "XGBreglinear",
		# "XGBreglogistic",
		"NearestNeighbors",
		# "LinearSVM",
		"DecisionTree",
		"RandomForest",
		"AdaBoost",
		#"NeuralNet",
		#"NaiveBayes", 
		#"LDA",
		#"QDA"
		]

classifiers = [
		Perceptron(),
		# xgb.XGBClassifier(objective='reg:linear'),
		# xgb.XGBClassifier(objective='reg:logistic'),
		KNeighborsClassifier(10),
		# SVC(kernel="linear"),
		DecisionTreeClassifier(max_depth=5),
		RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
		AdaBoostClassifier(),
		#MLPClassifier(verbose=False),
		#GaussianNB(),
		#LinearDiscriminantAnalysis(),
		#QuadraticDiscriminantAnalysis()
    ]



def getBestClassifiers(X,y,testPerc=0.4):
	global classifiers
	global names
	X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=testPerc, random_state=43)
	for name, clf in zip(names, classifiers):
		clf.fit(X_train, y_train)
		score = clf.score(X_test, y_test)
		print (name, round(score,2))