import fileinput
import sys, getopt
import numpy as np
import time
import math
import random
import os
from copy import deepcopy

import crossoverOperators

DEBUG = 0

def handleArgs(argv):
	script = os.path.basename(__file__)
	inputFile = ''
	outputFile = ''
	usage = 'Usage: ' + script + ' -i <inputfile>' + "\n"
	usage += "Optionals: -o <outputfile>" + "\n"
	usage += "Optionals: -p <population>" + "\n"
	usage += "Optionals: -g <generations>" + "\n"
	usage += "Optionals: -g <mutation rate>" + "\n"
	usage += "Optionals: -m <mutation rate>" + "\n"
	usage += "Optionals: -c <crossover rate>" + "\n"
	usage += "Optionals: -e <elites rate>"

	if(len(argv) == 0):
		print(usage)
		sys.exit()
	try:
		opts, args = getopt.getopt(argv, "h:i:p:g:m:c:e:f:u:o:")
	except getopt.GetoptError:
		print(usage)
		sys.exit(2)

	dic = {}
	for opt, arg in opts:
		if opt == '-h':
			print(usage)
			sys.exit()
		elif opt in ("-i"):
			dic["input"] = arg
		elif opt in ("-p"):
			dic["populationSize"] = int(arg)
		elif opt in ("-g"):
			dic["generations"] = int(arg)
		elif opt in ("-m"):
			dic["mutationRate"] = float(arg)
		elif opt in ("-c"):
			dic["crossoverRate"] = float(arg)
		elif opt in ("-e"):
			dic["elitesRate"] = float(arg)
		elif opt in ("-f"):
			dic["fitnessValidFactor"] = float(arg)
		elif opt in ("-u"):
			dic["upgradeMutationRate"] = float(arg)
		elif opt in ("-o"):
			dic["output"] = arg
	return dic

def openOutput(fp):
	global outputFile
	try:
		outputFile = open(fp, "w")
		return 1
	except IOError:
		print ("Error: File does not appear to exist.")
		return 0

def wantStatistics():
	return outputFile is not None

def write(string):
	if outputFile is not None:
		outputFile.write(string)

def readFileInstance(file):
	nodes = 0
	edges = 0
	inputEdges = []
	population = []

	for line in fileinput.input(file):
		if(line[0] == 'p'):
			params = line.split()
			nodes = int(params[2])
			edges = int(params[3])
		elif (line[0] == 'e'):
			params = line.split()
			fromVertex = int(params[1])
			toVertex = int(params[2])
			inputEdges.append([fromVertex, toVertex])
		elif (line[0] == 'b'):
			params = line.split()
			cromaticNumber = int(params[1])

	graph = [0] * nodes
	vectorList = [0] * nodes
	edgeList = []
	for j in range(nodes):
		graph[j] = [0] * nodes
		vectorList[j] = [] * nodes

	for x in inputEdges:
		j = x[0] - 1
		i = x[1] - 1
		graph[j][i] = 1
		graph[i][j] = 1
		edgeList.append([i,j])
		vectorList[i].append(j)
		vectorList[j].append(i)

	return graph, edgeList, nodes, edges, vectorList, cromaticNumber

def getCrossoverReturn(crossoverMethod):
	anyInd = Individual(0, 10)

	crossoverReturn = crossoverMethod(anyInd, anyInd, 5)

	if(isinstance(crossoverReturn, Individual)):
		return 0
	else:
		return 1

class Individual:
	def __init__(self, mutationRate, fitnessValidFactor):
		self.vertexColors = np.random.randint(1, numNodes+1, size=numNodes) #creates an assortment of random colors
		self.mutationRate = mutationRate
		self.fitnessValidFactor = fitnessValidFactor

	def setMutation(self, mutationRate):
		self.mutationRate = mutationRate

	#@profile
	def fitness(self):
		score = 0
		edgeViolationScore = numEdges
		for edge in edgeList:
			if(self.vertexColors[edge[0]] == self.vertexColors[edge[1]]):
				#print("Warning: {0} ({1}) to {2} ({3})".format(i, self.vertexColors[i], j, self.vertexColors[j]))
				edgeViolationScore -= 1

		normalizedColors = numNodes - self.validColors() + 1
		vertexColoringScore = normalizedColors * self.fitnessValidFactor

		if(self.isValidSolution()):
			score += edgeViolationScore + vertexColoringScore
		else:
			score += edgeViolationScore + (vertexColoringScore / 2)
		return score

	def validColors(self):
		return len(np.unique(self.vertexColors))

	def mutate(self):
		#print(self.vertexColors)
		for position in range(numNodes):
			r = np.random.random()
			if(self.mutationRate > r):
				if(bFoundValid == 1):
					# USED BEFORE, SIMPLE MUTATION
					self.vertexColors[position] = np.random.randint(1, numNodes+1)
				else:
					# GET VALID COLOR
					colors = list(map(lambda x: self.vertexColors[x], vectorList[position]))
					solved = False
					while(not solved):
						tryColor = np.random.randint(1, numNodes+1)
						if tryColor not in colors:
							self.vertexColors[position] = tryColor
							solved = True

	#@profile
	def isValidSolution(self):
		# global isValid
		for edge in edgeList:
			if(self.vertexColors[edge[0]] == self.vertexColors[edge[1]]):
				return False
		return True

	def __str__(self):
		return self.visual()

	def visual(self):
		return str(self.vertexColors) + " (" + str(self.fitness()) + ")"

