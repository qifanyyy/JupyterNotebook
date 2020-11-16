import numpy as np
import scipy as sp
#import matplotlib.pyplot as plt
import math
import itertools
import time
from operator import itemgetter
import random
def MST(a):
    counter = 0
    var=0
    graphplot(a)
    ktime,kcost = kruskal(a)
    ptime,pcost = prim(a,var)
    stime,scost = sollin(a,var)
    print ('Kruskal Time:',ktime,'\nKruskal Cost:', kcost,'\nPrim Time:',ptime,'\nPrim Cost:', pcost,'\nSollin Time:',stime,'\nSollin Cost:', scost)
    return ktime,ptime,stime
 #   plt.show()
    
    
def graphplot(a):
    size = len(a)
    x=[]
    y=[]
  #  theta = 2*math.pi/size
  #  ax1=plt.subplot(2,2,1)
  #  plt.title('Original Graph')
   # for i in range(size):
    #    x.append(math.cos(i*theta))
     #   y.append(math.sin(i*theta))
      #  plt.text(x[i],y[i],i+1,fontsize=15,color='green')
 #   for i in range(size):
  #      for j in range(i,size):
   #         if a[i][j] != 0:
    #            plt.plot([x[i],x[j]],[y[i],y[j]],'b-',linewidth=3)
     #           plt.text((x[i]+x[j])/2,(y[i]+y[j])/2,a[i][j],fontsize=15,color='red')
            
   # plt.scatter(x,y,s=50)
    #ax1.xaxis.set_visible(False)
    #ax1.yaxis.set_visible(False)
    #plt.show()

def kruskal(a):
    #graphplot(a)
    t=time.time()
    arclist=[]
    parclist=[]
    stree=[]
    forest=[]
    
    for i in range(len(a)):
        forest.append([i])
    for i in range(len(a)):
        for j in range(i,len(a)):
            arclist.append([i,j,a[i][j]])
    for i in range(len(arclist)):
        arclist[i].append(random.randrange(0,10))
    arclist=sorted(arclist,key=itemgetter(2,3))
    for k in arclist:
        if k[2] != 0:
            parclist.append(k)
    for l in parclist:
        if len(forest)>1: 
            stree.append(l)
            counter = 0
            for m in forest:
                if l[0] in m and l[1] in m:
                    counter = counter +1
            if counter != 0:
                stree.pop()
            if counter ==0:
                t1=0
                t2=0
                for n in range(len(forest)):
                    if l[0] in forest[n]:
                        t1=n
                    if l[1] in forest[n]:
                        t2=n
                forest[t1]=list(set(forest[t1]+forest[t2]))
                forest.pop(t2)

    
    x=[]
    y=[]
    cost = 0
    theta = 2*math.pi/len(a)
    #ax2=plt.subplot(2,2,2)
   # plt.title('Kruskal Tree')
    #for i in range(len(a)):
#        x.append(math.cos(i*theta))
 #       y.append(math.sin(i*theta))
  #      plt.text(x[i],y[i],i+1,fontsize=15,color='green')
    for k in stree:
    #    plt.plot([x[k[0]],x[k[1]]],[y[k[0]],y[k[1]]],'c-',linewidth=3)
     #   plt.text((x[k[0]]+x[k[1]])/2,(y[k[0]]+y[k[1]])/2,k[2],fontsize=15,color='red')
        cost = cost + k[2]
 #   plt.scatter(x,y,s=50)
    s=time.time()-t
    
  #  ax2.xaxis.set_visible(False)
   # ax2.yaxis.set_visible(False)
    return s, cost
    #plt.show()
    
            
            
            
            
        
        
        
        

def prim(a,var):
    ptime = time.time()
    arclist = []
    var =0 
    parclist=[]
    ttemplist=[]
    #a.pop(0)
    innode=[0]
    stree=[]
    c=0
    for i in range(len(a)):
        for j in range(i,len(a)):
            arclist.append([i,j,a[i][j]])
   # for i in range(len(arclist)):
    #    arclist[i].append(random.randrange(0,10))
    arclist=sorted(arclist,key=itemgetter(-1))
    for k in arclist:
        if k[2] != 0:
            parclist.append(k)
    for m in range(len(a)-1):
        templist=[]
        c=0
        while templist ==[]:
            n=parclist[c]
            if (n[0] in innode and n[1] not in innode) or (n[1] in innode and n[0] not in innode):
                templist.append(n)
            c=c+1
        #templist=sorted(templist,key=itemgetter(2,3))
##        for k in templist:
##            if k[2] == templist[0][2]:
##                ttemplist.append(k)
##        random.shuffle(ttemplist)
        stree.append(templist[0])
        innode.append(templist[0][0])
        innode.append(templist[0][1])
        innode = list(set(innode))

    x=[]
    y=[]
    pcost = 0
