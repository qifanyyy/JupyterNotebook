"""
@author: David Lei
@since: 21/08/2016
@modified: 

Implementation of graph data structure using Adjacency Matrix
Assuming undirected graph
- O(1) find edge
- O(1) remove edge
- O(1) add edge
- O(n) enumerate edges for node

Isn't that good for algorithms, other representations can give us a list of nodes easier

with space complexity O(v^2)
"""

class Adjacency_Matrix:
    def __init__(self, no_vertices):           # need to know the no_vertices to make matrix, might be a pain resizing
        self.matrix = [[0 for _ in range(no_vertices)] for _ in range(no_vertices)]
        self.no_vertices = no_vertices

    def print_matrix(self):
        for row in self.matrix:
            print(row)

    def add_edge(self, origin, destination):    # assuming we start at vertex 0
        self.matrix[origin][destination] += 1   # assuming bi-directional, otherwise just have og and dest
        #self.matrix[destination][origin] += 1  # <- not bidirectional

    def add_vertex(self):
        self.no_vertices += 1
        for row in self.matrix:
            row.append(0)
        self.matrix.append([0 for _ in range(self.no_vertices)])

    def find_edge(self, origin, destination):
        if self.matrix[origin][destination] == 0:
            return False
        return True

    def remove_edge(self, orgin, desintation):
        og_dest = self.matrix[orgin][desintation]
        dest_og = self.matrix[desintation][orgin]
        if og_dest > 0:
            self.matrix[orgin][desintation] -= 1
        if dest_og > 0:
            self.matrix[desintation][orgin] -= 1

    def get_edges(self, orgin):
        """O(v) running time as we need to iterate though all vertices even if they don't have an edge with origin"""
        og_edges = self.matrix[orgin]
        results = []
        for i in range(len(og_edges)):
            if og_edges[i] > 0:
                results.append((orgin, i, og_edges[i]))
        return results
    def get_vertices(self):
        # return list of vertices represented as integers starting at 0
        return [x for x in range(self.no_vertices)]
if __name__ == "__main__":
    G = Adjacency_Matrix(5)
    print("5x5 matrix")
    G.print_matrix()
    print("6x6 matrix, added vertex")
    G.add_vertex()
    G.print_matrix()
    G.add_edge(5,1)
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 4)
    G.add_edge(4,3)
    G.add_edge(0,1)
    G.add_edge(0,5)
    G.add_edge(5,2)
    print("added edges, (origin, destination, number of edges)")
    G.print_matrix()
    print("edges from vertex 1")
    v1_edges = G.get_edges(1)
    for e in v1_edges:
        print(e)
    # implementation works :D