class Population:
	global generation

	def __init__(self, size, mutationRate, crossoverRate, elitesRate, fitnessValidFactor, upgradeMutationRate, crossoverMethod):
		numNodes = len(graph[0])
		self.size = size
		self.crossoverRate = crossoverRate
		self.population = self.initialize(upgradeMutationRate, fitnessValidFactor)
		self.mutationRate = mutationRate # TODO MOVE TO INDIVIDUAL
		self.upgradeMutationRate = upgradeMutationRate # TODO MOVE TO INDIVIDUAL
		self.crossover = crossoverMethod
		self.crossoverReturnsDouble = getCrossoverReturn(crossoverMethod)
		self.numOfElites = math.ceil(size * elitesRate)
		print("Running for...")
		print("Population size: {0}".format(size))
		print("Number of elites: {0}".format(self.numOfElites))
		print("Mutation rate: {0}%".format(mutationRate*100))
		print("Crossover rate: {0}%".format(crossoverRate*100))
		print("Fitness valid factor: {0}".format(fitnessValidFactor))
		print("upgradeMutationRate rate: {0}%".format(upgradeMutationRate*100))

		write("h Generation, Mean fitness, Best fitness, Valid solutions, Colors, Mean Colors\n");

	def __str__(self):
		pop = ""
		for i in self.population:
			pop += i.visual() + "\n"
		return pop

	def initialize(self, mutationRate, fitnessValidFactor):
		population = []
		for i in range(self.size):
			individual = Individual(mutationRate, fitnessValidFactor)
			population.append(individual)
		return population

	def beautifulGraph(self):
		for i in range(numNodes):
			if(i == 0):
				sys.stdout.write("  ")
				for x in range(numNodes):
					sys.stdout.write(chr(x + 65) + " ")
				print()
			for j in range(numNodes):
				if(j == 0):
					sys.stdout.write(chr(i + 65) + " ")
				sys.stdout.write(str(graph[i][j]) + " ")
			print()

	def updatePopulationMutationRate(self, mutationRate):
		for i in range(self.size):
			self.population[i].setMutation(mutationRate)

	def nextGen(self):
		global generation
		global bFoundValid
		#bFoundValid = False #amount of valid individuals on the population
		totalScore = 0
		scores = [0] * self.size
		accumulated = [0] * self.size

		for i in range(self.size):
			scores[i] = self.population[i].fitness()

		if(not bFoundValid):
			doOnce = False
			for i in range(self.size):
				if(self.population[i].isValidSolution()):
					bFoundValid = True
					if(not doOnce):
						self.updatePopulationMutationRate(self.mutationRate)
						doOnce = True
						write("i Changed mutation\n")

		# Sort score population pairs list based on the score
		scores, sortedPopulation = list(zip(*sorted(zip(scores, self.population),
		 	key=lambda x: x[0])))

#===================================== PRINTS =====================================
		# print("-------- Best so far -------")
		# #print("Colors: {0}".format(sortedPopulation[self.size-1].vertexColors))
		# #print("{0}/{1} are valid solutions".format(valid,self.size))
		# print("Number of colors: {0}".format(sortedPopulation[self.size-1].validColors()))
		# print("Is valid solution: {0}".format("yes" if
		# 	sortedPopulation[self.size-1].isValidSolution() else "no"))
		# print("Best = {0}".format(scores[self.size-1]))
#==================================================================================

		# compute cumulative score
		for i in range(self.size):
			totalScore += scores[i]
			accumulated[i] = totalScore

#===================================== DEBUG ======================================
		if DEBUG == 1:
			probs = [0] * self.size
			for i in range(self.size):
				probs[i] = (scores[i] / totalScore) * 100
			print("Input population (sorted):")
			for i in range(self.size):
				validity = "valid" if sortedPopulation[i].isValidSolution() else "invalid"
				print(str(sortedPopulation[i].vertexColors) +
				" (" + str(sortedPopulation[i].validColors()) + ")" +
				" " + str(validity) +
				" - " + str(scores[i]) + " / " + str(totalScore) +
				" (" + str(round(probs[i], 2)) + "%)")
