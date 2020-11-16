# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 11:17:53 2017

@author: Aditya
"""
# Reading the graph data. Graph is stored in different formats in each file 
def graph_read(graph_data):
    with open(graph_data) as f:
        lines= [ line.strip() for line in f.readlines()] # Open the file read each line removinfg white spaces and /n 
        lines= [x.split() for x in lines] # Split each line
        if len(lines[0])==1: # Given the count of vertices in first line
            lines=lines[1:]    # remove the first line
        v=[]            
        for l in lines[1:]: # get the list of vertices in the data
            for x in l:
                if x not in v:
                    v.append(x)                    
    adj = dict() #Create an adjacency dict
    for i in v:
       adj[i]=[] # Intialize an empty list for the vertices 
    for i in v: 
         for j in lines:
            if i in j: # see if the vertex present in lines of graphdata  
                if j.index(i)==0: # Append other
                    adj[i].append(j[1])
                else:
                    adj[i].append(j[0])
    return adj

# Tests
adj=graph_read('graphdata.txt') # Numeric graphdata with vertices count
data2=graph_read('graphdata2.txt')# Alphabet graphdata without vertices count
data3=graph_read('graphdata3.txt')# Alphanumeric graphdata without vertices count

# Implementation of Breadth First Search Traversal Method
from collections import deque

queue = deque

def enqueue(q, item):
    q.append(item)

def dequeue(q):
    return q.popleft()

def bfs(adj, s):
    color = dict()
    d = dict()
    pi = dict()
    for u in adj.keys():
        color[u] = 'white'
        d[u] = float('inf')
        pi[u] = None
    color[s] = 'gray'
    d[s] = 0
    pi[s] = None
    q = queue()
    enqueue(q, s)
    while len(q) != 0:
        print('q =', q)
        u = dequeue(q)
        for v in adj[u]:
            if color[v] == 'white':
                color[v] = 'gray'
                d[v] = d[u] + 1
                pi[v] = u
                enqueue(q, v)
        color[u] = 'black'
    return d, pi

s = input("Enter starting vertex:")
y= input("Enter ending vertex:")

d, pi = bfs(adj, s)

for u in adj.keys():
    print(u, pi[u], d[u])

def print_path(adj,s, v):
    if v == s:
        print(s)
    elif pi[v] == None:
        print('no path')
    else:
        print_path(adj, s, pi[v])
        print(v)

print_path(adj,s,y)


# Implementation of Depth First Search Traversal DFS 
stack = deque
def push(q, item): # push the vertex on stack
    q.append(item)

def pop(q):
    return q.pop() # Pop the vertex from stack

def dfs(adj, s):
    color = dict()
    pi = dict()
    q = stack()
    push(q, s)
    print(q)
    for u in adj.keys():
        color[u] = 'white'
        pi[u] = None
    while len(q) != 0:
        print('q =', q)
        a = '0'
        cnt=0
        u = pop(q) # 
        for x in adj[u]: # find the adjacent vertex 
            if color[x] == 'white':
                color[x] = 'gray'
                push(q,x) # push them on stack
                if cnt== 0:
                    pi[x]= u
                    cnt+=1
                    a=x
                else:
                    pi[x] = a
                    a=x
        color[u]='black'
    return pi
print('##### DFS ##########') 
pi_dfs= dfs(adj, s)

for u in adj.keys():
   print(u, pi_dfs[u])

def print_path_dfs(adj,s, v):
    if v == s:
        print(s)
    elif pi_dfs[v] == None:
        print('no path')
    else:
        print_path_dfs(adj, s, pi_dfs[v])
        print(v)
        
print_path_dfs(adj,s,y)