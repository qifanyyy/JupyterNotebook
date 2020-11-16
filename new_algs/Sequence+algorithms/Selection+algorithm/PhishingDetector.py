import numpy as np
import tensorflow as tf

import arff

from sklearn.metrics import matthews_corrcoef
from sklearn.model_selection import train_test_split
from sklearn import svm

from neuron import *

#this is the same util2 used for the first assigment
from util2 import Arff2Skl

import logging

import sys

# Set the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)


class phishing_detector():

	# Init the class
	def __init__(self, features_selected):
		

		# check only features_selected has values of 0s and 1s
		if ~((features_selected == 0) | (features_selected == 1)).all():
			logger.error("There are values others than 0 or 1")
			raise ValueError("features_selected must contain only 0 or 1")

		# check features_selected has len of 30
		if len(features_selected) is not 30:
			logger.error("The input is not a vector size 30")
			raise ValueError("features_selected must be an array of 30 values")

		# At least one of the values in features_selected must be 1
		if ((features_selected == 0)).all():
			logger.error("There must be at least one feature selected with 1")
			raise ValueError("At least one of the values in features_selected must be 1")

		# the input is the features to be selcted
		self.features_selected = features_selected


		# get the data from the data set
		dataset = arff.load(open('phishing.arff', 'r'))
		data = np.array(dataset['data'])

		#parse the phishing.arff dataset
		cvt = Arff2Skl("phishing.arff")
		logger.debug("Data set read")


		# eliminate the columns with values 0 of the instances
		self.X = np.delete(data[:,:-1], np.where(self.features_selected == 0), axis=1)
		logger.debug("Eliminating the columns not selected by features_selected")

		
		_, self.y = cvt.transform()

		# get the training and testing dataset
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.33, random_state=33)
		logger.debug("Getting training and testing data")

		#modifythe type from np.float64 (default type) to np.float32
		self.X_train = self.X_train.astype(np.float32)
		self.y_train = self.y_train.astype(np.int32)
		self.X_test = self.X_test.astype(np.float32)
		self.y_test = self.y_test.astype(np.int32)




	# test the classifier with neural network, the function will return the MCC value
	def test_features_neural_network(self):
		
		# Parameters for the classifier
		learning_rate = 0.001
		batch_size = 128 #the classifier will take blocks of 128 to run the classifier
		display_step = 5
		num_steps = int(self.X_train.shape[0]/batch_size) # 58 = ceil(7406/128) = ceil(57.85)


		# Network Parameters
		n_hidden_1 = 256 # 1st layer number of neurons
		n_hidden_2 = 256 # 2nd layer number of neurons
		num_input = self.X.shape[1] # number of features
		num_classes = 2 # total amount of classes

		logger.debug("init the NeuronNetworkTwoHiddenLayer class")
		clf = NeuronNetworkTwoHiddenLayer(learning_rate = learning_rate, batch_size = batch_size,\
						 n_hidden_1 = n_hidden_1, n_hidden_2 = n_hidden_2, num_input = num_input, num_classes = num_classes)


		# train the classifier
		logger.debug("train the classifier")
		clf.train(self.X_train, self.y_train)

		# test the classifier
		logger.debug("test the classifier")
		y_out = clf.predict(self.X_test)

		# clear the classifier
		logger.debug("clear some values")
		clf.clear()

		# get the Matthews correlation coefficient of the classifier is 
		mcc = matthews_corrcoef(self.y_test[:,0], y_out.round()[:,0])
		logger.debug("get the Matthews correlation coefficient of the Neural Network classifier is "+ str(mcc))


		return mcc


	# test the classifier using SVM, the function return the MCC value
	def test_features_svm(self):
		
		# The SVM using SKLearn can only works with vector for the class labels, not in matrix like TensorFlow
		y_train_svm = self.y_train[:,0]
		y_test_svm = self.y_test[:,0]

		logger.debug("init the classifier")
		clf = svm.SVC()

		logger.debug("training the classifier")
		clf.fit(self.X_train, y_train_svm) 

		logger.debug("test the classifier")
		y_out = clf.predict(self.X_test)

		# get the Matthews correlation coefficient of the classifier is 
		mcc = matthews_corrcoef(y_test_svm, y_out)
		logger.debug("get the Matthews correlation coefficient of the SVM classifier is "+ str(mcc))

		return mcc
