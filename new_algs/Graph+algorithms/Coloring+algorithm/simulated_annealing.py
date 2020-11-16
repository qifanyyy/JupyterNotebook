# -*-coding:Utf-8 -*

import random
import math

class SimulatedAnnealing(object):
    
    def __init__(self, system, fitnessFunct, showInfo = lambda a,b: 0, temperature = 5, coolSpeed = 0.000002, modificationRate = 0.1, limitTemp = 0, power = 1.8):
        super(SimulatedAnnealing, self).__init__()

        self.showInfo = showInfo
        
        self.coolSpeed = float(coolSpeed)
        self.power = float(power)
        self.temperature = float(temperature)
        self.limitTemp = limitTemp
        self.modificationRate = modificationRate
        self.criterions = fitnessFunct
        self.metal = system
        
        self.solution = self.simulated_annealing_algorithm()
        
    def randomize_solution (self, lenSolution):
        nbrAtoms = lenSolution
        solution = [0]*lenSolution
        for i in range(nbrAtoms):
            solution[i] = random.randint(self.metal[i][0], self.metal[i][1])
        return solution

    def change_solution(self, solution):
        nbrAtoms = int(len(solution)*self.modificationRate)
        proposition = solution[:]
        
        randPos = random.sample(range(len(solution)), nbrAtoms)
        
        for pos in randPos:
            proposition[pos] = ((((solution[pos] - self.metal[pos][0]) 
                                        + random.randint(1, self.metal[pos][1]))
                                        % (self.metal[pos][1] + 1))
                                        + self.metal[pos][0])
            
        return proposition

    #Fitness function must be a 'less is better' evaluation 
    def assess_scores (self, solution):
        result = 0
        for fitness in self.criterions:
            result += fitness(solution)
        return result

    def simulated_annealing_algorithm(self):
        firstTemp = self.temperature
        currentSolution = self.randomize_solution(len(self.metal))
        currentScore = self.assess_scores(currentSolution)
        bestSolution = currentSolution[:]
        bestScore = currentScore
        x = 0.00
        
        while firstTemp > self.limitTemp:
            newSolution = self.change_solution(currentSolution)
            newScore = self.assess_scores(newSolution)
            prob = math.exp((-(newScore-currentScore))/self.temperature)
            
            info = []
            for fitness in self.criterions:
                info.append(fitness(bestSolution))
            self.showInfo(bestSolution, info)
           
            if newScore < currentScore or random.random() < prob:    
                currentSolution = newSolution
                currentScore = newScore
            
                if currentScore < bestScore:
                    bestSolution = currentSolution[:]
                    bestScore = currentScore
            else:
                currentSolution = bestSolution[:]
                currentScore = bestScore
            
            firstTemp = (self.temperature-(math.pow(x, self.power)*self.coolSpeed))
            x+=1
            
        return bestSolution