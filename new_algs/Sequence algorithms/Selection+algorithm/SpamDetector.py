import numpy as np
import tensorflow as tf

from sklearn.metrics import matthews_corrcoef
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

from neuron import *

import csv

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


class spam_detector():


	

	def load_spam_data():
		
		classes = ["spam", "ham"]

		# Data File
		file = "spam.csv"

		# Lists to store all word frequencies from messages
		# used to find top words for each class
		content_spam = {}
		content_ham = {}

		# Lists for each message and corresponding label
		messages = []
		y = []

		amount_spam = 0
		amount_ham = 0

		# open the file for processing as a CSV
		with open(file, 'r') as f:
			reader = csv.reader(f)

			for i, row in enumerate(reader):
				if i == 0:
					continue

				# split the string and remove all non alpha characters (or ')
				words = [''.join(c for c in word if c.isalpha() or c == "'") for word in row[1].lower().split()]

				if row[0] == "spam":
					amount_spam+=1
				else:
					amount_ham+=1
	            
				# Add and count words for spam and ham classes
				content = content_spam if row[0] == "spam" else content_ham
				for w in words:
					if len(w) > 3:
						if w in content:
							content[w] += 1
						else:
							content[w] = 1

				# Append full messages
				messages.append(" ".join(words))
				y.append(classes.index(row[0]))

		# sort each each word based on value count
		sorted_X_spam = sorted(content_spam, key=content_spam.get, reverse=True)
		sorted_X_ham = sorted(content_ham, key=content_ham.get, reverse=True)
		# populate the bag-of-words with top 50 words from each class (and remove duplicates)
		bow = []
		for i in range(80):
			if sorted_X_spam[i] not in bow:
				bow.append(sorted_X_spam[i])
			if sorted_X_ham[i] not in bow:
				bow.append(sorted_X_ham[i])


		return bow, messages, np.array(y)

	# Init the class
	def __init__(self, features_selected):

		# check only features_selected has values of 0s and 1s
		if ~((features_selected == 0) | (features_selected == 1)).all():
			logger.error("There are values others than 0 or 1")
			raise ValueError("features_selected must contain only 0 or 1")

		# check features_selected has len of 141
		if len(features_selected) is not 141:
			logger.error("The input is not a vector size 141")
			raise ValueError("features_selected must be an array of 141 values")

		# At least one of the values in features_selected must be 1
		if ((features_selected == 0)).all():
			logger.error("There must be at least one feature selected with 1")
			raise ValueError("At least one of the values in features_selected must be 1")

		# the input is the features to be selcted
		self.features_selected = features_selected

		logger.debug("	")
		bow, messages, self.y = spam_detector.load_spam_data()

		#Get the vector X 
		self.X = CountVectorizer(vocabulary=bow).fit_transform(messages)

		# eliminate the columns with values 0 of the instances
		self.X = np.delete(self.X.A, np.where(self.features_selected == 0), axis=1)
		logger.debug("Eliminating the columns not selected by features_selected")

		#y is a vector, it has to be a matrix, this loop creates a matrix size y.shape[0]x2
		y2 = np.zeros((self.y.shape[0], 2))
		for i in range(self.y.shape[0]):
			y2[i, 0] = self.y[i]
			if self.y[i] == 0:
				y2[i, 1] = 1
			else:
				y2[i, 1] = 0
		self.y = y2

		


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
		learning_rate = 0.01
		batch_size = 16 #the classifier will take blocks of 128 to run the classifier
		display_step = 5
		num_steps = int(self.X_train.shape[0]/batch_size) # 58 = ceil(7406/128) = ceil(57.85)


		# Network Parameters
		n_hidden_1 = 32 # 1st layer number of neurons
		n_hidden_2 = 32 # 2nd layer number of neurons
		num_input = self.X.shape[1] # number of features
		num_classes = self.y.shape[1] # total amount of classes

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


# input_ = np.ones(141)
# test = spam_detector(input_)
# test.test_features_neural_network()
# test.test_features_svm()