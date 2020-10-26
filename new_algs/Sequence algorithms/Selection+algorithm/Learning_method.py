#This file implement different learning method

import Problem
from sklearn.ensemble import RandomForestRegressor
import numpy as np

"""
This class implement a basicrandomforestregression
to predict algorithms performances
"""
class classical_forestRegression:
  def __init__(self, max_depth=20, random_state=0, n_estimators=100):
    self.regressor=RandomForestRegressor(max_depth=20, random_state=0, n_estimators=100)

  #this function take an item an instance (a problem) and return a two list X and Y of (input and output) (equal size of course !)
  def __transform_item__(self,input_type,item):
    X=[]
    Y=[]
    for parameters,dim,target,alg_performances,best,features,_ in item:
      if features==None and input_type=="features":
        raise Exception('Classical_forestRegression, no features', "problem : "+ str(parameters))
      if input_type=="parameters":
        X.append([dim,target]+parameters)
      if input_type=="features":
        X.append([dim,target]+features)
      Y.append(alg_performances)
    return X,Y

  #this function will train the learning method with X as input and Y as output
  def train(self,X,Y,input_size,output_size):
    nb_item=len(X)
    X=np.array(X)
    Y=np.array(Y)
    X.shape=(nb_item,input_size)
    Y.shape=(nb_item,output_size)
    self.regressor.fit(X,Y)

  def get_prediction_form(self):
    return "Id Best Algorithm Predicted"

  #this function make a simple prediction given the input features
  def predict(self,feat,input_size):
    features=np.array(feat)
    features.shape=(1,input_size)
    prediction=self.regressor.predict(features)
    return list(prediction[0]).index(min(list(prediction[0])))

  #this function will test all input in X on the previously regressor
  #return a matrix of size dimensions*targets which contains result
  def test(self,featList,input_size,dimensions,targets):
#    nb_item=len(featList)
#    X=np.array(featList)
#    X.shape=(nb_item,input_size)
    temp_result=[self.predict(i,input_size) for i in featList]
#    all_best=[list(prediction[0]).index(max(list(prediction[0]))) for prediction in temp_result]
    return [temp_result[x:x+targets] for x in range(0, len(temp_result), targets)]

