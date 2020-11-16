import math
from graph import *
from fibheap import *

def initSingleSource(G, s):
    for v in G.V:
        v.d = math.inf
        v.pre = None
    s.d = 0

def relax(u, v, w):
    if v.d > u.d + w:
        v.d = u.d + w
        v.pre = u

def extractMin(Q):
    min = 0
    for index in range(0,len(Q)):
        if Q[min].d > Q[index].d:
            min = index
    return Q.pop(min)


def bellmanFord(G, s):
    initSingleSource(G, s)
    for i in range(0, len(G.V)):
        for e in G.E:
            relax(e.u, e.v, e.weight)
    for e in G.E:
        if e.v.d > e.u.d + e.weight:
            return False
    return True

def dijkstra(G, s):
    initSingleSource(G, s)
    S = []
    Q = G.V[:]
    while len(Q) != 0:
        u = extractMin(Q)
        S.append(u)
        for e in G.getAdj(u):
            relax(e.u, e.v, e.weight)
    return S

def yenRelax(u, v, w, D):
    if v.d > u.d + w:
        v.d = u.d + w
        v.pre = u
        D[v.value] = True

def Yen(G, s):
    initSingleSource(G,s) #number vertices arbitrarily from s
    C = [s]
    D = [False] * len(G.V)
    while C != []:
        for u in G.V:
            edges = G.getAdj(u)
            if u in C or D[u.value]:
                for uv in edges:
                    yenRelax(uv.u, uv.v, uv.weight, D)
        for i in range((len(G.V)-1),-1,-1):
            u = G.V[i]
            edges = G.getAdj(u)
            if u in C or D[u.value]:
                for uv in edges:
                    yenRelax(uv.u, uv.v, uv.weight, D)
        C = []
        for i in range(0, len(D)-1):
            if D[i]:
                C.append(G.V[i])
        D = []
        D = [False] * len(G.V)


def fibDijkstra(G, s):
    n = len(G.V)    #intentionally 1 more than the number of vertices, keep the 0th entry free for convenience
    visited = [False]*(n)
    distance = [math.inf]*n

    heapNodes = [None]*(n+1)
    heap = FibonacciHeap()
    for i in range(1, n+1):
        heapNodes[i] = heap.insert(math.inf, i)     # distance, label

    distance[s.value] = 0
    heap.decrease_key(heapNodes[s.value + 1], 0)

    S = []
    while heap.total_nodes:
        current = heap.extract_min().value - 1

        visited[current] = True
        S.append(current)
        for e in G.adj[current]:
            neighbor = e.v.value
            cost = e.weight
            if not visited[neighbor]:
                if distance[current] + cost < distance[neighbor]:
                    distance[neighbor] = distance[current] + cost
                    heap.decrease_key(heapNodes[neighbor + 1], distance[neighbor])
    return S
