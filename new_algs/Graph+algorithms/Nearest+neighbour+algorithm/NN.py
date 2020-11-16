import numpy as np

class NearestNeighbour:
  def _init_(self):
    pass

  def train(self, X, y):
    """ X is NxD where each row is an example. Y is a 1 dimension of size N"""
    #Nearest neighbour classifier remembers all data
    self.Xtr= X
    self.ytr= y

  def predict(self, X):
    """ X is NxD where each row is an example we wish to predict label for"""
    num_test = X.shape[0]
    #Making sure output type matches input type
    Ypred = np.zeros(num_test, dtype = self.ytr.dtype)


  #loop over all test rows
  for i in xrange(num_test):
    #find nearest training image to i-th test image
    #using L1 distance(Absolute sum of differences)
    distances = np.sum(np.abs(self.Xtr - X[i,:]), axis=1)
    min_index = np.argmin(distances)#get index with smallest distance
    Ypred[i] = self-ytr[min_index]#Predict label of nearest example

  return Ypred
