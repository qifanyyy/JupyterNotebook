# -*-coding:Utf-8 -*

'''
Created on Dec 14, 2012
'''
import math
import random

class GeneticAlgorithm(object):
	'''
	Class that take a hydraulic network and try to build
	the merely best solution.
	'''
	def __init__(self, speciesCharac, fitnessFunct, showInfo = lambda a,c: 0, nbrOfGenerations = 1000, populationSize = 40, tournamentSize = 2, selectionRate = 0.50, crossoverProb = 0.50, mutationProba = 0.01, elitisme = 0.025):
		self.speciesCharac = speciesCharac
		self.characteristicLength = len(speciesCharac)
		self.population = [self.generate_random_indiv()for i in range(populationSize)]
		self.fitnessFunct = fitnessFunct
		self.elitisme = elitisme
		self.selectionRate = selectionRate
		self.popSize = populationSize
		self.nbrOfGenerations = nbrOfGenerations
		self.mutationProba = mutationProba
		self.crossoverProb = crossoverProb
		self.tournamentSize = tournamentSize
		self.showInfo = showInfo
		self.generationNbr = 1
		
		self.solution = self.genetic_process()
		
	def generate_random_indiv(self):
		chromosome = [random.randint(self.speciesCharac[i][0], self.speciesCharac[i][1]) for i in range(self.characteristicLength)]
		return chromosome
	
	#The top solution are added to the next generation ("not dead yet ones, because the best for the moment") 
	def elitism(self, rankedPop):
		elitePop = int(self.popSize*self.elitisme)
		return rankedPop[0:elitePop]
	
	#Returning two children per crossover
	#Multi-point crossover, the number depending on the length of the chromosome and the rate wanted
	#Uniform crossover, each allele have a chance to be switch
	#Uniform crossover or multi-point crosover ?
	def crossover(self, indiv1, indiv2):
		child1 = indiv1[:]
		child2 = indiv2[:]

		#Multi-Point Crossover
#		nbrPoints = int(self.characteristicLength*self.crossoverProb)
#		points = random.sample(range(self.characteristicLength)[1:self.characteristicLength-2], nbrPoints)
#		points.append(0)
#		points.append(self.characteristicLength)
#		points.sort()
#		points = [(i1, i2, i3) for (i1, i2, i3) in zip(points[:(len(points)-2):2], points[1:(len(points)-1):2],points[2::2])]
#		for i1, i2, i3 in points:
#			child1[i1:i3] = indiv1[i1:i2]+indiv2[i2:i3]
#			child2[i1:i3] = indiv2[i1:i2]+indiv1[i2:i3]
		
		#Uniform Crossover
		for i in range(self.characteristicLength):
			if self.crossoverProb < random.random():
				child1[i] = indiv2[i]
				child2[i] = indiv1[i]
		
		return [child1, child2]
	
	#Bit-flip Mutation, each allele has the same probability to flip 
	def mutate(self, indiv):
		subject = indiv[:]
		for allelePos in range(len(subject)):
			if random.random() < self.mutationProba:
				subject[allelePos] = ((((indiv[allelePos] - self.speciesCharac[allelePos][0]) 
										+ random.randint(1, self.speciesCharac[allelePos][1]))
										% (self.speciesCharac[allelePos][1] + 1))
										+ self.speciesCharac[allelePos][0])
		return subject

	#Fitness function must be a 'less is better' evaluation 
	def assess_fitness (self, indiv):
		result = 0
		for fitness in self.fitnessFunct:
			result += fitness(indiv)
		return result
	
	def selection (self, rankedPop):
		#Tournament Selection
		selectionPopSize = int(self.popSize*self.selectionRate)
		best = random.randint(0, selectionPopSize)
		
		for i in range(self.tournamentSize-1):
			adv = random.randint(0, selectionPopSize)
			if adv < best:
				best = adv
		return rankedPop[best]
			
	def genetic_process(self):
		for i in range(self.nbrOfGenerations):
			scores = [(self.assess_fitness(indiv), indiv) for indiv in self.population]
			scores.sort()
			ranked = [indiv[1] for indiv in scores]
			
			if i%1 == 0:
				info=[]
				for fitness in self.fitnessFunct:
					info.append(fitness(ranked[0]))
				self.showInfo(ranked[0], info)
				
			self.population = self.elitism(ranked)
			
			while len(self.population) < self.popSize:
				dad = self.selection(ranked)
				mom = self.selection(ranked)
				child1, child2 = self.crossover(dad, mom)
				self.population.append(self.mutate(child1))
				self.population.append(self.mutate(child2))
			
			if len(self.population)%2 != self.popSize%2:
				self.population.pop()
			self.generationNbr+=1
			
			#Si tout les individus sont les même -> stop
			if self.population.count(self.population[0]) == self.popSize:
				break	
		
		scores = [(self.assess_fitness(indiv), indiv) for indiv in self.population]
		scores.sort()
		self.population = [indiv[1] for indiv in scores]
		return self.population[0]


class GeneticAlgorithmVariation(GeneticAlgorithm):
	
	def __init__(self, speciesCharac, fitnessFunct, showInfo = lambda a,b: 0, nbrOfGenerations = 100, populationSize = 40, tournamentSize = 2, selectionRate = 0.50, crossoverProb = 0.50, elitisme = 0.125, mutationVariation = 510000, mutationStart = 0.05, power = 2.2):
		self.mutationVariation = mutationVariation
		self.mutationStart = mutationStart
		self.power = power
		GeneticAlgorithm.__init__(self, speciesCharac, fitnessFunct, showInfo, nbrOfGenerations, populationSize, tournamentSize, selectionRate, crossoverProb, 0.1, elitisme)
	
	#Variation of the mutation rate in the time.
	#Each allele has the same probability to be flip but this probability change with the time.
	def mutate(self, indiv):
		subject = indiv[:]
		self.mutationProba = (self.mutationStart-(math.pow(self.generationNbr, self.power)/self.mutationVariation))
		for allelePos in range(len(subject)):
			if random.random() < self.mutationProba:
				subject[allelePos] = ((((indiv[allelePos] - self.speciesCharac[allelePos][0]) 
										+ random.randint(1, self.speciesCharac[allelePos][1]))
										% (self.speciesCharac[allelePos][1] + 1))
										+ self.speciesCharac[allelePos][0])
		return subject