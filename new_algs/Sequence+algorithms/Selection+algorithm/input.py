#!/usr/bin/env python

# Katie Abrahams
# abrahake@pdx.edu
# ML Independent Study
# Winter 2016

import random
from letter import letter
import numpy as np

# process data from file
with open('letter-recognition.data', 'rb') as f:
    data = f.read().split('\n')

# split data in half for training and testing
training_data = data[:10000] # data up to, not including data[10000]
testing_data = data[10000:20000] # data from data[10000] to the end of the list

# sort by letter (first element of list)
training_data = sorted(training_data)
testing_data = sorted(testing_data)

# create a list of letters from training data
letters_list_training = []
for (i, training_data) in enumerate(training_data):
    letters_list_training.append(letter(training_data.split(',')))
#    print letters_list_training[i].value
#    print letters_list_training[i].attributes

# print letters_list_training[0].value
# for letter in letters_list_training: print letter.value

# shuffle training data
random.shuffle(letters_list_training)
#np.random.shuffle(letters_list_training)
# for letter in letters_list_training: print letter.bias_input_plus_attributes
# for ltr in letters_list_training: print ltr.attributes

# create a list of letters from testing data
letters_list_testing = []
for (i, testing_data) in enumerate(testing_data):
    letters_list_testing.append(letter(testing_data.split(',')))

#print letters_list_testing[0].value
#for letter in letters_list_testing: print letter.value
random.shuffle(letters_list_testing)
#np.random.shuffle(letters_list_testing)
