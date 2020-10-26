#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 13:59:25 2018

@author: yasin
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from random import randrange
#TASK1
def genetic (x_init):
    lst=[]
    for m in range (200):    
        j=randrange(100)
        if x_init[0,j]==0:
            x_init[0,j]=1
        else:
            x_init[0,j]=0
        lst.append(x_init.sum())
    return lst

x=np.zeros((1000, 200))
for i in range (1000):
    x_init=np.zeros((1, 100))        
    lst=genetic(x_init)
    x[i]=lst
    plt.plot(lst)

plt.xlabel('Number Of Generations')
plt.ylabel('The Sum')
plt.title('Sum vs. 200 Generations')
plt.show()

mean1=np.mean(x, axis=0)
plt.plot(mean1)
plt.xlabel('Number Of Generations')
plt.ylabel('Mean')
plt.title('Mean of Ensemble')
plt.show()

#derivative of mean
v = [mean1[i+1]-mean1[i] for i in range(len(mean1)-1)]
plt.plot(v)
plt.xlabel('Number Of Generations')
plt.ylabel('Derivative')
plt.title('Derivative Of Mean')
plt.show()

#TASK2

def genetic (x_init,nrchild):
    lst=[]
    x_initr=x_init
    for m in range (200):
        x_slct=selct(x_initr,nrchild)
        n=randrange(100)
        if x_slct[0,n]==0:
            x_slct[0,n]=1
        else:
            x_slct[0,n]=0
        lst.append(x_slct.sum())
        x_initr=x_slct
    return lst
def selct(x_init1,nrchild):
    xchild=np.zeros((nrchild+1,100))
    xchild[0]=x_init1
    for j in range (nrchild):
        k=randrange(100)
        x_init2=np.array([xchild[0]])
        if x_init2[0,k]==0:
            x_init2[0,k]=1
        else:
            x_init2[0,k]=0
        xchild[j+1]=x_init2
    sum_=np.sum(xchild, axis=1)
    ind = np.argmax(sum_)
    return np.array([xchild[ind]])
x1=np.zeros((1000, 200))
for i in range (1000):
    x_init=np.zeros((1, 100))        
    lst=genetic(x_init,3)
    x1[i]=lst
    plt.plot(lst)

plt.xlabel('Number Of Generations')
plt.ylabel('The Sum')
plt.title('Sum vs. 200 Generations')
plt.show()

mean1=np.mean(x1, axis=0)
plt.plot(mean1)
plt.xlabel('Number Of Generations')
plt.ylabel('Mean')
plt.title('Mean of Ensemble')
plt.show()

#derivative of mean
v = [mean1[i+1]-mean1[i] for i in range(len(mean1)-1)]
plt.plot(v)
plt.xlabel('Number Of Generations')
plt.ylabel('Derivative')
plt.title('Derivative Of Mean')
plt.show()
#Expected Improvement
array=x1[:,199]
nom=array[999]
denom=100
res=1-(nom/denom)


x2=np.zeros((1000, 200))
for j in range (200):    
    array=x1[:,j]
    lis=[]
    for i in range(1000):
        nom=array[i]
        denom=100
        res=1-(nom/denom)**3
        lis.append(res)
    x2[:,j]=lis

mean2=np.mean(x2, axis=0)
plt.plot(mean2)
plt.xlabel('Number Of Generations')
plt.ylabel('Exp. Imp.')
plt.title('Expected Improvement')
plt.show()


#TASK3
def flip (x_init, nchild):
    lstm =[]
    #v = []
    for m in range(200):
        max_indices = []
        max_imp = 0
        for i in range(nchild):
            #for three mutation
            j,k,l,m,n=randrange(100),randrange(100),randrange(100),randrange(100),randrange(100)
            imp = np.where(x_init[0,[j,k,l,m,n]]==0, 1, 0)
            # if current imp is greater than max_imp, update max_indices and max_imp
            if max(imp) > max_imp: 
                max_imp = max(imp)
                max_indices = [j, k, l, m, n]
              
        x_init[0, max_indices] = np.where(x_init[0, max_indices]==0, 1, 0)
        lstm.append(np.sum(x_init))
    v=[lstm[o+1]-lstm[o] for o in range(199)]
    return lstm, v

x=np.zeros((1000, 200))
x1=np.zeros((1000, 199))
for i in range (1000):
    x_init=np.zeros((1, 100))        
    lst,v1 =flip(x_init,3)
    x[i]=lst
    x1[i]=v1
    plt.plot(lst)

plt.xlabel('Number Of Generations')
plt.ylabel('The Sum')
plt.title('Sum vs. 200 Generations')
plt.show()

mean1=np.mean(x, axis=0)
plt.plot(mean1)
plt.xlabel('Number Of Generations')
plt.ylabel('Mean')
plt.title('Mean of Ensemble')
plt.show()

mean2=np.mean(x1, axis=0)
plt.plot(mean2)
plt.xlabel('Number Of Generations')
plt.ylabel('Emprical Improvement')
plt.title('Expected Improvement')
plt.show()

x2=np.zeros((1000, 200))
for j in range (200):    
    array=x[:,j]
    lis=[]
    for i in range(1000):
        nom=array[i]
        denom=100
        res=1-(nom/denom)**3
        lis.append(res)
    x2[:,j]=lis

mean3=np.mean(x2, axis=0)
plt.plot(mean3, label="Analytical Imp.")
plt.plot(mean2, label="Emrical Imp.")
plt.legend(loc='upper right')
plt.xlabel('Number Of Generations')
plt.ylabel('Exp. Imp.')
plt.title('Expected Improvement')
plt.show()


