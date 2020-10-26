#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 05:56:10 2018

@author: Andrew Shillito

TestCase1: cuts are [(1,7), (4,5)]
TestCase2: cuts are [(1,7), (4,5)]
TestCase3: cut is [(4,5)]
TestCase4: cut is [(4,5)]
TestCase5: not listed
TestCase6: not listed
    
"""

import random, copy, re, os, pdb

def testCaseRead():
    """Builds graphs of testcase data, edgeList list of lists of tuples, and list of ints of their output
    graphList is list of dicts (graphs) and outputList is a list of ints
    returns tuple(graphList, edgeList, outputList)"""
    graphList = []
    outputList = []
    edgeList= [[],[],[],[],[],[]]
    for x in range(1,7):
        graph = {}
        file = open(os.getcwd()+"\\testCases\\"+"TestCase"+str(x)+".txt")
        for line in file:
            line = re.split(r"\D", line)
            if '' in line:
                line.remove('')
            graph[line[0]]=line[1:]
            for y in range(len(line[1:])):
                edgeList[x-1].append((line[0], line[1:][y]))
        graphList.append(graph)
        #implement edgeList as list of tuples
        #format: (tail, head)
        #however - must remove both one each - (tail, head) and (head, tail)
        #when removing
        file.close()
        outputFile = open(os.getcwd()+"\\testCases\\"+"TestCase"+str(x)+"Output.txt")
        for lne in outputFile:
            lne = re.split(r"\D", lne)
            outputList.append(int(lne[0])) #Only works for single digit numbers
        outputFile.close()
#    print(graphList)
#    print(outputList)
    return (graphList, edgeList, outputList)

def selectEdge(availableEdges):
    """Assumes availableEdges is a list of previously unchosen edges relating to graph
    selects edge at random and removes the edge and its reverse ie: (1,2)/(2,1)
    from the list. Returns tail, head as tuple for contraction later"""
#    pdb.set_trace()
    selectedEdge = random.sample(availableEdges, 1)[0]
    try:
        availableEdges.remove(selectedEdge)
        availableEdges.remove((selectedEdge[1], selectedEdge[0]))
    except ValueError:
        pass
    return (selectedEdge[0], selectedEdge[1])

def removeSelfLoops(graph, tail, head):
    """Removes self-loops from new contracted nodes"""
    tailNodes = re.split(r"\D", tail)
    while ' ' in tailNodes:
        tailNodes.remove(' ')
    headNodes = re.split(r"\D", head)
    while ' ' in headNodes:
        headNodes.remove(' ')
    graph[tail] = [x for x in graph[tail] if x not in tailNodes and x not in headNodes]
    graph[head] = [y for y in graph[head] if y not in tailNodes and y not in headNodes]
    return None

def combine(graph, availableEdges):
    """Hub for contract, removeSelfLoops, updateEdgeList subroutines
    contracts selected node chosen by selectEdge and 
    updates the graph and edgeLists"""
#    pdb.set_trace() #debugging beginning
    tail, head = selectEdge(availableEdges)
    contract(graph, tail, head) #also calls removeSelfLoops as a subroutine
    updateEdgeList(availableEdges, tail, head)
    return None

def contract(graph, tail, head):
    """Builds new node, removes self loops, and deletes previous nodes"""
    removeSelfLoops(graph, tail, head)#also Updates EdgeList
    graph[tail+", "+head] = graph[tail]+graph[head]
    del graph[tail]
    del graph[head]
    return None

def graphMinCut(graph, edgeList, numTests):
    """karger's algorithm for randomized minCut
    runs numTests times editing copies of graph and edgeList in place"""
    best = 10000
    for i in range(numTests):
        testGraph = copy.deepcopy(graph)
        availableEdges = copy.deepcopy(edgeList)
        while len(testGraph)>2:
            combine(testGraph, availableEdges)
            #to check after every iteration - I changed this and haven't double checked the results yet
#            for j in testGraph: 
#                best = min([best, len(testGraph[j])]) #double check this
        for j in testGraph:
            best = min([best, len(testGraph[j])])
    return best

def updateEdgeList(availableEdges, tail, head):
    """Bookkeeping for available edgeList"""
    remove = []
    for i in range(len(availableEdges)):
        #find the edges where tail or head are nodes
        #replace the node i[0] with tail, head
        #if head:tail or tail:head - remove the edge
        if availableEdges[i][0]==tail or availableEdges[i][0]==head:
            if availableEdges[i][1]==tail or availableEdges[i][1]==head:
#                del availableEdges[i]
                remove.append(i)
            else:    
                availableEdges[i]=(tail+', '+head, availableEdges[i][1])
        elif availableEdges[i][1]==tail or availableEdges[i][1]==head: #check for if tail or edge appear in any tuples
            availableEdges[i] = (availableEdges[i][0], tail+', '+head)
#    print(availableEdges)
    if remove!=[]:
        remove = remove[::-1] #sort returns noneType if called with empty list
        for j in remove:
            del availableEdges[j]
    return None

#graphs, edgesList, outputs = testCaseRead()

#for 5th test case testing
#graph = graphs[4]
#edgeList = edgesList[4]
#output = outputs[4]

def testCaseTesting():
    """testing for all testCases"""
    graphs, edgesList, outputs = testCaseRead()
    for i in range(len(graphs)):
        print(graphMinCut(graphs[i], edgesList[i], 10000)==outputs[i])
#updateEdgeList(edgeList, '1', '2')
def testCase5Test():
    """testing for testCase5"""
    graphs, edgesList, outputs = testCaseRead()
    graph = graphs[4]
    edgeList = edgesList[4]
    output = outputs[4]
    print(graphMinCut(graph, edgeList, 1000))
    print("expected:", output)
    
def finalTestRead():
    """programming assignment graph & edgeList builder"""
    graph = {}
    edgeList = []
    file = open("\\testCases\\kargerMinCut.txt")
    for line in file:
        line = re.split(r"\D", line)
        while '' in line:
            line.remove('')
        graph[line[0]]=line[1:]
        for y in range(len(line[1:])):
            edgeList.append((line[0], line[1:][y]))        
    file.close()
    return graph, edgeList


def testDriver(graph, edgeList, numTests, numSeeds):
    #    pdb.set_trace()
    best = 10000
    for x in range(numSeeds):
        random.seed(x)
        best = min([best, graphMinCut(graph, edgeList, numTests)])
        print(best)
    return best

#uncomment to run final assignment test
#graph, edgeList = finalTestRead()
#testDriver(graph, edgeList, 1000, 2)