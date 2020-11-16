# -*- coding: utf-8 -*-
"""
Created on Sat May 16 20:02:24 2020

@author: Asad
"""

import math
import operator 

def euclideanDistance(testInstance, trainInstance, length):
	distance = 0
	for x in range(length):
		distance += pow((testInstance[x] - trainInstance[x]), 2)
	return math.sqrt(distance)

def manhattan(testInstance,trainInstance,length):
    # formula is: distance=|a1-b1|+|a2-b2|
    distance=0
    for x in range(length):
        distance+=abs(testInstance[x]-trainInstance[x])
    return distance

def minkowski(testInstance,trainInstance,length):
    # formula is: distance=(sum(a-b)^r)^1/r
    distance=0
    for x in range(length):
        distance+=pow(abs(testInstance[x]-trainInstance[x]),length)
    return pow(distance,1/length)


def getNeighbors(trainingData,testData,k,measure="Euclidean"):
    dist=0
    distances=[]
    eachtestdistance=[]
    length=len(testData[0])-1
    for eachtestData in testData:
        eachtestdistance=[]
        for eachtrainData in trainingData:
            # Make one method for all distances but call distance methods.
            if measure=="Euclidean":
                dist=euclideanDistance(eachtestData,eachtrainData,length)
            elif measure=="Manhattan":
                dist=manhattan(eachtestData,eachtrainData,length)
            elif measure=="Minkowski":
                dist=minkowski(eachtestData,eachtrainData,length)
            eachtestdistance.append((eachtrainData,dist,eachtestData)) # making one list of each  testInstance distance with TrainInstances
        distances.append(eachtestdistance) # appending all testInstances distances
    neighbors=[]
    for eachTest in distances:
        eachtrainingInstance=[]
        for test in eachTest:
            eachtrainingInstance.append(test)
        eachtrainingInstance.sort(key=operator.itemgetter(1))
        eachtrainKthInstances=[]
        for x in range(k):
            eachtrainKthInstances.append(eachtrainingInstance[x][0])
        neighbors.append(eachtrainKthInstances)
    
    return neighbors




def getResponse(neighbors):
    classVotes={}
    outputs=[]
    for neighbor in neighbors:
        for eachoutput in neighbor:
            response=eachoutput[-1]
            if response in classVotes:
                classVotes[response]+=1
            else:
                classVotes[response]=1
        sortedVotes = sorted(classVotes.items(),key=operator.itemgetter(1), reverse = True)
        outputs.append(sortedVotes[0][0])
    return outputs


def for_each_Distance_Measure(neighbors):
    i=1
    for each in neighbors:
        print("For Test Instance {} Neighbors are  \n{}".format(i,each))
        print("\n")
        i=i+1    
    response = getResponse(neighbors)
    for x in range(len(response)):
        print("For Test Instance {} Final Output is {}".format(testInstance[x],response[x]))

def main(trainSet):
   
    neighbors = getNeighbors(trainSet, testInstance, k,measure="Euclidean")
    print("<--------------By Euclidean Distance---------------->")
    for_each_Distance_Measure(neighbors)
    neighbors = getNeighbors(trainSet, testInstance, k,measure="Manhattan")
    print("\n<-------------------By Manhattan Distance------------------>")
    for_each_Distance_Measure(neighbors)
    neighbors = getNeighbors(trainSet, testInstance, k,measure="Minkowski")
    print("\n<-------------------By Minkowski Distance----------------->")
    for_each_Distance_Measure(neighbors)
    
if __name__=='__main__':
    testInstance =  [[0.51,0.50] ,[0.1,0.9] , [0.4,0.3]]
    k = 3
    #AND GATE
    trainSetAND_GATE = [[0.0, 0.0, 0],[1.0,1.0,1], [0.0, 1.0, 0],[1.0, 0.0, 0]]
    print("<-......................By applying AND Gate..................>\n")
    main(trainSetAND_GATE)
    
    # OR GATE
    trainSetOR_GATE=[[0.0, 0.0, 0],[1.0,1.0,1], [0.0, 1.0, 1],[1.0, 0.0, 1]]
    print("\n<......................By applying OR Gate.................>\n")
    main(trainSetOR_GATE)