from graphs import *
from random import random
import colors

NUM_INDIVIDUALS = int(1e3)
MUTATION_RATE = 0.05

# Calculates the fitness of the graph between 0 and 1 (inclusive)
# Fitness is calculate based on the number of vertices with no neighboring vertex with the same color
def fitness(graph):
	correctVertices = 0
	for vertex in graph.getVertices():
		if vertex.differentColorNeighbor():
			correctVertices+=1
	return correctVertices/len(graph.getVertices())

# Creates a list of length NUM_INDIVIDUALS with randomly colored graphs
def createInitialPopulation(graph_path, colorNum):
	population = []
	for _ in range(NUM_INDIVIDUALS):
		graph = Graph(graph_path, colorNum)
		graph.setRandomColoring()
		population.append(graph)
	return population

# Evaluates the entire generation and outputs a tuple with three elements
# First element is a list with all the fitness scores
# Second element is the best graph
def evaluateGeneration(population):
	argMax = None
	maxFitness = 0
	fitnessScores = []
	for instance in population:
		fitnessScore = fitness(instance)
		fitnessScores.append(fitnessScore)
		if maxFitness <= fitnessScore:
			argMax = instance
			maxFitness = fitnessScore

	return (fitnessScores, argMax)


def matingRandom(parent1, parent2):
	child = parent1.copy()
	for vertex in parent2.getVertices():
		if random() < 0.5:
			child.getVertex(vertex.getName()).setColor(vertex.getColor())
	return child

def matingHalfHalf(parent1, parent2):
	child = parent1.copy()
	verticesNum = len(parent1.getVertices())
	for vertexI in range(verticesNum//2, verticesNum):
		parent2Vertex = parent2.getVertex(vertexI)
		child.getVertex(vertexI).setColor(parent2Vertex.getColor())
	return child

def mutateGeneration(population):
	for graph in population:
		mutateGraph(graph)

def mutateGraph(graph):
	vertices = graph.getVertices()
	for vertex in vertices:
		rand = random()
		if rand < MUTATION_RATE:
			vertex.setColor(colors.getRandomColor(graph.colorNum))


