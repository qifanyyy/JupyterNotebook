#!/usr/bin/python

import GenGraph
import Sollins
import Prims
import Kruskals
import time
import copy
from Node import Node

def driver():
	print "Hello! This is a program which randomly generates nodes and edges to connect those nodes.",
	print "After the graph is generated, you can then choose from finding an MST of each tree created",
	print "by using either Prim's, Kruskal's, or Sollin's algorithm. Addtionally, there are two methods",
	print "of generating edges. The first method is to randomly assign a weight between 1 and the user-defined",
	print "maximum edge weight, the second is to assign the weight based on the actual distance between",
	print "the two nodes. Finally, the amount of nodes in the graph, the size of the graph, and the k-value,",
	print "which determines the likelihood any two nodes will have an edge between them."

	print "Which method of edge generation would you like to use?"
	print "1: Weight based on actual distance between nodes"
	print "2: Weight based on user-defined maximum edge weight"
	edgeMethod = int(raw_input('> '))

	print "How many nodes are in the graph (any number greater than 0)?"
	totalNodes = int(raw_input('> '))
	print "How big is the graph (any number greater than 0)?"
	graphSize = int(raw_input('> '))
	print "What is the k-value that should be used (any number greater than 0)?"
	kval = int(raw_input('> '))
	maxWeight = 0
	if edgeMethod == 2:
		print "What is the maximum weight of an edge (any number greater than 0)?"
		maxWeight = int(raw_input('> '))
	trees = GenGraph.GenerateGraph(totalNodes, graphSize, maxWeight, kval, edgeMethod)
	print "Here are the adjacency lists of the trees randomly generated using your inputs (format = ((x,y,) weight)):"
	printTrees(trees, "Tree")
	print "Here are the MSTs for each of the generated trees."
	pTrees = copy.deepcopy(trees)
	start= time.clock()
	MSTs = Prims.runPrims(pTrees)
	pTot = (time.clock()-start)
	print "Result of Prim's"
	printTrees(MSTs,"MST")
	kTrees = copy.deepcopy(trees)
	start= time.clock()
	MSTs = Kruskals.runKruskals(kTrees)
	kTot = (time.clock()-start)
	print "Result of Kruskal's"
	printTrees(MSTs,"MST")
	sTrees = copy.deepcopy(trees)
	start= time.clock()
	MSTs = Sollins.runSollins(sTrees)
	sTot = (time.clock()-start)
	print "Result of Sollin's"
	printTrees(MSTs,"MST")
	print "Prim's Algorithm Run Time = "+str(pTot)
	print "Kruskal's Algorithm Run Time = "+str(kTot)
	print "Sollin's Algorithm Run Time = "+str(sTot)

def printTrees(trees, term):
	print term+"s:"
	for t in trees:
		print term+":{"
		for x in t:
			print printNode(x)+": {",
			for y in x.adjList:
				print "("+printNode(y)+", "+str(round(x.adjList[y],2))+")",
			print "}"
		print "}"

def printNode(n):
	return "("+str(n.xloc)+","+str(n.yloc)+")"

driver()