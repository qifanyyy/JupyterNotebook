import random
import math

class Chromosome:
    'Representation of any Cloud Service Provider'

    Count = 0
    MutateProbability = 0.20
    CrossOverProbability = 0.60

    def __init__(self,rankString):
        self.rankString = rankString
        Chromosome.Count += 1

    def displayRankString(self):
        print "My Rank String is " ,self.rankString

    def mutate(self,maxRank):
        start  = 0
        end    = len(self.rankString)
        mutateIndexCount = (int)(Chromosome.MutateProbability * len(self.rankString))
        for i in range(mutateIndexCount):
            index = random.randrange(start,end,1)
            self.rankString[index] = round(random.uniform(0,maxRank),1)

    @staticmethod
    def crossover(chrome1,chrome2):
        if(random.random() < Chromosome.CrossOverProbability):
            start = 0
            end = len(chrome1.rankString)
            crossoverpt = random.randrange(start,end,1)
            offspr1 = chrome1.rankString[:-(end-crossoverpt)] + chrome2.rankString[(crossoverpt):]
            offspr2 = chrome2.rankString[:-(end-crossoverpt)] + chrome1.rankString[(crossoverpt):]
            return [Chromosome(offspr1),Chromosome(offspr2)]
        else:
            return [chrome1,chrome2]

    @staticmethod
    def distance(chrome1,chrome2):
        total = 0
        count = 0
        for i in range(len(chrome1.rankString)):
            count = (chrome1.rankString[i] - chrome2.rankString[i])**2
            total = count+total
        dist = math.sqrt(total)
        return dist

    @staticmethod
    def randomChromosomeString(maxRank,length):
        string = []
        for i in range(length):
            string.append(round(random.uniform(0,maxRank),1))
        return string

    @staticmethod
    def calculateProbability(population,userChromosome):
        totalFitness = 0
        populationLength = len(population)

        for i in range(populationLength):
            population[i].fitness = 1.0 / (Chromosome.distance(population[i],userChromosome)+1)
            totalFitness += population[i].fitness
        for i in range(populationLength):
            population[i].probability = population[i].fitness / totalFitness
        return population

    @staticmethod
    def rouletteSelection(population,userChromosome):

        population = Chromosome.calculateProbability(population,userChromosome)
        populationLength = len(population)
        newPopulation = []
        for i in range(populationLength):
            rand = random.random()
            temp = 0
            for i in range(populationLength):
                temp += population[i].probability
                if(temp > rand):
                    newPopulation.append(population[i])
                    break
        return newPopulation

    @staticmethod
    def getFittestChromosome(population):
        index = 0
        for i in range(len(population)):
            if(population[i].probability > population[index].probability):
                index = i
        return index

    @staticmethod
    def printPopulation(population):
        for i in range(len(population)):
            print "Chromosome",i+1," : ",population[i].rankString