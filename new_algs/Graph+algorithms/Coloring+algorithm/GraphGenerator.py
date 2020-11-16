from graph import Graph
from node import Node
import random
from math import pow
from math import sqrt

def euclidianDist(x1,y1,x2,y2):
	return sqrt(pow(x1-x2,2) + pow(y1-y2,2))

def generateDisconnectedRandomGeometricGraph(n,r=0.05):
	nodesPos=[]
	nodes=[]
	for i in range (n):
		newNode = Node()
		x=random.random()
		y=random.random()
		j=0
		for otherNode in nodesPos:
			if euclidianDist(x,y,otherNode[0],otherNode[1]) <= r :
				newNode.add(nodes[j])
			j+=1
		nodesPos.append([x,y,i])
		nodes.append(newNode)
	g = Graph("",*nodes)
	return g

def generateConnectedRandomGeometricGraph(n,r=0.05):
	nodesPos=[]
	nodes=[]
	
	for i in range (n):
		newNode = Node()		

		connected = False
		while (not connected):
			if(i == 0):
				connected=True
			x=random.random()
			y=random.random()
			j=0
			for otherNode in nodesPos:
				if euclidianDist(x,y,otherNode[0],otherNode[1]) <= r :
					newNode.add(nodes[j])
					connected=True
				j+=1
		nodesPos.append([x,y,i])
		nodes.append(newNode)
	g = Graph("",*nodes)
	return g

if __name__ == "__main__":
	print (generateConnectedRandomGeometricGraph(10))
