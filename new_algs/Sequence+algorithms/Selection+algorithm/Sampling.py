'''
Helper class for Greedy Sampling 
Author: Tushar Makkar <tusharmakkar08[at]gmail.com>
Date: 5.02.2015
'''

import datareader, mushrooms_bfgs, mlpy, nltk, PGCM, operator

def GreedySampling (PGCM_matrix, numberOfFeatures, Aggregation):
    '''
    Returns the Sampled Matrix with the Aggregation Function used
    Args:
        PGCM_Matrix : Input PGCM Matrix
        numberOfFeatures : total number of features
        Aggregation : Aggregation used for sampling eg : min, max, avg
    Returns:
        The Sampled matrix
    '''
    X = {}
    Y = {}
    score = {}
    for i in xrange(1, numberOfFeatures + 1): 
        if Aggregation == "min":
            score [i] = 100
        else :
            score[i] = 0 
    for i in xrange(1, numberOfFeatures + 1): 
        #~ X[i] = oldPGCM[(i,i)]
        for j in xrange(i + 1, numberOfFeatures+1):
            #~ Y[(i,j)] = PGCM_matrix[(i,j)]
            if Aggregation == "min":
                score[i] = min(score[i], PGCM_matrix[(i,j)])
                score[j] = min(score[j], PGCM_matrix[(i,j)])
            if Aggregation == "max":
                score[i] = max(score[i], PGCM_matrix[(i,j)])
                score[j] = max(score[j], PGCM_matrix[(i,j)])
            if Aggregation == "avg":
                score[i] = score[i] + PGCM_matrix[(i,j)]
                score[j] = score[j] + PGCM_matrix[(i,j)]
    for i in xrange(1, numberOfFeatures + 1): 
        if Aggregation == "avg":
            score[i] = score[i] / ((numberOfFeatures - 1)*100.00)
        else:
            score[i] = score[i] / 100.00
    return score
    
def test_initialize():
    #~ (train_X, train_y, test_X, test_y) = mushrooms_bfgs.initialize(float(99)/100)
    #~ print "Number of Training Data =",len(train_y)
    #~ print "Number of Testing Data =",len(test_y)
    #~ PGCM_0 = PGCM.makePairs(train_X, train_y, test_X, test_y)
    fileread = open("PGCM_0",'r').read()
    PGCM_0 = eval(fileread)
    #~ print PGCM_0
    #~ oldPGCM = PGCM_0
    N = 22
    #~ GreedySampling(PGCM_0, oldPGCM, N, "avg")
    featureImportanceDictionary = GreedySampling(PGCM_0, N, "max")
    sortedFeatureDictionary = sorted(featureImportanceDictionary.items(), key=operator.itemgetter(1))
    return sortedFeatureDictionary
    #~ print len(sortedFeatureDictionary)
    
if __name__ == "__main__":
    print (test_initialize())

