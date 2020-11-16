'''
	Your goal is to color a map of these regions with two requirements: 
	1) make sure that each adjacent department do not share a color, so you can clearly distinguish each 
	department, and 
	2) minimize these numbers of colors.
	
	The input will be a variation of the list of French departments, represented as an adjacency list[5] . This challenge is essentially solving for Graph coloring[6] , where 
	you must print each department's color (a unique integer).

	Input Description:
		On standard console input, you will be given an integer N which represents the following N-lines of an adjacency list. These lines of data will always be in the format 
		of integers A B C D ... where A is the source node / vertex that points to vertices B C D... etc. Remember that this data really means that A is the ID of a department, 
		and B C D ... are the bordering departments.
		Writing up the French department list as an adjacency list is very tedious; feel free to only work on a subset.
	Output Description:
		For each given node (a department), print the unique color identifier after it. A color identifier is unique integer, starting from 0, that represents a unique color. 
		Remember that bordering departments (e.g. adjacent nodes) cannot have the same color index!
'''
import random
DEBUG = True
class District():
	'''
		district class used to encode representations of a set of district and its adjacent neighbors
	'''
	districtId = ''
	neighbors = []
	color = 0
	fitness = 0

	def __init__(self, districtId, neighbors, color):
		self.districtId = str(districtId)
		self.neighbors = neighbors
		self.color = color

	def getNeighbors(self):
		return self.neighbors

	def getId(self):
		return self.districtId

	def getColor(self):
		return self.color

	def setFitness(self, newFitness):
		self.fitness = newFitness

	def getFitness(self):
		return self.fitness

	def __str__(self):
		stringRepresentation = "Id = %s, Color = %s, Neighbors = [%s] " %( self.districtId, str(self.color), ', '.join(map(str, self.neighbors)) )
		return stringRepresentation

def read_adjlist():
	'''
		function used to read in the input and create an adjacency list from it. 
		returns an adjacency list constructed from the inputs
	'''
	# open the input file and make a dictionary of lists, where the keys are the verticies and the lists are the nodes
	f = open('input.txt')
	n = int(f.readline())
	li = [f.readline().split() for _ in range(n)]
	vers = [sl[0] for sl in li]
	return {sl[0]:[v for v in sl[1:] if v in vers] for sl in li}

# dataInput = read_adjlist()

def initialize_population(adjacencyList):
	'''
		generate a random individual answer for population creation
		you must make many of these to seed an initial population

		Returns the initial randomly colored population
	'''
	districts = []
	for item in adjacencyList:
		newList = [{adjacencyList[item][x]:random.randrange(0,7)} for x in range(len(adjacencyList[item]))]
		newObj = District(item, newList, random.randrange(0,7))	
		districts.append(newObj)	

	return districts
	

def fitness_function(individual):
	'''
		fitness function to determine fit of individuals in the population.
		the best individuals don't have the same color as their adjacent districts according to the criteria, 
		and the best solutions have the fewest colors
	'''
	BASEFITNESS = 10
	matches = [individual.getColor() in dist.values() for dist in individual.neighbors]
	numericalMatches = [int(result) for result in matches]
	fitnessReduction = sum(numericalMatches)
	fitness = BASEFITNESS - fitnessReduction

	if DEBUG:
		print ("\n**** FITNESS FUNCTION ****")
		print ("individual: ")
		print (individual)
		print ("color: ")
		print (individual.color)
		print ("neighbor colors: ")
		for dist in individual.neighbors:
			print (dist.values())
		print ("matches: ")
		print (matches)
		print ("numerical representation of the matches: ")
		print (numericalMatches)
		print ("total reduction in fitness: ")
		print (fitnessReduction)
		print ("new fitness score: ")
		print (fitness)
		print ("**** END FITNESS FUNCTION ****\n")

def crossover():
	'''
		crossover method for population
		use 1 point crossover
		Parameters
			takes in two fit individuals
		Returns	
			a hybrid individual
	'''
	pass

def mutation():
	'''
		mutation method for population
		use random mutation
		Parameters
			takes in an individual
		Returns
			an individual who has a random amount of colors mutated randomly
	'''
	pass

def run_experiment():
	'''
		run genetic algorithm
	'''
	N = 10
	adjacencyList = read_adjlist()
	population = []
	for i in range(N):
		# generate initial population of 100 randomly colored individuals
		population.append(initialize_population(adjacencyList))
	
	if DEBUG:
		# a population consists of N individuals 
		# each individual will have 8 adjacency lists inside of it, (one for each district)
		# each adjacency list will have its own fitness due to color matching
		# each individual will have a fitness based on number of colors used
		for individual in population:
			print (individual)

		# fitness_function(population[0][0])

	# generations 
	n = 100
	# crossover rate
	crossoverRate = .5
	# mutation rate 
	mutationRate = .5

	# iterate through n generations, doing the following:
	for x in range(n):
		# evaluate the fitness of every individual in the generation
		# stochastically select the most fit individuals from the generation
		# recombine two fit individual to produce an offspring
		# mutate some of these offspring randomly
		# repeat
		pass

run_experiment()