# Put your solution here.

import networkx as nx
import random
from heapq import heappop, heappush
from itertools import count

def solve(client):
    client.end()
    client.start()

    graph = client.G

    mst = nx.minimum_spanning_tree(graph)

    mst_remote(mst, client)

    print("Number of bots needed to be resqued:")
    print(client.l)
    print("Number of final rescued bots:")
    print(client.bot_count[client.home])

    client.end()

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