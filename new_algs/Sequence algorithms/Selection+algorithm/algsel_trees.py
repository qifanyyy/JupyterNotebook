# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Python imports
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Standard Python lib
import sys
import os
import re
import math

# Additional includes: argument parsing
import argparse

# Additional includes: Numpy and Scipy
import numpy as np
from   numpy import recfromtxt
import scipy
from   scipy import spatial
import copy

# Additional includes: Matplotlib (only needed for plotting)
import matplotlib
matplotlib.use('Agg')   #  nothing (for X11), Agg (for PNGs), PDF, SVG, or PS
import matplotlib.pyplot as plt
# ------------------------------------------------------------------------------
# END: Python imports
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Argument parsing, default values, and help
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser(prog='algsel_trees')

# common arguments across both modes
parser.add_argument('-v', '--version',      action='version', version='%(prog)s ' + __version__)

parser.add_argument('-p', '--penalty',          type=float, help='timeout penalty for PAR score (default: 5.0)', default=5.0) 
parser.add_argument('-f', '--featureTransform', action='store_true', help='use feature transformation (default: no)', default=False)

parser.add_argument('-o', '--outfile',  type=str, help='name of file to output performance numbers to (default: none)', default='')
parser.add_argument('-g', '--graphics', action='store_true', help='create plots (default: no)', default=False)
parser.add_argument('-m', '--model', type=str, help='model type: [ M-ET | M-RF | S-ET | S-RF ] (default: M-ET)', default='M-ET') 
parser.add_argument('-t', '--target', type=int, help='target type 1:y 2:log10(10+y) 3:log10(y) 4:sqrt(y) 5:PARk (default: 1)', default=1) 
parser.add_argument('-n', '--ntrees', type=int, help='num of trees in trained model (default:400)', default=200) 
parser.add_argument('-a', '--alpha', type=float, help='Hybrid parameter. alpha*M_multi+(1-alpha)*M_single: [0-1] (default:0.5)', default=0.5) 
parser.add_argument('trnFeatures',      type=str, help='training data: features file')
parser.add_argument('trnTimes',         type=str, help='training data: runtimes file')
parser.add_argument('tstFeatures',      type=str, help='test data: features file')
parser.add_argument('tstTimes',         type=str, help='test data: runtimes file')
parser.add_argument('timeout',          type=float, help='timeout for the portfolio')

args = parser.parse_args()

strFileNameTestFeatures     = ''
strFileNameTestTimes        = ''
strFileNameTrainFeatures    = args.trnFeatures
strFileNameTrainTimes       = args.trnTimes
strFileNameTestFeatures     = args.tstFeatures
strFileNameTestTimes        = args.tstTimes
constTimeOut                = args.timeout
strFileNameOutputPerf       = args.outfile
bCreatePlots                = args.graphics
# ------------------------------------------------------------------------------
# END: Argument parsing and help
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Global Constants
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Max values for floats used for feature range (max/min)
constMaxFloat                   =  1e+36
constMinFloat                   = -1e+36
constMaxInt                     =  1e+36
# Min distance to work with
# Penalize a timeout of a solver by this factor
constPAR                        = args.penalty

constDoFeatureTransform         = args.featureTransform

# Counter for the number of test instances processed
nTestInstances          = 0.0

# Counter for number of newly learned instances
# Counter for time outs
nTimeOuts               = 0
# Counter for VBS time outs
nVBSTimeOuts            = 0

# Folder to put generated plots in
strPlotsFolder    = 'plots'

# ------------------------------------------------------------------------------
# END: Global Constants
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Create data structures dictionary and array (not very conceice)
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Makes a dictionary to look up features/times based on filename
# - Input : Record from Text, maximal column to be considered (optional)
# - Output: Dictonary Name -> Data, List of names 
def makeDict(instIds, data_from_file, maxColumn=constMaxInt):
    data_dict = {}
    data_names_list = []
    nCount = 0
    for instId, items in zip(instIds, data_from_file):
        list_only_values = []
        for i in range(0,min(len(items),maxColumn)):
            value = float(items[i])
            value = max(value,constMinFloat)
            value = min(value,constMaxFloat)
            list_only_values.append(value)
        data_dict[instId] = list_only_values
        data_names_list.append(instId)
        nCount += 1

    return data_dict, data_names_list


