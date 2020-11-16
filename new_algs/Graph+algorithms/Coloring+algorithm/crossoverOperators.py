import numpy as np
from copy import deepcopy

#@profile
def singlePointCrossover(indiv1, indiv2, numNodes):
	crossedIndividual1 = deepcopy(indiv1)
	crossedIndividual2 = deepcopy(indiv2)
	cut = np.random.randint(1, numNodes-1)
	for i in range(cut,numNodes):
		crossedIndividual1.vertexColors[i], crossedIndividual2.vertexColors[i] = indiv2.vertexColors[i], indiv1.vertexColors[i]
	return crossedIndividual1, crossedIndividual2
	
def newCrossover(indiv1, indiv2, numNodes):
	offspring = deepcopy(indiv1)
	for i in range(numNodes):
		r = np.random.randint(1, 3) # either 1 or 2
		if(r == 2): #offspring is a copy of indiv1, so just to change colors to indiv2 
			offspring.vertexColors[i] = indiv2.vertexColors[i]
	return offspring
