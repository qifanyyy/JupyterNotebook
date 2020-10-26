# -*- coding: utf-8 -*-
"""
COMP 551 A2

Author: Shatil Rahman
ID:     260606042

Contains the algorithm for the 2-class Probabilistic LDA
"""

import numpy as np
import matplotlib.pyplot as plt
import performance as perf

def loadData(fname):
    data = np.loadtxt(fname, delimiter=',',dtype=float)
    X = data[:,:-1]
    Y = data[:,-1].reshape((X.shape[0],1))
    
    return [X, Y]
    
def estimate_priorY(Y):
    #Estimate prior probabilities of the 2 classes, P(y_k)
    n0 = 0
    n1 = 0
    for i in range(0,Y.shape[0]):
        if(Y[i] == 1):
            n0 = n0 + 1
        else:
            n1 = n1 + 1
        
    p_y0 = n0/(float(n0+n1))
    p_y1 = n0/(float(n0+n1))
    
    return p_y0,p_y1
    
def estimate_means(X,Y):
    #Estimate the means of the Conditional Probabilities P(x|y_k)
    n0 = 0.0
    n1 = 0.0
    sums0 = np.zeros((X.shape[1]))
    sums1 = np.zeros((X.shape[1]))
    for i in range(0,X.shape[0]):
        if(Y[i] == 1):
            n0 = n0 + 1
            sums0 = sums0 + X[i,:].T
        else:
            n1 = n1 + 1
            sums1 = sums1 + X[i,:].T
        
    mu_0 = sums0/n0
    mu_1 = sums1/n1
    
    return mu_0, mu_1
    
   
def estimate_cov(X,Y,mu_0,mu_1):
    #Estimate the (Shared) Covariance Matrix of the Conditional Probabilities
    n0 = 0.0
    n1 = 0.0
    S0 = np.zeros((mu_0.shape[0], mu_0.shape[0]))
    S1 = np.zeros((mu_0.shape[0], mu_0.shape[0]))
    
    
    
    for i in range(0,X.shape[0]):
        if(Y[i] == 1):
            n0 = n0 + 1
            temp = X[i,:].T - mu_0
            temp = temp.reshape(temp.shape[0],1)
            S0 = S0 + np.dot(temp, temp.T)
            
        else:
            n1 = n1 + 1
            temp = X[i,:].T - mu_1
            temp = temp.reshape(temp.shape[0],1)
            S1 = S1 + np.dot(temp, temp.T)
            
    S = S0 + S1
    Cov = S/(n0+n1)
    
    return Cov
    
def LDA(X_train, Y_train):
    #Trains the LDA Classifier, returns the weights of the decision boundary
    #as W0 and W1
    #Each of X_train must be a sample
    p_y0, p_y1 = estimate_priorY(Y_train)
    mu_0, mu_1 = estimate_means(X_train,Y_train)
    Cov = estimate_cov(X_train,Y_train,mu_0,mu_1)
    
    mu_0 = mu_0.reshape(mu_0.shape[0],1)
    mu_1 = mu_1.reshape(mu_1.shape[0],1)
    
    inv_Cov = np.linalg.inv(Cov)
    
    diff_priors = np.log(p_y0) - np.log(p_y1)
    
    Quad0 = np.linalg.multi_dot((mu_0.T,inv_Cov,mu_0))
    Quad1 = np.linalg.multi_dot((mu_1.T,inv_Cov,mu_1))
    
    W0 = diff_priors - 0.5*Quad0 + 0.5*Quad1
    W1 = np.dot(inv_Cov, (mu_0 - mu_1))
    
    return W0, W1
    
def predict(W0,W1, x):
    #make prediction for 1 sample
    # x must be a row vector (ie (1,n) shape)
    if(W0 + np.dot(x,W1)) > 0:
        return 1.0
    else:
        return -1.0
    

def predictNsamples(W0,W1,X):
    Y_predicted = np.empty((X.shape[0],1))
    for i in range(0, X.shape[0]):
        x = X[i,:]
        Y_predicted[i] = predict(W0,W1,x)
    return Y_predicted
       
       
       

X_train, Y_train = loadData('DS2_training.csv')
X_test,Y_test = loadData('DS2_test.csv')
W0,W1 = LDA(X_train,Y_train)
Y_predicted = predictNsamples(W0,W1,X_test)

accuracy, precision, recall, f1_score = perf.evaluate(Y_test, Y_predicted)
print "Performance of Probabilistic LDA:"
print "Accuracy: " + str(accuracy)
print "Precision: " + str(precision)
print "Recall: " + str(recall)
print "f1_score: " + str(f1_score)




    


    

    
'''
#Just testing with 2 features
m0 = [1.3, 1.3]
m1 = [2.30, 4.0]

cov = np.array([[0.5, -1.3], [-1.3, 5.6]])

 
DS1_pos = np.random.multivariate_normal(m0,cov,size=(2000))
pos = 1.0*np.ones((2000,1))
DS1_pos = np.concatenate((DS1_pos,pos),axis=1)
DS1_neg = np.random.multivariate_normal(m1,cov,size=(2000))
neg = -1.0*np.ones((2000,1))
DS1_neg = np.concatenate((DS1_neg,neg),axis=1)
DS1_training = np.concatenate((DS1_pos[600:,:], DS1_neg[600:,:]))
X_train = DS1_training[:,:-1]
Y_train = DS1_training[:,-1].reshape((X_train.shape[0],1))

W0,W1 = LDA(X_train,Y_train)

y1 = -1.0*(W0/(W1[1])) - (W1[0]/W1[1]) * 1.0
y2 = -1.0*(W0/(W1[1])) - (W1[0]/W1[1]) * 5.0

y = []
y.append(y1[0,0])
y.append(y2[0,0])
print y
x = [1.0, 5.0]
plt.plot(DS1_pos[:,0], DS1_pos[:,1], 'bo')
plt.plot(DS1_neg[:,0], DS1_neg[:,1], 'ro')
plt.plot(x, y, 'g-' )
plt.show
'''





