from copy import deepcopy
import numpy as np
import pandas as pd
import Tkinter
from array import array
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

def dist(m, n, ax=1):
    d=np.linalg.norm(m-n, axis=ax)
    return d

data = pd.read_csv('dataset1.csv')
data.head()
X = data['x'].values
Y = data['y'].values
arr = np.array(list(zip(X, Y)))
clusters = np.zeros(len(arr))
plt.scatter(X,Y,c='blue',s=7)
plt.show()
k = 6

cent=[]
centx=[]
centy=[]
max=0
td=0;
cent1=arr[1];
cent2=arr[2];
#finding two farthest points
for i in range(len(arr)):
    p=arr[i]
    for j in range(len(arr)):
        q=arr[j]
        td=dist(arr[i],arr[j],None)
        if(td>max):
            max=td
   	    cent1=p
            cent2=q
cent.append(list(cent1))
cent.append(list(cent2))
centx.append(cent1[0])
centx.append(cent2[0])
centy.append(cent1[1])
centy.append(cent2[1])

kcount=2
pt=[]
#Selecting remaining k-2 centriods
while(kcount<k):
    mean=np.mean(np.array(cent, dtype=np.float32), axis=0)  #representative centroid
    max=0
    for i in range(len(arr)):
        if(dist(mean,arr[i],None)>max and (list(arr[i]) not in cent)):
            max=dist(mean,arr[i],None)
            pt=arr[i]
    kcount=kcount+1
    cent.append(list(pt))
    centx.append(pt[0])
    centy.append(pt[1])

cent = np.array(cent, dtype=np.float32)
centx = np.array(centx, dtype=np.float32)
centy = np.array(centy, dtype=np.float32)

print("The centroids selected initially are ")
print(cent)

centold = np.zeros(cent.shape)

plt.scatter(X,Y,c='blue',s=7)
plt.scatter(centx,centy,marker='*',s=150,c='red')
plt.show()
error = dist(cent,centold,None)
count=1

distarray=np.array(range(len(arr)),dtype=np.float32)
#Clustering
while error!=0:
    for i in range(len(arr)):
        if(count>1 and (distarray[i]<dist(arr[i],cent[int(clusters[i])],None))):
            distances = dist(arr[i],cent)
            distarray[i]=min(distances)
            cluster = np.argmin(distances)
            clusters[i] = cluster
        elif(count==1):
            distances = dist(arr[i],cent)
            distarray[i]=min(distances)
            cluster = np.argmin(distances)
            clusters[i] = cluster

    centold = deepcopy(cent)
    #Updating centriods
    for i in range(k):
        points = [arr[j] for j in range(len(arr)) if clusters[j] == i]
        cent[i] = np.mean(points, axis=0)
    error = dist(cent,centold, None)
    print "Iteration", count,"   => Centroids are "
    print cent
    count=count+1

colors = ['r', 'g', 'b', 'y', 'c', 'm']
fig, ax = plt.subplots()
for i in range(k):
        points = np.array([arr[j] for j in range(len(arr)) if clusters[j] == i])
        ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
ax.scatter(cent[:, 0],cent[:, 1],marker='*',s=200,c='black')
plt.show()
