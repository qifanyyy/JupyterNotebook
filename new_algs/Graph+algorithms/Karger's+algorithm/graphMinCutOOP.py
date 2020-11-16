#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 19:34:35 2018

@author: Andrew Shillito

Possible Future Changes:
    self.graph[node]->set() instead of list
"""

import random, copy, os, re, pdb

class Graph(object):
    def __init__(self): 
        self.edges = []
        self.graph = {}
        
    def getNodes(self):
        return list(self.graph.keys())
    
    def getEdges(self):
        return self.edges[:]
  
    def contractNodes(self):
        """Karger's algorithm for random node contraction"""
        edge = self.selectEdge() #select random edge
#        print("Selected", edge)
        source = edge.getSrc() #find source node
        dest = edge.getDest() #find destination node
        newNodeName = source.getName()+', '+dest.getName()

        #create new superNode
        newNode = Node(newNodeName)
        self.addNode(newNode) #just leave as is - broke program somehow when I changed addNode function      
        self.graph[newNode]=list(set(self.graph[source])^set(self.graph[dest]))

#        print([str(i)[6:] for i in self.edges]))
        self.updateEdges(source, dest, newNode)
#        print([str(i)[6:] for i in self.edges]))
        
        del self.graph[source]
        del self.graph[dest]
#        print(self)
        return None
    
    def updateEdges(self, source, dest, newNode):
        """Remove self-loops and change source nodes/dest nodes of edges to newNode if necessary"""
        #iterate over self.edges[:]
        #remove self loops from self.edges
        #update edge tail or head accordingly of edges connecting to newNode
        #since edges are changed the graph updates simultaneously
        for i in self.edges[:]:
            #removes self loops
            if i.tail==source and i.head==dest:
                self.edges.remove(i) #O(n) time each time
            elif i.tail==dest and i.head==source:
                self.edges.remove(i)
            #updates edges
            elif i.tail==source or i.tail==dest:
                i.setSrc(newNode)
            elif i.head==source or i.head==dest:
                i.setDest(newNode)
        return None

    def selectEdge(self):
        randEdge = random.sample(self.edges, 1)[0]
        return randEdge
    
    def removeSelfLoops(self, node, otherNode, edge):
        return None
    
    def contract(self, node, otherNode):
        return None
    
    def addNode(self, node):
        self.graph[node]=[]
        return None
    
    def removeNode(self, node):
        del self.graph[node]
        try:
            del self.graph[node]
        except KeyError:
            print("No such node in Graph")
        return None
    
    def addEdge(self, node, otherNode):
        newEdge = Edge(node, otherNode)
        self.graph[node].append(newEdge)
        self.graph[otherNode].append(newEdge)
        self.edges.append(newEdge)
        return None
    
    def removeEdge(self, edge):
        try:
            self.edges.remove(edge)
            self.graph[edge.getSrc()].remove(edge)
            self.graph[edge.getDest()].remove(edge)
        except ValueError:
            print("Edge not present")
            pass
        return None
    
    def __str__(self):
        ansString = '\nGraph: Node-->Edges\n'
        for node in self.graph:
            ansString+= node.getName()+" --> "
            for edge in self.graph[node]:
                temp = edge.getNodes()
                ansString+='('+temp[0].getName()+ "->" +temp[1].getName()+')'+', '
            ansString = ansString[:-2]+'\n'
        return ansString[:-1]
    

class Node(object):
    
    nodeDict = {} #purely for building graphs from the files given
    
    def __init__(self, name): #edges a list of edges??
        self.name = name
        Node.nodeDict[name]=self
    
    def getName(self):
        return self.name
    
    def getNodeByName(name): #only used for graph construction
        try:
            return Node.nodeDict[name]
        except KeyError:
            return False #this could redirect to graph keys if graph passed in
        
    def __str__(self):
        return "Node: "+self.name
    
class Edge(object):
    
    def __init__(self, tail, head):
        self.tail = tail
        self.head = head

    def getNodes(self):
        return (self.tail, self.head)
    
    def getSrc(self):
        return self.tail
    
    def getDest(self):
        return self.head
    
    def setSrc(self, source):
        self.tail = source
        return None
    
    def setDest(self, dest):
        self.head = dest
        return None
    
    def __str__(self):
        ansString = "Edge: "+self.tail.name+" --> "+self.head.name
        return ansString

