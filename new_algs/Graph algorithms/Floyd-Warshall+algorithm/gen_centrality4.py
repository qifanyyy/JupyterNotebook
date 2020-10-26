import sys
import snap
import Gnuplot
from numpy import inf
from itertools import product

#Set Seed of SNAP to 42
Rnd = snap.TRnd(42)
Rnd.Randomize()

Graph = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1]+".elist", 0, 1)

nodes = Graph.GetNodes()
edges = Graph.GetEdges()

fil = open(sys.argv[1]+".elist","r")
node_list = set()
line_num = 0
for line in fil:
	if line_num > 2 :	
		a, b = map(int, line.split("	"))  
		node_list.add(a-1)
		node_list.add(b-1)
	line_num += 1	
fil.close()

#Degree Centrality

D={}
y = sys.argv[1]+"-degree-centrality-4.txt"

InDegV = snap.TIntPrV()
snap.GetNodeInDegV(Graph, InDegV)

for item in InDegV:
	D[item.GetVal1()] = item.GetVal2()

D = sorted(D.iteritems(), key = lambda x : x[1],reverse=True)

f= open(y,"w+")
f.write("#NId Centrality\r\n")
for NId,value in D: 
    f.write("%d %d\r\n" % (NId,value) )	 
f.close()
#print("Degree Centrality done !")

#Closeness Centrality

D = {}
file_name = sys.argv[1]+"-closeness-centrality-4.txt"

if len(sys.argv) < 2:
	print "Check README for usage."
	sys.exit(-1)
	
try:	
	fil = open(sys.argv[1]+".elist", "r")
except IOError:
	print "File not found."
	sys.exit(-1)

# no of vertices
V = nodes

# array of shortest path distances 
dist = {i : {} for i in node_list}

# no of edges
E = edges

# array to count number of shortest paths between two nodes
counting = {i : {} for i in node_list}

# path nodes for each i,j pair (used to check other shortest paths)
path = {i : {} for i in node_list}

# initialize to infinity
for i in node_list:
        dist[i] = {j : float("inf") for j in node_list}
        counting[i] = {j : 1 for j in node_list}
	
for i in node_list:
	path[i] = {j : [] for j in node_list}
	print i

temp1 = fil.readline()
temp2 = fil.readline()
temp3 = fil.readline()

# read edges from input file and store
for i in range (0,E):
    t = fil.readline().strip().split()
    x = int(t[0])-1
    y = int(t[1])-1
    w = 1
    dist[x][y] = w
    dist[y][x] = w

fil.close()

# path from vertex to itself is set to 0
for i in node_list:
    dist[i][i] = 0

# initialize the path matrix
for i in node_list:
    for j in node_list:
	path[i][j].append(i)
	path[i][j].append(j)

# floyd warshall algorithm
for k in node_list:
    for i in node_list:
        for j in node_list:
	    if dist[i][j] > dist[i][k] + dist[k][j]:
		temp_ik = set(path[i][k])
		temp_kj = set(path[k][j])		
		temp_ij = temp_ik.union(temp_kj)     
		path[i][j] = list(temp_ij)           
		dist[i][j] = dist[i][k] + dist[k][j]

for k in node_list:
    for i in node_list:
        for j in node_list:
	    if dist[i][j] == dist[i][k]+dist[k][j] and k != j and k != i and i!=j:              
		temp_ik = set(path[i][k])
		temp_kj = set(path[k][j])		
		temp_ij = set(path[i][j]) 		
		if len((temp_ik.union(temp_kj)).difference(temp_ij)) != 0:
	            temp_ij = temp_ij.union(temp_ik.union(temp_kj))
		    path[i][j] = list(temp_ij) 
		    counting[i][j] += 1		
"""
for i in node_list:
        for j in node_list:
		print "counting",i+1,j+1," = ",counting[i][j]
"""

# compute closeness centrality

for i in node_list:	
    count = 0
    for j in node_list:
	if i != j:	
	    count += dist[i][j]
    #print "count",i,"=",count
    D[(i+1)] = float(nodes)/float(count)

D = sorted(D.iteritems(), key = lambda x : x[1],reverse=True)

f= open(file_name,"w+")
f.write("#NId Centrality\r\n")
for NId,value in D: 
    f.write("%d %f\r\n" % (NId,value) )	 
f.close()

#print("Closeness Centrality done !")

#Betweeness Centrality

D = {}
file_name = sys.argv[1]+"-betweenness-centrality-4.txt"

for k in node_list:
    D[k+1] = 0
    for i in node_list:	
        for j in node_list:
	    if i != j and i!=k and k!=j and dist[i][j] == dist[i][k]+dist[k][j] :		
		#print k+1,i+1,j+1    		
		D[k+1] += float(counting[i][k]*counting[k][j])/float(counting[i][j])


D = sorted(D.iteritems(), key = lambda x : x[1],reverse=True)

f= open(file_name,"w+")
f.write("#NId Centrality\r\n")
for NId,value in D: 
    f.write("%d %f\r\n" % (NId,value) )	 
f.close()

#print("Betweenness Centrality done !")
