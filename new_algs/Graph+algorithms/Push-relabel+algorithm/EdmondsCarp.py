from Network import Vertex


# Edmonds-Carp implementation of the max flow problem
class EdmondsCarp:
    def __init__(self, network):
        self.network = network
        self.source = self.network.source
        self.sink = self.network.sink
        # raise an exception if either the source or the sink is not in the network
        if (self.source not in self.network.vertices.keys()) or (self.sink not in self.network.vertices.keys()):
            raise RuntimeError("Requested source or sink do not exist!")

    # use Breadth first search to find the bottle neck of the current shortest path
    def BFS(self):
        # set visited to false for all vertices first
        visited = dict.fromkeys(self.network.vertices.keys(), False)
        paths = {self.source: []}
        # set the initial queue to the source and set the initial flow of the path to infinity
        queue = [(self.source, float('inf'))]
        visited[self.source] = True
        # while the queue is not empty
        while queue:
            # pop the front element of the queue
            currVertex, currFlow = queue.pop(0)
            # for each neighbor of the current vertex
            for neighbor in self.network.vertices[currVertex]:
                currEdge = self.network.getEdge(currVertex, neighbor)
                currEdgeCapacity = currEdge.currentCapacity
                # if we haven't visited it and the edge between them has a positive current capacity
                if (not visited[neighbor]) and currEdgeCapacity > 0:
                    # add neighbor to visited
                    visited[neighbor] = True
                    # update the flow of the path if the current capacity is less than the current flow
                    # (because we're trying to find the bottle neck)
                    newFlow = min(currFlow, currEdgeCapacity)
                    # add parent's path to neighbor
                    paths[neighbor] = paths[currVertex] + [currEdge]
                    # if the neighbor is the sink, return the capacity of the path
                    # this path will be the shortest path from the source to sink
                    if neighbor == self.sink:
                        return newFlow, paths[neighbor]
                    # append the neighbor along with the new flow capacity
                    queue.append((neighbor, newFlow))
        # if there's no flow available, return 0
        return 0, []

    def getMaxFlow(self, currMaxFlow=0):
        # if 0 is returned, return
        bottleNeck, path = self.BFS()
        if bottleNeck == 0:
            return currMaxFlow
        # otherwise, add the current flow to the max flow
        currMaxFlow += bottleNeck
        for edge in path:
            self.network.addFlow(edge, bottleNeck, True)
        return self.getMaxFlow(currMaxFlow)
