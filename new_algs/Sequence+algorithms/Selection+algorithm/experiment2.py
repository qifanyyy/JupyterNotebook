#!/usr/bin/env python
# -*- coding: utf-8 -*-
##  utf-8 for non-ASCII chars

# Machine Learning 445
# HW 2: Neural Networks
# Katie Abrahams, abrahake@pdx.edu
# 1/28/16


from __future__ import division # want float and not int division
# import data structures, variables, and neural net from neural_net
# data structures in the global scope
from neural_net_ga import *
import string
import matplotlib.pyplot as plt


###############
# function defs
###############
def forward_propagation(row):
    """
    Function called in train()
    Forward propagate the input through the neural network
    during neural network training
    Does not include error computation
    :param row of data matrix:
    :return output of neural net:
    """

    # transpose row vector for matrix multiplication
    X_row = np.mat(row)
    X_col = X_row.transpose()

    # forward propagation
    # initial run of data, use sigmoid activation function
    # pass in dot products of inputs and weights
    hidden_layer = sigmoid(np.dot(input_to_hidden_weights, X_col), False)

    # hidden_layer is the activation at the hidden layer
    # use activations as input for the output layer

    # use hidden layer activations to get activations for output layer
    # append one row of 1s to hidden layer to allow for bias input
    bias_input_hidden_layer = np.full((1, 1), 1.0)
    hidden_layer_concat = np.concatenate((hidden_layer, bias_input_hidden_layer), axis=0)

    # matrix multiply (hidden layer) dot (weights from hidden -> output)
    output_layer = np.dot(hidden_to_output_weights, hidden_layer_concat)

    # apply sigmoid function to output layer
    # to get activations at output layer
    Y = sigmoid(output_layer, False)

    # return activations from hidden and output layers
    return hidden_layer, Y

################################################################################################

