import random
import numpy as np
from datetime import datetime
from state import *
from math import exp, log

class Simulation():

    n = 0                       # total of available items
    w = []                      # list with item weights
    v = []                      # list with item values
    maxWeight = 0               # maximum weight supported by the knapsack
    bestSolution = None         # State of the best solution found so far
    currentSolution = None      # State of the current algorithm solution (except Hill Climbing)
    initialSolution = None      # State of the initial solution generated on object constructor
    optimum = 0                 # value of the optimal solution for the instance
    transitionProb = {}         # dictionary with uniform transition probability coming out of the key state
    executions = 1              # number of iterations for the algorithms (except Simulated Annealing)

    def __init__(self, file, executions = 1):
        random.seed(datetime.now())
        self.executions = executions
        self.n = 0
        self.w = []
        self.v = []
        self.initialSolution = None
        self.currentSolution = None
        self.transitionProb = None
        self.transitionProb = {}
        with open(file) as f:
            self.n = int(f.readline().split()[1])
            self.maxWeight = int(f.readline().split()[1])
            self.optimum = int(f.readline().split()[1])
            f.readline()
            self.initialSolution = State()
            self.currentSolution = State()
            for line in f:
                _, lineV, lineW, _ = list(map(int, line.split(',')))
                self.v.append(lineV)
                self.w.append(lineW)
                if random.random() < 0.5 and self.isValidStateWith(lineW):
                    self.currentSolution.items.append(1)
                    self.currentSolution.v += lineV
                    self.currentSolution.w += lineW
                else:
                    self.currentSolution.items.append(0)
        self.initialSolution = self.currentSolution.copy()

    def restartInstance(self):
        self.currentSolution = self.initialSolution.copy()
        self.bestSolution = self.initialSolution.copy()

    def isValidStateWith(self, w, state = State()):
        if len(state.items) == 0:
            state = self.currentSolution
        return state.w + w <= self.maxWeight

    def isBetterSolution(self, solution):
        if (solution.v > self.bestSolution.v) or (solution.v == self.bestSolution.v and solution.w < self.bestSolution.w):
            self.bestSolution = solution.copy()
            return True
        return False

    def allNewStates(self, state = State()):
        if len(state.items) == 0:
            state = self.currentSolution.copy()

        possibleStates = []
        for i in range(self.n):
            new = State()
            new = self.newStateFor(i, state)
            if len(new.items) != 0:
                possibleStates.append(new.copy())
        return possibleStates[:]
    
    def transitionProbFrom(self, state = State()):
        if len(state.items) == 0:
            state = self.currentSolution.copy()
        
        pij = self.transitionProb.setdefault(state, None)
        if pij == None:
            pij = 1 / len(self.allNewStates(state.copy()))
            self.transitionProb[self.currentSolution] = pij
        return pij
    
    def newStateFor(self, i, state = State()):
        if len(state.items) == 0:
            state = self.currentSolution.copy()
        
        state_i = State()
        state_i = state.copy()
        if state_i.items[i] == 0:
            if self.isValidStateWith(self.w[i], state):
                state_i.setIn(i, self.v[i], self.w[i])
                return state_i
        else:
            state_i.setOut(i, self.v[i], self.w[i])
            return state_i
    
        return State()

    def randomWalk(self, p):
        self.restartInstance()

        name = 'Random Walk p = ' + str(p)
        t = 0   # steps
        ret = [self.currentSolution.v]
        while t < self.executions:
            t += 1
            unif = random.random()
            if unif < p:
                possibleStates = self.allNewStates()
                index = random.randint(0, len(possibleStates)-1)
                newState = State()
                newState = possibleStates[index].copy()
                self.currentSolution = newState.copy()
                if self.isBetterSolution(self.currentSolution):
                    if self.bestSolution.v == self.optimum:
                        ret.append(self.bestSolution.v)
                        break
            ret.append(self.bestSolution.v)
        return name, ret

    def accept(self, newState, pij, pji):
        unif = random.random()
        # alfa = (newState.v * math.log(self.currentSolution.w)) / (currentSolution.v * math.log(newState.w))
        alfa = (newState.v * pji) / (self.currentSolution.v * pij)
        if unif < alfa:
            return True
        return False

    def calculeteP(self, states):
        p = []
        p_ii = 1
        currentV = self.currentSolution.v
        for state in states:  
            
            p_ij = min(1, state.v / currentV) / len(states)
            p.append(p_ij)
            p_ii -= p_ij
            if p_ij < 0:
                print(state, len(state.items), self.n)
        p.append(p_ii)
        return p[:]    
    
    def metropolisHasting(self):
        self.restartInstance()
        
        name = 'Metropolis Hasting'
        t = 0   # steps
        ret = [self.currentSolution.v]
        while t < self.executions:
            t += 1
            currentChanged = False
            newState = State()
            while len(newState.items) == 0:
                index = random.randint(0, self.n-1)
                newState = self.newStateFor(index).copy()

            delta = newState.v - self.currentSolution.v
            if delta > 0:
                # accept = 1
                self.currentSolution = newState.copy()
                currentChanged = True
            else:
                pij = self.transitionProbFrom()
                pji = self.transitionProbFrom(newState)
                if self.accept(newState, pij, pji):
                    self.currentSolution = newState.copy()
                    currentChanged = True
            
            if currentChanged and self.isBetterSolution(self.currentSolution):
                if self.bestSolution.v == self.optimum:
                    ret.append(self.bestSolution.v)
                    break
            ret.append(self.bestSolution.v)
        return name, ret

    def hillClimbing(self):
        self.restartInstance()
        
        # bestSolution is always currentSolution
        name = 'Hill Climbing'
        t = 0   # steps
        ret = [self.bestSolution.v]

        while 1:
            t += 1
            newState = State()
            newState = max(self.allNewStates(self.bestSolution))
            if self.isBetterSolution(newState):
                ret.append(self.bestSolution.v)
            else:
                ret.append(self.bestSolution.v)
                break
        return name, ret
    
    def boltzman(self, deltaV, t, pij, pji):
        return exp(deltaV/t) * pji / pij

    def simulatedAnnealing(self, initialT, epsilon, coolingStrategy, beta):
        self.restartInstance()
        
        def format_e(n):
            #format large number in scientific notation
            a = '%E' % n
            return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

        name = 'Simulated Annealing T = ' + str(format_e(initialT)) + ' b = ' + str(beta) + ' ' + coolingStrategy.__name__
        temperature = initialT
        t = 0   # steps
        ret = [self.currentSolution.v]
        while temperature > epsilon:
            t += 1
            currentChanged = False
            newState = State()
            while len(newState.items) == 0:
                index = random.randint(0, self.n-1)
                newState = self.newStateFor(index).copy()
            delta = newState.v-self.currentSolution.v
            if delta > 0:
                # boltzman = 1
                self.currentSolution = newState.copy()
                currentChanged = True
            else:
                pij = self.transitionProbFrom()
                pji = self.transitionProbFrom(newState)
                if random.random() < self.boltzman(delta, temperature, pij, pji):
                    self.currentSolution = newState.copy()
                    currentChanged = True

            if currentChanged and self.isBetterSolution(self.currentSolution):
                if self.bestSolution.v == self.optimum:
                    ret.append(self.bestSolution.v)
                    break
            ret.append(self.bestSolution.v)
            temperature = coolingStrategy(initialT, beta, t, delta)
        return name, ret
        

    def linearCoolingStrategy(self, initialT, beta, t, delta):
        return initialT - beta * t

    def expCoolingStrategy(self, initialT, beta, t, delta):
        return initialT * (beta ** t)

    def dynamicCoolingStrategy(self, initialT, beta, t, delta):
        return initialT - beta * t - (log(abs(delta)) / delta) * t

    def verifyValues(self, solution):
        sum = 0
        for i in range(len(solution.items)):
            if solution.items[i]:
                sum += self.v[i]
        return sum