import numpy as np
from math import sqrt
import queue
import scipy.sparse.csgraph as cs

ID=0
graphs={}
init_residuals={}
Ds={}
Neighbours={}

while ID<100:
    with open("graph_"+str(ID)+".txt", "r") as file:
        load=np.loadtxt(file, delimiter=" ")
        graphs[ID]=load
        n=int(sqrt(np.size(load)))
        Ds[ID]=n-2
        load=np.where(load==0,load,1)
        init_residuals[ID]=load
    N=[]
    for i in range(n):
        L=np.nonzero(load[i])[0]
        N.append(L)
    Neighbours[ID]=np.array(N)
    ID +=1


def breadth_first(Matrix,neighbours,s0,t0):
    predecessors,dist=cs.dijkstra(Matrix,return_predecessors=True,indices=s0)
    res=np.array([])
    t=t0
    while t != s0 and not(np.isnan(t)):
        res=np.append(res,t)
        t=predecessors.item(t)
    if not(np.isnan(t)):
        res=np.append(res,s0)
    return np.flipud(res),res.size>1




