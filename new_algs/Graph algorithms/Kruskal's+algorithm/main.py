from graph import Graph
from kruskal import MST_Kruskal
import sys

def driver():
    #redirects print statements to out.text
    sys.stdout = open("out.txt", "w")
    #builds an empty graph
    graph = Graph()
    #inserts vertices into graph
    #a=0, b=1,c=2,d=3,e=4,f=5
    a = graph.insert_vertex(0)
    b = graph.insert_vertex(1)
    c = graph.insert_vertex(2)
    d = graph.insert_vertex(3)
    e = graph.insert_vertex(4)
    f = graph.insert_vertex(5)
    #inserts edges into graph
    graph.insert_edge(a, b, 4)
    graph.insert_edge(a, c, 1)
    graph.insert_edge(b, c, 3)
    graph.insert_edge(b, d, 6)
    graph.insert_edge(b, e, 5)
    graph.insert_edge(b, f, 4)
    graph.insert_edge(c, d, 4)
    graph.insert_edge(d, e, 2)
    graph.insert_edge(d, f, 3)
    graph.insert_edge(e, f, 2)
    #builds MST from graph
    kruskalTree = MST_Kruskal(graph)
    print("Graph Edges: Origin, Destination, Weight of edge \n")
    print("Vertex legend: a=0, b=1,c=2,d=3,e=4,f=5 \n")
    totalWeight = 0
    for edge in kruskalTree:
        totalWeight += edge._element
        print("Origin: " + str(edge._origin._element) + " Destination: " + str(edge._destination._element) + " Weight of edge: " + str(edge._element) + "\n")
    print("Sum of Original Graph Weights:")
    print(str(34) + "\n")
    print("Kruskal MST Weight:")
    print(str(totalWeight))
    sys.stdout.close()    

if __name__ == '__main__':
    driver()
