from algorithm import BellmanFord
from graph import Graph
from edge import Edge

graph = Graph(8)

graph.addEdge(0, 1, 1)
graph.addEdge(1, 2, 1)
graph.addEdge(1, 6, 1)
graph.addEdge(2, 3, 1)
graph.addEdge(3, 4, 1)
graph.addEdge(4, 5, -4)
graph.addEdge(5, 3, 2)
graph.addEdge(2, 6, 3)
graph.addEdge(2, 7, 2)
graph.addEdge(6, 7, 4)
graph.addEdge(0, 7, 5)

bellmanFord = BellmanFord()
d = bellmanFord.calculateShortestPath(graph, 0)

for i in range(graph.V):
    print("The cost to get from node % d to % d is: % 5.2f" %(0, i, d[i]))