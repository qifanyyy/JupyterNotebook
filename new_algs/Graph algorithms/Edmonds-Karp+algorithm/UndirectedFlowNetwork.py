# Network Max Flow Algorthim from wikipedia with minor change
# Unidrected is just directed flos on both sides
# http://stackoverflow.com/questions/7687732/maximum-flow-ford-fulkerson-undirected-graph
# Run in test see how it works

class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.sink = v
        self.capacity = w

    def __repr__(self):
        return '%s -> %s : %s ' %(self.source, self.sink, self.capacity)

class UndirectedFlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}

    def add_vertex(self, vertex):
        self.adj[vertex] = []

    def get_edges(self, v):
        return self.adj[v]

    def add_edge(self, u, v, w = 0):
        if u == v:
            raise ValueError('u == v')
        edge = Edge(u, v, w)
        # add reverse edge
        redge = Edge(v, u, w)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0

    # original wikipedia version, using DFS
    # def find_path(self, source, sink ,path):
    #     if source == sink:
    #         return path
    #     for edge in self.get_edges(source):
    #         residual = edge.capacity - self.flow[edge]
    #         if residual > 0 and edge not in path and edge.redge not in path:
    #             result = self.find_path(edge.sink, sink, path + [edge])
    #             if result != None:
    #                 return result

    # my implementation of BFS version
    def find_path(self, source, sink, path):
        queue = [(source, path)]
        while queue:
            (source, path) = queue.pop(0)
            for edge in self.get_edges(source):
                residual = edge.capacity - self.flow[edge]
                if residual > 0 and edge not in path and edge.redge not in path:
                    if edge.sink == sink:
                        return path + [edge]
                    else:
                        queue.append((edge.sink, path + [edge]))


    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [])
        while path != None:
            print 'path', path
            residuals = [edge.capacity - self.flow[edge] for edge in path]
            flow = min(residuals)
            print 'flow', flow
            for edge in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink, [])
            # print 'flow', self.flow

        return sum(self.flow[edge] for edge in self.get_edges(source))
