import cancerModel as cm
import pandas
import random
import numpy as np
import math
import gc
import copy



class SimAnnealing:

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

    # randomly select k features out of n choices to be the starting features
    # return an array of selected features with 1 representing selected features 0 for non-selected
    def randomStart(self, n=None, k=None):
        if not n:
            n = self.size
        if not k:
            k = self.limit

        featureSet = np.zeros(n)
        featureSet[:k] = 1
        np.random.shuffle(featureSet)
        return featureSet

    # uniformly randomly return an integer 0 to k-1
    def randomFlip(self, k):
        ind = random.randint(0, k-1)
        return ind


    # main search algorithm
    def startSearch(self):
        data = self.data
        size = self.size
        currentTemp = self.t0
        endTemp = self.t1
        alpha = self.alpha

        shortCancerData = data
        currentScore = 0
        featureSetIndex = self.randomStart()
        bestSolScore = currentScore
        bestSolSet = featureSetIndex[:]

        featureSize = len(featureSetIndex)

        # set termination conditions
        maxCounter = math.pow(2, size)
        counter = 0
        iterSize = 100
        print ("Started Simulated Annealing with data size: %d,  t: %.2f and limit: %d ... " % (size, currentTemp, self.limit))

        while counter < maxCounter and currentTemp > endTemp:
            for ind in range(iterSize):
                # select the index of a random feature to include or exclude
                k = self.randomFlip(featureSize)
                featureSetIndex[k] = (featureSetIndex[k] != 1)

                # if the result makes the set contain zero features, pick again
                while sum(featureSetIndex) == 0:
                    featureSetIndex[k] = (featureSetIndex[k] != 1)
                    k = self.randomFlip(featureSize)
                    featureSetIndex[k] = (featureSetIndex[k] != 1)

                # use the indice to construct the model and run evaluation function
                features = [0]
                for i, obj in enumerate(featureSetIndex):
                    if obj:
                        features.append(i + 1)
                newSCD = shortCancerData.iloc[:, features]
                score = float(cm.LogesticRegression(newSCD))

                # OPTIONAL: record down the best result set. This is not part of the SA algorithm.
                if score > bestSolScore:
                    bestSolScore = score
                    bestSolSet = copy.deepcopy(featureSetIndex)

                # Perform score evaluation according to the current T
                if score > currentScore:
                    currentScore = score
                else:
                    x = random.random()
                    acceptanceX = math.exp((currentScore-score)/currentTemp)
                    if x < acceptanceX:
                        currentScore = score
                    else:
                        featureSetIndex[k] = (featureSetIndex[k] != 1)

            currentTemp = currentTemp*alpha
            iterSize = int(math.ceil(iterSize / alpha))


            if not self.silent:
                print ("Calculation round %.6f complete. CBA: %.6f; CA %.6f" % (currentTemp, bestSolScore, currentScore))
                shortFeaturesName = list(shortCancerData.columns.values)
                selectedFeaturesName = []
                for ind, obj in enumerate(bestSolSet):
                    if obj:
                        selectedFeaturesName.append(shortFeaturesName[ind + 1])
                print ("Features Selected: ",)
                print (selectedFeaturesName)

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

        self.result = [("Current", selectedFeaturesName, currentScore), ("Best", bestFeatureName, bestSolScore)]
        return self.result
