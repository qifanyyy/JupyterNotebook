## PRIMs_MST.py
## PRIM's algorthm implementation to find Mininum Spanning Tree.

from collections import defaultdict;            ## use dict/hash to construct the graph.
from heapq import heapify, heappop, heappush;   ## use min_heap for the edges priority queue.

class Graph:
    ## Graph class, used for PRIM's MST implementation.

    def __init__(self, n_vertices = 0, edges = []):
        
        self.edges      =   defaultdict(list);      ## pool the edges in dict/hash format.
        self.n_vertices =   0;                      ## total # of vertices.
        self.vertices   =   set();                  ## vertice labels; must be int or str.

        for edge in edges:
            self.add_edge( edge);
        
        return;

    def add_edge(self, edge):

        ## Function to add an edge to the graph. Returns None.

        u, v, weight    =   edge;

        self.edges[u].append(   [v, weight]);
        self.edges[v].append(   [u, weight]);

        self.vertices |= {u, v};

        self.n_vertices = len(self.vertices);

        return;

    def edge_heappush(self, queue, edge):
        ## Add an edge to min_heap priority queue (based on weight).
        ## Retuns None.

        item    =   [edge[2]] + edge[:2];
        heappush(queue, item);
        return;
    
    def edge_heappop(self, queue):
        ## Returns the minimum weight edge.

        weight, u, v    =   heappop(queue);
        return [u,v,weight];

    def PRIMs_MST(  self):
        ## Returns list of edges that's MST.

        ## Algorthm:
        ## Use set to keep tracks of MST vertices.
        ## min_heap as min priority queue (based on weight).
        ## Use greedy algorythm to trace adjacent vertices with smallest weight.

        mst_set     =   set();      ## Keeps track of each visited vertices.
        mst_prims   =   [];         ## Keeps track of the MST edges.

        edges_min_heap  =   [];     ## Min_heap priority queue to pool the edges.


        ### start with a random vertice.
        for u in self.vertices:     break;
        mst_set.add(u);


        # Keeps looping as long as there's unvisited vertices, or 
        #   there's still edges need to be processed in min_heap.

        while len(mst_set) <= self.n_vertices:            

            ## add adjacent vertices;
            for v_edge in self.edges[u]:                
                v, weight   =   v_edge;

                ## add the edge if vertice v is not yet visited.
                if v not in mst_set:
                    self.edge_heappush( edges_min_heap, [u,v,weight]);
            
            ## if there's no more edges to be processed, the break the loop.
            if not edges_min_heap:      break;

            ## Keeps processing vertice with minimum weight,
            ## as long as it's not yet visited.

            while edges_min_heap:
                u, v, weight    =   self.edge_heappop(  edges_min_heap);

                ## if vertice v is not yet visited, add the edge v to the MST.
                if v not in mst_set:
                    mst_set.add(v);
                    mst_prims.append( sorted([u,v]) + [weight]);
                    u = v;

                    break;
        
        return mst_prims;

        


