#!/usr/bin/env python
# -*- coding: utf-8 -*-
##  utf-8 for non-ASCII chars

# Machine Learning 445
# HW 2: Neural Networks
# Katie Abrahams, abrahake@pdx.edu
# 1/28/16

import numpy as np
from input import letters_list_training, letters_list_testing
# preprocessing to scale training data
from sklearn import preprocessing

# Neural network to recognize letters
# after training with the UCI machine learning repository.
# Network has 16 inputs (mapping to the 16 attributes of the letters in the data set)
# one layer of hidden units, and 26 output units (for 26 classes of letters)
#### Structures defined here used in experiment 4 for low or high number of hidden units ####

#################
# hyperparameters
#################

################
# Experiment 4 #
################
# Test how changing the number of hidden units changes results
# learning rate
eta = 0.3
# momentum
alpha = 0.3
# smaller number of hidden units
n_low = 2
# larger number of hidden units
n_high = 8

###############
# function defs
###############
# sigmoid activation function for neurons
# The derivative of the sigmoid activation function is easily expressed in terms of the function itself:
# d sigma(z)/dz = sigma(z)x(1 - sigma(z))
# This is useful in deriving the back-propagation algorithm
# If derivative argument is true, return the derivative of the sigmoid
# Derivative is not needed for this assignment, we use equations from the slides instead
def sigmoid(z, derivative):
    if derivative:
        return sigmoid(z) * (1-sigmoid(z))
    else: # derivative is False
        return 1 / (1+np.exp(-z))

#################
# data structures
#################

######################################################################################################

#### Training data as a 10000x17 matrix seeded with letter attributes ####
# Rows in data matrices correspond to number of items in minibatch
# columns correspond to values of these items (values of xi for all items X in training data)
# numpy stores data in row major order
X_attributes = np.full( (len(letters_list_training),16), [ltr.attributes for ltr in letters_list_training] )

#### save targets in the order entered into the matrix ####
X_targets = np.array([list(ltr.value) for ltr in letters_list_training])

#### preprocessing input using sklearn package, returns array ####
# scaled to be Gaussian with zero mean and unit variance along each column (feature)
X_scaled = preprocessing.scale(X_attributes)

#### Concatenate scaled data with the 1s needed for bias inputs ####
# put bias input at the end so we don't need to worry about indexing [1:25]
# when going from hidden -> output layer
bias_input = np.full((len(letters_list_training), 1), 1.0)
X = np.concatenate((X_scaled, bias_input), axis=1)
# The preprocessing module provides a utility class StandardScaler
# that implements the Transformer API to compute the mean and standard deviation
# on a training set so you can reapply the same transformation on the testing set
# see scikit-learn.org/stable/modules/preprocessing.html

######################################################################################################

#### Testing data as a 10000x17 matrix seeded with letter attributes ####
# Rows in data matrices correspond to number of items in minibatch
# columns correspond to values of these items (values of xi for all items X in testing data)
X_test_attributes = np.full( (len(letters_list_testing),16), [ltr.attributes for ltr in letters_list_testing] )

#### save targets in the order entered into the matrix ####
X_test_targets = np.array([list(ltr.value) for ltr in letters_list_testing])

#### preprocessing input using sklearn package, returns array ####
# scaled to be Gaussian with zero mean and unit variance along each column (feature)
# Scale the test data using the μi and σi values
# computed from the training data (X_attributes), not the test data.
scaler = preprocessing.StandardScaler().fit(X_attributes)
X_test_scaled = scaler.transform(X_test_attributes)

#### Concatenate scaled data with the 1s needed for bias inputs ####
# put bias input at the end so we don't need to worry about indexing [1:25]
# when going from hidden -> output layer
test_bias_input = np.full((len(letters_list_testing), 1), 1.0)
X_test = np.concatenate((X_test_scaled, test_bias_input), axis=1)

######################################################################################################

#### Weight matrix input -> hidden layer ####
# Weight matrices have the same number of columns as units in the previous layer
# and the same number of rows as units in the next layer
# n is the number of hidden units
input_to_hidden_weights_n_low = np.random.uniform(low= -.25, high= .25, size=(n_low, 17))
input_to_hidden_weights_n_high = np.random.uniform(low= -.25, high= .25, size=(n_high, 17))

#### Weights from hidden layer to output layer ####
# 5 columns to allow for bias input (one column of 1s)
hidden_to_output_weights_n_low = np.random.uniform(low= -.25, high= .25, size=(26,n_low+1) )
hidden_to_output_weights_n_high = np.random.uniform(low= -.25, high= .25, size=(26,n_high+1) )

######################################################################################################

#### Output layer matrix, 1 row by 26 columns for 26 letters of the alphabet ####
# only 1 row, only need one output (activations) for output layer
# don't initialize to anything
Y = np.full((1, 26), None)

