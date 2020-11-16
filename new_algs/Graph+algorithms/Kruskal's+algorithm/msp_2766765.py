# @ Name : Lane Gramling
# @ Due Date : April 15, 2019
# @ Brief: Generates a Minimum Spanning Tree for a given weighted graph, using
#           Kruskal's Algorithm. Uses path compression & union-by-rank in union operation.
#  		Usage: python msp_2766765.py input.txt > output.txt

import sys # Used for getting command-line arguments
import re  # Used for parsing inputs with regexes

class Kruskal:
    def __init__(self, filename):
        self.graph = []         # Graph Structure
        self.VERTEX_COUNT = 0   # VERTEX_COUNT
        self.MST = []           # Store computed MST
        g = {}                  # Temporarily used in building the graph structure

        matrix = [weight_list.split(' ') for weight_list in open(filename, 'r').read().split('\n')] # Read & structure input
        for row in matrix: row.remove('')                                                           # Clean input
        matrix = [list(map(int, x)) for x in matrix]                                                # Format input
        for v_i, weight_list in enumerate(matrix):                                                  # Generate temporary 2D graph structure
            if weight_list:                                                                         # ...
                g[v_i] = {}                                                                         # ...
                for v_j, weight in enumerate(weight_list): g[v_i][v_j] = weight                     # ... Assign weights to vertices
            else: matrix.pop(v_i)                                                                   # (Final input cleaning)
        for u in range(len(g)):                                                                     # Build graph structure
            for v in range(len(g)):                                                                 # ...
                if g[u][v]: self.graph.append([u,v,g[u][v]])                                        # ...
        self.VERTEX_COUNT = len(matrix)                                                             # Update vertex count

    def FIND_SET(self, component, vertex): # Find operation with path compression
        if component[vertex] != vertex: return self.FIND_SET(component, component[vertex])
        return vertex

    def union(self, component, rank, u, v):   # Union operation using union-by-rank implementation
        u_root = self.FIND_SET(component, u)
        v_root = self.FIND_SET(component, v)
        if rank[u_root] < rank[v_root]: component[u_root] = v_root      # Determine who becomes the subtree
        elif rank[u_root] > rank[v_root]: component[v_root] = u_root
        else:
            component[v_root] = u_root
            rank[u_root] += 1           # Increment rank for node as necessary

    def computeMST(self):
        component = []  # Tracks parents using component array implementation described on pg. 152
        rank = []       # Tracks ranks for union-by-rank operation
        i_edge = 0      # Tracks current edge index

        self.graph = sorted(self.graph, key=lambda edge: edge[2]) # Sort by weight
        for node in range(self.VERTEX_COUNT):                     # MAKE_SET(v)
            component.append(node)
            rank.append(0)

        i = 0
        while i_edge < self.VERTEX_COUNT - 1:                     # MST computation
            u, v, weight = self.graph[i]
            i = i + 1
            u_root = self.FIND_SET(component, u)                  # Determine connectedness
            v_root = self.FIND_SET(component, v)
            if u_root != v_root:
                i_edge = i_edge + 1
                self.MST.append([u, v, weight])                   # A U {(u, v)}
                self.union(component, rank, u, v)

# Execution on runtime
if len(sys.argv) < 2:
    print("[Usage]: python msp_2766765.py <input-file> > <output-file>")
else:
    k = Kruskal(sys.argv[1])
    k.computeMST()
    for edge in k.MST: print("{} {}".format(edge[0], edge[1]))
