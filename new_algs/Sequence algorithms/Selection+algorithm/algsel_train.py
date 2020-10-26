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
parser = argparse.ArgumentParser(description='details',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)

# positional argument
parser.add_argument('trnFeatures', type=str,
    help='training data: features file')
parser.add_argument('trnTimes', type=str,
    help='training data: runtimes file')
parser.add_argument('timeout', type=float,
    help='timeout for the portfolio')

# optional argument
parser.add_argument('-p', '--penalty', type=float,
    help='timeout penalty for PAR score (default: 5.0)', default=5.0)

parser.add_argument('-o', '--outmodel', type=str,
    help='name of file to output the trained model (default: model.pickle)',
    default='model.pickle')
parser.add_argument('-m', '--modeltype', type=str,
    help=''' model type:
    MultiOut-ET  | MultiOut-RF  |
    SingleOut-ET | SingleOut-RF |
    Stacking-ET  | Stacking-RF  |
    Combined-ET  | Combined-RF  |
    (default: MultiOut-ET)''',
    default='MultiOut-ET')
parser.add_argument('-t', '--target', type=int,
    help='target type \n1:y 2:log10(10+y) 3:log10(y) 4:sqrt(y) 5:PAR-k (default: 1)',
    default=1)
parser.add_argument('-n', '--ntrees', type=int,
    help='num of trees in trained model (default:400)',
    default=400)
parser.add_argument('-a', '--alpha', type=float,
    help='Combined parameter. \nalpha*M_multi+(1-alpha)*M_single: [0-1] (default:0.5)',
    default=0.5)

args = parser.parse_args()

strFileNameTrainFeatures    = args.trnFeatures
strFileNameTrainTimes       = args.trnTimes
constTimeOut                = args.timeout
strFileNameOutputModel      = args.outmodel
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
constPAR                        = args.penalty

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


def parseData(strFileNameTrainFeatures, strFileNameTrainTimes):
    # print "---------------------------------------------------------------------"
    print 'Parsing Data'

    print ' -> Reading Train Features :', strFileNameTrainFeatures
    instIds, train_features = readfile_data(strFileNameTrainFeatures)
    train_dict_features, train_list_names_features = makeDict(instIds, train_features)
    train_array_features = train_features

    print ' -> Reading Train Times    :', strFileNameTrainTimes
    instIds, train_times = readfile_data(strFileNameTrainTimes)
    train_dict_times, train_list_names_times = makeDict(instIds, train_times)
    train_array_features_orig = np.array(train_array_features)

    nAlgs     = len(train_dict_times[train_list_names_times[0]])
    nFeatures = len(train_dict_features[train_list_names_features[1]])

    print
    print 'Basic Information on Data: '
    print ' --> Number of Algorithms            :', nAlgs
    print ' --> Number of Features              :', nFeatures
    print ' --> Number of Train-Feature-vectors :', len(train_dict_features)
    print ' --> Number of Train-Time-vectors    :', len(train_dict_times)

    # print "---------------------------------------------------------------------"

    X_train = []
    Y_train = []
    for idTrainInstance in train_list_names_features:
        X_train += [train_dict_features[idTrainInstance]]
        Y_train += [train_dict_times[idTrainInstance]]
    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    return X_train, Y_train
# ------------------------------------------------------------------------------
# END: Parsing data
# ------------------------------------------------------------------------------

def runtime_transformat(target_type, Y_train):
    y_train = copy.copy(Y_train)
    print 'target:',
    if target_type == 1:
        print 'y'
    elif target_type == 2:
        print 'log10(10+y)'
        y_train = np.log10(10+y_train)
    elif target_type == 3:
        print 'log10(y)'
        y_train = np.log10(y_train+0.0001)
    elif target_type == 4:
        print 'sqrt(y)'
        y_train = np.sqrt(y_train)
    elif target_type == 5:
        print 'PAR',constPAR
        for i in range(y_train.shape[1]):
            idx = y_train[:,i]>constTimeOut
            y_train[idx,i] = constTimeOut*constPAR
    return y_train


def main():
    print 'COMMANDLINE: python', ' '.join(sys.argv)
    print

    print
    # print "---------------------------------------------------------------------"
    print "Main Options:"
    print " -> Target type                      " + str(args.target)
    if args.target==5:
        print " -> Penalty used in PAR              " + str(args.penalty)
    print " -> Num of trees                     " + str(args.ntrees)
    if 'Combined' in args.modeltype:
        print " -> alpha                            " + str(args.alpha)
    # print "---------------------------------------------------------------------"

    from time import time
    t1 = time()

    # Parse Data
    X_train, Y_train = parseData(strFileNameTrainFeatures, strFileNameTrainTimes)

    target_type = args.target
    ntrees = args.ntrees

    # Normalize complete feature matrix
    y_train = runtime_transformat(target_type, Y_train)

    from algsel_models import AlgSel_SingleOutputModel
    from algsel_models import AlgSel_MultiOutputModel
    from algsel_models import AlgSel_StackModel
    from algsel_models import AlgSel_CombinedModel

    algsel_type=args.modeltype
    if algsel_type == 'MultiOut-ET':
        model = AlgSel_MultiOutputModel(modeltype='ET', n_estimators=ntrees, n_jobs=-1)
    elif algsel_type == 'MultiOut-RF':
        model = AlgSel_MultiOutputModel(modeltype='RF', n_estimators=ntrees, n_jobs=-1)
    elif algsel_type == 'SingleOut-ET':
        model = AlgSel_SingleOutputModel(modeltype='ET', n_estimators=ntrees, n_jobs=-1)
    elif algsel_type == 'SingleOut-RF':
        model = AlgSel_SingleOutputModel(modeltype='RF', n_estimators=ntrees, n_jobs=-1)
    elif algsel_type == 'Stacking-ET':
        model = AlgSel_StackModel(modeltype='ET', n_estimators=ntrees, n_jobs=-1)
    elif algsel_type == 'Stacking-RF':
        model = AlgSel_StackModel(modeltype='RF', n_estimators=ntrees, n_jobs=-1)
    elif algsel_type == 'Combined-ET':
        model = AlgSel_CombinedModel(modeltype='ET', n_estimators=ntrees, n_jobs=-1)
    elif algsel_type == 'Combined-RF':
        model = AlgSel_CombinedModel(modeltype='RF', n_estimators=ntrees, n_jobs=-1)
    else:
        print 'error'
        sys.exit()

    model.fit(X_train, y_train)

    import pickle
    f = open(strFileNameOutputModel,'wb')
    pickle.dump(model, f)
    f.close()
    print 'model is saved in', strFileNameOutputModel
    print 'Training time: %.2f' % (time()-t1)
    print

# ------------------------------------------------------------------------------

# Main
if __name__ == "__main__":
    main()