def back_propagation(hidden_activations, output_activations, target, row, eta):
    """
    Function called in train()
    The the back-propagation algorithm is used
    during training to update all weights in the network.
    Pass in activation of output layer and
    target letter corresponding to the row that is currently being passed through the neural net
    :param hidden_activations, output_activations, target, row of input:
    :return error:
    """

    #### 2. Calculate the error terms ####
    #### calculate error delta_k for each output unit ####
    #   For each output unit k, calculate error term δk :
    #   δk ← ok(1 − ok)(tk − ok)
    #
    # o_k is output: 26 outputs
    # t_k is target: per training instance: if input is A,
    # then output for for matching node should be .9
    # the rest of the outputs should be .1

    # map target value to output node (e.g. A == node[0])
    target_unit = ltr_to_index[target.tostring()]

    # calculate target for each node
    # for node matching letter, t = .9, otherwise t = .1
    output_layer_targets = [.1 for i in range(0, 26)]
    output_layer_targets[target_unit] = .9

    # list for errors at output layer and hidden layer
    output_layer_error = []
    hidden_layer_error = []
    # counters to move through nodes of output and hidden layers
    output_node_index = 0
    hidden_node_index = 0

    ### calculate error for each output layer node ###
    # use target list indices
    for k in range(len(output_activations)):
        # get the error at an individual node, using the place in the target list
        # that corresponds to the target for the individual node
        node_error = output_activations[k] * (1 - output_activations[k]) * (
            output_layer_targets[output_node_index] - output_activations[k])
        # append this node's error to the list of output layer errors
        output_layer_error.append(node_error)
        output_node_index += 1 # move index of node forward by one

    #### Calculate error for each hidden node ####
    # For each hidden unit j, calculate error term δj :
    # δj ← hj(1−hj) ( (∑ k∈output units) wkj δk )
    # h_j is activation of each hidden unit j
    for j in range(len(hidden_activations)):
        output_node_index = 0 # reset counter for use in summing
        output_sum = 0 # keeps track of (∑ k∈output units) wkj δk )
        # get the sum of weight[k][j]*node_error for all output units
        for k in range(len(output_activations)):
            output_error = (output_activations[k] * (1 - output_activations[k]) * (
                output_layer_targets[output_node_index] - output_activations[k]))
            output_sum += (hidden_to_output_weights[output_node_index][hidden_node_index] * output_error)
            output_node_index += 1

        ## calculate error at an individual hidden node using the formula from class notes
        # including the output_sum (∑ k∈output units) wkj δk )
        hidden_node_error = hidden_activations[j] * (1 - hidden_activations[j]) * (output_sum)

        output_sum = 0 # reset for next hidden node
        # add this node's error to the list of errors for the hidden layer
        hidden_layer_error.append(hidden_node_error)
        hidden_node_index += 1 # move index of hidden node forward by one

    #### 3. change weights after each training example ####
    # To avoid oscillations at large η, introduce momentum,
    # in which change in weight is dependent on past weight change:
    # Δw^t =η*δ_j*x_ji + αΔw^(t−1)_ji

    #### Change weights from hidden -> output layer ####
    # For each weight wkj from the hidden to output layer:
    #   wkj ← wkj +Δwkj
    #counter to make sure all weights are being updated
    no_change = 0

    # save deltas for the next iteration of weight change
    # used in current iteration as the weight change from the previous iteration
    hidden_to_output_deltas = np.full((26, n+1), 0)
    for j in range(len(hidden_activations)):
        for k in range(len(output_activations)):
            ###delta = eta * output_layer_error[k] * hidden_activations[j]
            delta = eta * output_layer_error[k]*hidden_activations[j] + alpha*hidden_to_output_deltas[k][j]
            # save deltas for the next iteration of weight change
            hidden_to_output_deltas[k][j] = delta

            # update weight
            hidden_to_output_weights_kj_prior = hidden_to_output_weights[k][j]
            hidden_to_output_weights[k][j] = hidden_to_output_weights[k][j] + delta
            # counter to make sure all weights are being updated
            if(hidden_to_output_weights[k][j] == hidden_to_output_weights_kj_prior):
                no_change += 1
    #check to make sure all weights are being updated
    # print "\nnum of weights unchanged hidden to output", no_change
    # print "hidden to output weights after change\n", hidden_to_output_weights
    # print "new weights hidden to output:\n", hidden_to_output_weights

    #### Change weights from input -> hidden layer ####
    # For each weight wji from the input to hidden layer:
    #   wji ←wji +Δwji
    input_to_hidden_weights_ji_prior = 0
    # save deltas for the next iteration of weight change
    # used in current iteration as the weight change from the previous iteration
    input_to_hidden_deltas = np.full((len(hidden_activations), len(row)), 0)
    no_change_input_to_hidden_weight = 0
    for i in range(len(row)):
        for j in range(len(hidden_activations)):
            # weight delta = Δw^t =η*δ_j*x_ji + αΔw^(t−1)_ji
            # input_to_hidden_deltas[j][i] is the previous iteration's change in weights
            delta = eta * hidden_layer_error[j]*X[j][i] + alpha*input_to_hidden_deltas[j][i]
            # save deltas for the next iteration of weight change
            input_to_hidden_deltas[j][i] = delta
            input_to_hidden_weights_ji_prior = input_to_hidden_weights[j][i]
            # update weight:
            input_to_hidden_weights[j][i] = input_to_hidden_weights[j][i] + delta
            # counter to make sure all weights are being updated
            if(input_to_hidden_weights[j][i] == input_to_hidden_weights_ji_prior):
                no_change_input_to_hidden_weight += 1
    #check to make sure all weights are being updated
    # if(no_change_input_to_hidden_weight > 0):
    #     print "\nnum of weights unchanged input to hidden", no_change_input_to_hidden_weight
    # print "input to hidden weights after change\n", input_to_hidden_weights
    # print input_to_hidden_weights




################################################################################################

