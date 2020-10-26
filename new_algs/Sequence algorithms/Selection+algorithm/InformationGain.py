# This function discretizes the given features into 3 categories
def discretize_feature(feature):
  import numpy as np
  mean=np.mean(feature)
  std=np.std(feature)
  discretized=np.copy(feature)
  
  discretized[np.where(feature<(mean+std/2)) ,]=2#within 1/2 std div
  discretized[np.where(feature>(mean-std/2)),]=2#within 1/2 std div
  
  discretized[np.where(feature>(mean+std/2)),]=0#greater than half
  discretized[np.where(feature<(mean-std/2)),]=1#less than half
  
  return discretized

class TargetClassException(Exception):
  pass

#Function for caculating entropy
def entropy(num_pos,num_neg):
  import numpy as np
  
  if num_pos!=0 and num_neg!=0:
    return -((num_pos/(num_pos+num_neg))*np.log2(num_pos/(num_pos+num_neg)))-((num_neg/(num_pos+num_neg))*np.log2(num_neg/(num_pos+num_neg)))
  elif num_pos==0 and num_neg!=0:
    return -((num_neg/(num_pos+num_neg))*np.log2(num_neg/(num_pos+num_neg)))
  elif num_pos!=0 and num_neg==0:
    return -((num_pos/(num_pos+num_neg))*np.log2(num_pos/(num_pos+num_neg)))
  else:
    return 0

  
"""
Call This function if you wish to find the information gain scores of the an attribute set called 'feature' against the discretized feature 'targetClass'
"""
def info_Gain(feature,targetClass):
  import numpy as np
  s=np.unique(targetClass)
  iG=[]
  if len(s)!=2:
    raise TargetClassException('This function only Works for 2-Class Classification Problems. %d Classes Found!'%(len(s)),s)
    
  S=entropy(len(np.where(targetClass==s[0])[0]),len(np.where(targetClass==s[1])[0]))
  #print("Entropy of whole dataset:",S)
  
  for x in feature:
    discrete_feature=discretize_feature(feature[x])
    gain=S
    for y in [0,1,2]:
      
      sv=len(np.where(discrete_feature==y)[0])
      numPos=len(np.where(targetClass[np.where(discrete_feature==y)[0]]==s[0])[0])
      numNeg=len(np.where(targetClass[np.where(discrete_feature==y)[0]]==s[1])[0])
      
     # print(numPos,numNeg)
     
      gain-=(sv/len(targetClass))*entropy(numPos,numNeg)
      
    iG.append(gain)
    #print(x,gain)
  return np.array(iG)