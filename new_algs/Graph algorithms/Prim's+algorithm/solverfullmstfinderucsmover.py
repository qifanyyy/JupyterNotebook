# Put your solution here.

import networkx as nx
from math import ceil
import random
from heapq import heappop, heappush
from itertools import count
from client_tester import Client
from datetime import datetime
from statistics import stdev, mean
import pandas as pd
import os, pickle

epsilon = 0.2
rho = 0.000005
a = 0.8
b = 0.4
#0.4 and 0.2, ~40%. 1 and 0.5 also bad.

filename = 'finalized_model.sav'
model = pickle.load(open(filename, 'rb'))

def solve(client):
    client.end()
    client.start()

    graph = client.G

    #Start by finding location of all bots using scout and remote.
    all_students = list(range(1, client.students + 1))
    totalNodes = len(graph.nodes)
    minNumTruth = ceil(totalNodes / 2)

    numTruth = [0 for _ in range(client.students)]
    numLies = [0 for _ in range(client.students)]
    worstcaseprob = [(minNumTruth - numTruth[i]) / (totalNodes - numTruth[i] - numLies[i]) for i in range(client.students)]

    nodeReports = {}
    nodeDistance = {}
    botsAt = {}
    unvisited = list(graph.nodes())
    botsleft = client.bots - sum(client.bot_count)
    counter = 0
    shortest_path_mst = produce_shortest_path_mst(graph, list(graph.nodes()), client.h)

    while botsleft > 0 and len(unvisited) > 0:
        #Pick node selector
        unvisitedOrHasBot = combinelist(unvisited, client.bot_locations)
        #   Pick a subset of nodes from unvisited
        #       Use shortest path mst
        #mst = produce_shortest_path_mst(graph, unvisited, client.h)
        #       Use sparse mst for unvisited
        #mst = produce_sparse_mst(graph, unvisited, client.h)
        #       Use sparse mst for unvisited or has bot, but remove leaves until all leaves are unvisited
        # totalMst = produce_sparse_mst(graph, unvisitedOrHasBot, client.h)
        # totalMstLeaves = get_leaf_nodes(totalMst)
        # allLeavesUnvisited = False
        # while not allLeavesUnvisited:
        #    allLeavesUnvisited = True
        #    for checkLeaf in totalMstLeaves:
        #        if checkLeaf not in unvisited:
        #            totalMst.remove_node(checkLeaf)
        #            allLeavesUnvisited = False
        #    totalMstLeaves = get_leaf_nodes(totalMst)
        # mst = totalMst
        # leaves = get_leaf_nodes(mst)
        #   Pick all nodes in unvisited
        leaves = unvisited
        #   Remove home node if it is in leaves
        if client.h in leaves:
            leaves.remove(client.h)

        #Pick best node
        #   Scout and get reports for all node candidates
        for leaf in leaves:
            if leaf not in nodeReports:
                nodeReports[leaf] = list(client.scout(leaf, all_students).values())
                #print("Report:")
                #print(nodeReports[leaf])
                #print("For node: "+str(leaf))
        #   Pick distance measure mst
        #mstDist = nx.minimum_spanning_tree(graph)
        #mstDist = shortest_path_mst
        #mstDist = produce_sparse_mst(graph, leaves, client.h)
        #mstDist = produce_sparse_mst(graph, unvisited, client.h)
        #mstDist = produce_sparse_mst(graph, unvisitedOrHasBot, client.h)
        # for leaf in leaves:
        #     nodeDistance[leaf] = nx.shortest_path_length(mstDist, source=leaf, target=client.h)
        for leaf in leaves:
            closest_node = get_closest_node(graph, leaf)
            nodeDistance[leaf] = graph.edges[leaf,closest_node]['weight']
            #print("For node: " + str(leaf)+" minimum weight edge is " + str(nodeDistance[leaf]))
        targetLeaf = student_judgment(numTruth, numLies, worstcaseprob, leaves, nodeReports, nodeDistance, epsilon, rho, a, b)
        #print("Target leaf:" + str(targetLeaf))

        #Pick remote direction
        #mstRemote = nx.minimum_spanning_tree(graph)
        #mstRemote = produce_shortest_path_mst(graph, list(graph.nodes()), client.h)
        #mstRemote = produce_sparse_mst(graph, leaves, client.h)
        #mstRemote = produce_sparse_mst(graph, unvisited, client.h)
        #mstRemote = produce_sparse_mst(graph, unvisitedOrHasBot, client.h)
        mstRemote = shortest_path_mst
        remoteToNode = nx.shortest_path(mstRemote, source=targetLeaf, target=client.h)[1]
        #remoteToNode = get_closest_node(graph, targetLeaf)
        botsRemoted = client.remote(targetLeaf, remoteToNode)
        unvisited.remove(targetLeaf)
        if targetLeaf not in botsAt:
            botsAt[targetLeaf] = 0
        if remoteToNode not in botsAt:
            botsAt[remoteToNode] = 0
        initialTargetLeafBots = botsRemoted - botsAt[targetLeaf]
        botsAt[targetLeaf] = 0
        botsAt[remoteToNode] += botsRemoted
        #   Update truth/lie arrays for scouts
        if initialTargetLeafBots == 1:
            targetLeafBot = True
        else:
            targetLeafBot = False
        if initialTargetLeafBots > 1 or initialTargetLeafBots < 0:
            print("Error!")
        targetReports = nodeReports[targetLeaf]
        for i in range(client.students):
            if targetReports[i] == targetLeafBot:
                numTruth[i] += 1
            else:
                numLies[i] += 1
            worstcaseprob[i] = (minNumTruth - numTruth[i]) / (totalNodes - numTruth[i] - numLies[i])

        botsleft = client.bots - sum(client.bot_count)
        counter += 1

    print("Number of Remotes taken to discover all bots: " + str(counter))
    print("Time Cost: " + str(client.time))

    # When all the locations discovered, we do algorithm in q2. (Prim's combined with Uniform Cost Search)
    # Uses client.bot_count

    sparsemst = produce_sparse_mst(graph, client.bot_locations, client.h)

    mst_remote(sparsemst, client)
    # print("Number of rescued bots: " + str(client.bot_count[client.home])+'/'+str(client.l))

    score = client.end()
    print("Total Score: " + str(score))
    print()
    return score