# Training a multi-layer neural network
# Repeat for a given number of epochs or until accuracy on training data is acceptable:
# For each training example:
# 	1. Present input to the input layer.
# 	2. Forward propagate the activations times the weights to each node in the hidden layer.
# 	3. Forward propagate the activations times weights from the hidden layer to the output layer.
# 	4. At each output unit, determine the error E.
# 	5. Run the back-propagation algorithm to update all weights in the network.
def train(num_epochs, eta):
    """
    train() calls forward_propagation() and back_propagation()
    Run training examples through neural net to train for letter recognition
    Classification with a two-layer neural network (Forward propagation)
    For two-layer networks (one hidden layer):
    # includes multiple epochs
     I. For each test example:
         1. Present input to the input layer.
         2. Forward propagate the activations times the weights to each node in the hidden layer.
         3. Forward propagate the activations times weights from the hidden layer to the output layer.
         4. Interpret the output layer as a classification.
    """
    epoch_increment = 0

    training_acc_list = []
    testing_acc_list = []

    # run training for <num_epochs> number of epochs (defined before func is called in main)
    # each epoch runs through entire training set
    for iter in xrange(num_epochs):
        text = "\rEpoch "+str((epoch_increment)+1)+"/"+str(num_epochs)
        sys.stdout.write(text)

        # for loops:
        # training set: epoch
            # input -> hidden layer
            # hidden layer -> output layer

        # feedforward input through neural net: input layer -> hidden layer -> output
        # Y is the the output of the matrix, without any error correction
        # but already processed through the sigmoid function

        # iterate through data matrix to operate on individual training instances
        target_row = 0 # count keeps track of which index of target to pass in
        for row in X[0:50]:
            hidden_layer = [] # list to hold hidden layer, to pass to back_propagation once it's filled
            hidden_layer, Y = forward_propagation(row)

            # use back propagation to compute error and adjust weights
            # pass in activations of hidden and output layer and target letter corresponding to the row
            # that is currently being passed through the neural net
            # print X_targets[target_row]
            back_propagation(hidden_layer, Y, X_targets[target_row], row, eta)

            # move to next row of input data to use new target
            target_row += 1

        # increment epoch after all input data is processed
        epoch_increment += 1

        # After each epoch, calculate the network's accuracy
        # on the training set and the test set
        training_accuracy, testing_accuracy = calculate_accuracy(X[0:50], X_test[0:50], epoch_increment)
        training_acc_list.append(training_accuracy)
        testing_acc_list.append(testing_accuracy)

        # print "\ntraining list in training function:", training_acc_list
        # print "testing list in training function:", testing_acc_list

    # print "done with epochs"
    return training_acc_list, testing_acc_list

################################################################################################

