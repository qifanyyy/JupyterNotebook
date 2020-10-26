#!/usr/bin/env python
# coding=utf-8

# Katie Abrahams
# abrahake@pdx.edu
# ML Independent Study
# Winter 2016

from pybrain import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SoftmaxLayer

# This call returns a network that has two inputs, three hidden and a single output neuron.
# In PyBrain, these layers are Module objects and they are already connected with FullConnection objects.
n = buildNetwork(2, 3, 1)
n.activate((2, 3))
print n