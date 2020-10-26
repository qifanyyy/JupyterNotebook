#!/usr/bin/python

import math
import string

from matplotlib import pyplot
from path import Path

class PlotGraph:
	'''
	Plot a graph using the graphMat matrix provided.
	graphMat:
		matrix of type numpy.matrix
	'''

	def __init__(self, graphMat):
		self.graphMat = graphMat
		if not self.graphMat.shape[0] == self.graphMat.shape[1]:
			raise ValueError("Please enter a valid adjacency matrix!")

		# No. of vertices = no. of rows of the matrix
		self.numVertices = self.graphMat.shape[0]

		# Radius of the circle containing the vertices
		self.r = 1 

	def getVertextCoordinates(self):
		'''
		Return the cartesian coordinates of the graph based on the number of vertices 
		and radius of the circle containing the points
		'''
		pi = math.pi
		vertexCoords = []

		# Initializing the angle to be 0 radians
		theta = pi

		# Setting the interval based on the number of vertices
		interval = 2*pi / self.numVertices

		for x in xrange(self.numVertices):
			xCoord = round(self.r * math.cos(theta), 2)
			yCoord = round(self.r * math.sin(theta), 2)
			vertexCoords.append((xCoord, yCoord))
			theta += interval

		return vertexCoords

	def getEdges(self):
		'''
		Return a list of edges denoted by vertex numbers and not actual position
		Ex: (0,1) means Vertex 0 and Vertex 1
		'''
		numVertices = self.graphMat.shape[0]

		edgeList = []
		for i in xrange(numVertices):
			for j in xrange(numVertices):
				if self.graphMat[i,j]:
					edgeList.append((i,j))

		return edgeList

	def getOffsettedValues(self, xPos, yPos, offset):
		'''
		Return modified xPos and yPos values with the offset depending on the quadrant
		'''
		if yPos > 0:
			yPos += offset
			if xPos > 0:
				xPos += offset
			elif xPos < 0:
				xPos -= offset
		elif yPos < 0:
			yPos -= offset
			if xPos > 0:
				xPos += offset
			elif xPos < 0:
				xPos -= offset
		elif not yPos:
			if xPos > 0:
				xPos += offset
			elif xPos < 0:
				xPos -= offset
		elif not xPos:
			if yPos > 0:
				yPos += offset
			elif yPos < 0:
				yPos -= offset

		return xPos, yPos

	def plot(self):
		'''
		Plot the graph/network
		'''

		vertexCoords = self.getVertextCoordinates()
		print vertexCoords

		# Plotting the edges first
		edgeList = self.getEdges()
		print "Found %d edges in the graph" % len(edgeList)
		for edge in edgeList:
			print edge
			xPos  = vertexCoords[edge[0]]
			yPos = vertexCoords[edge[1]]
			pyplot.arrow(xPos[0], xPos[1], 
						 yPos[0]-xPos[0], yPos[1]-xPos[1], 
						 head_length=0.2, head_width=0.1, fc='k', ec='k',
						 length_includes_head=True, overhang=0.2)

		# Plotting the vertices and the labels
		alphabet = string.ascii_uppercase
		for v in xrange(self.numVertices):
			xPos, yPos = vertexCoords[v][0], vertexCoords[v][1]

			xPosLabel, yPosLabel = self.getOffsettedValues(xPos, yPos, 0.3)
			pyplot.text(xPosLabel, yPosLabel, alphabet[v], fontsize=20)

			xPosVertex, yPosVertex = self.getOffsettedValues(xPos, yPos, 0.07)
			pyplot.plot(xPosVertex, yPosVertex, 'wo', mew=2, ms=20) # ms : Marker Size

		pyplot.axis([-2*self.r, 2*self.r, -2*self.r, 2*self.r])
		pyplot.title("Graph of %d vertices, %d edges" % (self.numVertices, len(edgeList)), loc='center')
		pyplot.show()