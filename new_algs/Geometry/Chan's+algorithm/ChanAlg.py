#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 23:00:36 2017

This program was developed to satisfy requirements for the course:
    Computational and Discrete Geoemtry (MATH 380) at 
    the University of San Diego. 

The subroutines: myGrahamScan and GiftWrapping were taken/modified from existing 
subroutines posted on GitHub by Rodolfo Ferro, https://github.com/RodolfoFerro

The primary purpose of the program is to return/plot the convex hull of a 2D point cloud
as an exhibit of 'Chan's Algorithm' which involves the graham-scanning of subsets of 
the point cloud, and then gift-wrapping the subsets. 

See: https://en.wikipedia.org/wiki/Chan%27s_algorithm

@author: Quinn T. Pratt
"""

import numpy as np
import matplotlib.pyplot as plt

def main():
    
    # first, call our point-cloud creator which returns an n-by-2 matrix of points
    # the points can presently be created using uniform random variables or multiple
    # normal distributions, more detail is given in the pointCloud function. 
    n = 100
    P = pointCloud(n)
    
    # now we need a guess for how many points are on the boundary, this is used to 
    # divide up the point cloud into many segments. It is suggested that this number 
    # result in approximately 5-10 subsets.
    m = 15
    
    # arbitrary projected number of subsets in our point cloud. 
    k = np.floor(1 + n/m)
    
    # compute the convex hull for each subset. The subConv object is a dictionary 
    # where each key corresponds to a different convex hull. 
    # due to the anisotropy of the sub-convex hulls, it was simple to store it as a dictionary 
    # although, a more sophisticated programmer would recognise that this could be 
    # stored more efficiently.
    subConv = subsetConv(P,k)
    
    
    # here we plot our figure beginning with the point cloud, then we iterativley plot the
    # sub-convex hulls and then the final hull. 
    plt.figure()
    plt.plot(P[:,0],P[:,1],'b o',label='Point Cloud',markersize=10)
    plt.grid()
    plt.tick_params(axis='both', labelsize=20)
    plt.title(r'Implementation of Chan Algorithm',fontsize=30,color='red')
    
    # here we preallocate space for the number of points on the hull, as well as the 
    # points themselves. 
    nSubHullPoints = np.zeros(len(subConv))
    SubHullPoints = np.zeros(shape=(1,2))
    
    # for each sub-hull, we gather all of the points on the hull and plot them.
    for key, value in subConv.items():
        L = value
        SubHullPoints = np.concatenate((SubHullPoints,L),axis=0)
        nSubHullPoints[key] = np.shape(L)[0]
        plt.plot(L[:,0],L[:,1], 'b-', picker=5)
        plt.plot([L[-1,0],L[0,0]],[L[-1,1],L[0,1]], 'b-', picker=5)
        
    nSubHullPoints = np.sum(nSubHullPoints)     
    print('Points On Sub-Hulls = {}'.format(nSubHullPoints))
    SubHullPoints = np.delete(SubHullPoints,(0),axis=0)
    
    # here we gift-wrap (or Jarvis March) the point cloud created by the convex 
    # hulls of the subsets of our original point cloud. 
    H = GiftWrapping(SubHullPoints)
    print('Points On the Total Hull = {}'.format(len(H)))
    plt.plot(H[:,0],H[:,1],'r-',linewidth=3,label='Total Convex Hull')
    plt.plot(H[:,0],H[:,1],'r .',markersize=20,label='Total Convex Hull')
    plt.plot([H[-1,0],H[0,0]],[H[-1,1],H[0,1]], 'r-',linewidth=3)
    #plt.legend(fontsize=20)
    
    
def pointCloud(n):
    
    '''
    These first lines can be commented/uncommented depending on whether the user 
    wants to use multiple normal distributions or a uniform random distribution.
    '''
    
    #P = np.random.normal(loc=0,scale=1,size=(int(np.floor(n/4)),2))
    #P = np.concatenate((P,np.random.normal(loc=5,scale=1,size=(int(np.floor(n/4)),2))),axis=0)
    #P = np.concatenate((P,np.random.normal(loc=(5,-4),scale=1,size=(int(np.floor(n/4)),2))),axis=0)
    #P = np.concatenate((P,np.random.normal(loc=(-5,8),scale=1,size=(int(np.floor(n/4)),2))),axis=0)
    
    
    P = np.random.uniform(low=-1,high=2,size=(n,2))
    return P

def subsetConv(P,k):
    # split the index into k parts. 
    subset_indicies = splitPoints(range(len(P)),k)
    # preallocate space for the sub-hulls in a dictionary. 
    subHulls = dict.fromkeys(range(len(subset_indicies)), [])
    # loop though the requested number of subsets, creating sub-sets out of our point-cloud
    for k in range(len(subset_indicies)):
        Pi = P[subset_indicies[k]]
        
        # now we have the points that we need to use for the Grahm Scan
        subHulls[k] = myGrahmScan(Pi)
        # now we have our Grahm-Scanned Subsets.
    return subHulls


def splitPoints(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def myGrahmScan(P):
    P = np.array(P)
    # Sorts the points by the y coordinate. 
    P = sorted(P,key=lambda x:x[1])
    L_upper = [P[0],P[1]]
    for i in range(2,len(P)):
        L_upper.append(P[i])
        while len(L_upper) > 2 and not RightTurn(L_upper[-1],L_upper[-2],L_upper[-3]):
            del L_upper[-2]
            
    L_lower = [P[-1], P[-2]]
    for i in range(len(P)-3,-1,-1):
        L_lower.append(P[i])
        while len(L_lower) > 2 and not RightTurn(L_lower[-1],L_lower[-2],L_lower[-3]):
            del L_lower[-2]
    del L_lower[0]
    del L_lower[-1]
    #L = np.add(L_upper, L_lower)
    try:
        L = np.concatenate((L_upper,L_lower),axis=0)
    except ValueError:
        print("Entire Sub-Pointset is Hull. Perhaps run again")
        L = L_upper
        
    return np.array(L)


def RightTurn(p1, p2, p3):
	if (p3[1]-p1[1])*(p2[0]-p1[0]) >= (p2[1]-p1[1])*(p3[0]-p1[0]):
		return False
	return True
# Function to know if we have a CCW turn
def CCW(p1, p2, p3):
	if (p3[1]-p1[1])*(p2[0]-p1[0]) >= (p2[1]-p1[1])*(p3[0]-p1[0]):
		return True
	return False

def GiftWrapping(S):
    # number of points in the set.
    n = len(S)
    # preallocation of hull points. 
    P = [[None for x in range(2)] for y in range(n)]
    # sort the points by their x coordinate.
    S = sorted(S,key=lambda x:x[0])
    # the left-most point is the first on the hull. 
    pointOnHull = S[0]
    i = 0
    while True:
        P[i] = pointOnHull
        endpoint = S[0]
        for j in range(1,n):
            if (endpoint[0] == pointOnHull[0] and endpoint[1] == pointOnHull[1]) or not CCW(S[j],P[i],endpoint):
                endpoint = S[j]
        i = i + 1
        pointOnHull = endpoint
        if endpoint[0] == P[0][0] and endpoint[1] == P[0][1]:
            break
    P = [p for p in P if p[0] is not None]
	
    return np.array(P)

if __name__ == '__main__':
    main()