# Makes an array for features/times (not using a filename)
# - Input : Record from Text, maximal column to be considered (optional)
# - Output: Numpy array (without name=1st column)
def makeArray(instIds, data_from_file, maxColumn=constMaxInt):
    list_values = []
    for instId, items in zip(instIds, data_from_file):
        list_only_values = []
        for i in range(0,min(len(items),maxColumn)):
            value = float(items[i])
            value = max(value,constMinFloat)
            value = min(value,constMaxFloat)
            list_only_values.append(value)
        list_values.append(list_only_values)
    return np.array(list_values)
# ------------------------------------------------------------------------------
# END: Create data structures dictionary and array
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Normalization
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Normalize array to 0..1
# - Input: Numpy array
# - Output: Normalized Numpy array
def normalize(my_array):
    # Create a new 2D array
    array_normalized = np.array(my_array)
    
    # Subtract mean, divide by stddev
    array_normalized -= array_normalized.mean(0)[None,:]
    array_normalized /= (array_normalized.std(0)[None,:] + 0.01)
    
    # Normalize to fit the range [0..1]
    minv = array_normalized.min(axis=0)
    maxv = array_normalized.max(axis=0)
    for col in range(0, my_array.shape[1] ):
        for row in range(0, my_array.shape[0] ):
            if abs(float(maxv[col]) - float(minv[col])) == 0.0:
                f_value = 0.5
            else:
                f_value = (array_normalized[row][col]  - float(minv[col])) / (float(maxv[col]) - float(minv[col])) 
            array_normalized[row][col] = f_value
    
    # Return normalized version of input array
    return array_normalized
# ------------------------------------------------------------------------------
# END: Normalization
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Compute Geometric Mean
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Compute shifted geometric mean given a list of numbers
def computeGeometricMean(numbers, shift=0.0):
    sumlogs = 0.0
    for n in numbers:
        sumlogs += math.log(n + shift) 
    avglogs = sumlogs / len(numbers)
    return (math.exp(avglogs) - shift)

# Compute solver score given runtime information f_value
# ------------------------------------------------------------------------------
# END: Compute Geometric Mean
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# PCA inspired feature reduction and representation
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------        
# Computes features transformed in space based on principal components
# Input:  Numpy array (features)
# Output: Transformed Numpy array (features)
def feature_transformation(array_available_features_normalized):
        # Get eigenvalues/vector of covariance matrix
        [u,v] = np.linalg.eig(numpy.cov(array_available_features_normalized, rowvar=0, bias=1))
        # Remove features with hardly any correlation
        # Sort v in the sorted order of u
        v = v[:, np.argsort(u)[::-1]]
        # Sort u
        u.sort()    
        # Go through eigenvalues and remove 'small' eigenvalues
        nCutOff = 0
        for coefficient in u:
            if coefficient < 0.0001: # This value controls what features will be considered
                nCutOff += 1
        # Cut off features with low values
        v = v[nCutOff:]
        # Use reduced v on original data to obtain changed/reduced data
        array_available_features_normalized = np.dot(array_available_features_normalized, v.T)
        # Return transformed np array
        return array_available_features_normalized
# ------------------------------------------------------------------------------
# END: PCA inspired feature reduction and representation
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Parsing data
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------    
def readfile_data(strFileName):
    f = open(strFileName)
    instIds = []
    data = []
    for l in f.readlines():
        l = l.split(',')
        if len(l) > 0:
            instIds += [l[0]]
            data += [[float(ll) for ll in l[1:]]]
    return instIds, np.array(data)