def constructGraph():
    directory = os.getcwd()+"\\testCases\\"
    graphs = []
    outputs = []
    testFiles = [i for i in os.listdir(directory) if "Output" not in i and ".rtf" not in i and "karger" not in i]
#    print(testFiles)
    outputFiles = [j for j in os.listdir(directory) if "Output" in j]
#    print(outputFiles)
    for x in range(len(testFiles)):
        graph = Graph()
        testFileRead(directory+testFiles[x], graph)
        outputs.append(outputFileRead(directory+outputFiles[x]))
        graphs.append(graph)
        Node.nodeDict = {}
    return graphs, outputs

def testFileRead(fileName, graph):
    file = open(fileName)
#    pdb.set_trace()
    for line in file: #first build the graph nodes
        temp = re.split(r"\D", line)
        while "" in temp:
            temp.remove('')
        node = Node(temp[0])
        graph.addNode(node)
#    print(graph, "\n")
    file.close()
    file = open(fileName)
    for linePass2 in file: #now add the edges
        temp = re.split(r"\D", linePass2)
        while "" in temp:
            temp.remove('')
        node = Node.getNodeByName(temp[0])
        temp = temp[1:] #isolate edges
        if len(graph.graph[node])==0:
            for i in temp:
                otherNode = Node.getNodeByName(i)
                graph.addEdge(node, otherNode)
        else:
            #this node is a head for an edge
            #find src node of each edge
            #remove src node name from temp if present
            #continue and add all remaining edges as normal
            for edge in graph.graph[node]:
                if edge.getSrc().name in temp:
                    temp.remove(edge.getSrc().name)
            for j in temp:
                otherNode = Node.getNodeByName(j)
                graph.addEdge(node, otherNode)
    file.close()
    return None
    
def outputFileRead(fileName):
    file = open(fileName)
    for line in file:
        temp = re.split(r'\D', line)
        ans = temp[0]
    file.close()
    return ans

def graphMinCut(graph, numTests):
    """graphMinCut takes graph of nodes/edges, duplicates it using copy.deepcopy() 
    and run's karger's contraction algorithm numTests times.
    graph.contractNodes() is the actual algorithm
    returns best (shortest length) min cut num"""
    best = 100000 #arbitrarily large num
#    pdb.set_trace()
    for i in range(numTests):
        if i%10==0:
            print("Trial num:", i)
        testGraph = copy.deepcopy(graph)
        while len(testGraph.graph)>2:
            testGraph.contractNodes() #this is the hub for the entire algorithm
        Node.nodeDict.clear
        for node in testGraph.graph: #exactly 2 tests but each should be the same length
            if len(testGraph.graph[node])<best:
                best = len(testGraph.graph[node])
                minCutGraph = copy.deepcopy(testGraph)
    return best, minCutGraph

def simpleTest():
    graphList, outputs = constructGraph()
#    print(outputs)
    ans = graphList[0]
    print(ans, "\n")
#    ans.contractNodes()
    return ans #for now - graphList later

def singleGraphTest(numTrials, graphIndexNum):
    """builds graphs, runs numtrials karger algo on graph selected by graphIndex from graphList
    constructed by constructGraph()"""
    graphList, outputs = constructGraph()
    testGraph = graphList[graphIndexNum]
    print(testGraph)
    output = outputs[graphIndexNum]
    best, minCut = graphMinCut(testGraph, numTrials)
    return best, minCut, int(output)==best

def finalGraphTest(numTrials):
    directory = os.getcwd()+"\\testCases\\"
    testFiles = [i for i in os.listdir(directory) if "karger" in i]
    for x in range(len(testFiles)):
        graph = Graph()
        testFileRead(directory+testFiles[x], graph)
        Node.nodeDict = {}
    ans = 17
    best, minCut = graphMinCut(graph, numTrials)
    return best, minCut, best==ans

#single graph test case testing - just change index for different graphs 0-5
#best, minCut, test = singleGraphTest(100, 4)
#print("\nBest:", best, test, minCut)
