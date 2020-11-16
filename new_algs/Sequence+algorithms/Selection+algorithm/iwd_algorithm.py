'''
A program to pick the n best features of a dataset, out of m (m > n), using the intelligent drop algorithm.

Algorithm: The intelligent water drop algorithm is similar to the ant colony optimization (ACO) algorithm. 

Last edited : 14 Sep 2014
Modification to IWD original: For random number r, if:
 r1 >= r >= 0 : use infogain rankings in place of probabilities
 r2 >= r >= r1: use linear or exponential ranking (based on user input)
  1 >= r >= r2: use exploitation. select the node with the least soil
'''
import numpy as np
import sklearn
from sklearn import cross_validation
from sklearn import datasets
from sklearn import svm
import random
import sys
import argparse
#import time
#import os
#import subprocess

# Parsing commandline arguments using argparse
parser = argparse.ArgumentParser(description='Example:\npython iwd_algorithm.py datasets/wine.csv datasets/wine.csv.infogain 5 10 100 0.3 0.7 --linear 1.5 rbf 100 0.1 10 1.0 0.01 1 1 1.0 0.01 1 2 0.9 0.9 0.001 3 100')
parser.add_argument("dataset_filename", help="the dataset csv file (class label in the first column, and features in the other columns)")
parser.add_argument("infogain_filename", help="the the infogain (txt/csv) file containing only infogain rankings (one column only) of features sorted according to feature number")
parser.add_argument("final_no_of_features", help="the final no. of features to be selected", type=int)
parser.add_argument("nIWD", help="Number of IWDs", type=int)
parser.add_argument("nIter", help="Number of iterations", type=int)
parser.add_argument("r1", help="value between 0 and 1 below which infogain rankings are used as probability for selecting next node", type=float)
parser.add_argument("r2", help="value between 0 and 1 above which exploitation is done (the path with lease soil is selected)", type=float)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--linear', help="linear ranking selection (of next node)", action="store_true")
group.add_argument("--exponential", help="exponential ranking selection (of next node)", action="store_true")
group.add_argument("--fps", help="fitness proportionate selection (of next node)", action="store_true")
parser.add_argument("selection_pressure", type=float, help="For linear rankking: 1 <= selection_pressure <= 2\nFor exponential ranking: 0 < selection_pressure < 1\nFor fitness proportionate selection (fps), enter any value")
parser.add_argument("svm_kernel", help="Enter the type of SVM kernel to use: linear, rbf, etc.")
parser.add_argument("svm_C", help="Enter the SVM penalty parameter of the error term (normally 1.0)", type=float)
parser.add_argument("svm_gamma", type=float, help="Kernel coefficient for 'rbf', 'poly' and 'sigmoid'. If gamma is 0.0 then 1/nfeatures will be used instead.")
parser.add_argument("svm_cv_folds", type=int, help="number of cross validation folds")
parser.add_argument("a_v", type=float, help="a_v term in velocity update parameter (try 1.0)")
parser.add_argument("b_v", type=float, help="b_v term in velocity update parameter (try 0.01)")
parser.add_argument("c_v", type=float, help="c_v term in velocity update parameter (try 1.0)")
parser.add_argument("alpha", type=int, help="alpha term in velocity update parameter (try 1)")
parser.add_argument("a_s", type=float, help="a_s term in soil update parameter (try 1.0)")
parser.add_argument("b_s", type=float, help="b_s term in soil update parameter (try 0.01)")
parser.add_argument("c_s", type=float, help="c_s term in soil update parameter (try 1.0)")
parser.add_argument("theta", type=int, help="theta term in soil update parameter (try 2)")
parser.add_argument("rho_s", type=float, help="rho_s : soil update coefficient (try 0.9)")
parser.add_argument("rho_IWD", type=float, help="rho_IWD : soil update coefficient (try 0.9)")
parser.add_argument("epsilon_s", type=float, help="term in denominator to prevent zero division (try 0.001)")
parser.add_argument("weight_infogain", type=int, help="int term to multiply infogain with")
parser.add_argument("initialVelocity", type=float, help="float term for initial velocity of IWD")