def parseData(strFileNameTrainFeatures, strFileNameTrainTimes, strFileNameTestFeatures, strFileNameTestTimes):
    print "---------------------------------------------------------------------------------------------"
    print 'Parsing Data'

    print ' -> Reading Train Features :', strFileNameTrainFeatures
    instIds, train_features = readfile_data(strFileNameTrainFeatures)
    train_dict_features, train_list_names_features = makeDict(instIds, train_features)
    train_array_features = train_features

    print ' -> Reading Train Times    :', strFileNameTrainTimes
    instIds, train_times = readfile_data(strFileNameTrainTimes)
    train_dict_times, train_list_names_times = makeDict(instIds, train_times)

    train_array_features_orig = np.array(train_array_features)

    print ' -> Reading Test Features  :', strFileNameTestFeatures
    instIds, test_features = readfile_data(strFileNameTestFeatures)
    test_dict_features, test_list_names_features = makeDict(instIds, test_features)

    print ' -> Reading Test Times     :', strFileNameTestTimes

    instIds, test_times = readfile_data(strFileNameTestTimes)
    test_dict_times, test_list_names_times = makeDict(instIds, test_times)

    nAlgs     = len(train_dict_times[train_list_names_times[0]])
    nFeatures = len(train_dict_features[train_list_names_features[0]])

    print
    print ' Basic Information on Data: '
    print ' --> Number of Algorithms            :', nAlgs
    print ' --> Number of Features              :', nFeatures
    print ' --> Number of Train-Feature-vectors :', len(train_dict_features)
    print ' --> Number of Train-Time-vectors    :', len(train_dict_times)
    print ' --> Number of Test-Feature-vectors  :', len(test_dict_features)
    print ' --> Number of Test-Time-vectors     :', len(test_dict_times)

    print "---------------------------------------------------------------------------------------------"
    return train_dict_features, train_list_names_features, train_array_features, train_array_features_orig, train_dict_times, train_list_names_times, test_dict_features, test_list_names_features, test_dict_times, test_list_names_times, nAlgs, nFeatures
# -------------------------------------------------------------------------------------
# END: Parsing data
# -------------------------------------------------------------------------------------

def runtime_transformat(target_type, Y_train, Y_test):
    y_train = copy.copy(Y_train)
    Y_test = copy.copy(Y_test)
    print 'target:',
    if target_type == 1:
        print 'y'
    elif target_type == 2:
        print 'log10(10+y)'
        y_train = np.log10(10+y_train)
        Y_test = np.log10(10+Y_test)
    elif target_type == 3:
        print 'log10(y)'
        y_train = np.log10(y_train+0.0001)
        Y_test = np.log10(Y_test+0.0001)
    elif target_type == 4:
        print 'sqrt(y)'
        y_train = np.sqrt(y_train)
        Y_test = np.sqrt(Y_test)
    elif target_type == 5:
        print 'PAR',constPAR
        for i in range(y_train.shape[1]):
            idx = y_train[:,i]>constTimeOut
            y_train[idx,i] = constTimeOut*constPAR
            idx = Y_test[:,i]==constTimeOut
            Y_test[idx,i] = constTimeOut*constPAR
    return y_train, Y_test


from sklearn import ensemble

