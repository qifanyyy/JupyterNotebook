from flow_network import FlowNetwork

class PushRelabel:
    """
    Push-Relabel data structure.
    """

    def __init__(self, network, source, sink):
        """
        Generates push-relabel data structure to
        compute max-flows.
        """
        self.network = network
        self.source = source
        self.sink = sink
        self.overflow = []
        self.pushable = {}
        self.excess = {}
        self.height = {}


    def initializePreflow(self):
        """
        Initializes a pre-flow that will evolve into a 
        max-flow during the execution of the algorithm.
        Sets the source at the highest level and pushes
        flow in a greedy way, completely saturating its
        leaving edge capacities.
        """
        for vertex in self.network.vertices():
            self.excess[vertex] = 0
            self.height[vertex] = 0
            self.pushable[vertex] = set() 

        for edge in self.network.edges():
            self.network.setFlow(edge, 0)

        self.height[self.source] = len(self.network.vertices())

        for neighbor in self.network.neighbors(self.source):
            edge = (self.source, neighbor)
            capacity = self.network.getCapacity(edge)

            self.network.setFlow(edge, capacity)
            self.excess[self.source] -= capacity
            self.excess[neighbor] = capacity

            if neighbor != self.sink:
                self.overflow.append(neighbor)


    def push(self, fromVertex, toVertex):
        """
        Pushes as much excess flow as possible through the edge
        (fromVertex, toVertex), possibly restoring a correct flow
        through the source vertex, fromVertex, and potentially
        making the destination vertex, toVertex, overflow.
        """
        edge = (fromVertex, toVertex)
        edgeResidualCapacity = self.network.getResidualCapacity(edge)
        deltaFlow = min(self.excess[fromVertex], edgeResidualCapacity) 

        self.network.increaseFlow(edge, deltaFlow)
        self.excess[fromVertex] -= deltaFlow
        self.excess[toVertex] += deltaFlow

        if self.excess[fromVertex] > 0:
            self.overflow.append(fromVertex)

        if self.excess[toVertex] == deltaFlow and toVertex != self.sink:
            self.overflow.append(toVertex)

        if self.network.getResidualCapacity(edge) > 0:
            self.pushable[fromVertex].add(toVertex)


    def relabel(self, vertex):
        """
        Relabels an overflowing vertex with the proper heigh so that
        it can push part of its excess flow to one of its residual
        neighbors at subsequent steps.
        """
        self.height[vertex] = 1 + min(self.height[v] for v in self.network.residualNeighbors(vertex))

        for neighbor in self.network.adjacent[vertex]:
            edge = (vertex, neighbor)

            if vertex in self.pushable[neighbor]: 
                self.pushable[neighbor].remove(vertex)
                
            elif self.isPushable(edge):
                self.pushable[vertex].add(neighbor)


    def isPushable(self, edge):
        """
        Checks whether an edge is suitable to push flow.
        """
        fromVertex, toVertex = edge
        return self.network.getResidualCapacity(edge) > 0 \
               and self.height[fromVertex] == self.height[toVertex] + 1 


    def maxFlow(self):
        """
        Computes a max-flow across the network. Initializes a pre-flow,
        maximally overcharging the flow across the vertices directly
        reachable from the source, and discharges overflowing vertices
        step by step.
        """
        self.initializePreflow()

        while self.overflow:
            fromVertex = self.overflow.pop()

            if self.canPush(fromVertex):
                toVertex = self.pushable[fromVertex].pop()
                self.push(fromVertex, toVertex)

            else:
                self.relabel(fromVertex)
                self.overflow.append(fromVertex)

        return self.network.getFlowAcrossVertex(self.source) 


    def canPush(self, fromVertex):
        """
        Checks whether there are pushable edges leaving a vertex.
        """
        return len(self.pushable[fromVertex]) > 0

