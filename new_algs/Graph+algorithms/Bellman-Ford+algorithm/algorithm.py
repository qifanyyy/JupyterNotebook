class BellmanFord(object):

    def calculateShortestPath(self, graph, start):
        
        dist = [float("inf") for x in range(graph.V)]
        dist[start]=0.0

        #calculate shortest paths from start vertex to all other vertices
        self.calc(graph, dist, False)

        #rerun algorithm to find vertices which are part of a negative cycle
        self.calc(graph, dist, True)

        return dist

    def calc(self, graph, dist, findNegativeCycle):

        numVertices = graph.V
        numEdges = len(graph.edges)

        for i in range(0, numVertices-1):
            for j in range (numEdges):
                for edge in graph.getEdge(j):
                    minDist = dist[edge.targetVertex]
                    newDist = dist[edge.startVertex] + edge.weight

                    if newDist < minDist:
                        if findNegativeCycle==True:
                            dist[edge.targetVertex] = float("-inf") 
                        else:
                            dist[edge.targetVertex] = newDist
        
        return dist