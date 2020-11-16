import numpy as np
import pandas as pd

def getEdges(e):
    E=[]
    for i in range(e):
        E.append(list(map(int,input("Enter Edge "+str(i+1)+" v1 v2 w :").split())))
    #print(E)
    return E
def initCost(n,E):
    c=[[99 for j in range(n)] for i in range(n)]
    for i in E:
        c[i[0]-1][i[1]-1]=i[2]
        c[i[1]-1][i[0]-1]=i[2]
    return c

def printMat(m):
    mp = {99: "∞"}
    m=[list(mp.get(int(e), e) for e in s) for s in m]
    x=[i for i in range(1,len(m)+1)]
    y=[i for i in range(1,len(m[0])+1)]
    df=pd.DataFrame(m,columns=y,index=x)
    print(df)
def ptree(tree):
    print("\n\t SPANNING TREE EDGES\n")
    printMat(tree)
def pnear(near):
    print("\n\n Near array = ",near)
def liner():
    print("")
    print("-"*60)
    print("")
        
    
####################################


n=int(input("no. of vertices : "))
e=int(input("no of Edges : "))
E=getEdges(e)
    
#E=[[1,2,10],[1,3,20],[2,4,10],[3,5,10],[4,6,40],[5,6,5],[3,4,30],[2,5,25]]
#n=6   

E=sorted(E,key=lambda x: x[2])
#print(E)
cost=initCost(n,E)
print("\n\n\t THE COST ADJACENCY MATRIX \n\n\n")
printMat(cost)
print("\n\n")
near=[0 for i in range(n)]
tree=[]
mincost=E[0][2]
k=E[0][0]
l=E[0][1]
print("Minimum cost edge ("+str(E[0][0])+","+str(E[0][1])+") is chosen")
print("\nMincost = ",mincost)
tree.append([k,l])

ptree(tree)

print("\n\nInitialize Near Array\n")
for i in range(n):
    print("\ni = ",i+1)
    print("\ncost[",i+1,",",l,"] < cost[",i+1,",",k,"]")
    if(cost[i][l-1]<cost[i][k-1]):
        if(cost[i][l-1]==99 and cost[i][k-1]==99):
            print("∞ < ∞ True.. So near[",i+1,"] = ",l)
        elif(cost[i][k-1]==99):
            print(cost[i][l-1]," < ∞ True.. So near[",i+1,"] = ",l)
        elif(cost[i][l-1]==99):
            print("∞ < ",cost[i][k-1]," True.. So near[",i+1,"] = ",l)
        else:
            print(cost[i][l-1]," < ",cost[i][k-1]," True.. So near[",i+1,"] = ",l)
        near[i]=l
              
    else:
        near[i]=k
        if(cost[i][l-1]==99 and cost[i][k-1]==99):
            print("∞ < ∞ False.. So near[",i+1,"] = ",l)
        elif(cost[i][k-1]==99):
            print(cost[i][l-1]," < ∞ False.. So near[",i+1,"] = ",l)
        elif(cost[i][l-1]==99):
            print("∞ < ",cost[i][k-1]," False.. So near[",i+1,"] = ",l)
        else:
            print(cost[i][l-1]," < ",cost[i][k-1]," False.. So near[",i+1,"] = ",k)
    pnear(near)
print("\n\n near[",l,"]=near[",k,"]=0")
near[k-1]=near[l-1]=0
pnear(near)


###
print("\n\n for i = 2 to n-1\n\n")
for i in range(1,n-1):
    #get j min and near[j] not 0
    dic={}
    for j in range(len(near)):
        if(near[j]==0):
            continue
        dic[j]=cost[j][near[j]-1]
   
    j=min(dic, key=dic.get)
    
    print("min cost and near[j] not equal to 0, j = ","cost(",j+1,",",near[j],")")
    tree.append([j+1,near[j]])
    print("\nAdd to tree:\n")
    ptree(tree)
    print("\nmincost = ",mincost,"+",dic[j])
    mincost=mincost+dic[j]
    near[j]=0
    print("\nnear[j]=0\n\n for k=1 to n\n\n")
    for k in range(n):
        print("\nk = ",k+1)
        if(near[k]!=0 and (cost[k][near[k]-1]>cost[k][j])):
           near[k]=j+1
           print("\nnear[",k+1,"] not 0 and cost[",k+1,",near[",k+1,"]] > cost[",k+1,",",j+1,"] is TRUE,\n near[",k+1,"] = ",j+1)
           pnear(near)
        else:
            print("\nnear[",k+1,"] not 0 and cost[",k+1,",near[",k+1,"]] > cost[",k+1,",",j+1,"] is False")

    liner()
print("\n\n FINAL MINIMUM COST : ",mincost)
print("\n\n Final Spaning Tree :\n")
ptree(tree)


                
        
    