args = parser.parse_args()

# Import dataset (NOTE: dataset should have class/label in first column)
original_dataset = np.genfromtxt(args.dataset_filename, delimiter=',', skip_header=1)
nodes = len(original_dataset[1,:]) - 1
target = original_dataset[:,0]
original_features = original_dataset[:,1:]
infogain = np.genfromtxt(args.infogain_filename)

final_no_of_features = args.final_no_of_features

# Initialization of static parameters
iterCount = 0 # no. of iterations finished as of now
nIWD = args.nIWD # no. of water drops
nIter = args.nIter

totalPaths = []
totalAccList = []
# define iterPaths = [] at the beginning of every iter
iterBestPaths = []
globalBestAccList = []
globalBestAcc = 0
globalBestPath = []

#Velocity-update parameters
a_v = args.a_v
b_v = args.b_v
c_v = args.c_v 
alpha =  args.alpha 

#Soil-update parameter
a_s =  args.a_s# soil-updating parameter (maybe reduce this value? a_s)
b_s = args.b_s
c_s = args.c_s
theta = args.theta


rho_s = args.rho_s
rho_IWD = args.rho_IWD #global soil-updating parameter

epsilon_s = args.epsilon_s # to prevent zero division

# w_1, w_2, w_3 in paper
weight_infogain = args.weight_infogain  # for weighted gene ranking used in computing time(i,j)

selection_pressure = args.selection_pressure

# SVM parameters
svm_kernel = args.svm_kernel
svm_C = args.svm_C
svm_gamma = args.svm_gamma
svm_cv_folds = args.svm_cv_folds

# Initialization of dynamic parameters
soilMatrix = np.identity(nodes)
soilMatrix.fill(1000)


for a in range(nodes):	# Precaution: Increase the soil for a node to itself so as to have little probability of picking itself
 soilMatrix[a][a]=sys.maxsize

#probMatrix = np.identity(nodes)
#probMatrix.fill(0)

initialVelocity = args.initialVelocity # Initial velocity of each IWD
velocity = initialVelocity

unvisited = range(nodes) # List of cities not visited, initially this 
			 # contains even the initial node.

# Parameters to be updated after every node
#minSoil = 0 # Run through all the nodes remaining in unvisited & update with the the minimum soil in path. So the checking would proceed as soil[currentNode,nextNodeWithMinSoilBetween]

# Function definitions

def f(x,y):
 minOfSoilMatrix = np.amin(soilMatrix)
 if(minOfSoilMatrix>=0):
  #print np.amin(soilMatrix)
  return 1.0/(epsilon_s + (soilMatrix[x][y]))
 else:
  #print min(soilMatrix) 
  return 1.0/(epsilon_s + (soilMatrix[x][y] - minOfSoilMatrix))

def linear_ranking_prob(N, selection_pressure, i):
 return ( selection_pressure - ( (2*(selection_pressure-1)) * float(i-1)/(N-1) ) ) / N

def exponential_ranking_prob(N, selection_pressure, i):
 return (selection_pressure**(i-1)) * float(1-selection_pressure)/float(1-selection_pressure**N)

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
 return a_v/(b_v + (c_v * (soilMatrix[x][y])**(2*alpha)) )

def time(v, nextNode):
 #return 1.0/((weight_infogain*infogain[nextNode]) + v)
 return 1.0/(v)

def changeInSoil(x,y,vel):
 return a_s/(b_s + (c_s * time(vel, y)**(2*theta) ) )

#This function updates the soilMatrix corresponding to the tour passed to it
def globalTourSoilUpdate(tour, soil_of_IWD):
 for dM in range(0, len(tour)-1):
  soilMatrix[tour[dM]][tour[dM+1]] = (rho_s * soilMatrix[tour[dM]][tour[dM+1]] ) - ((rho_IWD * soil_of_IWD)/(len(tour) - 1) )
  soilMatrix[tour[dM+1]][tour[dM]] = (rho_s * soilMatrix[tour[dM+1]][tour[dM]] ) - ((rho_IWD * soil_of_IWD)/(len(tour) - 1) )


