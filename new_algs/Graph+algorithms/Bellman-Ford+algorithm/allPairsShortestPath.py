import argparse
import os
import re
import sys
import time
import cProfile, pstats, io
import profile

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the shortest path between all pairs of vertices in a graph')
parser.add_argument('--algorithm',default='a',\
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ellman-ford only or (f)loyd-warshall only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',help='Input file containing graph')

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices=[]
edges=[]

def BellmanFord(G):
    pathPairs=[]
    # TODO: Fill in your Bellman-Ford algorithm here
    # V = number of vertices in graph
    # S = source vertex
    # dist = V x V array of min distances
    numVertices = len(vertices)
    
    for j in vertices:
        
        dist = [float("inf")] * numVertices
        prev = [float(0)] * numVertices
        # for every vertex V in G
        #print("test")
        dist[j] = 0
        # for each vertex V in G
        
        for i in range(0, len(vertices) - 1):
            for V in range(0, len(vertices)):
                
                # for each edge (U, V) in G do
                for U in range(0, len(edges)):
                    
                    # w = weight of distance from U to V
                    w = float(edges[V][U])
                    
                    # tempDist = dist[U] + edge_weight(U, V)
                    tempDist = dist[V] + w
                    
                    if tempDist < dist[U]:
                        # dist[V] = tempDist
                        dist[U] = tempDist
            #print("test")
        #print(dist)
        pathPairs.append(dist)
    # for each edge (U, V) in graph G do
        
        # if dist[U] + edge_weight(U, V) < dist[V] then
            # return false ; there is a negative cycle
    # return dist[], prev[]for j in vertices:
    
    for j in vertices:
        if pathPairs[j][j] < 0:
            return [[0,0]]
    
    print('BellmanFord algorithm is incomplete')
    # The pathPairs list will contain the 2D array of shortest paths between all pairs of vertices 
    # [[w(1,1),w(1,2),...]
    #  [w(2,1),w(2,2),...]
    #  [w(3,1),w(3,2),...]
    #   ...]
    return pathPairs

def FloydWarshall(G):
    pathPairs=[]
    
    numVertices = len(vertices)
    # V = number of vertices in graph
    # dist = V x V array of min distances
    dist = []
    for i in vertices:
        r = [float("inf")] * numVertices
        dist.append(r)
    # TODO: Fill in your Floyd-Warshall algorithm here
    # for each vertex v do
    for V in range(0, len(vertices)):
        # distance from V to itself is 0
        
        # for each edge (u, v)
        for U in range(0, len(edges)):
            #w = float(edges[V][U])
            dist[U][V] = float(edges[U][V])
        # dist[u][v] = weight(u, v)
        
        dist[V][V] = 0
        
    #print(dist)
    # end for
    
    
    #print("test")
    
    # for k from 1 to V
    for k in range(0, len(vertices)):
        # for i from 1 to V
        for i in range(0, len(vertices)):
            # for j from 1 to V
            for j in range(0, len(vertices)):
                temp = dist[i][k] + dist[k][j]
                # if dist[i][j] > (dist[i][k] + dist[k][j]) then
                if dist[i][j] > temp:
                    # dist[i][j] = dist[i][k] + dist[k][j])
                    dist[i][j] = temp
                    
    for j in vertices:
        if dist[j][j] < 0:
            return [[0,0]]
    
    pathPairs = dist
    
    #print("test")
    
    print('FloydWarshall algorithm is incomplete')
    # The pathPairs list will contain the 2D array of shortest paths between all pairs of vertices 
    # [[w(1,1),w(1,2),...]
    #  [w(2,1),w(2,2),...]
    #  [w(3,1),w(3,2),...]
    #   ...]
    return pathPairs

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)-1][int(sink)-1]=weight
    G = (vertices,edges)
    return (vertices,edges)

def matrixEquality(a,b):
    if len(a) == 0 or len(b) == 0 or len(a) != len(b): return False
    if len(a[0]) != len(b[0]): return False
    for i,row in enumerate(a):
        for j,value in enumerate(b):
            if a[i][j] != b[i][j]:
                return False
    return True


def main(filename,algorithm):
    G=readFile(filename)
    pathPairs = []
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        # TODO: Insert timing code here
        #pathPairs = BellmanFord(G)
        pr = cProfile.Profile()
        pr.enable()
        pathPairs = BellmanFord(G)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
    if algorithm == 'f' or algorithm == 'F':
        # TODO: Insert timing code here
        #pathPairs = FloydWarshall(G)
        pr = cProfile.Profile()
        pr.enable()
        pathPairsFloyd = FloydWarshall(G)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
    if algorithm == 'a':
        print('running both') 
        pathPairsBellman = BellmanFord(G)
        pathPairsFloyd = FloydWarshall(G)
        pathPairs = pathPairsBellman
        if not matrixEquality(pathPairsBellman,pathPairsFloyd):
            print('Floyd-Warshall and Bellman-Ford did not produce the same result')
    with open(os.path.splitext(filename)[0]+'_shortestPaths.txt','w') as f:
        for row in pathPairs:
            for weight in row:
                f.write(str(weight)+' ')
            f.write('\n')

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)

