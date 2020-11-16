'''
Created on Nov 30, 2017

@author: Manoj kumar
'''

from Vertex import Vertex;
from Edge import Edge;
import Algorithm;

node1 = Vertex("A");
node2 = Vertex("B");
node3 = Vertex("C");

edge1 = Edge(1,node1,node2);
edge2 = Edge(1,node2,node3);
edge3 = Edge(1,0);

node1.adjacenciesList.append(edge1);
node1.adjacenciesList.append(edge2);
node2.adjacenciesList.append(edge3);

vertexList ={node1,node2,node3};

Algorithm.calculateShortestPath(vertexList, node1);
Algorithm.getShorttestpathTo(node3)