#==================================================================================

		# generate a new population
		numPointers = self.size - self.numOfElites

		pointerDistance = math.floor(totalScore / numPointers)

		start = np.random.randint(0, pointerDistance)

		pointers = np.arange(start, totalScore, pointerDistance)

		mating = []

		pointerCount = 0
		i = 0
		while(i < self.size and pointerCount < numPointers):
			if accumulated[i] > pointers[pointerCount]:
				mating.append(i)
				pointerCount += 1
				i -= 1
			i += 1
		np.random.shuffle(mating)

		newPopulation = []
		for i in range(0, numPointers, 1 + self.crossoverReturnsDouble):
			#print("Acessing {0} of length {1} / {2}".format(i, len(mating), numPointers))
			firstIndividual = sortedPopulation[mating[i]]

			if i + 1 >= numPointers:
				secondIndividual = sortedPopulation[mating[0]]
			else:
				secondIndividual = sortedPopulation[mating[i+1]]

			r = np.random.random()
			if self.crossoverRate > r:
				offspring = []
				offspring = self.crossover(firstIndividual, secondIndividual, numNodes)
				# add to new population
				if self.crossoverReturnsDouble:
					newPopulation.append(offspring[0])
					if(len(newPopulation) < numPointers):
						newPopulation.append(offspring[1])
				else:
					newPopulation.append(offspring)
			else:
				firstCrossed = deepcopy(firstIndividual)
				# add to new population
				newPopulation.append(firstCrossed)
				if(self.crossoverReturnsDouble):
					secondCrossed = deepcopy(secondIndividual)
					newPopulation.append(secondCrossed)

#===================================== DEBUG ======================================
		if DEBUG == 1:
			print("Crossover population:")
			for i in range(numPointers):
				print(newPopulation[i])
#==================================================================================

		# do mutation
		for i in range(len(newPopulation)):
			newPopulation[i].mutate()

		for i in range(1, self.numOfElites+1):
			newPopulation.append(deepcopy(sortedPopulation[i*-1]))

		self.population = newPopulation

		if wantStatistics():
			numValids = 0
			totalColors = 0
			for individual in self.population:
				totalColors += individual.validColors()
				if individual.isValidSolution():
					numValids += 1

			scoreMean = int(totalScore / self.size)
			bestScore = format(scores[self.size-1])
			colors = format(sortedPopulation[self.size-1].validColors())
			colorsMean = int(totalColors / self.size)
			stats = ""
			stats += str(generation) + ', '
			stats += str(scoreMean) + ', '
			stats += str(bestScore) + ', '
			stats += str(numValids) + ', '
			stats += str(colors) + ', '
			stats += str(colorsMean)
			stats += "\n"
			write(stats)

		generation += 1

#===================================== DEBUG ======================================
		if DEBUG == 1:
			print("Crossover + Mutated population: \n{0}".format(self))
			print("----------------------------")
#==================================================================================

def main(argv):
	global bFoundValid
	global graph
	global edgeList
	global numNodes
	global numEdges
	global outputFile
	global generation
	global vectorList
	global cromaticNumber
	bFoundValid = False

	outputFile = None
	generation = 1

	io = handleArgs(argv)

	if('output' in io):
		openOutput(io['output'])

	# example for execution: py gcp.py -i flat1000_76_0.col -o output.csv -g 1000000 -p 50 -m 0.001 -c 0.8 -e 0.1
	# explain what each parameter is:
	# -i is the graph instance, a file that represents amount of nodes and edges
	# -o is the name of the output file, used to generate graphs for analysis
	# -g is the maximum number of generations the program will loop for
	# -p is the population size
	# -m is the mutation rate
	# -c is the crossover rate
	# -e is the percentage of elites that will be taken from the population after each generation

	if('input' in io):
		graph, edgeList, numNodes, numEdges, vectorList, cromaticNumber = readFileInstance(io['input']) # flat1000_76_0 simple complicated

		params = {
	        'populationSize': 100,
	        'generations': 1000000,
	        'mutationRate': 0.1,
			'crossoverRate': 0.8,
			'elitesRate': 0.1,
			'fitnessValidFactor': 10,
			'upgradeMutationRate': 0.8
	    }

		for key, value in params.items():
			if key in io:
				params[key] = io[key]

		start = time.time()
		population = Population(params['populationSize'], params['mutationRate'], params['crossoverRate'], params['elitesRate'], params['fitnessValidFactor'], params['upgradeMutationRate'], crossoverOperators.newCrossover)
		for i in range(1, params['generations'] + 1):
			#print("Generation {0}: ".format(i))
			best = population.population[params['populationSize']-1]
			if (best.validColors() == cromaticNumber):
				break;
			population.nextGen()
		end = time.time()
		elapsed = end - start
		print("Elapsed time is {0}".format(elapsed))
		write("i Elapsed time is {0}\n".format(round(elapsed, 2)))
		best = population.population[params['populationSize']-1]
		isValid = "valid" if best.isValidSolution() else "invalid"
		write("i Best is {0} colors and its {1}\n".format(best.validColors(), isValid))

if __name__ == "__main__":
   main(sys.argv[1:])
