import queue
from copy import deepcopy


G1={
    0:{1:4,2:3,3:3},
    1:{2:-2},
    2:{3:1},
    3:{}
}
V1=[0,1,2,3]

G2={
    0:{1:4,2:2},
    1:{2:3,3:2,4:3},
    2:{1:1,3:4,4:5},
    3:{},
    4:{3:1}
}
V2=[0,1,2,3,4]



def Dijkstras(G,V,s):
    dist=[]
    prev=[]
    mark=[]
    path=[]
    record=[]
    recordv=[]
    for v in V:
        dist.append(float('Inf'))
        prev.append(None)
        mark.append(0)
    dist[s]=0
    Q=queue.PriorityQueue()
    Q.put([dist[s],s])
    while(Q.empty()==False):
        U=Q.get()
        u=U[1]
        mark[u]=1
        for v in G[u]:
            recordv=[]
            if mark[v]==0:
                if dist[u]+G[u][v]<dist[v]:
                    dist[v]=dist[u]+G[u][v]
                    prev[v]=u
                    Q.put([dist[v],v])
                    for v in V:
                        recordv.append([v,dist[v],prev[v]])
                        record.append(recordv)

    #find path from s to all vertices in V
    for v in V:
        if prev[v]==None:
            path.append(None)
        else:
            pathv=[v]
            while(prev[v]!=s):
                pathv.append(prev[v])
                v=prev[v]
            pathv.append(s)
            pathvr=list(reversed(pathv))
            path.append(pathvr)
    return dist,prev,path,record


def BellmanFord(G,V,s):
    dist = []
    prev = []
    for v in V:
        dist.append(float('Inf'))
        prev.append(None)
    dist[s]=0
    for i in range(1,len(V)):
        for u in G:
            for v in G[u]:
                if dist[u]+G[u][v]<dist[v]:
                    dist[v] = dist[u] + G[u][v]
                    prev[v] = u
    for u in G:
        for v in G[u]:
            if dist[u] + G[u][v] < dist[v]:
                return None
    return dist,prev


def reweight(G,V):
    #add new node s to re-weight
    Vs=deepcopy(V)
    #serial number of s
    sn=len(V)
    Vs.append(sn)
    #add new edges from s to all nodes,weight 0
    Gs=deepcopy(G)
    sweight = {}
    for i in range(0, len(V)):
        sweight[i] = 0
    Gs[sn] = sweight
    #using Bellman-Ford to get h for re-weight
    H=BellmanFord(Gs,Vs,sn)
    h=H[0]
    #print('h[]:',h)
    #re-weight
    Gw=deepcopy(G)
    for i in Gw:
        for j in Gw[i]:
            Gw[i][j]=G[i][j]+(h[i]-h[j])
    #return re-weighted graph
    return Gw

Gw=reweight(G1,V1)
print('Gw:',Gw)
#running Dijkstras on each vertices in Gw to find all-pair shortest path
# print("Without re-weight:")
# for v in V1:
#    Output=Dijkstras(G1,V1,v)
#    print(Output[2])
print("Johnson's:")
for v in V1:
   Output=Dijkstras(Gw,V1,v)
   print('path')
   print(Output[2])
   print('record')
   print(Output[3])