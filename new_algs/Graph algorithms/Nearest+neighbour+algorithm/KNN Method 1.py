import numpy as np
import matplotlib.pyplot as plt
import operator
from collections import  Counter
import seaborn as sns

def Data_Preperation():
    #Preparing Data

    mu=np.array([8,11])
    sigma=np.array([[1,1],[1,2]])
    samples1=100
    class1=np.random.multivariate_normal(mu,sigma,100)   #drawing samples from gaussian distribution

    samples2=80
    low=0
    high=1
    class2=np.zeros((80,2))
    #drawing samples from uniform distribution    
    for i in range(80):
        class2[i,0] = np.random.uniform(8,13)
        class2[i,1] = np.random.uniform(6,12)
        
    data = np.concatenate((class1,class2))
    #data = data.reshape(data.shape[0],1)
    label=np.empty(shape=(180,1))                    #Classes for training data
    label[0:samples1,:]=1
    label[samples1+1:samples1+samples2,:]=2


    return data, label

def euclid_dist(a, b):
    
    if len(a) != len(b):
        return False
    else:
        dist = 0
        for i in range(len(a)):
            dist += (a[i] - b[i])**2
        return np.sqrt(dist)
    

def KNN(data, gen, label):
    
    K = 11
    data_label = []
    
    for i in range(len(data)):
        dists = []
        for j in range(len(gen)):
            dists.append([euclid_dist(gen[j],data[i]),j])
        dists.sort()
        
        total = 0.0
        for j in dists[:K]:
            total += label[j[1]]
        if total/K <= 1.5:
            data_label.append(1)
        else:
            data_label.append(2)
            
    return data_label


def Main():
    x = np.linspace(5.0, 14.0, 100)
    y = np.linspace(5.0, 16.0,100)
    X, Y = np.meshgrid(x, y)            
    mu=np.array([8,11])
    sigma=np.array([[1,1],[1,2]])
    samples1=100
    class1=np.random.multivariate_normal(mu,sigma,100)   #drawing samples from gaussian distribution
    
    samples2=80
    class2=np.zeros((80,2))
    #drawing samples from uniform distribution    
    for i in range(80):
        class2[i,0] = np.random.uniform(8,13)
        class2[i,1] = np.random.uniform(6,12)    
    data_set = np.concatenate((class1,class2))
    
    data = [[] for i in range(10000)]
    for i in range(10000):
        data[i] = [5 + 9/100.0*(i%100), 5 + 11/100.0*(i//100)]

    gen,label = Data_Preperation()
    result1 = KNN(data_set,gen,label)
    error=sum(label-np.array(result1).reshape((180,1)))
    Misclassification_Error=error/180
    print Misclassification_Error
    
    result = np.array(KNN(data,gen,label)).reshape((100,100))
       
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    c1=ax1.scatter([i[0] for i in class1], [i[1] for i in class1], s=20, c='b', marker="o", label='class1')
    c2=ax1.scatter([i[0] for i in class2], [i[1] for i in class2], s=20, c='r', marker="o", label='class2')
    ax1.legend((c1, c2),
               ('Class 1', 'Class 2'))    
    ax1.set_title('Nearest Neighbour Algorithm, K=11 Misclassification Error %f' %(Misclassification_Error), fontsize=14)
    ax1.contour(X,Y,result,levels=[1])

Main()