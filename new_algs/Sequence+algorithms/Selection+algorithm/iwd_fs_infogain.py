'''
A program to pick the n best features of a dataset, out of m (m > n), using the intelligent drop algorithm.

Algorithm: The intelligent water drop algorithm is similar to the ant colony optimization (ACO) algorithm.
'''
import numpy as np
import sklearn
from sklearn import cross_validation
from sklearn import datasets
from sklearn import svm
import random
import time
import os
import sys
import argparse
#import subprocess

# Parsing commandline arguments using argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset_filename", help="the dataset csv file (class label in the first column, and features in the other columns)")
parser.add_argument("final_no_of_features", help="the final no. of features to be selected", type=int)
parser.add_argument("nIWD", help="Number of IWDs", type=int)
parser.add_argument("nIter", help="Number of iterations", type=int)
parser.add_argument("infogain_filename", help="the infogain (csv/txt) file containing only infogain rankings of features sorted according to feature number")

args = parser.parse_args()

# Import dataset (NOTE: dataset should have class/label in first column)
original_dataset = np.genfromtxt(args.dataset_filename, delimiter=',', skip_header=1)
target = original_dataset[:,0]
nodes = len(original_dataset[1,:]) - 1
original_features = original_dataset[:,1:nodes+1]
infogain = np.genfromtxt(args.infogain_filename)

required_no_of_features = args.final_no_of_features

# Initialization of static parameters
iterCount = 0 # no. of iterations finished as of now
nIWD = args.nIWD # no. of water drops
nIter = args.nIter

totalPaths = []
# define iterPaths = [] at the beginning of every iter
iterBestPaths = []
globalBestAccList = []
globalBestAcc = 0
globalBestPath = []

#Velocity-update parameters
a_v = 1000
b_v = 0.01
c_v = 1
#alpha_v = 

#Soil-update parameter
a_s = 1000 # soil-updating parameter (maybe reduce this value? a_s)
b_s = 0.1
c_s = 1
#theta_s = 

rho = 0.9
rho_n = 0.1 # local soild updating parameter

rho_IWD = 0.1 #global soil-updating parameter

epsilon_s = 0.0001 # to prevent zero division

weight_infogain = 1 # for weighted gene ranking used in computing time(i,j)

# Initialization of dynamic parameters
soilMatrix = np.identity(nodes)
soilMatrix.fill(1000)


for a in range(nodes):	# Precaution: Increase the soil for a node to itself so as to have little probability of picking itself
 soilMatrix[a][a]=sys.maxsize

probMatrix = np.identity(nodes)
probMatrix.fill(0)

initialVelocity = 100 # Initial velocity of each IWD
velocity = initialVelocity

unvisited = range(nodes) # List of cities not visited, initially this 
			 # contains even the initial node.

# Parameters to be updated after every node
#minSoil = 0 # Run through all the nodes remaining in unvisited & update with the the minimum soil in path. So the checking would proceed as soil[currentNode,nextNodeWithMinSoilBetween]

# Function definitions

def f(x,y):
 if(np.amin(soilMatrix)>=0):
  #print np.amin(soilMatrix)
  return 1.0/(epsilon_s + (soilMatrix[x][y]))
 else:
  #print min(soilMatrix) 
  return 1.0/(epsilon_s + (soilMatrix[x][y] - np.amin(soilMatrix)))


def weighted_choice(choices):
 totals = [] 
 running_total = 0
 
 for w in choices:
  running_total += w
  totals.append(running_total)

 rnd = random.random() * running_total
 for ii, total in enumerate(totals):
  if rnd < total:
   return ii


def changeInVelocity(x,y):
 return a_v/(b_v + (c_v * soilMatrix[x][y]) )

def time(v, nextNode):
 return 1.0/((weight_infogain*infogain[nextNode]) + v)

def changeInSoil(x,y,vel):
 return a_s/(b_s + (c_s * time(vel, y) ) )



