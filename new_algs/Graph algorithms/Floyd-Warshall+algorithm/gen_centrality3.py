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

node_list_1 = set()
node_list_2 = set()
node_list_3 = set()
node_list_4 = set()
node_list_5 = set()
node_list_6 = set()
node_list_7 = set()
node_list_8 = set()
node_list_9 = set()
node_list_10 = set()

for i in node_list:
	if len(node_list_1) < len(node_list)/10:
		node_list_1.add(i)
	elif len(node_list_2) < len(node_list)/10:
		node_list_2.add(i)
	elif len(node_list_3) < len(node_list)/10:
		node_list_3.add(i)
	elif len(node_list_4) < len(node_list)/10:
		node_list_4.add(i)
	elif len(node_list_5) < len(node_list)/10:
		node_list_5.add(i)
	elif len(node_list_6) < len(node_list)/10:
		node_list_6.add(i)
	elif len(node_list_7) < len(node_list)/10:
		node_list_7.add(i)
	elif len(node_list_8) < len(node_list)/10:
		node_list_8.add(i)
	elif len(node_list_9) < len(node_list)/10:
		node_list_9.add(i)
	else:
		node_list_10.add(i)

#Degree Centrality

D={}
y = sys.argv[1]+"-degree-centrality-1.txt"

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
file_name = sys.argv[1]+"-closeness-centrality-1.txt"

InDegV = snap.TIntPrV()
snap.GetNodeInDegV(Graph, InDegV)

# recursive function to obtain the path as a string
def obtainPath(i, j):
    if dist[i][j] == float("inf"):
        return " no path to "
    if parent[i][j] == i:
        return " "
    else :
        return obtainPath(i, parent[i][j]) + str(parent[i][j]+1) + obtainPath(parent[i][j], j)


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
dist = {}

# array of shortest paths
parent = {}

# no of edges
E = edges

# array to count number of shortest paths between two nodes
counting = {}

# array to count number of shortest paths through a node between two nodes
count_k = {}

# path nodes for each i,j pair (used to check other shortest paths)
path = {}

# initialize to infinity
for i in node_list:
    dist[i] = {}
    parent[i] = {}
    counting[i] ={}
    for j in node_list:
        dist[i][j] = (float("inf"))
        parent[i][j] = (0)
        counting[i][j] = (1)

for i in node_list:
    path[i] ={}
    for j in node_list:
	path[i][j] = set()

print "hi"

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
    parent[x][y] = x
    dist[y][x] = w
    parent[y][x] = y

fil.close()

# path from vertex to itself is set to 0
for i in node_list:
    dist[i][i] = 0

# initialize the path matrix
for i in node_list:
    for j in node_list:
	path[i][j].add(i)
	path[i][j].add(j)
        if dist[i][j] == float("inf"):
            parent[i][j] = 0
        else:
            parent[i][j] = i

# actual floyd warshall algorithm
for k in node_list_1:
    for i in node_list:
        for j in node_list:
	    if dist[i][j] > dist[i][k] + dist[k][j]:
		path[i][j] = path[i][k].union(path[k][j])                
		dist[i][j] = dist[i][k] + dist[k][j]
                parent[i][j] = parent[k][j]	

for k in node_list_1:
    for i in node_list:
        for j in node_list:
	    if dist[i][j] == dist[i][k]+dist[k][j] and k != j and k != i and i!=j:              
		if len((path[i][k].union(path[k][j])).difference(path[i][j])) != 0:
	            path[i][j] = path[i][j].union(path[i][k].union(path[k][j])) 
		    counting[i][j] += 1		
"""
for i in node_list:
        for j in node_list:
		print "counting",i+1,j+1," = ",counting[i][j]
"""

# compute closeness centrality

for i in node_list_1:	
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
file_name = sys.argv[1]+"-betweenness-centrality-1.txt"

for k in node_list_1:
    D[k+1] = 0
    for i in node_list:	
        for j in node_list:
	    if i != j and i!=k and k!=j and dist[i][j] == dist[i][k]+dist[k][j]:		
		#print k+1,i+1,j+1    		
		D[k+1] += float(counting[i][k]*counting[k][j])/float(counting[i][j])


D = sorted(D.iteritems(), key = lambda x : x[1],reverse=True)

f= open(file_name,"w+")
f.write("#NId Centrality\r\n")
for NId,value in D: 
    f.write("%d %f\r\n" % (NId,value) )	 
f.close()

#print("Betweenness Centrality done !")
