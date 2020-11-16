import snap
import pandas
import numpy as np
import statistics as stats
import random
import copy

# Ausiliary functions
def load_graph(file, prob_distr):

    p2p = snap.TNGraph.New()
    probs = {}

    # Open dataset file
    fIN = open(file, 'r')
    
    # i = 0
    # n = 100

    for line in fIN.readlines():
        # i +=1
        # if i == n:
        #     break
        if line[0] == '#':
            continue
        nodes = line.split()
        for node in nodes:
            node = int(node)
            if p2p.IsNode(node):
                continue
            else:
                p2p.AddNode(node)
        p2p.AddEdge(int(nodes[0]), int(nodes[1]))
        probs.update({(int(nodes[0]), int(nodes[1])) : prob_distr()})
    
    # Close file
    fIN.close()

    # UGraph = snap.GenRndGnm(snap.PUNGraph, 10, 40)
    # snap.DrawGViz(UGraph, snap.gvlNeato, "graph_undirected.png", "graph 2", True)
    
    #snap.DrawGViz(p2p, snap.gvlNeato, "graph.png", "Test", True)

    return (p2p, probs)

def decisione_differita(p2p, probs):
    for edge, prob in probs.items():
        rand = random.random()
        if rand < prob:
            p2p.DelEdge(edge[0], edge[1])

def get_degrees(p2p):
    nodeI = p2p.BegNI()
    degrees = {}

    degrees.update({nodeI.GetId(): nodeI.GetDeg()})
    while nodeI.Next() < p2p.EndNI():
        degrees.update({nodeI.GetId(): nodeI.GetDeg()})
    
    return degrees

# Thresholds functions and Probability Distributions
def ths_constant(p2p, degrees):
    ths = {}
    nodeI = p2p.BegNI()
    th = 1
    ths.update({nodeI.GetId() : th})
    while nodeI.Next() < p2p.EndNI():
        ths.update({nodeI.GetId() : th})
    
    return ths

def ths_majority(p2p, degrees):
    ths = {}
    nodeI = p2p.BegNI()
    deg = degrees[nodeI.GetId()]

    ths.update({nodeI.GetId() : deg/2})
    while nodeI.Next() < p2p.EndNI():
        deg = degrees[nodeI.GetId()]
        ths.update({nodeI.GetId() : deg/2})
    
    return ths

def ths_deg(p2p, degrees):
    ths = {}
    nodeI = p2p.BegNI()
    deg = degrees[nodeI.GetId()]

    ths.update({nodeI.GetId() : deg * 0.9})
    while nodeI.Next() < p2p.EndNI():
        deg = degrees[nodeI.GetId()]
        ths.update({nodeI.GetId() : deg * 0.9})
    
    return ths

def probs_constant():
    return 0.1

# Create Graph, computes degrees, sets ths
def createGraphFromFile(file, prob_distr, ths_fun):

    # Variables
    degrees = {}
    probs = {}
    ths = {}

    # Loading graph
    results = load_graph(file, prob_distr)
    p2p = results[0]
    probs = results[1]

    # Apply decisione differita
    decisione_differita(p2p, probs)
    
    # Compute degrees
    degrees = get_degrees(p2p)

    # Create thresholds
    ths = ths_fun(p2p, degrees)

    print("P2P Graph created correctly.")
    print("Nodes:", p2p.GetNodes(), "Edges:", p2p.GetEdges())
    print("Max degree:", max(degrees.values()), "Avg. degree:", stats.mean(degrees.values()), "Avg. threshold:", stats.mean(ths.values()), "Threshold type:", ths_fun.__name__)

    return (p2p, degrees, ths)

# Target Set Selection algorithm
def TSS(p2p, degrees, ths):
    V = [node for node in ths.keys()]
    S = []
    neighbors = snap.TIntV()
    while len(V) > 0:
        zero = -1
        less = -1
        for n in V:
            if ths[n] == 0:
                zero = n
                break
            elif degrees[n] < ths[n]:
                less = n
                break
        if zero != -1:
            node = zero
            snap.GetNodesAtHop(p2p, node, 1, neighbors, True)
            for neighbor in neighbors:
                ths[neighbor] = max(ths[neighbor] - 1, 0)
                degrees[neighbor] -= 1
        elif less != -1:
            node = less
            S.append(node)
            snap.GetNodesAtHop(p2p, node, 1, neighbors, True)
            for neighbor in neighbors:
                ths[neighbor] -= 1
                degrees[neighbor] -= 1
        else:
            max_value = max((ths[n]/(degrees[n]*degrees[n]+1)) for n in V)
            for n in V:
                if (ths[n]/(degrees[n]*degrees[n]+1)) == max_value:
                    node = n
                    break
            snap.GetNodesAtHop(p2p, node, 1, neighbors, True)
            for neighbor in neighbors:
                degrees[neighbor] -= 1
        
        V.remove(node)
        p2p.DelNode(node)

    print("S:", len(S))
    return len(S)

def TSS_opt(p2p, degrees, ths):
    V = [node for node in ths.keys()]
    S = []
    neighbors = snap.TIntV()
    while len(V) > 0:
        for node in V:
            if ths[node] == 0:
                snap.GetNodesAtHop(p2p, node, 1, neighbors, True)
                for neighbor in neighbors:
                    ths[neighbor] = max(ths[neighbor] - 1, 0)
                    degrees[neighbor] -= 1
            elif degrees[node] < ths[node]:
                S.append(node)
                #print(node)
                snap.GetNodesAtHop(p2p, node, 1, neighbors, True)
                for neighbor in neighbors:
                    ths[neighbor] -= 1
                    degrees[neighbor] -= 1
            else:
                max_value = max((ths[n]/(degrees[n]*degrees[n]+1)) for n in V)
                for n in V:
                    if (ths[n]/(degrees[n]*degrees[n]+1)) == max_value:
                        node = n
                        break
                snap.GetNodesAtHop(p2p, node, 1, neighbors, True)
                for neighbor in neighbors:
                    degrees[neighbor] -= 1

            V.remove(node)
            p2p.DelNode(node)

    print("S:", len(S))
    return len(S)


# Execution function
def exec(file, exec_number, probs_distr, ths_fun):
    results = []
    avg = 0

    for i in range(0, exec_number):
        returns = createGraphFromFile(file, probs_distr, ths_fun)
        p2p = returns[0]
        degrees = returns[1]
        ths = returns[2]
        results.append(TSS_opt(p2p, degrees, ths))

    avg = stats.mean(results)

    print("Avg Set size:", avg)

if __name__ == '__main__':

    #load_graph('./dataset/p2p-Gnutella08.txt', probs_constant)
    exec('./dataset/p2p-Gnutella08.txt', 10, probs_constant, ths_constant)
    