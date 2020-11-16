'''   
from epsilon value 0.0000003, less than this
value results in lower False alarm rate,
but lower detection rate
The detection rate for said epsilon is 0.6968, false alarm rate of 0.20
you can fine-tune the model by adjusting epsilon
@Min Zhe
'''

import pandas as pd 
import numpy as np
from scipy.stats import multivariate_normal 
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

pd.set_option('display.expand_frame_repr', False)
file = "SWaT_Dataset_Normal_v1.csv"
data = pd.read_csv(file)

NormAttList = data["Normal/Attack"]
data = data.drop([" Timestamp","Normal/Attack"], axis =1)
standardscaler = preprocessing.StandardScaler()

def estimateGaussian(dataset):
    mu = np.mean(dataset, axis=0)
    sigma = np.cov(dataset.T)
    return mu, sigma

def multivariateGaussian(dataset,mu,sigma):
    p = multivariate_normal(mean=mu, cov=sigma, allow_singular=True)
    return p.pdf(dataset)

#data2 = pd.read_csv("SWaT_Dataset_Attack_v0.csv")
#validationlist =  data2["Normal/Attack"]
#validationlist_numeric = [1 if i=="Attack"  else 0 for i in validationlist]
#data2 = data2.drop(["Normal/Attack"], axis = 1)
mu, sigma = estimateGaussian(data) # these are the "model"

#yval = multivariateGaussian(data2, mu, sigma)
#best_epi, bestF1 = selectThreshHold(validationlist_numeric, yval)

datatest = pd.read_csv("validation.csv")
y_test =  datatest["Normal/Attack"]

y_test_attack = np.array([val == 'Attack' for val in y_test])
y_test_normal = np.array([val == 'Normal' for val in y_test])

datatest = datatest.drop(["Normal/Attack"], axis = 1)
x_test = multivariateGaussian(datatest, mu, sigma)


epsilon = 0.0000003

bestdetection = 0
bestEpsilon = 0
bestfalsealarm = 1

stepsize =  0.000003
epslist = np.arange(epsilon, 1, stepsize)

for j in epslist:
    a = ([i<j for i in x_test])
    b = ([i>=j for i in x_test])
    TP = (np.sum(a & y_test_attack)) # True Positive
    FP = (np.sum(a & y_test_normal)) # False Positive
    TN = (np.sum(b & y_test_normal)) # True Negative
    FN = (np.sum(b & y_test_attack)) # False Negative
    detecttest = TP/(TP+FN)
    falsealarmtest = FP/(FP+TN)
    if falsealarmtest < bestfalsealarm or detecttest > bestdetection: 
        bestdetection = detecttest 
        bestfalsealarm = falsealarmtest
        bestEpsilon = j
        print(bestEpsilon)
        print("False alarm rate = ", bestfalsealarm )
        print("Detection rate = ", bestdetection)
 
