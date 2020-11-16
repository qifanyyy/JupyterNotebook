#!/usr/bin/python

import numpy 
from path import Path

class ReadGraph:
	'''
	Read the graph matrix from a text file and store it in a numpy matrix.
	Returns the same matrix
	'''

	def __init__(self, inputFile):
		self.inputFile = inputFile

	def read(self):
		'''
		Read the file contents into a matrix
		'''
		graphString = self.inputFile.text()
		graphMat = numpy.matrix(str(graphString))
		
		return graphMat