def student_judgment(numTruth, numLies, probabilities, potentialNodes, nodeReports, nodeDistances, epsilon, rho, a, b):
    # weights = [1 for _ in range(len(numTruth))]
    # totalweight = 0
    # for i in range(len(numTruth)):
    #     expo = -1*a*0.5*(1+probabilities[i]) + b
    #     weights[i] = (1 - epsilon)**expo
    #     totalweight += weights[i]
    # for i in range(len(numTruth)):
    #     weights[i] = weights[i]/totalweight
    nodeScores = [0 for _ in range(len(potentialNodes))]
    # curScores, distScores = [], []

    # for i in range(len(potentialNodes)):
    #     curScore = 0
    #     curReport = nodeReports[potentialNodes[i]]
    #     for j in range(len(numTruth)):
    #         results = model.predict_proba(pd.DataFrame([probabilities, int(curReport)]).T)
    #         curScore += results[:, 1]
    #         # print(curScore)
    #         # if curReport[j] == True:
    #         #     curScore += weights[j]
    #         # else:
    #         #     curScore -= weights[j]
    #     nodeScores[i] = curScore

    for i in range(len(potentialNodes)):
        curReport = nodeReports[potentialNodes[i]]
        #print(pd.DataFrame([probabilities, [int(x) for x in curReport]]).T)
        intCurReport = [int(x) for x in curReport]
        #print(model.predict_proba(pd.DataFrame([probabilities, intCurReport]).T))
        results = sum(model.predict_proba(pd.DataFrame([probabilities, intCurReport]).T)[:,1])
        nodeScores[i] = results
    bestNode = potentialNodes[nodeScores.index(max(nodeScores))]
    return bestNode

