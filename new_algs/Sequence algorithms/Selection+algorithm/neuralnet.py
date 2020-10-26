# !/usr/bin/env python
# coding=utf-8

# Katie Abrahams
# abrahake@pdx.edu
# ML Independent Study
# Winter 2016

import numpy as np
import sklearn.neural_network
from geneticalgorithm import *

###############################################################################

# 'Neural network in 11 lines of python', iamtrask
# iamtrask.github.io/2015/07/12/basic-python-network/
# 2 Layer Neural Network

# sigmoid function
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

###############################################################################

def main():
    # input dataset
    # Input dataset matrix where each row is a training example
    X = np.array([  [2,5,6],
                    [0,1,1],
                    [1,0,1],
                    [1,1,1] ])
    print X

    # output dataset
    # Output dataset matrix where each row is a training example
    y = np.array([[0,0,1,1]]).T

    # seed random numbers to make calculation
    # deterministic (just a good practice)
    np.random.seed(1)

    # initialize weights randomly with mean 0
    # First layer of weights, Synapse 0, connecting l0 to l1
    syn0 = 2*np.random.random((3,1)) - 1

    # start with 10 iterations to test
    # eventually want 10000
    for iter in xrange(10):

        # forward propagation
        # l0: First Layer of the Network, specified by the input data
        l0 = X
        # l1: Second Layer of the Network, aka the hidden layer
        l1 = nonlin(np.dot(l0,syn0))
        # l1 shape is (4,1)
        # Genetic algorithm population
        pop = gen_algorithm(len(l1))
        # use genetic algorithm to select feature subset
        # print "population:", pop

        # how much did we miss?
        l1_error = y - l1

        # multiply how much we missed by the
        # slope of the sigmoid at the values in l1
        l1_delta = l1_error * nonlin(l1,True)

        # update weights
        syn0 += np.dot(l0.T,l1_delta)

    print "Output After Training:"
    print l1


    # # input dataset
    # X = np.array([  [0,0,1],
    #                 [0,1,1],
    #                 [1,0,1],
    #                 [1,1,1] ])
    # # use GA population
    # pop = gen_algorithm()
    #
    # # output dataset
    # y = np.array([[0,0,1,1,0,1,0,0,1,1,
    #                0,0,1,1,0,1,0,0,1,1,
    #                0,0,1,1,0,1,0,0,1,1,
    #                0,0,1,1,0,1,0,0,1,1,
    #                0,0,1,1,0,1,0,0,1,1,]]).T
    #
    # # seed random numbers to make calculation
    # # deterministic (just a good practice)
    # np.random.seed(1)
    #
    # # initialize weights randomly with mean 0
    # syn0 = 2*np.random.random((50,10)) - 1
    # #
    # for iter in xrange(1000):
    #
    #     # forward propagation
    #     l0 = X
    #
    #     print "l0 shape", len(l0)
    #     print "syn0 shape", syn0.shape
    #     l1 = nonlin(np.dot(X,syn0))
    #
    #     # how much did we miss?
    #     l1_error = y - l1
    #
    #     # multiply how much we missed by the
    #     # slope of the sigmoid at the values in l1
    #     l1_delta = l1_error * nonlin(l1,True)
    #
    #     # update weights
    #     syn0 += np.dot(l0.T,l1_delta)
    #
    # print "Output After Training:"
    # print l1

if __name__ == "__main__":
    main()