#!/usr/bin/env python

from __future__ import division
import math
import random
import networkx as nx
import timeit

def quickSort(v, beg, end):  # list, int, int
    if end - beg > 0:  # only perform quicksort if we are dealing with > 1 values        
        pivot = v[beg] # we set the first item as our initial pivot
        i,j = beg,end   
        """
        NOTES ON OUR MAIN LOOP:
        ------------------------------
        To understand why we are using the comparison operators that we are let's look at 
        what is happening. 

        i is finding values that are larger than the pivot.
        j is finding values that are less than or equal to the pivot.

        We need to pick one variable (v[i] or v[j]) to be swapped with v[beg] when we are
        done. I chose j in this instance.
        ------------------------------
        When we are done moving i and j, j will be == or < i. i's final move will be to a 
        number that is larger than the pivot and it will overtake j's iterative position if
        j hasn't already been decreased to a position before i.

        IN ANY SITUATION THE FINAL SETUP j WILL BE THE LAST ITEM BEFORE ALL THE VALUES LARGER
        THAN THE PIVOT VALUE.
        ------------------------------
        FOR EXAMPLE:
                      | the first index is our pivot value                       
                      V
        start with:  [5][6][1][3][7][9][4]      <-- we continue until j <= i
                   i--^                 ^--j
        stop when:   [3][4][1][5][9][7][6]
                            j--^  ^--i          j <= i and our loop must stop
        """
        while j > i: 
            while v[i][2] <= pivot[2] and j > i:
                i+=1
            while v[j][2] > pivot[2] and j >= i:
                j-=1
            if j > i:
                v[i],v[j] = v[j],v[i]
        v[beg],v[j] = v[j],v[beg]
        quickSort(v, beg, j-1)
        quickSort(v, j+1, end)

def buildheap( aList ):
    # convert aList to heap
    length = len( aList ) - 1
    leastParent = length / 2
    for i in range ( int(leastParent), -1, -1 ):
        moveDown( aList, i, length )
    #print("buld heap done")
 
def moveDown( aList, first, last ):
    smallest = (first << 1) + 1
    while(smallest <= last):
        # select which of the children is smaller
        if (smallest < last) and (aList[smallest][2] < aList[smallest-1][2]):
            smallest = smallest
        else:
            smallest = smallest-1
        if aList[smallest][2] < aList[first][2]:
            aList[smallest], aList[first] = aList[first], aList[smallest]
            #swap(aList, smallest, first)
            first = smallest
            smallest = (first << 1) + 1
        else:
            return

def swap( A, x, y ):
    tmp = A[x]
    A[x] = A[y]
    A[y] = tmp

def mergesort(A):
    mergeSort(A, 0, len(A))

def MERGE(A,start,mid,end):
    L = A[start:mid]
    R = A[mid:end]
    i = 0
    j = 0
    k = start
    for l in range(k,end):
        if j >= len(R) or (i < len(L) and L[i][2] < R[j][2]):
            A[l] = L[i]
            i = i + 1
        else:
            A[l] = R[j]
            j = j + 1  

def mergeSort(A,p,r):
    if r - p > 1:
        mid = int((p+r)/2)
        mergeSort(A,p,mid)
        mergeSort(A,mid,r)
        MERGE(A,p,mid,r)

#=======================================================================
# Union-Find
#=======================================================================

class ArrayUnionFind:
    """Holds the three "arrays" for union find"""
    def __init__(self, S):
        self.group = dict((s,s) for s in S) # group[s] = id of its set
        self.size = dict((s,1) for s in S) # size[s] = size of set s
        self.items = dict((s,[s]) for s in S) # item[s] = list of items in set s
                                
def make_union_find(S):
    """Create a union-find data structure"""
    return ArrayUnionFind(S)
                
def find(UF, s):
    """Return the id for the group containing s"""
    return UF.group[s]

def union(UF, a,b):
    """Union the two sets a and b"""
    assert a in UF.items and b in UF.items
    # make a be the smaller set
    if UF.size[a] > UF.size[b]:
        a,b = b,a
    # put the items in a into the larger set b
    for s in UF.items[a]:
        UF.group[s] = b
        UF.items[b].append(s)
    # the new size of b is increased by the size of a
    UF.size[b] += UF.size[a]
    # remove the set a (to save memory)
    del UF.size[a]
    del UF.items[a]

