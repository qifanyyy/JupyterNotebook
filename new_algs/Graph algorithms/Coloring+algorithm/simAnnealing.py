import numpy as np
import time
from random import random, randint, choice
from readFiles import readFile
# ABSOLUTE PATH TO INSTANCES
games120 = "../games120.col.txt"
myciel6 = "/myciel6.col.txt"
anna = "../anna.col.txt"

# MAIN PROGRAM


def colorGraph(file):
    # Define starting parameters
    file = file
    numColors = 15
    temperature = 10.0
    minTemperature = 0.001
    alpha = 0.9
    steps = 100
    cost = 0
    # Best results found
    bestSolution = []
    # Count time used to process
    start = time.time()
    # While the algorithm can reach a cost of zero
    # decreases the number of colors
    while(cost == 0):
        solution, cost = anneal(
            file, numColors, temperature, minTemperature, alpha, steps)
        if(cost == 0):
            numColors -= 1
            bestSolution = solution
    elapsed = (time.time() - start)
    print("FINAL-> " + "Solution: " + str(bestSolution) + " / " + " Colors: " +
          str(numColors) + " / " + " Time Elapsed: " + str(elapsed) + "seconds")


# ANNEALING ALGORITHM
def anneal(file, numColors, temperature, minTemperature, alpha, steps):
    adjMatrix, numVertices = readFile(file)
    numColors = numColors
    numColors -= 1
    temperature = temperature
    minTemperature = minTemperature
    alpha = alpha
    steps = steps
    solution = generateSolution(numVertices, numColors)
    cost, startNeighbour = checkCost(adjMatrix, solution)
    while temperature > minTemperature and cost != 0:
        i = 1
        while i <= steps:
            newSolution = genNeighbour(
                solution, numColors, startNeighbour)
            newCost, startNeighbour = checkCost(
                adjMatrix, solution)
            accept = acceptance(cost, newCost, temperature)
            if accept > random():
                solution = newSolution
                cost = newCost
            i += 1
            print("Solution: " + str(solution) + " / " + " Colors: "
                  + str(numColors + 1) + " / " + " Temp: " + str(temperature) + " / " + " Cost: " + str(cost))
        temperature = temperature*alpha
    numColors += 1
    return solution, cost

# Generate Acceptance Probability based on the function:
#  Acceptance = e*(-(newCost - oldCost) / Temperature)


def acceptance(oldCost, newCost, temperature):
    if newCost < oldCost:
        return 1
    else:
        accept = np.exp(- (newCost - oldCost) / temperature)
        return accept

# Calculates cost of the the solution based on the number of collisions
# and which collision to process


def checkCost(adjMatrix, solution):
    cost = 0
    collisionList = []
    neighbourIndex = -1
    for i in range(len(adjMatrix)):
        for j in range(len(adjMatrix[i])):
            if(i != j and adjMatrix[i][j] == 1 and solution[i] == solution[j]):
                cost += 1
                collisionList.append(i)
    if(neighbourIndex == -1):
        prob = randint(1, 2)
        # Chooses a random collision to treat with 50% of chance
        if(prob % 2 == 0 and len(collisionList) != 0):
            neighbourIndex = choice(collisionList)
        elif(1 < i < (len(adjMatrix)-1)):
            ap = randint(1, 3)
            # Or chooses a random neighbour to a collision to treat
            if(ap % 3 == 0):
                neighbourIndex = choice(collisionList)
                neighbourIndex = neighbourIndex + prob
            elif(ap % 3 == 2):
                neighbourIndex = choice(collisionList)
                neighbourIndex = neighbourIndex - prob
            else:
                neighbourIndex = choice(len(solution))
    return cost, neighbourIndex

# Fill the solution array with random colors


def generateSolution(numVertices, numColors):
    solution = np.arange(numVertices)
    for i in range(numVertices):
        solution[i] = randint(0, numColors)
    return solution

# Generate a new neighbour solution


def genNeighbour(solution, numColors, startNeighbour):
    oldColor = solution[startNeighbour]
    newColor = randint(0, numColors)
    while (oldColor == newColor):
        newColor = randint(0, numColors)
    solution[startNeighbour] = newColor
    return solution


# Execute Program

colorGraph(myciel6)