########
if __name__ == '__main__':
 sM_iter = soilMatrix
 sM_iterNext = soilMatrix
 while(iterCount<nIter): # one run of this loop is nIWD drops building a solution, all using the same soilMatrix
  
  IWD_count = 0
  iterPaths = [] # paths of one iteration
  iterBestAcc = 0
  iterBestPath = []
  iterAccList = []
  
  sM_iter = sM_iterNext
  while(IWD_count < nIWD): # one run of this loop is one drop building a complete solution
	  soilMatrix = sM_iter
	  unvisited = range(nodes)
	  currentNode = random.choice(unvisited) # pick a random start
	  print (currentNode)
	  unvisited.remove(currentNode)
	  currentPath = []
	  currentPath.append(currentNode)
	  velocity = initialVelocity
	  soil_IWD = 0.0
	  pathAccList = []
	  print("iterCount: {},IWD_count: {}".format(iterCount, IWD_count))
	  while(len(unvisited)>(nodes - required_no_of_features)): #every run of this loop adds a node to the solution path
	   #print(velocity)
	   i = currentNode
	   
	   #Calulating probabilities
	   ListOfWProb = [1.0/sys.maxsize]*nodes
	   
	   for j in unvisited:
	    probMatrix[i][j]=f(i,j) 
	    ListOfWProb[j] = probMatrix[i][j]
	    #ListOfWProb.append(probMatrix[i][j])
	   
	   # Exploration vs. exploitation
	   randomNumber = random.random()
	   if(randomNumber < 0.7):	
		   I = ListOfWProb.index(max(ListOfWProb))
		   print (max(ListOfWProb))
		   print (I)
		   print ("Exploitation: {}".format(I))
	   else:
    		I = weighted_choice(ListOfWProb)
	    	print (I)
	   if(currentPath.count(I) != 0):  # error('Duplicate')
		   print ('duplicate')
		   print (currentPath)
		   print (unvisited)
		   print (ListOfWProb)
		   print (soilMatrix)
	   unvisited.remove(I)
	   currentNode=I
	   #print("Index: ", I)
	    
	   # update velocity of IWD
	   velocity = velocity - changeInVelocity(i, currentNode) #remember, i and currentNode are no longer same

	   # update IWD soil, and soilMatrix (soil in path just travelled)
	   nabla_soil = changeInSoil(i, currentNode, velocity)
	   soil_IWD = soil_IWD + nabla_soil 
	   soilMatrix[i][currentNode] -= nabla_soil
	   soilMatrix[currentNode][i] -= nabla_soil #added on 5sep2014
	   print("soilMatrix[{}][{}]".format(i, currentNode) + " = " + str(soilMatrix[i][currentNode]))

	   # update currentPath with the latest node
	   currentPath.append(currentNode)
	   print (currentPath)
	   
	  # send features on currentPath to svm to get 10-fold CV accuracy.
	  # this is done by creating a new dataset from the complete dataset containing only the target column and the selected features (points on currentPath)

	  #printing currentPath
	  print("currentPath: ")
	  for dummyVar1 in currentPath:
	   sys.stdout.write(str(dummyVar1) + " ")
	  print('')
	  currentData = original_features[:, currentPath]
	  clf = svm.SVC(kernel='linear', C=1)
	  scores = cross_validation.cross_val_score(clf, currentData, target, cv=10)
	  currentPathAcc = scores.mean() 
	  print ("currentPathAcc: ", currentPathAcc)
	  iterAccList.append(currentPathAcc)
	  #for dummyVar2 in pathAccList:
	  # sys.stdout.write(str(dummyVar2)+" ")
	  #print('')

	  # append currentPath to totalPaths. make iterBest if accuracy is greater than existing. Use iterBestAcc to store best CV %.
	  iterPaths.append(currentPath)iterAccList.append(currentPathAcc)
          
	  if(iterBestAcc < currentPathAcc):
	   iterBestAcc = currentPathAcc
	   iterBestPath = currentPath
           if(IWD_count == nIWD - 1):
	    sM_iterNext = soilMatrix #the best of an iteration will provide the soilMatrix for the next iteration

          IWD_count += 1


  # boost iterBestAcc path soil. (see below)

  for dummyVar1 in range(0, len(iterBestPath)-1):
   temp1 = soilMatrix[iterBestPath[dummyVar1]][iterBestPath[dummyVar1+1]]
   temp2 = soilMatrix[iterBestPath[dummyVar1+1]][iterBestPath[dummyVar1]]
   soilMatrix[iterBestPath[dummyVar1]][iterBestPath[dummyVar1+1]] *= 0.9
   soilMatrix[iterBestPath[dummyVar1]][iterBestPath[dummyVar1+1]] -= 0.1 * temp1
   soilMatrix[iterBestPath[dummyVar1+1]][iterBestPath[dummyVar1]] *= 0.9
   soilMatrix[iterBestPath[dummyVar1+1]][iterBestPath[dummyVar1]] -= 0.1 * temp2
	   
  totalPaths.append(iterPaths)
  globalBestAccList.append(iterBestAcc)
  if(iterBestAcc > globalBestAcc):
   globalBestAcc = iterBestAcc
   globalBestPath = iterBestPath
  iterCount += 1
 print("globalBestPath: ")
 for dummyVar3 in globalBestPath:
  sys.stdout.write(str(dummyVar3) + " ")
 print("")
 print("globalBestAcc: ", globalBestAcc)
 print("Exiting...")