def calculate_accuracy(training_data, test_data, epoch_num):
    """
    After each epoch, calculate the network's accuracy
    on the training set and the test set
    :param training_data, test_data, epoch_num
    :return training_accuracy, testing_accuracy:
    """
    # counters for neural net votes
    correct_train_vote = 0
    correct_test_vote = 0

    #### Training data ####
    # use forward_propagation to calculate predictions for training data
    training_predictions = []
    # record values for plotting
    training_letter_vote = []
    training_letter_actual = []
    target_row = 0
    for row in training_data:
        hidden_layer, Y_train = forward_propagation(row)
        training_predictions.append(Y_train)

        # map target value to output node (e.g. A == node[0])
        target_ltr = X_targets[target_row].tostring()
        target_unit = ltr_to_index[target_ltr]
        # print "target unit:", target_unit
        # record target letter for plotting
        training_letter_actual.append(target_ltr)
        # print training_letter_actual

        # calculate target for each node
        # for node matching letter, t = .9, otherwise t = .1
        output_layer_targets = [.1 for i in range(0, 26)]
        output_layer_targets[target_unit] = .9
        # print "output layer targets", output_layer_targets

        # compare highest valued output to target unit of .9
        # to see if the neurons have the correct output
        max_value = max(Y_train)
        Y_train_list = Y_train.tolist()
        max_index = Y_train_list.index(max_value)

        # test to see if max value in neural net output
        # matches the node with the highest target
        # if so, the neural net got the letter correct
        if max_index == target_unit:
            correct_train_vote += 1

        # move to next row of input data to use new target
        target_row += 1

    training_accuracy = correct_train_vote/float(len(training_predictions))

    ### Test data ####
    # use forward_propagation to calculate predictions for testing data
    test_predictions = []
    # record values for plotting
    test_letter_vote = []
    test_letter_actual = []
    # reset counter for iterating through letter targets
    target_row = 0
    for row in test_data:
        hidden_layer, Y_test = forward_propagation(row)
        test_predictions.append(Y_test)

        # map target value to output node (e.g. A == node[0])
        target_ltr = X_targets[target_row].tostring()
        target_unit = ltr_to_index[target_ltr]
        # record target letter for plotting
        test_letter_actual.append(target_ltr)

        # calculate target for each node
        # for node matching letter, t = .9, otherwise t = .1
        output_layer_targets = [.1 for i in range(0, 26)]
        output_layer_targets[target_unit] = .9

        # compare highest valued output to target unit of .9
        # to see if the neurons have the correct output
        max_value = max(Y_test)
        Y_test_list = Y_test.tolist()
        max_index = Y_test_list.index(max_value)

        # test to see if max value in neural net output
        # matches the node with the highest target
        # if so, the neural net got the letter correct
        if max_index == target_unit:
            correct_test_vote += 1

        # move to next row of input data to use new target
        target_row += 1

    testing_accuracy = correct_test_vote/float(len(test_predictions))
    return training_accuracy, testing_accuracy


################################################################################################

def plot_results(training_accuracy_list_low_eta, testing_accuracy_list_low_eta, training_accuracy_list_high_eta,
                 testing_accuracy_list_high_eta):
    """
    Plot results of accuracy computations

    :return:
    """
    # print len(training_accuracy_list)
    # print len(range(1, epochs+1))

    plt.title('Accuracy: Training and Testing, Experiment 2')
    plt.plot(range(1, epochs+1), training_accuracy_list_low_eta, 'ro', label='Training, eta=0.05')
    plt.plot(range(1, epochs+1), testing_accuracy_list_low_eta, 'b^', label='Test, eta=0.05')
    plt.plot(range(1, epochs+1), training_accuracy_list_high_eta, 'go', label='Training, eta=0.6')
    plt.plot(range(1, epochs+1), testing_accuracy_list_high_eta, 'r^', label='Test, eta=0.6')
    plt.xticks(np.arange(0, epochs+2), np.arange(0, epochs+2))
    plt.yticks(np.arange(0,1,0.1), np.arange(0,1,0.1))
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.grid(True)
    plt.legend(loc='upper right', numpoints=1)
    plt.show()



################################################################################################

#### dict mapping letters to number (index of unit in output row) ####
ltr_to_index = dict(zip(string.ascii_uppercase, range(0,26)))

################################################################################################

################
# Experiment 2 #
################

######
# main
######
epochs = 50
#train the neural net for <epochs> number of epochs
# using forward and back propagation
# lists for training and testing accuracies over multiple epochs
training_acc_list_low_eta = []
testing_acc_list_low_eta = []
training_acc_list_high_eta = []
testing_acc_list_high_eta = []
# run training with low learning rate
training_acc_list_low_eta, testing_acc_list_low_eta = train(epochs, eta_low)
# print "training accuracy (low eta) list in main:", training_acc_list_low_eta
# print "testing accuracy (low eta) list in main:", testing_acc_list_low_eta
# run training with high learning rate
training_acc_list_high_eta, testing_acc_list_high_eta = train(epochs, eta_high)
# print "training accuracy (high eta) list in main:", training_acc_list_high_eta
# print "testing accuracy (high eta) list in main:", testing_acc_list_high_eta
# plot results of accuracy testing
plot_results(training_acc_list_low_eta, testing_acc_list_low_eta, training_acc_list_high_eta, testing_acc_list_high_eta)
