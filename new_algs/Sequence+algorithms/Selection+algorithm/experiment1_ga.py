#!/usr/bin/env python
# coding=utf-8

# Katie Abrahams
# abrahake@pdx.edu
# ML Independent Study
# Winter 2016
# neural net code modified from ML HW 2

from __future__ import division # want float and not int division
# import data structures, variables, and neural net from neural_net
# data structures in the global scope
from neural_net_ga import *
import string
import matplotlib.pyplot as plt
import timing
from genetic_algorithm import *
from experiment1_non_ga import *

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=UserWarning)

####################
# Program parameters
####################
# number of slices taken from training and test sets
num_rows = 10
# number of epochs to train the neural net
epochs = 10
# number of times to run non-GA and GA algorithm epochs to get grand mean
rounds, ga_rounds = 10, 10


###############
# function defs
###############
def forward_propagation(row, input_to_hidden_weights):
    """
    Function called in train_and_test()
    Forward propagate the input through the neural network
    during neural network training
    Does not include error computation
    :param row: (row of data matrix)
    :param input_to_hidden_weights:
    :return output of neural net:
    """
    # check row shape
    # print "- row shape, forward prop:", len(row)

    # transpose row vector for matrix multiplication
    X_row = np.mat(row)
    X_col = X_row.transpose()

    hidden_weights_shape = input_to_hidden_weights.shape
    x_col_shape = X_col.shape
    # print "input to hidden weights shape", hidden_weights_shape
    # print "X_col shape", x_col_shape

    # forward propagation
    # initial run of data, use sigmoid activation function
    # pass in dot products of inputs and weights
    hidden_layer = sigmoid(np.dot(input_to_hidden_weights, X_col), False)

    # hidden_layer is the activation at the hidden layer
    # use activations as input for the output layer

    # use hidden layer activations to get activations for output layer
    # append one row of 1s to hidden layer to allow for bias input
    bias_input_hidden_layer = np.full((1, 1), 1.0)
    # print bias_input_hidden_layer
    hidden_layer_concat = np.concatenate((hidden_layer, bias_input_hidden_layer), axis=0)

    # matrix multiply (hidden layer) dot (weights from hidden -> output)
    output_layer = np.dot(hidden_to_output_weights, hidden_layer_concat)

    # apply sigmoid function to output layer
    # to get activations at output layer
    Y = sigmoid(output_layer, False)

    # return activations from hidden and output layers
    return hidden_layer, Y

################################################################################################


