"""
A Machine Learning Framework for Stock Selection
    
Authors:
XingYu Fu; JinHong Du; YiFeng Guo; MingWen Liu; Tao Dong; XiuWen Duan; 

Institutions:
AI&Fintech Lab of Likelihood Technology; 
Gradient Trading;
School of Mathematics, Sun Yat-sen University;

Contact:
fuxy28@mail2.sysu.edu.cn

All Rights Reserved.
"""


"""Import Libraries"""
import numpy as np
from evaluation import EvaluationClass


class GA:
    def __init__(self,  X_train, Y_train, X_test, Y_test, model_type, save_computaion):
        
        self.X_train = X_train
        self.Y_train = Y_train
        self.X_test = X_test
        self.Y_test = Y_test
        self.model_type = model_type
        self.save_computaion = save_computaion
        
        self.num_features = np.shape(X_train)[1]
        self.populationSize = 100
        
        self.crossoverProb = 0.2
        self.mutationProb = 0.1
 
        self.warmupNum = 1
        self.iteration = 10
    
    def IntialPopulation(self): 
        for i in range(self.warmupNum):
            chromosomes = np.random.randint(0, 2, (self.populationSize, self.num_features))
            chromosomes[np.sum(chromosomes, axis=1)<50, :] =  1 - chromosomes[np.sum(chromosomes, axis=1)<50, :]
            if i>0:
                _, _, fitness1 = self.Fitness(self.population)
                _, _, fitness2 = self.Fitness(chromosomes)
                print( fitness1<fitness2 )
                self.population[fitness1<fitness2,:] = chromosomes[fitness1<fitness2,:]
            else:
                self.population = chromosomes 
        prob, _, _ = self.Fitness(self.population)
        self.bestFitnessList.append(np.max(prob))
        self.bestSolutionsList.append(self.population[np.argmax(prob),:])        
    
    def CheckChromosome(self, chromosome):
        if np.sum(chromosome)>=2:
            return True
        else:
            return False

    def Crossover(self, population):  
        is_crossover = 1-np.random.binomial(1, self.crossoverProb, self.populationSize//2)
        for i in np.where(is_crossover)[0]:
            while True:
                chromosome1 = np.copy(population[2*i,:])
                chromosome2 = np.copy(population[2*i+1,:])
                where_crossover = np.random.randint(0, self.num_features, 1)
                chromosome1[where_crossover] = np.copy(self.population[2*i+1,where_crossover])
                chromosome2[where_crossover] = np.copy(self.population[2*i,where_crossover])                
                if self.CheckChromosome(chromosome1) and self.CheckChromosome(chromosome2):
                    population[[2*i,2*i+1],:] = np.array([chromosome1, chromosome2])
                    break
        return population          
        
    def Mutation(self, population):  
        is_mutate = 1-np.random.binomial(1, self.mutationProb, self.populationSize)
        for i in np.where(is_mutate)[0]:
            while True:
                chromosome = np.copy(population[i,:])
                where_mutate = np.random.randint(0, self.num_features, 1)
                chromosome[where_mutate] = 1 - chromosome[where_mutate]
                if self.CheckChromosome(chromosome):
                    population[i,:] = chromosome
                    break
        return population
    
    def Fitness(self, population):  
        fitness = np.zeros(self.populationSize)
        for i in range(self.populationSize):
            X_train_masked = self.X_train[:,population[i,:]==1]
            X_test_masked = self.X_test[:,population[i,:]==1]
            eva = EvaluationClass( X_train_masked, self.Y_train, X_test_masked, self.Y_test, self.model_type, self.save_computaion)
            fitness[i] = eva.evalu_sta()
        
        prob = fitness / np.sum(fitness)  
        cum_prob = np.cumsum(prob)     
        return prob, cum_prob, fitness        

    def Select(self, cum_fitness):  
        newpopulation = np.zeros_like(self.population)
        randoms = np.random.rand(self.populationSize)  
        for i, randoma in enumerate(randoms):  
            index = np.where(cum_fitness >= randoma)  
            newpopulation[i, :] = self.population[index[0][0], :] 

        return newpopulation  
    
    def Search(self):
        self.bestFitnessList = []  
        self.bestSolutionsList = []  
        self.IntialPopulation() 
        _, cum_fitness, _ = self.Fitness(self.population)  

        for iteration in range(self.iteration):  
            print(str(iteration+1)+"th Iteration of GA.")
            population = self.Select(cum_fitness)  
            crossoverPopulation = self.Crossover(population)  
            newPopulation = self.Mutation(crossoverPopulation)  

            prob, cum_fitness, fitness = self.Fitness(newPopulation)
            
            self.bestFitnessList.append(np.max(prob))
            self.bestSolutionsList.append(newPopulation[np.argmax(prob), :])  

        self.bestFitness = np.max(self.bestFitnessList)  
        self.bestSolutions = self.bestSolutionsList[np.argmax(self.bestFitnessList)]
