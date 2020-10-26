"""
@author: David Lei
@since: 21/08/2016
@modified:

An optimal implementation of the Graph data structure supporting
- O(1) find edge
- O(1) remove edge
- O(1) add edge
- O(e/v) enumerate edges for node

with space complexity O(e + v)

It allows for quick look up and deletions like in the adj matrix with the same space complexity as the adj list

Based on: Data Structures and Algorithms in Python
I(v) is the incidence collection of v, or vertices whose edges are
incident (connected) to v

Note: order you put things in dict isn't always reflected in output, so if i keep running this bfs result on
graph_map might change

! like a hashmap/dict
"""

from algorithms_datastructures.graphs.implementations.structures import Vertex, Edge

#from Structures import Vertex, Edge

class AdjacencyMap:
    def __init__(self, directed=False):
        """Create empty graph (undirected by default)"""
        self.outgoing = {}
        self.incoming = {} if directed else self.outgoing
        # note above line makes self.incoming point to the same thing as outgoing if not directed
        # if it is directed, there will be another dict for it

    def is_directed(self):
        """Return True of this is a directed graph, else False"""
        return self.incoming is not self.outgoing   # directed maps are distinct

    def vertex_count(self):
        return len(self.outgoing)

    def get_vertices(self):
        """Return an iteration of all vertices of the graph"""
        return self.outgoing.keys()

    def edge_count(self):
        """The total number of edges is the len of self.outgoing[v] or len of dict at the index v
        for each vertex in the graph (self.outgoing)"""
        total = sum(len(self.outgoing[v]) for v in self.outgoing)
        """if directed, then each edge is unique, else we have counted twice the amount of
        edges due to the bi-directional nature of undirected graphs"""
        return total if self.is_directed() else total//2

    def get_edges(self):
        """Return the set of all edges in the graph O(e/v) or average number of edges per vertex"""
        result = set()  # avoid double reporting edges of undirected graph
        """outgoing.values() is the list of the adjacency list, however they point to a
        mapping of edges to allow for the better time complexities"""
        for mapped_edges in self.outgoing.values():
            result.update(mapped_edges.values())    # key is the end vertex, values is the edge
        return result

    def get_edge(self, origin, destination):
        """Return the edge form origin to destination or None if not adjacent
        remember that outgoing[origin] is the hashmap (dictionary) of edges incident (adjacent)
        to the vertex origin, they are stored as destination: edge, so get.(destination) will
        give back an edge (or none)
        """
        return self.outgoing[origin].get(destination)

    def degree(self, v, outgoing_edges=True):
        """Return number of (outgoing) edges adjacent to vertex v
        if the graph is directed, optional parameter used ot count incoming edges"""
        adjacent = self.outgoing if outgoing_edges else self.incoming
        # grab our dictionary of outgoing edges and find those outgoing to vertex v
        return len(adjacent[v])

    def get_adjacent_edges(self, v, outgoing_edges=True):
        """Return all (outgoing) edges adjacent to vertex v
        if graph is directed, optional paramter used to reqest incomign edges"""
        adjacent = self.outgoing if outgoing_edges else self.incoming
        output = []
        for edge in adjacent[v].values():   # can use yield edge instead of appeding to a lsit
            output.append(edge)
        return output

    def add_vertex(self, x=None):
        v = Vertex(x)
        self.outgoing[v] = {}      # create a new dictionary at that 'index' of outgoing (acts as the array in adj list)
        # note that outgoing[v] creates an input into the dictionary outgoing
        if self.is_directed():
            self.incoming[v] = {}
        return v

    def add_edge(self, origin, destination, x=None):
        """Insert and return a new Edge from origin to destination"""
        e = Edge(origin, destination, x)
        self.outgoing[origin][destination] = e
        self.incoming[destination][origin] = e
        """It is so easy to add an edge!!!!!
        outcoming[origin] is a dictionary for vertices (and edges) adjacent to the origin vertex
        outcoming[origin][destination] is the key, value mapping form the origin vertex to the destination vertex
        and it sets e to be the value of that entry in the dictionary
        """
        return e

    def print_structure(self):
        """print structure of hwo the info is stored"""
        print("Printing Structure")
        for vertex in self.outgoing:
            print("\nVertex - ", end="")
            print(vertex, end="")
            print(" - name: " + str(vertex.name) + ", rep: " + str(vertex.rep))
            d = self.outgoing[vertex]
            print("Dictionary at this vertex: " + str(d))
            print("     Keys: " + str(d.keys()))
            print("             ", end="")
            for v in d.keys():
                print(v.name, end=" ")
            print("\n     Values: " + str(d.values()))
            print("             ", end="")
            for e in d.values():
                print(e.name, end=" ")
            print()

    def print_adj_list_rep(self):
        print("Printing Adjacency List like representation")
        for vertex in self.outgoing:
            print(str(vertex.name) + ": --> ", end="")
            for destination_vertex in self.outgoing[vertex]:
                #edge = self.outgoing[vertex][destination_vertex]    # don't need to do this, can just say dest_ver.name
                print(destination_vertex.name, end=" ")               # but this is an example how how it looks
            print()


    def print_graph(self):
        """Don't use this, just here to remind me what classes they are"""
        for thing in self.outgoing:
            print(thing.__class__)
            print(thing)
            print("NODE: name-" + str(thing.name) +", rep-" + str(thing.rep))
            b = self.outgoing[thing]
            print(b)
            print(b.__class__)
            print("things on this noode are: ", end=" -- ")
            print(b.values())
            print("\nNEXT\n")

    def remove_edge(self, origin_vertex, destination_vertex):
        if self.is_directed():                                  # directed, just need to delete once
            v_dict = self.outgoing[origin_vertex]
            del v_dict[destination_vertex]
        else:                                                   # undirected, delete from both sides
            v_dict = self.outgoing[origin_vertex]
            del v_dict[destination_vertex]
            v_dict_op = self.outgoing[destination_vertex]
            del v_dict_op[origin_vertex]

