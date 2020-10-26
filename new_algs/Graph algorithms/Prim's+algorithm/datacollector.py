# Put your solution here.

import networkx as nx
from math import ceil
import random
from heapq import heappop, heappush
from itertools import count
import random
import numpy as np

# when you solve for any graph, we will keep a matrix of size nk to build and save to separate file at the end
def solve(client):
    # f = open("results.txt", "a+")

    client.end()

    matrix = []

    for i in range(90):
        client.start()

        graph = client.G

        locations = list(graph.nodes())
        numlocations = len(list(graph.nodes()))
        print("numlocations is ", str(numlocations))

        all_students = list(range(1, client.students + 1))
        numstudents = client.students

        print("num students is", str(numstudents))

        minNumTruth = ceil(numlocations / 2)

        numTruth = [0 for _ in range(numstudents)]
        numLies = [0 for _ in range(numstudents)]

        #evaluate all locations but in random order
        loc = list(range(numlocations))
        random.shuffle(loc)

        for randomloc in loc:
            #scount on location and collect student reports
            temp_locations = client.scout(locations[randomloc], all_students)
            if temp_locations is None:
                continue
            studentreports = list(temp_locations.values())

            #remote on location get the actual value
            target = locations[randomloc]
            nextEdges = list(graph.edges(target, 'weight', default=0))
            minEdgeIndex = 0
            minEdge = -1
            for i in range(len(nextEdges)):
                if i == 0:
                    minEdge = nextEdges[i][2]
                    minEdgeIndex = i
                if nextEdges[i][2] < minEdge:
                    minEdge = nextEdges[i][2]
                    minEdgeIndex = i
            actualvalue = int(client.remote(target, nextEdges[minEdgeIndex][1]))

            for i in range(numstudents):
                studentreport = int(studentreports[i])
                if studentreport == actualvalue: #is telling the truth
                    numTruth[i] += 1
                else:
                    numLies[i] -=1
                worstcaseprob = (minNumTruth - numTruth[i]) / (numlocations - numTruth[i] - numLies[i])
                matrix.append([worstcaseprob, studentreport, actualvalue])
        client.end()

    np.savetxt("results.txt", np.array(matrix, np.float64))
    # f.write(str(matrix))
    # f.close()


    client.end()