class AlgoPickModel(object):
    def __init__(self, modeltype='M-ET', n_estimators=100, alpha=0.5, n_jobs=-1):
        self.modeltype = modeltype
        self.n_estimators = n_estimators
        self.learner = None
        self.alpha = alpha
        self.n_jobs = n_jobs

    def fit(self, X, y):
        print 'training', self.modeltype
        if self.modeltype=='M-ET':
            self.learner = ensemble.ExtraTreesRegressor(n_estimators=self.n_estimators, n_jobs=self.n_jobs)
            self.learner.fit(X, y)
        elif self.modeltype=='M-RF':
            self.learner = ensemble.RandomForestRegressor(n_estimators=self.n_estimators, n_jobs=self.n_jobs)
            self.learner.fit(X, y)
        elif self.modeltype=='S-ET':
            etrgrs = []
            for i in range(y.shape[1]):
                print '\tsingle-output', self.modeltype, i
                etrgr = ensemble.ExtraTreesRegressor(n_estimators=self.n_estimators, n_jobs=self.n_jobs)
                etrgr.fit(X, y[:,i])
                etrgrs += [etrgr]
            self.learner = etrgrs
        elif self.modeltype=='S-RF':
            etrgrs = []
            for i in range(y.shape[1]):
                print '\tsingle-output', self.modeltype, i
                etrgr = ensemble.RandomForestRegressor(n_estimators=self.n_estimators, n_jobs=self.n_jobs)
                etrgr.fit(X, y[:,i])
                etrgrs += [etrgr]
            self.learner = etrgrs
        elif self.modeltype=='C-ET':
            print '\tmulti-output', self.modeltype
            rgrmul = ensemble.ExtraTreesRegressor(n_estimators=self.n_estimators, n_jobs=self.n_jobs)
            rgrmul.fit(X, y)
            etrgrs = [rgrmul]
            for i in range(y.shape[1]):
                print '\tsingle-output', self.modeltype, i
                etrgr = ensemble.ExtraTreesRegressor(n_estimators=self.n_estimators, n_jobs=self.n_jobs)
                etrgr.fit(X, y[:,i])
                etrgrs += [etrgr]
            self.learner = etrgrs

    def predict_runtime(self, X):
        if self.modeltype=='M-ET' or self.modeltype=='M-RF':
            y_preds = self.learner.predict(X)
        elif self.modeltype=='S-ET' or self.modeltype=='S-RF':
            y_preds = []
            for etrgr in self.learner:
                y_pred = etrgr.predict(X)
                y_preds += [y_pred]
            y_preds = np.array(y_preds)
            y_preds = y_preds.T
        elif self.modeltype=='C-ET' or self.modeltype=='C-RF':
            y_preds_m = self.learner[0].predict(X)
            y_preds_s = []
            for etrgr in self.learner[1:]:
                y_pred = etrgr.predict(X)
                y_preds_s += [y_pred]
            y_preds_s = np.array(y_preds_s)
            y_preds_s = y_preds_s.T
            y_preds = self.alpha*y_preds_m + (1-self.alpha)*y_preds_s

        return y_preds

    def predict_algID(self, X):
        y_preds = self.predict_runtime(X)
        BestAlgIDs = y_preds.argmin(axis=1)
        return BestAlgIDs

