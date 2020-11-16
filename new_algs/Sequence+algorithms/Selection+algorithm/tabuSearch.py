import cancerModel as cm
import pandas
import numpy as np
import math
import gc
import copy



class TabuSearch:

    def __init__(self, data, size=None, t=None, limit=None, silent=True):
        self.data = data    # data to be analyzed with column 0 being the predictor column
        self.size = size    # the total number of features to be selected
        self.t = t          # taboo variable t, denoting how many turns with an action be forbidden
        self.limit = limit  # limits the maximum amount of features to be selected (thus limiting search space)
        self.result = None
        self.silent = silent
        if not size:        # Default size: number of columns in the dataframe without the predictor column
            self.size = len(data.columns) - 1
        if not t:           # Default t: the square root of the size
            self.t = math.ceil(math.sqrt(self.size))
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

    def startSearch(self):
        data = self.data
        size = self.size
        t = self.t
        limit = self.limit

        shortCancerData = data
        shortTermMemory = np.zeros(size)
        longTermMemory = 0
        featureSetIndex = self.randomStart()
        bestSol = []

        # set termination conditions
        ret = False
        maxCounter = math.pow(2, size)
        counter = 0
        featureRes = None
        featureIndex = None

        print ("Started Tabu Search with data size: %d,  t: %d and limit: %d ... " % (size, t, limit if limit else -1))

        while not ret and counter < maxCounter:
            allResults = []
            for ind, obj in enumerate(featureSetIndex):
                nFeatureSetIndex = copy.deepcopy(featureSetIndex)
                nFeatureSetIndex[ind] = (obj != 1)
                if sum(nFeatureSetIndex) != 0 and (sum(nFeatureSetIndex) < limit if limit else True):
                    features = [0]
                    for i, obj1 in enumerate(nFeatureSetIndex):
                        if obj1:
                            features.append(i + 1)

                    newSCD = shortCancerData.iloc[:, features]
                    result = cm.LogesticRegression(newSCD)
                    allResults.append((result, ind))

            allResults.sort(reverse=True)
            for index, var in enumerate(allResults):
                featureRes = var[0]
                featureIndex = var[1]
                if shortTermMemory[featureIndex] == 0:
                    featureSetIndex[featureIndex] = (featureSetIndex[featureIndex] != 1)
                    shortTermMemory[:] = [x - 1 if x != 0 else x for x in shortTermMemory]
                    shortTermMemory[featureIndex] = t
                    longTermMemory = featureRes if featureRes > longTermMemory else longTermMemory
                    bestSol = featureSetIndex if featureRes > longTermMemory else featureSetIndex
                    ret = False
                    break
                elif featureRes >= longTermMemory:
                    featureSetIndex[featureIndex] = (featureSetIndex[featureIndex] != 1)
                    shortTermMemory[:] = [x - 1 if x != 0 else x for x in shortTermMemory]
                    shortTermMemory[featureIndex] = t
                    bestSol = featureSetIndex
                    ret = False
                elif index == (len(featureSetIndex) - 1):
                    ret = True
            if not self.silent:
                print ("Calculation round %d complete. CBA: %s; CA %s" % (counter, longTermMemory, featureRes if featureRes else "NaN"))
                shortFeaturesName = list(shortCancerData.columns.values)
                selectedFeaturesName = []
                for ind, obj in enumerate(featureSetIndex):
                    if obj:
                        selectedFeaturesName.append(shortFeaturesName[ind + 1])
                print (selectedFeaturesName)

            gc.collect()
            counter += 1

        shortFeaturesName = list(shortCancerData.columns.values)
        selectedFeaturesName = []
        for ind, obj in enumerate(featureSetIndex):
            if obj:
                selectedFeaturesName.append(shortFeaturesName[ind + 1])

        self.result = (selectedFeaturesName, longTermMemory)
        return result
