# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:16:59 2018

@author: heera
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from numpy import genfromtxt
from sklearn.utils.linear_assignment_ import linear_assignment
from sklearn.metrics import confusion_matrix

train_data=[]
test_data=[]
TrainX=[]
TrainY=[]
TestX=[]
TestY=[]

def letters_to_digit_convert(letters):
    class_numbers=[]
    for i in range(65,91):
        temp=chr(i) 
        for j in range(0,len(letters)):
            element=letters[j]    
            if(element==temp): 
                char_num=i-64 
                class_numbers.append(char_num)    
    return class_numbers

def pick_data(class_numbers):
    my_data = genfromtxt('C:\\Datamining project1\\HandWrittenLetters.csv', delimiter=',')
    a = np.transpose(my_data)
    b = np.int_(a)
    data = []
    for i in range(len(b)):
        for j in class_numbers:
            if b[i][0] == j:            
                data.append(b[i])            
        np.savetxt('picked_data1.csv', data, fmt='%d', delimiter=",")

def test_train_data(training_instances,test_instances):    
    number_of_classes = 39
    data = genfromtxt('picked_data1.csv', delimiter=',')
    data = np.int_(data)
    array = np.roll(data,-1,-1)
    n=len(class_numbers)   
    for x in range(0,n):            
            for y in range(0,training_instances):
                temp=y+(x*number_of_classes)
                train_data.append(array[temp])
            for z in range(training_instances,training_instances+test_instances):
                temp2=z+(x*number_of_classes)
                test_data.append(array[temp2])                
    np.savetxt('train_data.csv', train_data, fmt='%d', delimiter=",")
    np.savetxt('test_data.csv', test_data, fmt='%d', delimiter=",")
    for i in range (0,len(train_data)):
        TrainX.append(train_data[i][0:320])
        TrainY.append(train_data[i][320])
    for i in range (0,len(test_data)):
        TestX.append(test_data[i][0:320])
        TestY.append(test_data[i][320])            
    np.savetxt('TrainX.csv', TrainX, fmt='%d', delimiter=",") 
    np.savetxt('TrainY.csv', TrainY, fmt='%d', delimiter=",")
    np.savetxt('TestX.csv', TestX, fmt='%d', delimiter=",")
    np.savetxt('TestY.csv', TestY, fmt='%d', delimiter=",")
    return TrainX, TrainY, TestX, TestY

def test_train_data_whole(training_instances,test_instances):    
    number_of_classes = 39
    data = genfromtxt('picked_data1.csv', delimiter=',')
    data = np.int_(data)
    array = np.roll(data,-1,-1)
    n=len(class_numbers)   
    for x in range(0,n):            
            for y in range(0,training_instances):
                temp=y+(x*number_of_classes)
                train_data.append(array[temp])
            for z in range(training_instances,training_instances+test_instances):
                temp2=z+(x*number_of_classes)
                test_data.append(array[temp2])                
    np.savetxt('train_data.csv', train_data, fmt='%d', delimiter=",")
    np.savetxt('test_data.csv', test_data, fmt='%d', delimiter=",")
    for i in range (0,len(train_data)):
        TrainX.append(train_data[i][0:320])
        TrainY.append(train_data[i][320])
    for i in range (0,len(test_data)):
        TestX.append(test_data[i][0:320])
        TestY.append(test_data[i][320])            
    np.savetxt('TrainX.csv', TrainX, fmt='%d', delimiter=",") 
    np.savetxt('TrainY.csv', TrainY, fmt='%d', delimiter=",")
    np.savetxt('TestX.csv', TestX, fmt='%d', delimiter=",")
    np.savetxt('TestY.csv', TestY, fmt='%d', delimiter=",")
    return TrainX, TrainY, TestX, TestY

def cluster_acc(y_true, y_pred):
    y_true = y_true.astype(np.int64)
    assert y_pred.size == y_true.size
    D = max(y_pred.max(), y_true.max()) +1
    w = np.zeros((D, D), dtype=np.int64)
    for i in range(y_pred.size):
        w[y_pred[i], y_true[i]] += 1
    ind = linear_assignment(w.max() - w)
    print ("Accuracy: ", end = '')
    return sum([w[i, j] for i, j in ind]) * 1.0 / y_pred.size

lett = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
choice = int(input("Enter 0 to specify number of classes else press 1 to use the whole data: "))
if(choice == 0):    
    num = int(input("Enter the number of classes that you want to consider: "))
    letter = []
    print("\nEnter the elements in order \"Write in Uppercase only\": ")
    for i in range(0,num):
        letter.append(input()) 
    class_numbers=letters_to_digit_convert(letter) 
    pick_data(class_numbers) 
    training_instances=int(input("Enter the number of training elements: "))
    test_instances=39-training_instances  
    TrainX, TrainY, TestX, TestY = test_train_data(training_instances,test_instances)
if(choice == 1):
    class_numbers=letters_to_digit_convert(lett) 
    pick_data(class_numbers)
    training_instances=int(input("Enter the number of training elements: "))
    test_instances=39-training_instances  
    TrainX, TrainY, TestX, TestY = test_train_data_whole(training_instances,test_instances)
    
k = int(input("Enter a value for k: "))
kmeans = KMeans(n_clusters = k)
kmeans.fit(TrainX)
y_kmeans = kmeans.predict(TestX)
y_true = np.array(TestY, dtype=np.int64)
y_pred = []
y_pred = y_kmeans
d = confusion_matrix(y_true, y_pred)
h = d[1:]
df = pd.DataFrame(h)
s = np.delete(h,len(df.columns)-1,axis = 1)
print ("Confusion Matrix: ")
print (s)
print ("Column-Index: " )
ind = linear_assignment(s.max() - s)
print (ind)
print (cluster_acc(y_true, y_pred))
print ("Labels and Cluster Index")
print (y_true, y_pred)
    














