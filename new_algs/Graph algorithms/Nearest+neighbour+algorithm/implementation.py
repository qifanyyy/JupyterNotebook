
# coding: utf-8

# <center> <h1> Naive Forward Attribute Reduction based on Neighborhood Rough Set model Implementation (NFARNRS) </h1> </center>

# <center><img src = "abstract.png">
# <br>
# <br>
# <img src = "f1.png">
# <br>
# <br>
# <img src = "f2.png">
# <br>
# <br>
# <img src = "algo.png"></center>

# In[1]:

# library imports
import numpy as np
import pandas as pd
import math
from sklearn.datasets import load_iris
from collections import defaultdict


# In[3]:

# data from CSV
df = pd.read_csv("diabetes1.csv")
df = df.loc[:20, :]
n = len(df)
df = df.drop("temp", 1)
df


# In[ ]:




# In[4]:

def euclideandist(a,b):
    """
    function to get euclidean distance between 2 ponits in any dimentions
    """
    
    return math.sqrt(((a - b)**2).sum())


# In[5]:

def getDelta(attrs, threshold):
    """
    function to calculate neighbourhood of each points with respect to difference attributes
    """
    
    p = defaultdict(set)
    for i in range(n):
        for j in range(n):
            #print(df.loc[i,attrs])
            #print(df.loc[j,attrs])
            if (euclideandist(df.loc[i,attrs],df.loc[j, attrs]) <= threshold):
                p[i+1].add(df["sn"][j])
    return p  # return all clusters data


# In[7]:

def getX(decAttr):
    
    """
    function to calculate all X
    """
    
    return df.groupby(decAttr)['sn'].apply(set)


# In[8]:

def getLowerApproximation(attrs, threshold, decAttr, Xi):
    
    """
    function to calculate the lower approximation of Xi
    """
    
    delset = getDelta(attrs, threshold)
    #print(delset)
    low_NXi = set()
    for i in delset:
        if (delset[i].issubset(Xi)):
            low_NXi.add(i)
    return low_NXi


# In[9]:

def getUpperApproximation(attrs, threshold, decAttr, Xi):
        
    """
    function to calculate the upper approximation of Xi
    """
    
    delset = getDelta(attrs, threshold)
    upp_NXi = set()
    
    for i in delset:
        if (delset[i].intersection(Xi)):
            upp_NXi.add(i)
    return upp_NXi

# print(getLowerApproximation(["a", "b"], 0.1, "d", getX("d")[0]))
# print(getUpperApproximation(["a", "b"], 0.1, "d", getX("d")[0]))

# print(getLowerApproximation(["a", "b"], 0.1, "d", getX("d")[1]))
# print(getUpperApproximation(["a", "b"], 0.1, "d", getX("d")[1]))


# In[10]:

def getPOSD(attrs, threshold, decAttr):
    
    """
    function to calculate the lower approximation of D (POS(D))
    """
    
    X = getX(decAttr)
    POS = set()
    for i in X:
        POS = POS.union(getLowerApproximation(attrs, threshold, decAttr, i))
    return POS

# getPOSD(["a"], 0.1, "d")


# In[11]:

def getUppND(attrs, threshold, decAttr):
        
    """
    function to calculate the upper approximation of D (N_Xi(D)))
    """
    
    X = getX(decAttr)
    uppND = set()
    for i in X:
        uppND = uppND.union(getUpperApproximation(attrs, threshold, decAttr, i))
    return uppND

# getUppND(["a", "b"], 0.1, "d")


# In[12]:

def computeSIG(C, red, B, D):
    
    """
    function to compute the significance of attributes
    """
    
    SIG_red_D = defaultdict(int)
    #print(C - red)
    for ai in (C - red):
        temp = set(B)
        gamma_red = len(getPOSD(list(temp), 0.1, D))/n
        temp.add(ai)
        gamma_red_ai = len(getPOSD(list(temp), 0.1, D))/n
        SIG_red_D[ai] = gamma_red_ai - gamma_red
        #print(gamma_red, gamma_red_ai, SIG_red_D[ai]) 
    #print(SIG_red_D)
    return SIG_red_D

def getNFARNRS(C, B, D,epslon):
    
    """
    function to compute the reduced number of attributes of dataset
    """
    
    red = set()

    SIG_red_D = computeSIG(C, red, B, D)
    
    ak = max(SIG_red_D, key=SIG_red_D.get)
    #print(ak)
    while(SIG_red_D[ak] > 0):
        red.add(ak)
        SIG_red_D = computeSIG(C, red, B, D)
        ak = max(SIG_red_D, key=SIG_red_D.get)
        
    return red          


# In[ ]:

print("Reduced Attributes:\n")
print(getNFARNRS(set(["a", "b", "c", "e", "f", "g", "h", "i"]), ["a"], "d", 0.001))


# In[ ]:



