import cancerModel as cm
import pandas
import random
import numpy as np
import math
import gc
import copy
import ACO.ACO as aco




class SaWAco:

    def __init__(self, data, size=None, alpha=None, t0=None, t1=None, limit=None, silent=True):
        self.data = data    # data to be analyzed with column 0 being the predictor column
        self.size = size    # the total number of features to be selected
        self.alpha = alpha  # the damping factor
        self.t0 = t0        # initial temperature of the SA
        self.t1 = t1        # termination temperature
        self.result = None
        self.limit = limit
        self.silent = silent
        if not self.alpha:
            self.alpha = 0.85
        if not self.t0:
            self.t0 = 0.2
        if not self.t1:
            self.t1 = self.t0/100
        if not size:        # Default size: number of columns in the dataframe without the predictor column
            self.size = len(data.columns) - 1
        if not limit:
            self.limit = self.size


    def randomPheromone(self, q, stepSize=0.1):
        return q * (1-stepSize + random.random()*stepSize*2)

    def runHeuristic(self, type, paramTuned):
        if not type:
            return None;
        if type == "ACO":
            if not paramTuned:
                paramTuned = 0.1
            Q = paramTuned
            acoModel = aco.ACO(self.data, maxIteration=20, antNumber=50, cc=1, Q=Q, e=0.95)
            score, featureSet, quality = acoModel.run()
            return score, featureSet, quality


    # main search algorithm
    def startSearch(self):
        data = self.data
        size = self.size
        currentTemp = self.t0
        endTemp = self.t1
        alpha = self.alpha

        shortCancerData = data
        currentScore = 0
        featureSetIndex = []
        bestSolScore = currentScore
        bestSolSet = []
        Q = 0.15


        # set termination conditions
        maxCounter = math.pow(2, size)
        counter = 0
        iterSize = 1
        print "Started Simulated Annealing with data size: %d,  t: %.2f and limit: %d ... " % (size, currentTemp, self.limit)

        while counter < maxCounter and currentTemp > endTemp:
            for ind in range(iterSize):
                oldPheromone = Q
                # generate a new pheromone that each ant may carry
                Q = self.randomPheromone(Q, stepSize=currentTemp*2)
                # get the score of such specify of ant colony
                score, featureSetIndex, colonyQuality = self.runHeuristic(type="ACO", paramTuned=Q)


                # OPTIONAL: record down the best result set. This is not part of the SA algorithm.
                if score > bestSolScore:
                    bestSolScore = score
                    bestSolSet = copy.deepcopy(featureSetIndex)

                # Perform score evaluation according to the current T
                if colonyQuality > currentScore:
                    currentScore = colonyQuality
                else:
                    x = random.random()
                    acceptanceX = math.exp((currentScore-colonyQuality)/currentTemp)
                    if x < acceptanceX:
                        currentScore = colonyQuality
                    else:
                        Q = oldPheromone

            currentTemp = currentTemp*alpha
            #iterSize = int(math.ceil(iterSize / alpha))


            if not self.silent:
                print "Calculation round %.6f complete. CBA: %.6f; CQ %.6f" % (currentTemp, bestSolScore, currentScore)
                print "Current Pheromone level %.6f" % oldPheromone
                # shortFeaturesName = list(shortCancerData.columns.values)
                # selectedFeaturesName = []
                # for ind, obj in enumerate(bestSolSet):
                #     if obj:
                #         selectedFeaturesName.append(shortFeaturesName[ind + 1])
                # print "Features Selected: ",
                # print selectedFeaturesName

            gc.collect()
            counter += 1

        # this is the result of the SA algorithm (local optimum)
        shortFeaturesName = list(shortCancerData.columns.values)
        selectedFeaturesName = []
        for ind, obj in enumerate(featureSetIndex):
            if obj:
                selectedFeaturesName.append(shortFeaturesName[ind + 1])

        # this is the result of the tracking maximum (possible global optimum)
        bestFeatureName = []
        for ind, obj in enumerate(bestSolSet):
            if obj:
                bestFeatureName.append(shortFeaturesName[ind + 1])

        self.result = [bestSolScore, bestFeatureName]
        return self.result
