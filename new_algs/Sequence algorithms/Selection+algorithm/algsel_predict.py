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

# ------------------------------------------------------------------------------
# END: Python imports
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Argument parsing, default values, and help
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='details',
        usage='use "%(prog)s --fafhelp" for more information',
        formatter_class=argparse.RawTextHelpFormatter)

# positional argument
parser.add_argument('tstFeatures', type=str, help='test data: features file')
parser.add_argument('tstTimes', type=str, help='test data: runtimes file')
parser.add_argument('timeout', type=float, help='timeout for the portfolio')

# optional argument
parser.add_argument('-i', '--inmodel', type=str,
    help='name of file to load the trained model (default: model.pickle)',
    default='model.pickle')
parser.add_argument('-o', '--outfile',  type=str,
    help='name of file to output performance numbers to (default: none)',
    default='')

args = parser.parse_args()

strFileNameTestFeatures     = ''
strFileNameTestTimes        = ''
strFileNameTestFeatures     = args.tstFeatures
strFileNameTestTimes        = args.tstTimes
constTimeOut                = args.timeout
strFileNameInputModel       = args.inmodel
strFileNameOutputPerf       = args.outfile
# ------------------------------------------------------------------------------
# END: Argument parsing and help
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Global Constants
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Min distance to work with
# Penalize a timeout of a solver by this factor

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

from util import readfile_data
from util import makeDict
from util import computeGeometricMean
from util import calc_par

def parseData(strFileNameTestFeatures, strFileNameTestTimes):
    # print "---------------------------------------------------------------------"
    print 'Parsing Data'

    print ' -> Reading Test Features  :', strFileNameTestFeatures
    instIds, test_features = readfile_data(strFileNameTestFeatures)
    test_dict_features, test_list_names_features = makeDict(instIds, test_features)

    print ' -> Reading Test Times     :', strFileNameTestTimes

    instIds, test_times = readfile_data(strFileNameTestTimes)
    test_dict_times, test_list_names_times = makeDict(instIds, test_times)

    nAlgs     = len(test_dict_times[test_list_names_times[0]])
    nFeatures = len(test_dict_features[test_list_names_features[0]])

    print
    print ' Basic Information on Data: '
    print ' --> Number of Algorithms            :', nAlgs
    print ' --> Number of Features              :', nFeatures
    print ' --> Number of Test-Feature-vectors  :', len(test_dict_features)
    print ' --> Number of Test-Time-vectors     :', len(test_dict_times)

    # print "---------------------------------------------------------------------"
    X_test = []
    Y_test = []
    for idTestInstance in test_list_names_features:
        X_test += [test_dict_features[idTestInstance]]
        Y_test += [test_dict_times[idTestInstance]]
    X_test = np.array(X_test)
    Y_test = np.array(Y_test)
    return X_test, Y_test
# ------------------------------------------------------------------------------
# END: Parsing data
# ------------------------------------------------------------------------------

def main():
    print 'COMMANDLINE: python', ' '.join(sys.argv)
    print

    from time import time
    t1 = time()

    # Parse Data
    X_test, Y_test = parseData(strFileNameTestFeatures, strFileNameTestTimes)

    import pickle
    f = open(strFileNameInputModel,'rb')
    trained_model = pickle.load(f)
    f.close()
    bestAlgIDs = trained_model.predict_algID(X_test)

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
    # print "---------------------------------------------------------------------"
    print "Main Options:"
    print " -> Trained model: " + str(args.inmodel)
    print "     ", trained_model
    # print "---------------------------------------------------------------------"

    global nTestInstances
    global nTimeOuts
    global nVBSTimeOuts

    # -------------------------------------------------------------------------------------
    # Loop over test instances using the same ordering as in the test features file
    for i, nAlg in enumerate(bestAlgIDs):
        # Get the time for the chosen algorithm (max=Timeout)
        f_timeChosenAlg = min(Y_test[i][nAlg], constTimeOut)
        # Keep track of all result times
        list_resulttimes.append(f_timeChosenAlg)
        # Keep track of timeouts and runtime on instances that are solved
        if f_timeChosenAlg >= constTimeOut:
            nTimeOuts += 1
        else:
            list_resulttimes_solved.append(f_timeChosenAlg)
        # Keep statistics for VBS as well
        fVBSTime = min(Y_test[i])
        if fVBSTime >= constTimeOut:
            nVBSTimeOuts += 1
        list_resultVBStimes.append(min(constTimeOut, fVBSTime))
        # Increment number of seen testinstances
        nTestInstances += 1
        # Output information to stdout and perf file
        # print str(nTestInstances), nAlg, f_timeChosenAlg, fVBSTime
        # print
        if strFileNameOutputPerf:
            print >>file_output, f_timeChosenAlg, fVBSTime


    # Close output file
    if strFileNameOutputPerf:
        file_output.close()

    print
    # print "---------------------------------------------------------------------"
    # If in analysis mode, show some summary statistics
    print 'Test-Instances                     :', nTestInstances
    print 'n-Solved                           :', (nTestInstances - nTimeOuts)
    print 'Percentage solved                  : %.2f' % \
        (((nTestInstances - nTimeOuts) / nTestInstances ) * 100.0)
    print 'Geometric-Mean (shifted by 10)     : %.2f' % \
        computeGeometricMean(list_resulttimes, 10.0)
    print 'Runtime-Mean                       : %.2f' % \
        (sum(list_resulttimes)/len(list_resulttimes))
    print 'Runtime-Mean-On-Solved             : %.2f' % \
        (sum(list_resulttimes_solved) / len(list_resulttimes_solved))
    print 'PAR-1                              : %.2f' % \
        calc_par(list_resulttimes, constTimeOut, k=1)
    print 'PAR-5                              : %.2f' % \
        calc_par(list_resulttimes, constTimeOut, k=5)
    print 'PAR-10                             : %.2f' % \
        calc_par(list_resulttimes, constTimeOut, k=10)
    print 'VBS-Solved                         :', (nTestInstances - nVBSTimeOuts)
    print 'VBS-Percentage solved              : %.2f' % \
        (((nTestInstances - nVBSTimeOuts) / nTestInstances ) * 100.0)
    print 'VBS-Mean                           : %.2f' % \
        (sum(list_resultVBStimes) / len(list_resultVBStimes))
    print 'VBS-Geometric-Mean (shifted by 10) : %.2f' % \
        computeGeometricMean(list_resultVBStimes, 10.0)
    print 'Testing time                       : %.2f' % (time()-t1)

# -------------------------------------------------------------------------------------

# Main
if __name__ == "__main__":
    main()
