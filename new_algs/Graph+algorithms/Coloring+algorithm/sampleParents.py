import numpy as np
from colors import *
from graphs import *
from geneticAlgorithm import NUM_INDIVIDUALS
import pdb

def getPrefixSums(lst):
    prefixSums = np.zeros((lst.shape))
    currSum = 0

    for i in range(lst.shape[0]):
        currSum += lst[i]
        prefixSums[i] = currSum
    totalSum = currSum

    return prefixSums, totalSum

def singleSample(prefixSums, totalSum):
    u = np.random.uniform(0, 1)
    target = u * totalSum

    low, high = 0, prefixSums.shape[0]
    while low < high:
        mid = low + (high - low) // 2
        if target > prefixSums[mid]:
            low = mid + 1
        else:
            high = mid

    return low

def sampleBestParents(fitnesses):
    fitnesses = np.array(fitnesses)
    prefixSums, totalSum = getPrefixSums(fitnesses)

    samples = []
    for _ in range(NUM_INDIVIDUALS):
        parent1 = singleSample(prefixSums, totalSum)
        parent2 = singleSample(prefixSums, totalSum)
        while parent2 == parent1:
            parent2 = singleSample(prefixSums, totalSum)

        samples.append( (parent1, parent2) )

    return samples