if __name__ == "__main__":

    # Testing, G is an undirected graph, dG is a directed graph
    # G will look like FIT2004 graphs slide 13
    print("\n   **  Test undirected graph   **  ")
    G = AdjacencyMap()
    A = G.add_vertex('A')
    B = G.add_vertex('B')
    C = G.add_vertex('C')
    D = G.add_vertex('D')
    E = G.add_vertex('E')
    # only need to insert 5 edges as undirected
    G.add_edge(A, C)
    G.add_edge(A, D)
    G.add_edge(A, E)
    G.add_edge(C, E)
    G.add_edge(D, E)

    G.print_structure()
    G.print_adj_list_rep()

    print("total edges: " +str(G.edge_count()))
    edges = list(G.get_edges())
    print([e.to_string(ends_vertex_obs=True) for e in edges])

    print("\nTest remove edge\n")
    G.remove_edge(A, D)
    G.print_adj_list_rep()              # remove successfully works!


    print("\n **  Testing a directed graph    **  \n")

    dG = AdjacencyMap(directed=True)

    dA = dG.add_vertex('-A')
    dB = dG.add_vertex('-B')
    dC = dG.add_vertex('-C')
    dD = dG.add_vertex('-D')
    dE = dG.add_vertex('-E')

    print("Test after same 5 inserts")
    # doing 5 insert_edges as above
    dG.add_edge(dA, dC)
    dG.add_edge(dA, dD)
    dG.add_edge(dA, dE)
    dG.add_edge(dC, dE)
    dG.add_edge(dD, dE)

    dG.print_adj_list_rep()     # should not print exactly like above after 5 insert_edges as directed

    print("Test after 5 more inserts")
    dG.add_edge(dC, dA)
    dG.add_edge(dD, dA)
    dG.add_edge(dE, dA)
    dG.add_edge(dE, dC)
    dG.add_edge(dE, dD)
    dG.print_adj_list_rep()     # should not print exactly like above after 5 insert_edges as directed

    print("total edges: " +str(dG.edge_count()))
    edges = list(dG.get_edges())
    print([e.to_string(ends_vertex_obs=True) for e in edges])

    print("\nTest remove edge\n")
    dG.remove_edge(dA, dD)
    dG.print_adj_list_rep()

    # everything works now!! :D yay

    """
    after insertions should look like
    A: --> D E C
    B: -->
    C: --> A E
    D: --> A E
    E: --> A C D

    (which it does ^_^)
    """
    adj_edges = dG.get_adjacent_edges(dA)
    print(adj_edges)
