"""
@author: Aditya Sawadh
"""

import heapq
invalid = '#invalid#'

def graph_read(graph_data):
    with open(graph_data) as f:
        lines= [line.strip() for line in f.readlines()] # Open the file read each line removinfg white spaces and /n 
        lines= [x.split() for x in lines] # Split each line
        adj = dict() #Create an adjacency dict
        v=[]            
        for l in lines: # get the list of vertices in the data
            for x in l[0:1]:
                if x not in v:
                   v.append(x)
    adj=dict()
    weigh=dict()
    for i in v:
       adj[i]=[] # Intialize an empty list for the vertices
    for i in v: 
         for j in lines:
            if i in j: # see if the vertex present in lines of graphdata  
                if j.index(i)==0: # Append other
                    adj[i].append(j[1])
                    weigh[(i,j[1])]=(j[2])
    return adj,weigh,v

def queue(init={}):
    q = [0, dict(), []]         # [size, dict, heap]
    for key, value in init:
        enqueue(q, value, key)
    return q

def enqueue(q,priority,item):
    q[0] += 1
    entry = [priority, item]
    q[1][item]= entry    
    heapq.heappush(q[2], entry)
    
def dequeue(q):
    priority, item = _pop(q)
    while item == invalid:
        priority, item = _pop(q)
    q[0] -= 1
    return priority, item

def _pop(q):
    priority, item = heapq.heappop(q[2])
    if item != invalid:
        del q[1][item]
    return priority, item

def update(q, priority, item):
    if item in q[1].keys():
        entry = q[1][item]
        entry[1] = invalid
    new_entry = [priority, item]
    q[1][item] = new_entry
    heapq.heappush(q[2], new_entry)
    
def dijkstra(G,s,e):
    Q= queue()
    d = {s: 0}
    p= dict()
    adj,weigh_list,vertex =graph_read(G) # Initialise single source
    for v in vertex:
        d[v] = 'inf'
        p[v] = 'Nil'
    d[s]=0
    S =set({s})
    
    for i in adj.get(s,[]):
        d[i]=(weigh_list[s,i])
        item=(s,i)
        enqueue(Q,int(d[i]),item)
        
    while Q:
        print (Q[2])
        weigh,item=dequeue(Q)
        u=item[1] 
        if u not in S:
            p[u]=item[0]
            S.add(u)
            if u == e:
                return p, d[u]
            for v in adj.get(u,[]):
                #if d.get(v):
                if  float(d[v]) > int(weigh_list[u,v])+ int(d[u]):
                        d[v]= str(int(weigh_list[u,v])+int(d[u]))
                        item=(u,v)
                        update(Q,int(d[v]),item)
                else:
                    d[v]= str(int(weigh_list[u,v])+ int(d[u]))
                    item=(s,i)
                    enqueue(Q,int(d[i]),item)
        print(S)        
    
def print_path(p,s,v):
    if v == s:
        print(s)
    elif p[v] == 'Nil':
         print('no path from', s ,'to' ,v, 'exists')
    else:
        print_path(p,s, p[v])
        print(v)

p, d=dijkstra('graph_dijskstra.txt',"s","x")
print_path(p,"s","x")


### Verify the Dijkstra’s algorithm implementation chooses shortest path using a Scope checker 
def dijkstra_checker(G,s,e):
    adj,weigh_list,vertex=graph_read(G)
    V={} 
    path=[]
    for i in vertex:
        V[i]=False
    path_finder(adj,weigh_list,s,e,V,path)

def path_finder(adj,weights,s,e,path_nodes,path):
    path_nodes[s]=True
    path.append(s)
    if s==e:# if start node is same as end node
        path_weight=0
        for i in range(len(path)-1): # Calculate the path length
            path_weight += int(weights[path[i],path[i+1]])
        print('Path:',path, ',length:', path_weight)
    else: # if the nodes are different 
        for i in adj[s]:
            if path_nodes[i]== False:
                path_finder(adj,weights,i,e,path_nodes,path)   
    path.pop()
    path_nodes[s]=False
        
dijkstra_checker('graph_dijskstra.txt',"s","x")