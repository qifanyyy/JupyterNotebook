#!/usr/bin/python

import GenGraph
import Sollins
import Prims
import Kruskals
import time
from Node import Node

def driver():
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
	maxWeight = 1
	if edgeMethod == 2:
		print "What is the maximum weight of an edge (any number greater than 0)?"
		maxWeight = int(raw_input('> '))
	pTot = list()
	kTot = list()
	sTot = list()
	for i in xrange(1000):
		print i
		trees = GenGraph.GenerateGraph(totalNodes, graphSize, maxWeight, kval, edgeMethod)
		start= time.clock()
		Prims.runPrims(trees)
		pTot.append(time.clock()-start)

		start= time.clock()
		Kruskals.runKruskals(trees)
		kTot.append(time.clock()-start)

		start= time.clock()
		Sollins.runSollins(trees)
		sTot.append(time.clock()-start)
	print "Prim's Algorithm Avg. Run Time = "+str(sum(pTot) / float(len(pTot)))
	print "Kruskal's Algorithm Avg. Run Time = "+str(sum(kTot) / float(len(kTot)))
	print "Sollin's Algorithm Avg. Run Time = "+str(sum(sTot) / float(len(sTot)))

def printTrees(trees, term):
	print term+"s:"
	for t in trees:
		print term+":{"
		for x in t:
			print printNode(x)+": {",
			for y in x.adjList:
				print "("+printNode(y)+", "+str(x.adjList[y])+")",
			print "}"
		print "}"

def printNode(n):
	return "("+str(n.xloc)+","+str(n.yloc)+")"

driver()