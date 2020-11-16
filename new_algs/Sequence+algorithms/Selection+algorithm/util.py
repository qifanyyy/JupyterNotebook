import sys
import os
import re
import math
import numpy as np

# Max values for floats used for feature range (max/min)
constMaxFloat                   =  1e+36
constMinFloat                   = -1e+36
constMaxInt                     =  1e+36

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

def calc_map(preds, Y_test, timeout):
    y_can_solve = (Y_test<timeout)
    map_arr = []
    for pred,r in zip(preds, y_can_solve):
        idx = np.argsort(pred)
        r = r[idx]
        p = np.cumsum(r)*1.0 / np.array(range(1,len(r)+1))
        denum = np.cumsum(r*p)
        num = np.cumsum(r)
        num[num==0] = 1
        map_arr += [denum/num]
    maps = np.mean(map_arr,axis=0)
    return maps

def calc_par(preds, timeout, k=10):
    r = np.array(preds)
    itimeout = (r>=timeout)
    r[itimeout] = timeout*k
    return np.mean(r)
