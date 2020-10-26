""" Find a blocking flow of a graph.
    In a blocking flow, every source-sink path has atleast
    one saturated edge -> there is no such path in the residual graph.

    Finding a blocking flow in the level graph guarantees that the
    source-sink distance will decrease by atleast one.
"""
from graph import display_graph, input_graph
from gui.image_display import ImageSequence
import matplotlib.image as mpimg
import numpy as np
from copy import deepcopy


class BlockingFlowImageSequence(ImageSequence):

    """ Find blocking flow from source to sink,
        given graph and distances array.

        For now, all intermediate states are computed on initialization,
        instead of when next_image is called.
    """
    def __init__(self, graph, nvertices, nedges, dist, source, sink):
        # Initialize all objects
        ImageSequence.__init__(self)
        self.graph = graph
        self.edges = nedges
        self.vertices = nvertices
        self.dist = dist
        self.source = source
        self.sink = sink

        self.done = False  # For GUI display
        self.states = []
        self.idx = 0
        self.current_flow = 0


    def init_image(self):

        display_graph(self.graph, filename="blocking_flow_init", source=self.source, sink=self.sink)
        # Find blocking_flow and store in self.block_flow
        self.block_flow, self.block_flow_mat = self.blocking_flow()
        self.idx = 0
        self.current_flow = 0
        print 'found blockflow', self.block_flow
        return mpimg.imread('blocking_flow_init.png')


    def next_image(self):
        if self.done:
            return None
        else:
            # self.idx keeps track of current image displayed in GUI
            if self.idx >= len(self.states):
                self.done = True
                return None

            # Display the sequence of images
            display_graph(self.states[self.idx][1],
                          filename="blocking_flow_next",
                          highlight_path=self.states[self.idx][0],
                          capacities=self.adj_matrix_capacitites,
                          source=self.source, sink=self.sink)
            self.current_flow = self.states[self.idx][2]
            print 'curr state', self.states[self.idx]
            self.idx += 1
            if self.idx >= len(self.states):
                self.done = True
            return mpimg.imread('blocking_flow_next.png')

    def complete(self):
        return self.done

    def path_found(self):
        print "path found"

    def blocking_flow(self):
        """
        Finds a blocking flow of graph from source to sink.
        s - source, t - sink
        """

        # Store objects
        graph = self.graph
        vert = self.vertices
        edges = self.edges
        source = self.source
        sink = self.sink

        # store the resulting graph
        final_graph_adj = np.zeros((vert, vert), dtype=np.int)
        final_graph = [[] for i in range(vert)]

        # Both adjacency list and adjacency matrix used.

        # Use sets as adjacency list so that queries are faster
        graph_sets = [set() for i in range(vert)]
        for i in range(vert):
            for j in range(len(graph[i])):
                temp1, temp2 = graph[i][j]
                graph_sets[i].add(temp1)

        # Adjacency Matrix ,A[i][j] stores residue of edge from i to j
        adj_matrix = np.zeros((vert, vert), dtype=np.int)
        for i in range(vert):
            for j in range(len(graph[i])):
                temp1, temp2 = graph[i][j]
                adj_matrix[i, temp1] = temp2
        self.adj_matrix_capacitites = deepcopy(adj_matrix)

        # loop |E| times on modified DFS
        # Loop can run maximum of |E| times
        for i in range(edges):
            # exit if no edge from source
            if len(graph_sets[source]) == 0:
                break

            # Find a s-t path
            path, self.current_flow = self.find_path(graph_sets, adj_matrix, final_graph_adj)
            # If no path exists then terminate the loop
            if path is None:
                continue

            # Now update the graph, using the flow for the augmenting path found
            # Save this graph so that it can be displayed in the GUI
            for i in range(vert):
                final_graph[i] = []
                for j in range(len(graph[i])):
                    temp1, temp2 = graph[i][j]
                    final_graph[i].append((temp1, final_graph_adj[i, temp1]))
            self.states.append((path, deepcopy(final_graph), self.current_flow))
            print 'found path', path

        # final_graph_adj stores the weights of each edge in the blocking flow graph
        # final_graph contains the blocking flow graph in reqd. format
        # process the final graph to required format
        for i in range(vert):
            final_graph[i] = []
            for j in range(len(graph[i])):
                temp1, temp2 = graph[i][j]
                final_graph[i].append((temp1, final_graph_adj[i, temp1]))

        return final_graph, final_graph_adj

    def find_path(self, graph_sets, adj_matrix, final_graph_adj):
        """
        Finds s-t path, returns 'None' if no such path exists
        """
        source = self.source
        sink = self.sink

        # initialize path and minimum weight along s-t path
        path = []
        path.append(source)

        ret_path = None
        current_flow = 0

        # finds a single s-t path and updates residues along that path.
        while True:

            # if path is empty then exit and terminate the bfs
            # since above means no s-t path is there
            if len(path) == 0:
                break

            # get last vertex in s-t path
            curr = path[-1]

            # Check if any vertices are adjacent to curr
            # If no, then no s-t path exists
            # Mark all incident edges for deletion next time they are seen
            # Achieve above by setting all adjacency matrix entries -1 for that vertex

            # Change to true if you find a child of curr
            child_exists = False

            # find the last available child of curr
            while (not child_exists) and len(graph_sets[curr]) != 0:
                # get last vertex adjacent to curr
                child = graph_sets[curr].pop()

                # if valid child found
                if adj_matrix[curr, child] != 0:
                    child_exists = True
                    # add back popped edge if it is a valid child
                    graph_sets[curr].add(child)

            # if no child node found, then set curr for deletion
            if len(graph_sets[curr]) == 0:
                # set for deletion in adj_matrix
                adj_matrix[:, curr] = 0
                # remove vertex from path
                path.pop()
                continue

            # else path augmentation with child
            # update path and min_wt in path

            path.append(child)

            # if s-t path is found
            if child == sink:

                # Find min_wt
                min_wt = float('inf')

                path_edges = zip(path, path[1:])

                for i, j in path_edges:
                    if adj_matrix[i, j] < min_wt:
                        min_wt = adj_matrix[i, j]

                # Decrement path weight by minimum weight along entire path
                # and update final_graph
                ret_path = list(path)

                current_flow += min_wt

                while len(path) > 1:
                    temp1 = path.pop()
                    temp2 = path[-1]
                    adj_matrix[temp2, temp1] = adj_matrix[temp2, temp1] - min_wt
                    final_graph_adj[temp2, temp1] = final_graph_adj[temp2, temp1] + min_wt
                print 'path', ret_path
                print 'current_flow', current_flow
                break
        return ret_path, current_flow