#    theta = 2*math.pi/len(a)
#    ax3=plt.subplot(2,2,3)
#    plt.title('Prim Tree')
#    for i in range(len(a)):
#        x.append(math.cos(i*theta))
#        y.append(math.sin(i*theta))
#        plt.text(x[i],y[i],i+1,fontsize=15,color='green')
    for k in stree:
#        plt.plot([x[k[0]],x[k[1]]],[y[k[0]],y[k[1]]],'c-',linewidth=3)
#        plt.text((x[k[0]]+x[k[1]])/2,(y[k[0]]+y[k[1]])/2,k[2],fontsize=15,color='red')
        pcost = pcost + k[2]
#    plt.scatter(x,y,s=50)

    
 #   ax3.xaxis.set_visible(False)
 #   ax3.yaxis.set_visible(False)
        
    ptime=time.time()-ptime
    return ptime,pcost

def sollin(a,var):
    
    stime=time.time()
    #a.pop(0)
    arclist = []
    parclist=[]
    innode=[0]
    stree=[]
    forest=[]

    for i in range(len(a)):
        forest.append([i])
    
    for i in range(len(a)):
        for j in range(i,len(a)):
            arclist.append([i,j,a[i][j]])
    arclist=sorted(arclist,key=itemgetter(-1))

    for k in arclist:
        if k[2] != 0:
            parclist.append(k)
    templist=[]
    while (len(stree)<len(a)-1):
        tforest=forest[:]
        
        for l in range(len(tforest)):

          #  print(tforest[l])
            c=0
            while templist==[]:
                n=parclist[c]
         #       print(n)
                if (n[0] in tforest[l] and n[1] not in tforest[l]) or (n[1] in tforest[l] and n[0] not in tforest[l]):
                    templist.append(n)
                c=c+1
            templist=sorted(templist,key=itemgetter(-1))
       #     print(templist)
            if templist[0] not in stree:
                stree.append(templist[0])
             #   print(stree)
                t1='a'
                t2='a'
                for m in range(len(forest)):
                    if templist[0][0] in forest[m]:
                        t1=m
                    if templist[0][1] in forest[m]:
                        t2=m
                forest[t1]=list(set(forest[t1]+forest[t2]))
                forest.pop(t2)        
            templist=[]
        
    x=[]
    y=[]
    scost = 0
#    theta = 2*math.pi/len(a)
#    ax4=plt.subplot(2,2,4)
 #   plt.title('Sollin Tree')
#    for i in range(len(a)):
 #       x.append(math.cos(i*theta))
#        y.append(math.sin(i*theta))
#        plt.text(x[i],y[i],i+1,fontsize=15,color='green')
    for k in stree:
#        plt.plot([x[k[0]],x[k[1]]],[y[k[0]],y[k[1]]],'c-',linewidth=3)
#        plt.text((x[k[0]]+x[k[1]])/2,(y[k[0]]+y[k[1]])/2,k[2],fontsize=15,color='red')
        scost = scost + k[2]
 #   plt.scatter(x,y,s=50)


    
  #  ax4.xaxis.set_visible(False)
  #  ax4.yaxis.set_visible(False)
    stime=time.time()-stime
    return stime,scost

def adjconvert(n,a):
    matrix=[]
    counter = 0
    for i in range(n):
        matrix.append([])
    for i in range(n):
        for j in range(n):
            matrix[i].append(0)

    for k in a:
        matrix[k[0]][k[1]]=k[2]
        matrix[k[1]][k[0]]=k[2]     

    for i in matrix[0]:
        counter = counter + i
    if counter == 0:
        matrix.pop(0)
        for i in range(len(matrix)):
            matrix[i].pop(0)
    return matrix
    
    

def randgraph(n,ntype,a,b):
    graph=[]
    for i in range(n):
        for j in range(i,n):
            graph.append([i,j])
    for i in range(len(graph)):
        if ntype=='boolean':
            graph[i].append(random.randrange(0,2))
        if ntype=='int':
            graph[i].append(random.randrange(a,b))
        if ntype=='float':
            graph[i].append(round(random.uniform(a,b),3))

    matrix=adjconvert(n,graph)

    size = n
    x=[]
    y=[]
#    theta = 2*math.pi/size
#    plt.figure(7)
#    plt.title('Random Graph')
#    for i in range(size):
#        x.append(math.cos(i*theta))
#        y.append(math.sin(i*theta))
#        plt.text(x[i],y[i],i+1,fontsize=15,color='green')
#    for i in range(size):
 #       for j in range(i,size):
 #           if matrix[i][j] != 0:
 #               plt.plot([x[i],x[j]],[y[i],y[j]],'b-',linewidth=3)
 #               plt.text((x[i]+x[j])/2,(y[i]+y[j])/2,matrix[i][j],fontsize=15,color='red')
            
  #  plt.scatter(x,y,s=50)
  #  plt.show()
    #time.sleep(10)
    #plt.clf()
    return matrix

def manyplots(a):
    for i in range(4):
        MST(a)
        time.sleep(10)
        
