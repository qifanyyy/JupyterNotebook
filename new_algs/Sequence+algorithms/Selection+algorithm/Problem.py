# This file contains basic class to store problems efficiently for the training
"""
if __name__ == "__main__":
  NB_PARAMETERS=4
  NB_DIMENSIONS=5
  DIMENSION_LIST=[16,20,32,40,50]
  NB_TARGETS=5
  TARGET_LIST=[0.5,0.75,0.90,0.95,1.0]
  NB_ALGORITHMS=9
  ALGORITHMS=["(1+(lda_lda))","(1+1)EA","(1+10)EA1","(1+10)EA3","(1+10)FGA","(1+2)EA","1hill","2hill","RandomSearch"]
"""
class Problem:
  #instanciate problem in a tree structure:
  # problem parameters (dummy, neutrality, epistasis, ruggedness)
  #					/	|	\
  # dimensions 			[d1, d2, ... , dk]
  #				/	|	\
  # targets		[0.5, 0.75, ..., 0.95, 1]
  #			/	|	\
  #algorithms
  # performances [ERT_alg1, ... ,  ... ]
  #
  #Input :
  # parameters : integers array of the size NB_PARAMETERS
  # dimensions : integers array of the size NB_DIMENSIONS
  # targets : integers array of the size NB_TARGETS
  # alg_performances: matrix of size NB_DIMENSIONS*NB_TARGETS*NB_ALGORITHMS
  # each cells of the form
  def __init__(self,ALGORITHMS,parameters,dimensions,targets, alg_performances):
    self.parameters=parameters
    self.algorithms=ALGORITHMS
    self.dimensions=dimensions
    self.targets=targets
    self.performances=alg_performances

    #best algorithm:
    self.bests=[[None for i in self.targets] for j in self.dimensions]
    for i,_ in enumerate(self.dimensions):
      for j,_ in enumerate(self.targets):
        self.bests[i][j]=self.performances[i][j].index(min(self.performances[i][j]))
    #predicted algorithms
    self.predictions=[[None for i in self.targets] for j in self.dimensions]

    #features
    #if features are not link to the problems, used features for the epm will be the parameters of the problem (confer White Box model)
    self.features=[None for j in self.dimensions]


  def __str__(self):
    res="\n-------------------------------------------------\nAlgorithms : "+str(self.algorithms)
    res+="\n-------------------------------------------------\nProblem : "+str(self.parameters)
    res+="\n\tDimensions : "+str(self.dimensions)
    res+="\n\tTargets : "+str(self.targets)
    res+="\n"
    res+="\nBest algorithms for all targets:\n"
    for id,i in enumerate(self.dimensions):
      res+="dim "+str(i)+"  |  "+str(self.bests[id])+"\n"
    res+="\n"
    res+="\nPredicted algorithms for all targets:\n"
    for id,i in enumerate(self.dimensions):
      res+="dim "+str(i)+"  |  "+str(self.predictions[id])+"\n"
    res+="\n-------------------------------------------------\n"
    return res

    #iteration over dimensions and targets
    #return parameters, actual dimension, actual target, algorithms performances for the actual dim and actual target, the best and features
  def __iter__(self):
    #iterators variables
    self.__index__=(0,0)
    self.__loopEnd__=0
    return self
  def __next__(self):
     a,b=self.__index__
     if (a,b)==(0,0) and self.__loopEnd__==1:
       self.__loopEnd__=0
       raise StopIteration
     NB_TARGETS=len(self.targets)
     NB_DIMENSIONS=len(self.dimensions)
     if b<NB_TARGETS-1:
       self.__index__=(a,b+1)
       return (self.parameters,self.dimensions[a],self.targets[b],self.performances[a][b],self.bests[a][b], self.features[a],self.predictions[a][b])
     elif ((b==NB_TARGETS-1) and (a<NB_DIMENSIONS-1)):
       self.__index__=(a+1,0)
       return (self.parameters,self.dimensions[a],self.targets[b],self.performances[a][b],self.bests[a][b], self.features[a],self.predictions[a][b])
     elif ((b==NB_TARGETS-1) and (a==NB_DIMENSIONS-1)):
       self.__index__=(0,0)
       self.__loopEnd__=1
       return (self.parameters,self.dimensions[a],self.targets[b],self.performances[a][b],self.bests[a][b], self.features[a],self.predictions[a][b])

  #link existing features to a problem
  def link_features(self,parameters,dimensions,features):
    assert self.parameters==parameters
    assert self.dimensions==dimensions
    assert len(features)==len(dimensions)
    self.features=features

  #link a list of problem to their features
def link_all_features(ProblemList,ParametersList,DimensionsList,FeaturesList):
  assert len(ProblemList)==len(ParametersList)
  assert len(ProblemList)==len(DimensionsList)
  assert len(ProblemList)==len(FeaturesList)
  for i, problem in enumerate(ProblemList):
    problem.link_features(ParametersList[i],DimensionsList[i],FeaturesList[i])
 