def back_propagation(hidden_activations, output_activations, target, row, input_to_hidden_weights):
    """
    Function called in train_and_test()
    The the back-propagation algorithm is used
    during training to update all weights in the network.
    Pass in activation of output layer and
    target letter corresponding to the row that is currently being passed through the neural net
    :param hidden_activations:
    :param output_activations:
    :param target:
    :param row:
    :param input_to_hidden_weights:
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
    # print "target unit:", target_unit

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
    # if(no_change > 0):
    #     print "\nnum of weights unchanged hidden to output", no_change

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

################################################################################################

# Training a multi-layer neural network
# Repeat for a given number of epochs or until accuracy on training data is acceptable:
# For each training example:
# 	1. Present input to the input layer.
# 	2. Forward propagate the activations times the weights to each node in the hidden layer.
# 	3. Forward propagate the activations times weights from the hidden layer to the output layer.
# 	4. At each output unit, determine the error E.
# 	5. Run the back-propagation algorithm to update all weights in the network.
#### Pass in GA population
def train_and_test(num_epochs, ga_initial_pop):
    """
    train_and_test() calls forward_propagation() and back_propagation()
    Run training examples through neural net to train for letter recognition
    Classification with a two-layer neural network (Forward propagation)
    For two-layer networks (one hidden layer):
    # includes multiple epochs
     I. For each test example:
         1. Present input to the input layer.
         2. Forward propagate the activations times the weights to each node in the hidden layer.
         3. Forward propagate the activations times weights from the hidden layer to the output layer.
         4. Interpret the output layer as a classification.
    :param num_epochs:
    :param ga_pop:
    """
    epoch_increment = 0

    # run genetic algorithm on initial population
    ga_pop = genetic_algorithm(ga_initial_pop)

    # get the number of features to use in feature subset selection
    # by finding the number of 1s in the ga_pop
    num_features = get_num_features(ga_pop)
    # create weights from input -> hidden layer using the correct number of features
    # selected by genetic algorithm (num_features)
    input_to_hidden_weights = np.random.uniform(low= -.25, high= .25, size=(n, num_features))

    training_acc_list = []
    testing_acc_list = []
    # clear list if need be
    if training_acc_list:
        training_acc_list[:] = []
    if testing_acc_list:
        testing_acc_list[:] = []

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

        ##################################
        # GA Feature
        # row for use as neural net input
        # selected by GA
        ##################################
        # input to neural net with GA-selected features in each row only
        ga_X = []
        ga_X_test = []
        # count keeps track of which index of target to pass in
        target_row = 0
        # iterate over input data
        for row in X[0:num_rows]:
            # print "\nTRAIN another row of X..."
            ######################################################################
            # GA Feature
            # Select feature subset from genetic algorithm to pass to forward prop
            # If the index in GA pop is 1, include that feature in training
            ######################################################################
            ga_row = [] # build training data
            for i in xrange(len(ga_pop)):
                for j in xrange(len(ga_pop[i])):
                    if ga_pop[i][j] == 1:
                        ga_row.append(row[j]) # build feature subset
            # print "len of ga_row, training:", len(ga_row)  # variable depending on number of 1s in pop
            # print "ga row", ga_row
            # pass in ga_row to forward_prop instead of row

            # build neural net input using rows with only a limited number of features
            ga_X.append(ga_row)

            hidden_layer = [] # list to hold hidden layer, to pass to back_propagation once it's filled
            #############################
            # Use GA row instead of 'row'
            #############################
            hidden_layer, Y = forward_propagation(ga_row, input_to_hidden_weights)
            # use back propagation to compute error and adjust weights
            # pass in activations of hidden and output layer and target letter corresponding to the row
            # that is currently being passed through the neural net
            back_propagation(hidden_layer, Y, X_targets[target_row], ga_row, input_to_hidden_weights)

            # move to next row of input data to use new target
            target_row += 1

        # increment epoch after all input data is processed
        epoch_increment += 1

        # check integrity of total input for GA neural net input
        # print "ga X:", ga_X

        # print "Done with training loop!\n"

        ############################################################
        # Build test data using features selected from GA population
        # used to test accuracy of training
        ############################################################
        ga_test_row = [] # build testing data
        ga_test_pop = ga_pop[:]
        # print "ga_test_pop in train\n", ga_test_pop
        # print "TEST Building test set..."
        # print "len ga_test_pop", len(ga_test_pop)
        for row in X_test[0:num_rows]:
            ga_test_row = [] # build training data
            for i in xrange(len(ga_test_pop)):
                for j in xrange(len(ga_test_pop[i])):
                    if ga_test_pop[i][j] == 1:
                        # ga_test_row.append(X_test[i][j])  # build feature subset
                        ga_test_row.append(row[j])
            # print "TEST len of ga_test_row", len(ga_test_row)  # variable depending on number of 1s in pop
            # print "ga row", ga_test_row
            # build neural net test input using rows with only a limited number of features
            ga_X_test.append(ga_test_row)

        # print "---------------------"
        # print "ga_X", len(ga_X)
        # print "---------------------"
        # print "ga_X_test", ga_X_test
        # print "---------------------"


        ###############
        # Test accuracy
        ###############
        # After each epoch, calculate the network's accuracy
        # on the training set and the test set
        training_accuracy, testing_accuracy = calculate_accuracy(ga_X, ga_X_test, X[0:num_rows], X_test[0:num_rows],
                                                                 epoch_increment, input_to_hidden_weights)
        training_acc_list.append(training_accuracy)
        testing_acc_list.append(testing_accuracy)
        # print "\ntraining list in train", training_acc_list
        # print "testing list in train", testing_acc_list

    # print "done with epochs"
    return training_acc_list, testing_acc_list


################################################################################################

def calculate_accuracy(ga_training_data, ga_test_data, training_data, test_data, epoch_num, input_to_hidden_weights):
    """
    After each epoch, calculate the network's accuracy
    on the training set and the test set
    :param ga_training_data, ga_test_data training_data, test_data, epoch_num, input_to_hidden_weights
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

    # use ga_training_data instead of training_data for GA
    for row in ga_training_data:
        hidden_layer, Y_train = forward_propagation(row, input_to_hidden_weights)
        training_predictions.append(Y_train)

        # map target value to output node (e.g. A == node[0])
        # start at 0 for target_row and increment below to go through neural net nodes
        target_ltr = X_targets[target_row].tostring()
        target_unit = ltr_to_index[target_ltr]
        # record target letter for plotting
        training_letter_actual.append(target_ltr)
        # print training_letter_actual

        # calculate target for each node
        # for node matching letter, t = .9, otherwise t = .1
        output_layer_targets = [.1 for i in range(0, 26)]
        output_layer_targets[target_unit] = .9

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
    # print "\ntraining accuracy:", training_accuracy

    # clear list contents
    training_predictions[:] = []
    # record values for plotting
    training_letter_vote[:] = []
    training_letter_actual[:] = []

    ### Test data ####
    # use forward_propagation to calculate predictions for testing data
    test_predictions = []
    # record values for plotting
    test_letter_vote = []
    test_letter_actual = []
    # reset counter for iterating through letter targets
    target_row = 0
    # use ga_test_data instead of test_data for GA
    for row in ga_test_data:
        hidden_layer, Y_test = forward_propagation(row, input_to_hidden_weights)
        test_predictions.append(Y_test)

        # map target value to output node (e.g. A == node[0])
        # start at 0 for target_row and increment below to go through neural net nodes
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

    # print "correct test vote", correct_test_vote
    # print "len of test predictions", len(test_predictions)
    testing_accuracy = correct_test_vote/float(len(test_predictions))
    # print "test accuracy:", testing_accuracy

    # clear list contents
    test_predictions[:] = []
    # record values for plotting
    test_letter_vote[:] = []
    test_letter_actual[:] = []

    return training_accuracy, testing_accuracy


