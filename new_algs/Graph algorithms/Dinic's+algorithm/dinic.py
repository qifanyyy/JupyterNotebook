""" Implementation of Dinic's algorithm for max flow """
from gui.image_display import ImageSequence
from block_flow import BlockingFlowImageSequence
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from graph import display_graph, graph_image
import random
import numpy as np
from Queue import Queue
from copy import deepcopy

INF = float('inf')  # use double inf


def find_distances(graph, source):
    """ Find distances using bfs """
    dist = [INF for _ in graph]
    q = Queue()
    dist[source] = 0
    q.put(source)
    while(q.empty() == 0):
        current = q.get()
        for t in graph[current]:
            if dist[t[0]] == INF:
                dist[t[0]] = dist[current] + 1
                q.put(t[0])
    return dist


class DinicImageSequence(ImageSequence):
    """ dinic image sequence """

    def __init__(self, graph, nvertices, nedges, source, sink):
        ImageSequence.__init__(self)

        # Self.graph is initialized to graph with all weights as zero
        self.graph_adj = np.zeros((nvertices, nvertices), dtype=np.int)

        self.graph = [[] for i in range(nvertices)]
        for i in range(nvertices):
            for j in range(len(graph[i])):
                temp1, temp2 = graph[i][j]
                self.graph[i].append((temp1, 0))
                self.graph_adj[i, temp1] = 0

        # Stores maximum capcities

        self.graph_capacity_adj = np.zeros((nvertices, nvertices), dtype=np.int)
        for i in range(nvertices):
            for j in range(len(graph[i])):
                temp1, temp2 = graph[i][j]
                self.graph_capacity_adj[i, temp1] = temp2

        self.residual_graph = graph

        # Store edges,vertices,source and sink vertex
        self.edges = nedges
        self.vertices = nvertices
        self.source = source
        self.sink = sink

        self.flow = 0
        self.done = False
        # status=1 when blocking flow is in progress
        self.status = 0
        self.blocking_flow = None
        self.current_flow = 0
        print "dinic with", graph

        # display graph in subplot
        # a = self.fig.add_subplot(1, 2, 1)
        # plt.imshow(graph_image(graph))

    def init_image(self):
        # set init image
        display_graph(self.residual_graph, 'dinic_init', source=self.source, sink=self.sink, size_graph = 'l')
        return mpimg.imread('dinic_init.png')

    def init_image_original(self):
        # set init image
        display_graph(self.residual_graph, 'dinic_init', source=self.source, sink=self.sink, size_graph = 's')
        return mpimg.imread('dinic_init.png')

    def find_level_graph(self):
        self.level_graph = [[] for _ in self.graph]
        for i, l in enumerate(self.residual_graph):
            for j, c in l:
                if self.dist[j] - self.dist[i] == 1:
                    self.level_graph[i].append((j, c))
                else:
                    self.level_graph[i].append((j, 0))

    def next_image(self):
        self.aux_text = 'Current flow : %d' % self.current_flow
        flow_graph_image = graph_image(self.graph, capacities=self.graph_capacity_adj, source=self.sink, sink=self.source)
        if self.status == 1:
            print 'in blocking flow'
            self.title = "in blocking flow"
            if self.blocking_flow.complete():
                print 'blocking flow complete'
                self.status = 0
                self.title = "Blocking Flow Complete"
                return graph_image(self.blocking_flow.block_flow,
                                   capacities=self.blocking_flow.adj_matrix_capacitites,
                                   source=self.source, sink=self.sink), flow_graph_image

            _next = self.blocking_flow.next_image()

            self.current_flow += self.blocking_flow.current_flow
            self.aux_text = 'Current flow : %d' % self.current_flow
            return _next, flow_graph_image
        else:
            self.find_residual()
            self.dist = find_distances(self.residual_graph, self.source)
            self.find_level_graph()
            self.title = 'Finding Residual and Level Graph'

            if self.dist[self.sink] == INF:
                self.done = True
                print 'completed dinics'
                self.title = 'Completed!'
                return graph_image(self.graph, highlight_path=None, capacities=self.graph_capacity_adj, source=self.source, sink=self.sink), flow_graph_image
            else:
                # find blocking flow
                print 'Finding Blocking Flow'
                self.blocking_flow = BlockingFlowImageSequence(self.level_graph, self.vertices, self.edges, self.dist, self.source, self.sink)
                self.status = 1

                image = self.blocking_flow.init_image()
                self.block_flow_graph = self.blocking_flow.block_flow
                self.block_flow_adj = self.blocking_flow.block_flow_mat

                self.update_flow()

                self.aux_text = 'Current flow : %d' % self.current_flow
                return image, flow_graph_image

    def complete(self):
        return self.done

    def find_residual(self):
        # capacity_graph gives a graph with all the maximum capacity of the edges

        vert = self.vertices

        # Residual graph
        res_graph = [[] for i in range(vert)]
        res_adj_matrix = np.zeros((vert, vert), dtype=np.int)

        # Capacity graph adj matrix
        wt_adj_matrix = deepcopy(self.graph_capacity_adj)

        # original graph adjacency matrix
        adj_matrix = np.zeros((vert, vert), dtype=np.int)

        for i in range(vert):
            for j in range(len(self.graph[i])):
                temp1, temp2 = self.graph[i][j]
                adj_matrix[i, temp1] = temp2

        # Find residual graph
        for i in range(self.vertices):
            for j in range(i + 1, self.vertices):
                res_adj_matrix[i, j] = (wt_adj_matrix[i, j] - adj_matrix[i, j]) + adj_matrix[j, i]
                res_adj_matrix[j, i] = (wt_adj_matrix[j, i] - adj_matrix[j, i]) + adj_matrix[i, j]

                # Store also as matrix and as a adjacency list form
                if res_adj_matrix[i, j] != 0:
                    res_graph[i].append((j, res_adj_matrix[i, j]))

                if res_adj_matrix[j, i] != 0:
                    res_graph[j].append((i, res_adj_matrix[j, i]))

        self.residual_graph = deepcopy(res_graph)

        return res_graph

    def update_flow(self):
        """
        Update self.graph etc, after getting a blocking_flow
        """
        self.graph_adj = self.graph_adj + self.block_flow_adj
        temp = deepcopy(self.graph)

        for i in range(self.vertices):
            temp[i] = []
            for j in range(len(self.graph[i])):
                t1, t2 = self.graph[i][j]
                temp[i].append((t1, self.graph_adj[i, t1]))

        self.graph = temp
