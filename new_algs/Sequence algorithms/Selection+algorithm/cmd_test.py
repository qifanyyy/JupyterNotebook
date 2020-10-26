# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 10:11:34 2018

@author: Casey
file to test command line stuff
"""
import sys
#sys.path.append(C:\\Users\\Casey\\Anaconda3\\Lib\\site-packages;C:\\Users\\Casey\\Anaconda3\\Library\\bin;C:\\Program Files (x86)\\Intel\\iCLS Client\\;C:\\Program Files\\Intel\\iCLS Client\\;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\;C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\DAL;C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\DAL;C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\IPT;C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\IPT;C:\\Program Files (x86)\\NVIDIA Corporation\\PhysX\\Common;C:\\Program Files\\Intel\\WiFi\\bin\\;C:\\Program Files\\Common Files\\Intel\\WirelessCommon\\;C:\\Program Files\\PuTTY\\;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\WINDOWS\\System32\\OpenSSH\\;E:\\Casey\\Matlab\\runtime\\win64;E:\\Casey\\Matlab\\bin;E:\\Casey\\Documents\\Git\\cmd;C:\\Program Files\\OpenVPN\\bin;C:\\Program Files\\nodejs\\;C:\\Users\\Casey\\Anaconda3;C:\\Users\\Casey\\Anaconda3\\Scripts;C:\\Users\\Casey\\Anaconda3\\Library\\bin;C:\\Users\\Casey\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Program Files (x86)\\SSH Communications Security\\SSH Secure Shell;C:\\Users\\Casey\\AppData\\Local\\GitHubDesktop\\bin;C:\\Users\\Casey\\AppData\\Roaming\\npm;)
import ast
import numpy as np
from test import test
#import pandas as pd
#from sklearn import linear_model,svm
#from sklearn.model_selection import cross_val_score
#from itertools import chain

import manually_choose_features
import single_feature_classifier
import recursive_feature_elimination

def main():
    input = sys.argv
    #input[0] is file name
    
    #later, specify model (i.e. regression) and data set.
    #if model is regression, specify feature index to compare
    #if model is classification, specify classes somehow, either manually, through a file, create dynamically, etc.
    #give option for cross val and num of folds
    #for relevant options, specify number of features to stop at
    #add some normalization options and specify a default
    #add a decision tree
    #ideally should have input validation
    #adding exceptions for args below would be nice
    #create an option to try all feature selection methods with given ml algs for best feature set overall
    #consider having separate data processing and feature selection components
    #it would be interesting to put the time to run on a file. Perhaps have that as an arg
    #it may be interesting to allow for variables entered from the command line to be used as x an y as well
    if(input[1] == '-manual'):#the person wants to manually enter feature indeces. Probably not commonly recommended
        
        mlAlg = input[2]
        
        XFile = './datasets/' + input[3]
        XFeatures = ast.literal_eval(input[4])
        yFile = './datasets/' + input[5]
        yFeature = ast.literal_eval(input[6])
        

        manually_choose_features.enterFeatureIndeces(XFeatures,yFeature,XFile,yFile,mlAlg)
    elif(input[1] == '-sfc'):#single feature classifier

        mlAlg = input[2]
        checkMLAlg(mlAlg)
        XFile = './datasets/' + input[3]
        yFile = './datasets/' + input[4]
        finalFeatureSetSize = input[5]#check that this is an int
        print('single feature classifier\n')
        #f = open("file.txt","a")
        #f.write('aardvark'+ '\n')
        #f.close
        #print(XFile)
        #exit()
        single_feature_classifier.specifyDataset(XFile,yFile,mlAlg,finalFeatureSetSize)
    elif(input[1] == '-rfe'):
        
        mlAlg = input[2]
        checkMLAlg(mlAlg)
        XFile = './datasets/' + input[3]
        yFile = './datasets/' + input[4]
        finalFeatureSetSize = input[5]#check that this is an int
        print('recursive feature elimination\n')
        recursive_feature_elimination.specifyDataset(XFile,yFile,mlAlg,finalFeatureSetSize)

        
def checkMLAlg(_mlAlg):
    if _mlAlg == 'lin_reg':
        return
    elif _mlAlg == 'svm':
        return
    
    else:
        printMLAlgOptions()
        exit()
    
def printMLAlgOptions():
    print("Machine learning algorithms to choose from and their argument names:\n")
    print('linear regression:  \"lin_reg\"')
    print('support vector machine: \"svm\"')

if __name__=="__main__":
    main()
    exit()