################################################################################################

def plot_results(training_accuracy_list, testing_accuracy_list, title):
    """
    Plot results of accuracy computations
    :return:
    """
    # print len(training_accuracy_list)
    # print len(range(1, epochs+1))

    plt.title(title)
    plt.plot(range(1, epochs+1), training_accuracy_list, 'ro', label='Training')
    plt.plot(range(1, epochs+1), testing_accuracy_list, 'b^', label='Test')
    plt.xticks(np.arange(0, epochs+2), np.arange(0, epochs+2))
    plt.yticks(np.arange(0,1,0.1), np.arange(0,1,0.1))
    plt.ylabel('Avg. accuracy')
    plt.xlabel('Epoch')
    plt.grid(True)
    plt.legend(loc='upper right', numpoints=1)
    plt.show()


################################################################################################

#### dict mapping letters to number (index of unit in output row) ####
ltr_to_index = dict(zip(string.ascii_uppercase, range(0,26)))

################################################################################################

################
# Experiment 1 #
################


######
# main
######
def main():
    # train the neural net for <epochs> number of epochs
    # using forward and back propagation

    # list of all 1s to get all features into "feature subset"
    # for comparison with genetic algorithm

    # lists for training and testing accuracies over multiple epochs
    training_acc_list_all_features = []
    testing_acc_list_all_features = []
    training_acc_list = []
    testing_acc_list = []
    training_acc_list_deux = []
    testing_acc_list_deux = []

    # vars for tracking accuracies
    improvements = []
    accuracy = 0
    prior_acc = 0
    avg_acc = 0
    accuracies_spanning_epochs = [[] for i in xrange(epochs)]
    accuracies_test_spanning_epochs = [[] for i in xrange(epochs)]


    #####################################################################################

    ####################
    # Using all features
    ####################
    # vars for tracking accuracies
    # reset values for neural net training
    improvements = []
    accuracy = 0
    prior_acc = 0
    avg_acc = 0
    accuracies_spanning_epochs = [[] for i in xrange(epochs)]
    print ("*******************")
    print ("Running neural net training & test with all features...")
    # run training for multiple rounds of epochs
    for i in xrange(rounds):
        # rounds of epochs for more testing, getting averages over epochs
        training_acc_list_all_features, testing_acc_list_all_features = train(epochs)
        print ("\nTraining accuracy, testing accuracy:", training_acc_list_all_features, testing_acc_list_all_features)

        # plot results of accuracy testing
        # plot_results(training_acc_list_all_features, testing_acc_list_all_features)

        # get avg of accuracy across epochs
        prior_acc = avg_acc
        # avg_acc = np.mean(training_acc_list)
        # store multiple epoch accuracies
        accuracies_spanning_epochs[i].append(training_acc_list_all_features)
        accuracies_test_spanning_epochs[i].append(testing_acc_list_all_features)
        print ("\n",i+1,"round(s) done.")
    print ("\nAll features run done.")
    print ("-------------------")
    # print "\nTraining accuracy, testing accuracy:", training_acc_list_all_features, testing_acc_list_all_features

    # calc grand mean for all rounds by averaging accuracies from epochs
    # record training accuracies
    avg_acc_training_per_epoch = []
    for i in xrange(len(accuracies_spanning_epochs)):
        avg_acc_training_per_epoch.append(np.mean(accuracies_spanning_epochs[i]))
    grand_mean_all_features = np.mean(avg_acc_training_per_epoch)

    # record test accuracies
    avg_acc_test_per_epoch = []
    for i in xrange(len(accuracies_test_spanning_epochs)):
        avg_acc_test_per_epoch.append(np.mean(accuracies_test_spanning_epochs[i]))
    grand_mean_all_features_test = np.mean(avg_acc_test_per_epoch)

    print ("Grand mean (training) of neural net using entire feature string, across runs of epochs:", grand_mean_all_features)
    print ("Grand mean (test) of neural net using entire feature string, across runs of epochs:", grand_mean_all_features_test)

    # plot results of accuracy testing over multiple epochs
    # plot_results(avg_acc_training_per_epoch, avg_acc_test_per_epoch, 'Average accuracies, all features')

    print ("*******************")


    #####################################################################################

    #############################################
    # Feature subset selection using GA algorithm
    # GA population calculated in neural net file
    #############################################

    # vars for tracking accuracies
    ga_accuracy = 0
    ga_prior_acc = 0
    ga_avg_acc = 0
    improvements[:] = []
    acc_improvement = False
    # store accuracies for multiple epochs
    ga_accuracies_spanning_epochs = [[] for i in xrange(epochs)]
    ga_accuracies_test_spanning_epochs = [[] for i in xrange(epochs)]

    # run training using GA algorithm for multiple rounds of epochs
    print ("Running nn training & test with GA feature subset...")
    # create initial population
    ga_population = create_gen_population()
    print ("ga population initial", ga_population)
    # ga_population = genetic_algorithm(ga_population)
    for i in xrange(ga_rounds):
        #####################################################
        # Run GA algorithm on feature subset selection string
        #####################################################

        training_acc_list_deux, testing_acc_list_deux = train_and_test(epochs, ga_population)
        print ("\nTraining accuracy, testing accuracy:", training_acc_list_deux, testing_acc_list_deux)

        # print "\nAvg of training accuracy for all epochs", np.mean(training_acc_list_deux)

        # get avg of accuracy across epochs and store for comparison with next run
        ga_prior_acc = ga_avg_acc
        ga_avg_acc = np.mean(training_acc_list_deux)
        if ga_avg_acc > ga_prior_acc:
            acc_improvement = True

        # store multiple epoch accuracies
        ga_accuracies_spanning_epochs[i].append(training_acc_list_deux)
        ga_accuracies_test_spanning_epochs[i].append(testing_acc_list_deux)
        print ("\n",i+1,"round(s) done.")
    print ("\nGA rounds complete.")
    print ("-------------------")
    # print "\nTraining accuracy, testing accuracy:", training_acc_list_deux, testing_acc_list_deux

    # calc grand mean for all rounds by averaging accuracies from epochs
    # recording training accuracies
    ga_avg_acc_training_per_epoch = []
    for i in xrange(len(ga_accuracies_spanning_epochs)):
        ga_avg_acc_training_per_epoch.append(np.mean(ga_accuracies_spanning_epochs[i]))
    ga_grand_mean = np.mean(ga_avg_acc_training_per_epoch)

    # record test accuracies
    ga_avg_acc_test_per_epoch = []
    for i in xrange(len(ga_accuracies_test_spanning_epochs)):
        ga_avg_acc_test_per_epoch.append(np.mean(ga_accuracies_test_spanning_epochs[i]))
    ga_grand_mean_test = np.mean(ga_avg_acc_test_per_epoch)

    print ("Grand mean (training) of neural net using GA feature selection, across runs of epochs:", ga_grand_mean)
    print ("Grand mean (test) of neural net using GA feature selection, across runs of epochs:", ga_grand_mean_test)

    # plot results of accuracy testing over multiple epochs
    # plot_results(ga_avg_acc_training_per_epoch, ga_avg_acc_test_per_epoch, 'Average accuracies, genetic algorithm feature subset')

    print ("*******************")

    # all results
    print (" ----- Grand Means, training -----")
    print ("  All features  | GA pop, mutated")
    print ("  _____________________________")
    print (" | ", grand_mean_all_features,"     | ", ga_grand_mean, "      | ")
    print (" |______________|______________|")

    print (" \n----- Grand Means, test -----")
    print ("  All features  | GA pop, mutated")
    print ("  _____________________________")
    print (" | ", grand_mean_all_features_test,"     | ", ga_grand_mean_test, "      | ")
    print (" |______________|______________|")

    # plot results
    plot_results(avg_acc_training_per_epoch, avg_acc_test_per_epoch, 'Average accuracies, all features')
    plot_results(ga_avg_acc_training_per_epoch, ga_avg_acc_test_per_epoch, 'Average accuracies, genetic algorithm feature subset')


if __name__ == "__main__":
    main()
