# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 13:35:40 2019

@author: Casey
"""

#from recursive_feature_elimination import specifyDataset
import numpy as np
from process_data import readAllFeatures, chooseFeatures
from sklearn.cross_validation import KFold
from sklearn import svm
from sklearn.metrics import accuracy_score
from itertools import chain
from joblib import Parallel, delayed#, dump
import multiprocessing
import time
import math

def oneVAll(attack, table):
    print('here withh ', attack)
    tempTable = np.array(table)
  #  print('r2l'==attack)
    for idx,el in enumerate(tempTable):
        if el != attack:
         #   print(el)
            tempTable[idx] = 0
        else:
            tempTable[idx]=1
           # if attack == 'r2l':
              #  print(idx)
            
    return tempTable

def rfe(X,y):
    pass

def parallelRFE(i,featureVals,labels):
    #reshape into a vector
    labels = labels.reshape(len(labels),)
    print('before getting vals',featureVals)
   # print('shape of featureVals', featureVals.shape)
    featureVals, non, non2 = chooseFeatures(featureVals,'./datasets/kc_house_data/kc_house_data_X.csv','./datasets/kc_house_data/kc_house_data_X.csv')#this is just a lazy way to get the feature name)
    print('after getting vals', featureVals[0][0])
    accuracyScores = []#np.array
    featureScores = []#scores for this round
    
    kf = KFold(len(labels),5)
   # print(kf)
    print('current feature: ',str(i))
    
    for train_index, test_index in kf:
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = featureVals[train_index], featureVals[test_index]
        y_train, y_test = labels[train_index], labels[test_index]
        
        myModel = svm.SVC(gamma='auto',kernel='rbf')#,C=20.0)#for gamma: (1/n_feats) * stdX. In this case, n_feats is 1, so first part is ignored
       # myModel = svm.SVC(gamma=2.0,kernel='rbf',C=5.0)
        # print(y_train.shape)
        myModel.fit(X_train,y_train)
        #predict
        predicted = myModel.predict(X_test)
        non,non2,nonFeatures = chooseFeatures([i],'./datasets/kc_house_data/kc_house_data_X.csv','./datasets/kc_house_data/kc_house_data_X.csv')#this is just a lazy way to get the feature name
        
        
        #the nature of time windows presents an interesting problem with metrics compared to usual classification tasks. A simple one to one comparison of prediction to label for each individual second does not completely capture the effectiveness of attack classification when an attack is a sequence of seconds, not a single second.
        #also important is the idea that ANY value of an attack window is classified as an attack (a single flagged event in an entire window may be enough for a sec analyst to check for (and discover) an attack). Of course this method alone neither takes into account reducing FPs and it does not give weight to the normal true positive rate. (e.g. if an attack is 1000 seconds, and only 1 sec is classified as such, a sec analyst would (reasonably) be more likely to overlook it than if 700 / 1000 are classified as an attack in the same window).
        #in other words, it looks more like a false positive. We want a measure that considers the total attacks correctly flagged, the percentage of individual attack seconds classified as such, and the individual regular seconds incorrectly classified as an attack. All three of these measures are important and impact the real world performance of an IDS, and any useful measure of an IDS should consider all three.
        #we want all of these things to be considered together and give us a measure between 0 and 1
        #accuracy alone is a poor predictor of IDS performance [cite base rate fallacy paper]
        
        #Factors for successful IDS metric: 
        #1 perAttackTPR: we want to maximize number of attacks classified as such (with even 1 packet correctly labelled in the entire attack) (domain specific) (gives each attack equal weight) (every attack is important to classify as such)
        #2 TNR: we want to minimize the percentage of false positives (equiv. maximize TNR: (1 - FPR) == TNR) (Regular traffic has an attack prediction.) (all false positives are bad bc of base rate fallacy) (the more, the worse)
        ####get rid of? 3: we want to maximize the average percentage of seconds correctly classified as an attack for each attack, which is equivalent to getting TPR (per attack basis) (this measure gives all attacks equal weight) (threshold)
        #4 TPR: we want to maximize the overall average percentage of true positives (eqiv: total number of correct attack seconds classified as such) (this gives larger attacks more weight (prob good for our purposes)) (per attack accuracy) (larger attacks are more relevant to time-based attacks and therefore should have more weight given to them)
       
        
        #we need a measure which gives all attacks weight, gives longer attacks more weight (time relevant), and penalizes false positives
        #in the future, experimentation can be done to consider the optimal weights given to each of these
        
        
        print('accuracy minus feature',str(i), nonFeatures[0],accuracy_score(y_test,predicted))
        
        #np.append(accuracyScores, accuracy_score(y_test,predicted))
        accuracyScores.append(accuracy_score(y_test,predicted))

    #print(accuracyScores.)
    print(accuracyScores)
    scoresAvg = np.mean(np.asarray(accuracyScores))# 
    featureScores.append([scoresAvg,nonFeatures[0],i])
        
    print(featureScores)
    return featureScores

def oneRound(startingFeatureIndeces,idx,feature,y):
    tempFeatures = [startingFeatureIndeces[0:idx]]
    tempFeatures.append(startingFeatureIndeces[idx+1:])
    tempFeatures = list(chain.from_iterable(tempFeatures))
            
    #tempFeatures = np.delete(startingFeatureIndeces,feature)#all features in current round minus one (i.e. remove a column)
    print('tempFeatures',tempFeatures)
            
    print('the feature index is', feature)
    #https://stackoverflow.com/questions/45346550/valueerror-unknown-label-type-unknown
    
    return parallelRFE(feature,tempFeatures,y.astype('int'))
    #featureScores.append(parallelRFE(feature,tempFeatures,y.astype('int')))
    #print('feature scores outside the loop')
    #print(featureScores)
    #print('\n\n')

def main():

    X,y,features = readAllFeatures('./datasets/kc_house_data/kc_house_data_X.csv','./datasets/kc_house_data/kc_house_data_y_classification_2_class.csv')
    
    print(y)
    
    y = oneVAll('average', y).reshape(len(y),)
    
    print(y)
    rfe(X,y)
    
    start = time.time()
    
    #temporary
    #X = X[:,0:4]
    
    startingFeatures = X
    
    startingFeatureIndeces = [] #get indeces of features for next round
    for i in range(len(startingFeatures[0])):
        startingFeatureIndeces.append(i)
    
    for round in range(len(X[0])):#total rounds to run.
        #print('feature scores for current round')
        #print(featureScores)
        featureScores = []
        print('startingFeatures is',startingFeatureIndeces)
    
        print('len of starting features', str(len(startingFeatureIndeces)))
        
        #here keep track of score from best features from previous round. If it is worse in new round, stop
        if len(startingFeatureIndeces)>1:#else this is the last element. don't perform another round
            #parallelize this
            
            num_cores = multiprocessing.cpu_count()
            print("the number of cores is", str(num_cores))
    
            retVal = Parallel(n_jobs=num_cores-2)(delayed(oneRound)(startingFeatureIndeces,idx, feature, y) for idx, feature in enumerate(startingFeatureIndeces))
            print(retVal)
            featureScores.append(retVal)
            
            #for feature in range(len(startingFeatures[0])):#number of features in current round
           # for idx, feature in enumerate(startingFeatureIndeces):    
              #  featureScores.append(oneRound(startingFeatureIndeces,idx,feature,y))
                
            sortedList = sorted(featureScores[0], reverse=False)#feature scores is a single element nested list
            print('sorted list',sortedList)
            
            print(len(sortedList)*.2)
            print(math.floor(len(sortedList)*.2))
            
            toElim = math.floor(len(sortedList)*0.2)#eliminates 20% of each round's features
            
            if(toElim == 0):#1 feature is less than threshold
                toElim = 1
            
            print('this round, eliminates', toElim,'features')
            for i in range(toElim):
            
                print('last place feature',sortedList[-1])
                print('\n\n\neliminate feature',(sortedList[-1][0][1]),'\n\n')
                #print(np.asarray(sortedList)[:,:-1])
                #startingFeatures = np.asarray(sortedList)[:,:-1]
                
                
                #number of elements to remove
                sortedList = sortedList[:-1]
            
            startingFeatureIndeces = []
            for el in sortedList:
                startingFeatureIndeces.append(el[0][2])
                
            print('new feature indeces', startingFeatureIndeces)
            
            startingFeatures, non, non2 = chooseFeatures(startingFeatureIndeces, './datasets/kc_house_data/kc_house_data_X.csv','./datasets/kc_house_data/kc_house_data_y_classification_2_class.csv')
                
            
            
            #exit()
                #X = sortedList
    
    print("the final feature set is", startingFeatures)
    
    print('total run time', (time.time() - start))
    #for total number of rounds (round)
        #featureScores = []
        
        #parallelize
        #for each feature (feature)
            #append to featureScores svm run score without (feature)
            
        #sort featureScores
        #remove worst feature
    
    #define the features to run before each parallel RFE call
    
    
    #specifyDataset(X,y,'svm',15)

main()