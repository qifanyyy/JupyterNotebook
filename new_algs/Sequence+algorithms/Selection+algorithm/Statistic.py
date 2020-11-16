# This file implement somes statistics about a trained and tested EPM

import Problem
import epm

#This function compute the Single Best Solver (SBS) of all problems for all targets mixed
#the SBS is the algorithms that have the minimal average ERT for all problems.
#It may lost it's meaning when we compute it over different targets
#input : epm
def SingleBestSolver(epm):
  data=epm.training_set+epm.testing_set
  algorithms=data[0].algorithms
  ERT_Algorithms=[0 for i in algorithms]
  nb_config=0
  for problem in data:
    for _,_,_,config,_,_,_ in problem:
      nb_config+=1
      for i,ERT in enumerate(config):
        ERT_Algorithms[i]+=ERT

  average_ERT=[(alg,ERT_Algorithms[i]/nb_config) for i,alg in enumerate(algorithms)]
  best,ert=min(average_ERT ,key=lambda x:x[1])
  return int(ert)

#This function compute the Virtual Best Solver (VBS) of all problems for all targets mixed
#the VBS is the ERT to solve all instances by a perfect EPM that always predict the fastest algorithm.
#It may lost it's meaning when we compute it over different targets
#input : epm
def VirtualBestSolver(epm):
  data=epm.training_set+epm.testing_set
  ERT=0
  nb_config=0
  for problem in data:
    for _,_,_,config,_,_,_ in problem:
      nb_config+=1
      ERT+= min(config)
  vbs=ERT/nb_config
  return int(vbs)

#This function compute the cost of the real solver (RS) to solve all problems in the training set.
#It may lost it's meaning when we compute it over different targets
#input : epm
def RealSolver(epm):
  data=epm.testing_set
  ERT=0
  nb_config=0
  for problem in data:
    for _,_,_,config,_,_,prediction in problem:
      nb_config+=1
      ERT+= config[prediction]
  rs=ERT/nb_config
  return int(rs)

#This function compute the Merit of the EPM: closer to 0, closer is the EPM to the VBS,
#if the Merit > 1 then using the SBS is better than using the model
def Merit(sbs,vbs,rs):
  a=rs-vbs
  b=sbs-vbs
  Merit=a/b
  return Merit