def main():
    print 'COMMANDLINE: python', ' '.join(sys.argv)
    print

    from time import time
    t1 = time()

    # Parse Data
    train_dict_features, train_list_names_features, train_array_features, train_array_features_orig, train_dict_times,  train_list_names_times, test_dict_features, test_list_names_features, test_dict_times, test_list_names_times, nAlgs, nFeatures  = parseData(strFileNameTrainFeatures, strFileNameTrainTimes, strFileNameTestFeatures, strFileNameTestTimes)

    X_train = [] 
    Y_train = []
    for idTrainInstance in train_list_names_features:       
        X_train += [train_dict_features[idTrainInstance]]
        Y_train += [train_dict_times[idTrainInstance]]
    X_test = [] 
    Y_test = []
    for idTestInstance in test_list_names_features:       
        X_test += [test_dict_features[idTestInstance]]
        Y_test += [test_dict_times[idTestInstance]]
    X_train = np.array(X_train) 
    Y_train = np.array(Y_train)
    X_test = np.array(X_test) 
    Y_test = np.array(Y_test)

    target_type = args.target
    n_estimators = args.ntrees
        
    # Normalize complete feature matrix (including the current test instance which was just added to the training set)
    # This is of course wasteful since the current test instance might not change the min/max
    # array_available_features_normalized = normalize(train_array_features)
    y_train, Y_test = runtime_transformat(target_type, Y_train, Y_test)

    modeltype=args.model
    
    model = AlgoPickModel(modeltype=modeltype, n_estimators=n_estimators, alpha=args.alpha, n_jobs=-1)
    model.fit(X_train, y_train)
    bestAlgIDs = model.predict_algID(X_test)
    
    # List of result runtimes achieved by chosen algorithm 
    list_resulttimes    = []
    # List of VBS runtimes achieved by best algorithm 
    list_resultVBStimes     = []
    # List of runtims achieved on instances that got actually solved
    list_resulttimes_solved = []
    
    # Open output file, if specified
    if strFileNameOutputPerf:
        file_output = open(strFileNameOutputPerf,'w')
    
    print
    print "---------------------------------------------------------------------------------------------"
    print "Main Options:"
    print " -> Penalty used in PAR              " + str(args.penalty)
    print " -> Target type                      " + str(args.target)
    print " -> Num of trees                     " + str(args.ntrees)
    print " -> alpha                            " + str(args.alpha)
    print "---------------------------------------------------------------------------------------------"

    global nTestInstances
    global nTimeOuts
    global nVBSTimeOuts

    # -------------------------------------------------------------------------------------
    # Loop over test instances using the same ordering as in the test features file
    for i, keyTestInstance in enumerate(test_list_names_features):
        # Exit if this key does not exist in dictionary
        if keyTestInstance not in test_dict_features:
            print "Error: Could not find instance " + keyTestInstance + " in the time data dictionary."
            exit()
            
        # print 'Test instance name:', keyTestInstance
        
        nAlg                    = 0
        f_timeChosenAlg         = 0.0
        
        # Based on the computed distance, number of algs, and time dictionary, we pick an algorithm
        nAlg = bestAlgIDs[i]
        
        # Get the time for the chosen algorithm (max=Timeout)
        f_timeChosenAlg = min(test_dict_times[ keyTestInstance ] [nAlg], constTimeOut)
        
        # Cap time by timeout
        f_timeChosenAlg  = min(constTimeOut, f_timeChosenAlg)
        
        # Keep track of all result times
        list_resulttimes.append(f_timeChosenAlg)    

        # Keep track of timeouts and runtime on instances that are solved
        if f_timeChosenAlg >= constTimeOut:
            nTimeOuts += 1
        else:
            list_resulttimes_solved.append(f_timeChosenAlg)
        
        # Keep statistics for VBS as well   
        fVBSTime = min(test_dict_times[ keyTestInstance ])
        if fVBSTime >= constTimeOut:
            nVBSTimeOuts += 1
        list_resultVBStimes.append(min(constTimeOut, fVBSTime))
    
        # Increment number of seen testinstances
        nTestInstances += 1
    
        # Output information to stdout and perf file
        # print str(nTestInstances) +  '.', keyTestInstance, nAlg, f_timeChosenAlg, fVBSTime
        # print
        if strFileNameOutputPerf:
            print >>file_output, keyTestInstance, f_timeChosenAlg, fVBSTime
            
        
    # Close output file
    if strFileNameOutputPerf:
        file_output.close() 
    
    print "---------------------------------------------------------------------------------------------"
    # If in analysis mode, show some summary statistics
    print 'Test-Instances                     :', nTestInstances
    print 'n-Solved                           :', (nTestInstances - nTimeOuts)
    print 'Percentage solved                  :', ((nTestInstances - nTimeOuts) / nTestInstances ) * 100.0
    print 'Geometric-Mean (shifted by 10)     :', computeGeometricMean(list_resulttimes, 10.0)
    print 'Runtime-Mean                       :', sum(list_resulttimes)/len(list_resulttimes)
    print 'Runtime-Mean-On-Solved             :', sum(list_resulttimes_solved) / len(list_resulttimes_solved)
    print 'VBS-Solved                         :', (nTestInstances - nVBSTimeOuts)
    print 'VBS-Percentage solved              :', ((nTestInstances - nVBSTimeOuts) / nTestInstances ) * 100.0
    print 'VBS-Mean                           :', sum(list_resultVBStimes) / len(list_resultVBStimes)
    print 'VBS-Geometric-Mean (shifted by 10) :', computeGeometricMean(list_resultVBStimes, 10.0)
    print 'Total consumed time                : %.2f s' % (time()-t1)

# -------------------------------------------------------------------------------------

# Main 
if __name__ == "__main__":
    main()


