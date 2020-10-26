import numpy as np
import matplotlib.pyplot as plt
import time as time
import datetime as datetime
from sklearn.datasets import fetch_mldata
from sklearn.utils import shuffle

class knn:
    def __init__(self):
        pass

    def train_model(self, X, Y):
        pass

    def compute_diff(self, X, Y, X_test,K):
        distanceLabel = []
        for i in range(len(X)):
            distanceLabel.append([i,np.sqrt(np.sum(np.square(X_test-X[i,:])))])
        distanceLabel = sorted(distanceLabel,key= lambda x: float(x[1]))
        #print("Distance with classes",distanceLabel)
        classDict = {}
        for i in range(K):
            classDict[Y[distanceLabel[i][0]]]=classDict.get(Y[distanceLabel[i][0]],0)+1
        #print("classDictionary",classDict)
        return classDict

    def predict_model(self,X,Y,X_test,K):
        classDict = self.compute_diff(X,Y,X_test,K)
        maxVal = -1
        maxKey = -1
        for key,val in classDict.items():
            if val > maxVal:
                maxVal = val
                maxKey = key
        print("Final Class",maxKey)
        return maxKey

    def accuracy_value(self,X,Y,X_test,Y_test,Klist):
        correct = 0
        for i in range(len(X_test)):
            if self.predict_model(X,Y,X_test[i,:],Klist)==Y_test[i]:
                correct+=1
        print("accuracy",(correct/len(Y_test)))
        return (correct/len(Y_test))





#fetch data
mnist = fetch_mldata('MNIST original', data_home="./")
print("data",mnist.data.shape)
print("target",mnist.target.shape)
print("target",mnist.target)
data = mnist.data
target = mnist.target
data,target = shuffle(data,target)
start_time = datetime.datetime.now()
print()
X_train = data[:6000,:]
Y_train = target[:6000]
X_train_test = data[:6000,:]
Y_train_test = target[:6000]
X_test_one = data[69880:69881, :]
Y_test_one = target[69880]
X_test = data[69000:70000, :]
Y_test = target[69000:70000]
print(X_train[99,:])
knn_model = knn()
#knn_model.predict_model(X_train, Y_train, X_test_one, 9)
knn_model.accuracy_value(X_train, Y_train, X_test, Y_test, 39)
print("difference =", datetime.datetime.now() - start_time)

accuracyListTest = []
accuracyListTrain = []
kVal = [1, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99]

accuracyListTest = knn_model.accuracy_value(X_train, Y_train, X_test, Y_test, kVal))
accuracyListTrain = knn_model.accuracy_value(X_train,Y_train,X_train_test,Y_train_test,kVal))

print("Plotting Started")
plt.plot(accuracyListTest, label="Testing Error")
plt.plot(accuracyListTrain, label="Training Error")
plt.xticks(range(11),kVal)
plt.xlabel('Different K values')
plt.ylabel('accuracy')
plt.title('Testing Error vs Training Error')
plt.legend()

plt.show()