def produce_sparse_mst(G, bot_locs, client_home):
    # Note: Relaxation not applied yet. Might be applied for further improvement.
    bot_exist_locs = bot_locs.copy()
    set_locs = [client_home]
    mst = nx.Graph()
    mst.add_node(client_home)
    while len(bot_exist_locs) > 0:
        init = False
        for bot_loc in bot_exist_locs:
            for node_in_set in set_locs:
                if not init:
                    cur_best_path = nx.shortest_path(G, source=bot_loc, target=node_in_set)
                    cur_best_length = nx.shortest_path_length(G, source=bot_loc, target=node_in_set)
                    cur_bot_loc = bot_loc
                    init = True
                this_length = nx.shortest_path_length(G, source=bot_loc, target=node_in_set)
                if this_length < cur_best_length:
                    cur_best_path = nx.shortest_path(G, source=bot_loc, target=node_in_set)
                    cur_best_length = this_length
                    cur_bot_loc = bot_loc
        for i in range(len(cur_best_path)-1):
            mst.add_node(cur_best_path[i])
            mst.add_edge(cur_best_path[i],cur_best_path[i+1])
            set_locs.append(cur_best_path[i])
        bot_exist_locs.remove(cur_bot_loc)
    return mst

def produce_shortest_path_mst(G, bot_locs, client_home):
    bot_exist_locs = bot_locs.copy()
    mst = nx.Graph()
    mst.add_node(client_home)
    while len(bot_exist_locs) > 0:
        init = False
        for bot_loc in bot_exist_locs:
            if not init:
                cur_best_path = nx.shortest_path(G, source=bot_loc, target=client_home)
                cur_best_length = nx.shortest_path_length(G, source=bot_loc, target=client_home)
                cur_bot_loc = bot_loc
                init = True
            this_length = nx.shortest_path_length(G, source=bot_loc, target=client_home)
            if this_length < cur_best_length:
                cur_best_path = nx.shortest_path(G, source=bot_loc, target=client_home)
                cur_best_length = this_length
                cur_bot_loc = bot_loc
        for i in range(len(cur_best_path)-1):
            mst.add_node(cur_best_path[i])
            mst.add_edge(cur_best_path[i],cur_best_path[i+1])
        bot_exist_locs.remove(cur_bot_loc)
    return mst

def mst_remote(mst, client):
    degrees = list(mst.degree)
    while (len(degrees) > 1):
        nodeindex = 0
        lenNodes = len(degrees)
        while nodeindex < lenNodes:
            if degrees[nodeindex][1] == 1 and degrees[nodeindex][0] != client.h:
                break
            nodeindex += 1
        u = degrees[nodeindex][0]
        v = list(mst[u].keys())[0]
        client.remote(u, v)
        mst.remove_node(u)
        degrees = list(mst.degree)
    return 1

def get_leaf_nodes(mst):
    return [x for x in mst.nodes() if len(mst.edges(x)) == 1]

def get_closest_node(graph, node):
    nextEdges = list(graph.edges(node, 'weight', default=0))
    minEdgeIndex = 0
    minEdge = -1
    for i in range(len(nextEdges)):
        if i == 0:
            minEdge = nextEdges[i][2]
            minEdgeIndex = i
        if nextEdges[i][2] < minEdge:
            minEdge = nextEdges[i][2]
            minEdgeIndex = i
    return nextEdges[minEdgeIndex][1]

def combinelist(list1, list2):
    combined_list = []
    for x in list1:
        combined_list.append(x)
    for x in list2:
        if x not in list1:
            combined_list.append(x)
    return combined_list

if __name__ == '__main__':
    testnum = 50

    count = 0
    scores, timeScores = [], []

    print('Epsilon: ' + str(epsilon))
    print('a in y = ax + b: ' + str(a))
    print('b in y = ax + b: ' + str(b))
    print('Rho: ' + str(rho))

    while count < testnum:
        timestart = datetime.now().strftime('%H:%M:%S')
        print('['+timestart+']'+' Iteration '+str(count+1))
        client = Client(False)
        score = solve(client)
        scores.append(score)
        timeScores.append(6 * score - 500)

        count += 1

    print()
    print("Overall Scores from Time Taken: " + str(scores))
    print("Average Overall Score from Time Taken: "+str(mean(scores)))
    print("SD of Overall Score from Time Taken: "+str(stdev(scores)))
    print()
    print("Normalized Scores from Time Taken: " + str(timeScores))
    print("Average Normalized Score from Time Taken: "+str(mean(timeScores)))
    print("SD of Normalized Score from Time Taken: "+str(stdev(timeScores)))