#=======================================================================
# Kruskal MST
#=======================================================================

def kruskal_mst(G, type1, UF):
    """Return a minimum spanning tree using kruskal's algorithm"""
    # sort the list of edges in G by their length
    Edges = [(u, v, G[u][v]['length']) for u,v in G.edges()]
    print(len(Edges));
    numOfEdges = len(Edges) -1

    # for edges in increasing weight
    mst = [] # list of edges in the mst
    #UF = make_union_find(G.nodes())        # union-find data structure
    numOfElements = len(G.nodes())
    if type1 == 1:
        # heaps
        buildheap(Edges)        
        # for edges in increasing weight
        for i in range ( numOfEdges, 0, -1 ):
            #print("u v = " + str(Edges[0][0])+" "+str(Edges[0][1]))
            setu = find(UF, Edges[0][0])
            setv = find(UF, Edges[0][1])
            # if u,v are in different components
            if setu != setv:
                mst.append((u,v))
                union(UF, setu, setv)
                setx = find(UF, 1)
                if(numOfElements == UF.size[setx]):
                    # mst complete
                    break
            if Edges[0][2] < Edges[i][2]:
                Edges[0], Edges[i] = Edges[i], Edges[0]
                #swap( Edges, 0, i )
                moveDown( Edges, 0, i - 1 )
    else:
        if type1 == 2:
            mergesort(Edges)
        elif type1 == 3:
            quickSort(Edges, 0, len(Edges)-1)
        for u,v,d in Edges:
            setu = find(UF, u)
            setv = find(UF, v)
            # if u,v are in different components
            if setu != setv:
                mst.append((u,v))
                union(UF, setu, setv)
                setx = find(UF, 1)
                if(numOfElements == UF.size[setx]):
                    # mst complete
                    break

    #print("printing sorted edges:")
    #for u,v,d in Edges:
    #    print("u " + str(u) + " v " + str(v) + " d " + str(d))
    return mst

#=======================================================================
# MST Testing and Visualization Code
#=======================================================================

def dist(xy1, xy2):
    """Euclidean distance"""
    return math.sqrt((xy1[0] - xy2[0])**2 + (xy1[1] - xy2[1])**2)

def random_mst_graph(n, k=4):
    """Make a random graph by choosing n nodes in the [0,1.0] by [0,1]
    square. The 'length' of each edge is the euclidean distance between
    them. Edges connect to the k nearest neighbors of each node.""" 

    # build random nodes
    G = nx.Graph()
    for i in range(n):
        G.add_node(i, pos=(0.9*random.random()+0.05,0.9*random.random()+0.05))

    # add edges
    for i in G.nodes():
        near = [(u, dist(G.node[i]['pos'],G.node[u]['pos'])) for u in G.nodes() if u != i]
        near.sort(key=lambda x: x[1])
        for u,d in near[0:k]:
            G.add_edge(i, u, length=d)

    # ensure it's connected
    CC = nx.connected_components(G)
    for i in range(len(CC)-1):
        u = random.choice(CC[i])
        v = random.choice(CC[i+1])
        G.add_edge(u,v, length=dist(G.node[u]['pos'], G.node[v]['pos']))
    return G

def test_kruskal(type_sort, node):
    """Draw the MST for a random graph."""
    print(node)
    start = timeit.default_timer()
    N = random_mst_graph(int(node))
    stop = timeit.default_timer()
    print(str(stop-start))
    UF = make_union_find(N.nodes())        # union-find data structure
    start = timeit.default_timer()
    kruskal_mst(N, type_sort, UF)
    stop = timeit.default_timer()
    print(str(stop-start))

def main():
    import sys
    if len(sys.argv) >= 3:
        if sys.argv[1] == "kruskal_heap": test_kruskal(1, sys.argv[2])
        if sys.argv[1] == "kruskal_merge": test_kruskal(2, sys.argv[2]);
        if sys.argv[1] == "kruskal_quick": test_kruskal(3, sys.argv[2]);
    else:
        print ("Usage: kruskal.py [kruskal_heap|kruskal_merge|kruskal_quick] [number of nodes]")

if __name__ == "__main__": main()
