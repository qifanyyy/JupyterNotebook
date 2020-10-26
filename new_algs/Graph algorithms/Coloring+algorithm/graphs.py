from colors import *
from random import randint

class Vertex:
	def __init__(self, name):
		self.name = name
		self.color = Colors.BLACK
		self.neighbors = []

	def getName(self):
		return self.name

	def getColor(self):
		return self.color

	def setColor(self, color):
		self.color = color

	def differentColorNeighbor(self):
		for neighbor in self.neighbors:
			if neighbor.color == self.color:
				return False
		return True

	def __repr__(self):
		return str(self.name)

class Graph:
	def __init__(self, filename, colorNum):
		self.filename = filename
		self.verticesDict = Graph.buildVerticesDict(filename)
		self.colorNum = colorNum

	def getVertices(self):
		return list(self.verticesDict.values())

	def setRandomColoring(self):
		for vertex in self.getVertices():
			vertex.color = list(Colors)[randint(0,self.colorNum-1)]

	def copy(self):
		newGraph = Graph(self.filename, self.colorNum)
		for newVertexName in newGraph.verticesDict:
			newVertex = newGraph.verticesDict[newVertexName]
			newVertex.color = self.verticesDict[newVertexName].color
		return newGraph

	def getVertex(self, vertexName):
		return self.verticesDict[vertexName]

	@staticmethod
	def buildVerticesDict(filename):
		graphText = open(filename, 'r')
		verticesDict = {} #vertex name -> vertex object

		while True:
			vertexLine = graphText.readline()
			if not vertexLine:
				break

			lineValues = vertexLine.split(" ")
			vertexName = int(lineValues[0])
			vertex = verticesDict.get(vertexName, Vertex(vertexName))
			verticesDict[vertexName] = vertex
			neighborsNames = lineValues[1].strip().split(",")[:-1]
			for neighborNameStr in neighborsNames:
				neighborName = int(neighborNameStr)
				neighbor = verticesDict.get(neighborName, Vertex(neighborName))
				verticesDict[neighborName] = neighbor
				vertex.neighbors.append(neighbor)

		graphText.close()

		return verticesDict
