from flow_network import FlowNetwork
from linked_list import LinkedList

class RelabelToFront:
    """
    Relabel-To-Front data structure.
    """

    def __init__(self, network, source, sink):
        """
        Generates a relabel-to-front data structure to
        compute mas-flows.
        """
        self.network = network
        self.source = source
        self.sink = sink
        self.excess = {}
        self.height = {}
        self.current = {}

    
    def initializePreflow(self):
        """Initializes a pre-flow that will evolve into a
        max-flow during the execution of the algorithm.
        Sets the source at the highest level and pushes
        flow in a greedy way, completely saturating its
        leaving edge capacities.
        """
        for vertex in self.network.vertices():
            self.excess[vertex] = 0
            self.height[vertex] = 0

        for edge in self.network.edges():
            self.network.setFlow(edge, 0)

        self.height[self.source] = len(self.network.vertices())

        for vertex in self.network.neighbors(self.source):
            edge = (self.source, vertex)
            capacity = self.network.getCapacity(edge)

            self.network.setFlow(edge, capacity)
            self.excess[self.source] -= capacity
            self.excess[vertex] = capacity


    def push(self, fromVertex, toVertex):
        """
        pushes as much excess flow as possible through the edge
        (fromVertex, toVertex).
        """
        edge = (fromVertex, toVertex)

        deltaFlow = min(self.excess[fromVertex],
                        self.network.getResidualCapacity(edge))

        self.network.increaseFlow(edge, deltaFlow)
        self.excess[fromVertex] -= deltaFlow
        self.excess[toVertex] += deltaFlow


    def relabel(self, vertex):
        """
        Relabels an overflowing vertex with the proper height so that
        it can push part of its excess flow to one of its residual
        neighbors at subsequent steps.
        """
        self.height[vertex] = 1 + min(self.height[v] for v in self.network.residualNeighbors(vertex))


    def canPush(self, fromVertex, toVertex):
        """
        Checks whether an edge is suitable to push flow.
        """ 
        edge = (fromVertex, toVertex)
        return self.network.getResidualCapacity(edge) > 0 \
               and self.height[fromVertex] == self.height[toVertex] + 1


    def discharge(self, fromVertex):
       """
       Discharges an overflowing vertex completely, iterating over its
       residual neighbors, pushing flow and relabeling as appropriate.
       """
       while self.excess[fromVertex] > 0:
            if self.current[fromVertex] < len(self.network.adjacent[fromVertex]):
                toVertex = self.network.adjacent[fromVertex][self.current[fromVertex]]

                if self.canPush(fromVertex, toVertex):
                    self.push(fromVertex, toVertex)

                else:
                    self.current[fromVertex] += 1

            else:
                self.relabel(fromVertex)
                self.current[fromVertex] = 0
    

    def maxFlow(self):
        """
        Computes a max-flow across the network. Initializes a pre-flow,
        maximally overcharging the vertices directly reachable from the
        source, and maintains a queue to ensure that the vertices are
        processed in the correct order, completely discharging an over-
        flowing vertex at each step.
        """
        self.initializePreflow()

        vertices = LinkedList()
        for vertex in self.network.vertices():
            if vertex != self.source and vertex != self.sink:
                vertices.add(vertex)
            self.current[vertex] = 0

        vertex = vertices.head
        while vertex != None:
            prevHeight = self.height[vertex.value]
            self.discharge(vertex.value)
            if self.height[vertex.value] > prevHeight:
                vertices.moveToFront(vertex)
            vertex = vertex.next

        return self.network.getFlowAcrossVertex(self.source)