########
if __name__ == '__main__':
 print("---")
 print ("total_no_of_features: ", nodes)
 print ("final_no_of_features: ", final_no_of_features)
 print ("nIWD: ", nIWD,)
 print ("nIter", nIter,)
 print ("ranking selection: ",)
 if(args.fps):
  print ("fitness proportionate selection")
 elif(args.linear):
  print ("linear ranking selection, selection_pressure: ", selection_pressure)
 elif(args.exponential):
  print ("exponential ranking selection, selection_pressure: ", selection_pressure)
 print ("SVM parameters: kernel: ", svm_kernel, ", C = ", svm_C, ", gamma = ", svm_gamma, ", CV = ", svm_cv_folds)

 sM_iter = soilMatrix
 sM_iterNext = soilMatrix
 while(iterCount<nIter): # one run of this loop is nIWD drops building a solution, all using the same soilMatrix
  
  IWD_count = 0
  totalPaths.append([])
  totalAccList.append([])
  iterPaths = [] # paths of one iteration
  iterBestAcc = 0
  iterBestPath = []
  iterAccList = []
  iterIWDSoils = []
  
  sM_iter = sM_iterNext
  while(IWD_count < nIWD): # one run of this loop is one drop building a complete solution
	  soilMatrix = sM_iter
	  unvisited = range(nodes)
	  currentNode = random.choice(unvisited) # pick a random start
          #print currentNode
	  unvisited.remove(currentNode)
	  currentPath = []
	  currentPath.append(currentNode)
	  velocity = initialVelocity
	  soil_IWD = 0.0
	  iterAccList = []
	  print("iterCount: {},IWD_count: {}".format(iterCount, IWD_count))
	  while(len(unvisited)>(nodes - final_no_of_features)): #every run of this loop adds a node to the solution path
	   #print(velocity)
	   i = currentNode
	   
	   # Infogain for prob. vs. Exploration (via linear or exponential) vs. Exploitation
	   randomNumber = random.random()
	   if(randomNumber < args.r1): # Use infogain for prob.
	    ListOfWProb=[]
	    #print "Infogain: ", infogain
	    for j in infogain:
	     ListOfWProb.append(j)
	     #dM = ListOfWProb.index(j)
	    for dM in currentPath:
	     ListOfWProb[dM]=0
	    currentNode=weighted_choice(ListOfWProb)
	    unvisited.remove(currentNode)
	   elif(randomNumber < args.r2): # Use exploration via fitness proportionate selection / linear / exponential ranking
	    if(args.fps): # fitness proportionate selection (fps)
	     ListOfWProb = [1.0/sys.maxsize]*nodes
	     for j in unvisited:
	      ListOfWProb[j]=f(i,j)
	    else: # linear or exponential ranking selection
             Dict={}
	     for j in unvisited:
	      Dict[j]=soilMatrix[currentNode][j]

	     ranked_nodes = sorted(Dict, key=Dict.get)
	     ListOfWProb = []
	     for k in range(0,len(ranked_nodes)):
	      if(args.linear): # linear ranking selection
	       ListOfWProb.append(linear_ranking_prob(len(ranked_nodes), args.selection_pressure, k+1))
	      elif(args.exponential): # exponential ranking selection
	       ListOfWProb.append(exponential_ranking_prob(len(ranked_nodes), args.selection_pressure, k+1))
	     #elif(args.fps):
	     # ListOfWProb=[1.0/sys.maxsize]*nodes
	     # for j in unvisited:
	     #  ListOfWProb

	    Index=weighted_choice(ListOfWProb)
	    currentNode = ranked_nodes[Index]
	    unvisited.remove(currentNode)
	     
	   else: # Exploitation: pick node with lease soil in between
	    Dict={}
	    for j in unvisited:
	     Dict[j]=soilMatrix[currentNode][j]
	    ranked_nodes = sorted(Dict, key=Dict.get)
	    currentNode = ranked_nodes[0]
	    unvisited.remove(currentNode)
	   
	   
	   # update velocity of IWD
	   velocity = velocity - changeInVelocity(i, currentNode) #remember, i and currentNode are no longer same

	   # update IWD soil, and soilMatrix (soil in path just travelled)
	   nabla_soil = changeInSoil(i, currentNode, velocity)
	   soil_IWD = soil_IWD + nabla_soil 
	   soilMatrix[i][currentNode] -= nabla_soil
	   soilMatrix[currentNode][i] -= nabla_soil #added on 5sep2014
	   #print("soilMatrix[{}][{}]".format(i, currentNode) + " = " + str(soilMatrix[i][currentNode]))

	   # update currentPath with the latest node
	   currentPath.append(currentNode)
	   #print currentPath
	   
	  # send features on currentPath to svm to get 10-fold CV accuracy.
	  # this is done by creating a new dataset from the complete dataset containing only the target column and the selected features (points on currentPath)

	  #printing currentPath
	  #print "currentPath", currentPath,
	  #print("currentPath: ")
	  #for dummyVar1 in currentPath:
	  # sys.stdout.write(str(dummyVar1) + " ")
	  #print('')
	  currentData = original_features[:, currentPath]
	  if(svm_kernel=='linear'):
	   clf = svm.SVC(kernel=svm_kernel)
	  else:
	   clf = svm.SVC(kernel=svm_kernel, C=svm_C, gamma=svm_gamma)
	  scores = cross_validation.cross_val_score(clf, currentData, target, cv=10)
	  currentPathAcc = scores.mean() 
          #print "currentPathAcc: ", currentPathAcc, "+/- Standard deviation: ", scores.std()
	  #for dummyVar2 in pathAccList:
	  # sys.stdout.write(str(dummyVar2)+" ")
	  #print('')

	  # append currentPath to totalPaths. make iterBest if accuracy is greater than existing. Use iterBestAcc to store best CV %.
	  iterPaths.append(currentPath)
          iterAccList.append(currentPathAcc)
	  totalPaths[iterCount].append(currentPath)
          
	  if(iterBestAcc <= currentPathAcc):
	   iterBestIWDIndex = IWD_count
	   iterBestAcc = currentPathAcc
	   iterBestPath = currentPath

	  iterIWDSoils.append(soil_IWD)

	  # Global soil update (occurs at the end of an iteration)
	  # Update the soilMatrix values corresponding to the top 3 paths
	  # Here's how it is done:
	  # copy iterAccList to dispensibleIterAccList. Get the index of the highest accuracy using index(max(dispensibleIterAccList)). Call globalTourSoilUpdate(iterPaths[index(max(dispensibleIterAccList))], iterIWDSoils[index(max(dispensibleIteraccList))]) and then change that tour's accuracy in the dispensible list to 0. Call globalTourSoilUpdate again, this time the soils of the second highest accuracy will be updated. Change that tour's acc. to 0. Call again. This will update the 3rd best tour
	  if(IWD_count == nIWD-1):
	   #print "iterPaths:", iterPaths
	   #print "iterIWDSoils:", iterIWDSoils
	   print "iterBestAcc: ", iterBestAcc
	   print "iterBestAcc (via iterAccList[iterBestIWDIndex]): ", iterPaths[iterBestIWDIndex]
	   #print "iterBestAcc (via totalAccList[iterCount][iterBestIWDIndex]a): ", totalAccList[iterCount][iterBestIWDIndex]
	   #print "iterAccList:", iterAccList
	   dispensibleIterAccList = iterAccList
	   #print "dispensibleIterAccList: ", dispensibleIterAccList

	   iii = dispensibleIterAccList.index(max(dispensibleIterAccList))
	   #print "iii: ", iii
	   print "iterPaths[{}] = {}".format(iii, iterPaths[iii])
	   #print "iterIWDSoils[{}]={}".format(iii, iterIWDSoils[iii])
	   globalTourSoilUpdate(iterPaths[iii], iterIWDSoils[iii])
	   dispensibleIterAccList[iii] = 0
	   #sM_iterNext = soilMatrix #best of iteration will provide soilMatrix for next iteration

	   # second best of iteration
	   iii = dispensibleIterAccList.index(max(dispensibleIterAccList))
	   #print "iii: ", iii
	   #print "iterPaths[{}] = {}".format(iii, iterPaths[iii]) 
	   #print "iterIWDSoils[{}]: {}".format(iii, iterIWDSoils[iii])
	   globalTourSoilUpdate(iterPaths[iii], iterIWDSoils[iii])
	   dispensibleIterAccList[iii] = 0
	   
	   # third best of iteration
	   iii = dispensibleIterAccList.index(max(dispensibleIterAccList))
	   #print "iii: ", iii
	   #print "iterPaths[{}] = {}".format(iii, iterPaths[iii])
	   #print "iterIWDSoils[{}]={}".format(iii, iterIWDSoils[iii])
	   globalTourSoilUpdate(iterPaths[iii], iterIWDSoils[iii])
	   dispensibleIterAccList[iii] = 0
	   sM_iterNext = soilMatrix #providing the soilMatrix for next iteration

          IWD_count += 1


  # boost iterBestAcc path soil. (see below)

  #for dummyVar1 in range(0, len(iterBestPath)-1):
  # temp1 = soilMatrix[iterBestPath[dummyVar1]][iterBestPath[dummyVar1+1]]
  # temp2 = soilMatrix[iterBestPath[dummyVar1+1]][iterBestPath[dummyVar1]]
  # soilMatrix[iterBestPath[dummyVar1]][iterBestPath[dummyVar1+1]] *= 0.9
  # soilMatrix[iterBestPath[dummyVar1]][iterBestPath[dummyVar1+1]] -= 0.1 * temp1
  # soilMatrix[iterBestPath[dummyVar1+1]][iterBestPath[dummyVar1]] *= 0.9
  # soilMatrix[iterBestPath[dummyVar1+1]][iterBestPath[dummyVar1]] -= 0.1 * temp2
	   
  totalPaths.append(iterPaths)
  globalBestAccList.append(iterBestAcc)
  if(iterBestAcc >= globalBestAcc):
   globalBestAcc = iterBestAcc
   globalBestPath = iterBestPath
  iterCount += 1
 print("globalBestPath: ", globalBestPath)
 print("")
 print("globalBestAcc: ", globalBestAcc)

 ###
 print "Checking to cross validation accuracy on globalBestPath: "
 if(svm_kernel=='linear'):
  clf=svm.SVC(kernel='linear')
 else:
  clf=svm.SVC(kernel=svm_kernel, C=svm_C, gamma=svm_gamma)
 currentData = original_features[:, globalBestPath]
 scores = cross_validation.cross_val_score(clf, currentData, target, cv=svm_cv_folds)
 print "Mean CV accuracy: ", scores.mean()
 
 ###
 #print("Using the globalBestPath features for constructing SVM model...")
 #trainingDataSubset = original_dataset[:,globalBestPath]
 #clf = svm.SVC(kernel="linear", C=1)
 #clf.fit(trainingDataSubset, target)
 #print("SVM model ready for training subset...")
 # Now, load the test dataset. as testDataSubset and testTarget
 # testDatasubset = test_data[:,globalBestPath]
 #test_data = np.genfromtxt('datasets/coepra/coepra_test.csv', delimiter=',', skiprows=1)
 #test_data = test_data[:,1:]
 #nodes_test = len(test_data[0,:] - 1)
 #testDataSubset = test_data[:,nodes-1]
 print("---")
