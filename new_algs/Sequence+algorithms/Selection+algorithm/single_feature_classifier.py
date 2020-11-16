# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 10:59:32 2018

@author: Casey
"""

from process_data import chooseFeatures,readAllFeatures
from run_ml_alg import getModelScores
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from joblib import Parallel, delayed
import multiprocessing
import time
    
def classifierForTopNFeatures(n,sortedFeatures,XFile,yFile,mlAlg):
    topFeatureIndeces = []
    for i in range(n):
        topFeatureIndeces.append(sortedFeatures[i][2])
    print(topFeatureIndeces)
    allX, allY, features = chooseFeatures(topFeatureIndeces, XFile,yFile)
    scores = getModelScores(mlAlg,allX,allY,10)
    print('error for top 6 features',features,scores.mean())
    
    
    #when selecting top 6 features, they are 5,11,12,19,4,9. This is run above
    #code below replaces 12 from above with 10 (a worse performing individual feature) for an overall better score combined
    
    #allX, allY, features = chooseFeatures([3,9,8,17,2,7], XFile,yFile)   
    #scores = getModelScores(mlAlg,allX,allY,10)
    
def singVarClassifier(i,XFile,yFile,mlAlg,numFeatures):
    allX,allY,features = chooseFeatures([i],XFile,yFile)
    print(i)
    scores=getModelScores(mlAlg,allX,allY,30)
    print(scores.mean(),features[0],i)
    return [scores.mean(),features[0],i]

def specifyDataset(XFile,yFile,mlAlg,numFeatures):#if featuresList is empty, by default start with all features specified in dataset


    f = open("file.txt","a")
    f.write("newew")
    
    f.write('newew')

    loopLength,non,non1 = readAllFeatures(XFile,yFile)# just to get length of x
    emptyList = []
    start = time.time()
    num_cores = multiprocessing.cpu_count()
    var = Parallel(n_jobs=num_cores)(delayed(singVarClassifier)(i,XFile,yFile,mlAlg,numFeatures) for i in range(len(loopLength[0])))
    end = time.time()
    print("time for parallel ", str(end-start))
    print('var is')
    print(var)
   # emptyList.append(var)
   # print(emptyList)
  #  emptyList = []
      
    start = time.time()
    for i in range(len(loopLength[0])):#there are 19 total features in standard X file
        if i != 1 and i != 2:
            allX,allY,features = chooseFeatures([i], XFile,yFile)
            scores = getModelScores(mlAlg,allX,allY,10)
            #print(scores.mean(),features[0],i)
            #f = open("file.txt","a")
            #f.write('here')
     #       f.write(str(scores.mean())+ ' ' + features[0]+ ' ' +str(i) + '\n')
            #f.close
            
     
            emptyList.append([scores.mean(),features[0],i])
    end = time.time()
    print("time for sequential", str(end-start)) 
    
    
    print(emptyList)
    sortedList = sorted(var, reverse=True)
    #f.write(sortedList)
    f.close
    
    for i in range(len(sortedList)):
        print(sortedList[i])
        
    classifierForTopNFeatures(6,sortedList,XFile,yFile,mlAlg)#first arg is number of top ranked features to run
