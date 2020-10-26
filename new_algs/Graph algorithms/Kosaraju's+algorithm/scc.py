# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary
"""
import sys
import resource

sys.setrecursionlimit(10 ** 6)
resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, 2 ** 30))

explored = set()
source_vertex = None
finishing_time = {} 
finish = 0
SCCs = {}
def DFS_rev(graph , node):
    global finishing_time
    global explored
    global finish
    explored.add(node)
    for edge in graph[node]:
        if edge not in explored:
            DFS_rev(graph , edge)
    finish += 1
    finishing_time[node] = finish
    
def DFS_loop_rev(graph):
    global explored
    for node in reversed(list(graph.keys())):
        if node not in explored:
            DFS_rev(graph , node)

def DFS(graph , node):
    global SCCs
    global explored
    global source_vertex
    explored.add(node)    
    for edge in graph[node]:
        if edge not in explored:
            DFS(graph,edge)
            SCCs[source_vertex] += 1
        
def DFS_loop(graph):
    global explored
    global SCCs
    explored.clear()
    global finishing_time
    global source_vertex
    f_time = sorted(list(graph.keys()), key = lambda f_time : finishing_time[f_time],reverse=True)
    for node in f_time:
        if node not in explored:
            source_vertex = node
            SCCs[source_vertex] = 1
            DFS(graph , node)            
    
graph = {}
rev_graph = {}
with open('SCC.txt') as f:
    data = f.readlines()
    for line in data:
        elements = list(map(str,line[:-1].split(" ")))
        try:
            (graph[elements[0]]).append(elements[1])
        except KeyError:
            graph[str(elements[0])] = [elements[1]]
        try:
            (rev_graph[elements[1]]).append(elements[0])
        except KeyError:
            rev_graph[str(elements[1])] = [elements[0]]
        if elements[0] not in rev_graph.keys():
            rev_graph[str(elements[0])] = []
        if elements[1] not in graph.keys():
            graph[str(elements[1])] = []
        
f.close()




DFS_loop_rev(rev_graph)
DFS_loop(graph)




ans = ""
sccs = sorted(list(SCCs.values()), reverse =True) 

for i in range(5):
    try:
        ans += str(sccs[i])
    except IndexError:
        ans+= "0"
    if i < 4:
        ans +=","
    
print(ans)