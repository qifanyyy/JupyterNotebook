"""
UCD Assignment Details:
Date Started: 03/03/17
Revision 2 - see report for revision history
Date Submitted: 12/03/17
Student Name (Student Number): Eoin Carroll (16202781)
Module Code: UCD MIS40550
Module Title: Network Software Modelling
Assessment Title: Network Software Modelling Assignment 1
Module Co-ordinator: Dr James McDermott

Code Details:
File name: MIS40550_Ass1_Eoin_Carroll_16202781_rev1

This python file includes:
- Main() Program to run dijkstra for n random networks
- dijkstra_list(): Basic dijkstra algorithm using a list data structure (Reference only - not used)
- dijkstra_priority(): Basic dijkstra algorithm using a priority queue data structure
- bi_dijkstra_priority(): Bbidirectional Dijkstra algorithm using a priority queue data structure
- class PriorityQueue: Priority heap data structure with peek feature

Note: This program differs to the programs in labs whereby the shortest path is not returned by default
Shortest path and cost can be returned by commenting out the last section in each algorithm and inserting a print()

Code is set to run for random graphs with n nodes where n = (500,1000,2000,3000,5000,10000). It will repeat this
10 times and report the average. Expected run time is in the range of 3 hours. The user can change these input values
to run smaller tests. Alternatively, import the python file and use dijkstra_priority(G, r, t) and
bi_dijkstra_priority(G, r, t) to find the shortest paths in your favourite graphs.

References: Parts are copied directly from sample code provided in module MIS40550
"""


import time
import math
import itertools
import random
import networkx as nx
import numpy as np
from heapq import heapify, heappush, heappop


class PriorityQueue:

    REMOVED = '<removed-task>' # placeholder for a removed task

    def __init__(self, tasks_prios=None):
        self.pq = []
        self.entry_finder = {} # mapping of tasks to entries
        self.counter = itertools.count() # unique sequence count -- tie-breaker when prios equal
        if tasks_prios:
            for task, prio in tasks_prios:
                self.add_task(task, prio) # would be nice to use heapify here instead

    def __iter__(self):
        return ((task, prio) for (prio, count, task) in self.pq if task is not self.REMOVED)

    def __len__(self):
        return len(list(self.__iter__()))

    def __str__(self):
        return str(list(self.__iter__()))

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task, priority # NB a change from the original: we return prio as well
        raise KeyError('pop from an empty priority queue')

    def peek(self):
        'Return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            x = list(self)
            return x[0]
        raise KeyError('peek from an empty priority queue')


def dijkstra_list(G, r, t):
    # dijkstra's algorithm from root r: works with positive edges
    if not G.has_node(r):
        raise ValueError("Source node " + str(r) + " not present")

    for e1, e2, d in G.edges(data=True):
        if d["weight"] < 0:
            raise ValueError("Negative weight on edge " + str(e1) + "-" + str(e2))

    P = {r}  # permanent set
    S = []  # V-P. using a list for S: inefficient!
    D = {}  # estimates of SPST lengths
    p = {}  # parent-pointers
    A = set()  # our result, an SPST

    for n in G.nodes():
        if n == r:
            D[n] = 0
        else:
            if G.has_edge(r, n):
                D[n] = G[r][n]["weight"]
            else:
                D[n] = math.inf

            p[n] = r
            S.append((n, D[n]))

    while len(S):
        prio = math.inf
        idx = -1
        item = -1
        for i, (n, Dn) in enumerate(S):
            # this loop finds the next lowest-D node.
            if Dn < prio:
                idx = i
                prio = Dn
        u, Du = S.pop(idx)  # get the next lowest-D node, and remove from S
        if u in P: continue

        # move u to P and add to A
        P.add(u)
        A.add((p[u], u))

        # look at all neighbours v of u to see if the estimate D[v]
        # and p[v] can be updated.
        for v, Dv in S:
            if v in P: continue
            if G.has_edge(u, v):
                if D[v] > D[u] + G[u][v]["weight"]:
                    D[v] = D[u] + G[u][v]["weight"]
                    p[v] = u

                    # either add v to S, or update its estimate in S.
                    overwrite = False
                    for i, (n, Dn) in enumerate(S):
                        if n == v:
                            # we are overwriting an existing entry with a new lower prio
                            S[i] = (v, D[v])
                            overwrite = True
                            break
                    if not overwrite:
                        # we didn't find it, so add as a new item
                        S.append((v, D[v]))

        if u == t:  # If we have added our goal node to the set A then stop
            # print("Goal node found, break here")
            break

        """
    # This section specifies only the shortest path to node t
    SP = set()  # our result, an SP
    x = t
    while not x == r:
        for i in A:
            if i[1] == x:
                SP.add(i)
        x = p[x]

    return SP, D[u]"""


def dijkstra_priority(G, r, t):
    if not G.has_node(r):
        raise ValueError("Source node " + str(r) + " not present")

    for e1, e2, d in G.edges(data=True):
        if d["weight"] < 0:
            raise ValueError("Negative weight on edge " + str(e1) + "-" + str(e2))

    P = {r}  # permanent set
    S = PriorityQueue()  # V-P. This is the crucial data structure.
    D = {}  # estimates of SPST lengths
    p = {}  # parent-pointers
    A = set()  # our result, an SPST

    for n in G.nodes():
        if n == r:
            D[n] = 0
        else:
            if G.has_edge(r, n):
                D[n] = G[r][n]["weight"]
            else:
                D[n] = math.inf

            p[n] = r
            S.add_task(n, D[n])

    while len(S):
        u, Du = S.pop_task()
        if u in P: continue

        P.add(u)  # move one item to the permanent set P and to SPST A
        A.add((p[u], u))

        for v, Dv in S:
            if v in P: continue
            if G.has_edge(u, v):
                if D[v] > D[u] + G[u][v]["weight"]:
                    D[v] = D[u] + G[u][v]["weight"]
                    p[v] = u
                    S.add_task(v, D[v])  # add v, or update its prio

        if u == t:  # If we have added our goal node to the set A then stop
            # print("Goal node found, break here")
            break

    """
    # Important note: Turn on this code to return (A, Du)

    # This section specifies only the shortest path to node t
    SP = set()  # our result, a SP
    x = t
    while not x == r:
        for i in A:
            if i[1] == x:
                SP.add(i)
        x = p[x]

    return SP, D[u]"""


def bi_dijkstra_priority(G, r, t):
    if not G.has_node(r):
        raise ValueError("Source node " + str(r) + " not present")

    for e1, e2, d in G.edges(data=True):
        if d["weight"] < 0:
            raise ValueError("Negative weight on edge " + str(e1) + "-" + str(e2))

    Pf = {r}  # permanent set. f stands for forward
    Pb = {r}  # permanent set. b stands for backward
    Sf = PriorityQueue()  # V-P. This is the crucial data structure.
    Sb = PriorityQueue()  # V-P. This is the crucial data structure.
    Df = {}  # estimates of SPST lengths
    Db = {}  # estimates of SPST lengths
    pf = {}  # parent-pointers
    pb = {}  # parent-pointers
    Af = set()  # our result, an SPST
    Ab = set()  # our result, an SPST
    link_node = 0  # our temporary goal node, will be updated when two algs meet

    for n in G.nodes():  # set up forward algorithm
        if n == r:
            Df[n] = 0
        else:
            if G.has_edge(r, n):
                Df[n] = G[r][n]["weight"]
            else:
                Df[n] = math.inf

            pf[n] = r
            Sf.add_task(n, Df[n])

    for n in G.nodes():  # set up backward algorithm
        if n == t:
            Db[n] = 0
        else:
            if G.has_edge(t, n):
                Db[n] = G[t][n]["weight"]
            else:
                Db[n] = math.inf

            pb[n] = t
            Sb.add_task(n, Db[n])

    for i in G.edges():  # Worst case, run this for every edge
        uf = Sf.peek()[1]  # Check lowest cost next move in forward queue
        ub = Sb.peek()[1]  # Check lowest cost next move in backward queue
        # print("Duf:", uf)
        # print("Dub:", ub)

        if uf <= ub:  # If forward move is lowest cost, continue with forward alg as normal
            u, Du = Sf.pop_task()
            if u not in Pf:
                Pf.add(u)  # move one item to the permanent set P and to SPST A

                Af.add((pf[u], u))
                # print(Af)

                for v, Dv in Sf:
                    if v in Pf: continue
                    if G.has_edge(u, v):
                        if Df[v] > Df[u] + G[u][v]["weight"]:
                            Df[v] = Df[u] + G[u][v]["weight"]
                            pf[v] = u
                            Sf.add_task(v, Df[v])  # add v, or update its prio

                if u == t:  # If we have added our goal node to the set A then stop
                    # print("Goal node found, break here")
                    break

                # If we have added our goal node to both algs then stop and set link node.
                # We must also not have seen a shorter path in either direction
                if (u in Pb) and (Df[u] + Db[u] <= Df[t]) and (Df[u] + Db[u] <= Db[r]):
                    link_node = u
                    break

        else:  # Otherwise backward move is lowest cost, continue with backward alg as normal
            u, Du = Sb.pop_task()
            if u not in Pb:

                Pb.add(u)  # move one item to the permanent set P and to SPST A

                Ab.add((u, pb[u]))  # Switched parent and child as we are moving backwards

                for v, Dv in Sb:
                    if v in Pb: continue
                    if G.has_edge(u, v):
                        if Db[v] > Db[u] + G[u][v]["weight"]:
                            Db[v] = Db[u] + G[u][v]["weight"]
                            pb[v] = u
                            Sb.add_task(v, Db[v])  # add v, or update its prio

                if u == r:  # If we have added our goal node to the set A then stop
                    # print("Goal node found, break here")
                    break

                # If we have added our goal node to both algs then stop and set link node.
                # We must also not have seen a shorter path in either direction
                if (u in Pf) and (Df[u] + Db[u] <= Df[t]) and (Df[u] + Db[u] <= Db[r]):
                    link_node = u
                    break

    """
    # Important note: Turn on this code to return (A, Du)

    # print("Af:", Af)
    # print("Ab:", Ab)
    # print("Link Node:", link_node)

    # This section specifies only the shortest path to link node in Af from start
    SPf = set()  # our result, an SP
    x = link_node
    while not x == r:
        for i in Af:
            if i[1] == x:
                SPf.add(i)
        x = pf[x]

    # This section specifies only the shortest path to link node in Ab backward from goal
    SPb = set()  # our result, an SP
    x = link_node
    while not x == t:
        for i in Ab:
            if i[0] == x:
                SPb.add(i)
        x = pb[x]

    SP = SPf | SPb  # Union of Ab and Af SPs

    return SP, Df[link_node] + Db[link_node]  # Return shortest path and cost of reaching link node from start and goal"""


def dijkstra():
    """
    # This is the undirected graph on week 4 slide 28. The solution on the
    # following slide is: {('C', 'F'), ('A', 'C'), ('C', 'D'), ('B',
    # 'G'), ('A', 'B'), ('F', 'E')}
    G = nx.Graph()
    E = (
        ("A", "B", 2),
        ("A", "C", 6),
        ("A", "D", 8),

        ("B", "G", 10),
        ("B", "C", 8),

        ("C", "D", 1),
        ("C", "E", 5),
        ("C", "G", 9),
        ("C", "F", 3),

        ("D", "F", 9),
        ("G", "E", 4),
        ("E", "F", 1)
        )


    r = "A" #Set source node
    t = "G" # Set goal node
    G.add_weighted_edges_from(E)
    """

    reps = 10  # Repeat tests this many times and take an average
    n_range = (500,1000,2000,3000,5000,10000)  # Range of n to run over
    density = 0.10  # Fill this percentage of edges from randomly created matrix

    print("Dijkstra results averaged over", reps, "repetitions for each n with density =", density)

    for n in n_range:  # Number of nodes in random graph
        run_time_d = 0  # Variable to store total runtime dijkstra
        run_time_bi_d = 0  # Variable to store total runtime bi_dijkstra

        for i in range(reps):
            # Create random graph
            M = np.random.rand(n, n)
            G = nx.Graph()
            for i in range(np.shape(M)[0]):  # Never need to add from last row
                for j in range(np.shape(M)[1]):
                    if j < i:  # Account for Mji and duplicates
                        if not (i == n-1 and j == 0):  # Do not make a direct connection between 1 and n
                            if random.random() > 1 - density:  # Fill a matrix for roughly X% of connections in matrix M
                                G.add_edge(i + 1, j + 1, weight=M[i][j])
            r = 1  # Set source node
            t = n  # Set goal node

            """
            start = time.time()
            dijkstra_list(G, r, t)
            end = time.time()
            print("dijkstra_list time: " + str(end - start))
            """

            for i in range(reps):
                start = time.time()
                dijkstra_priority(G, r, t)
                end = time.time()
                run_time_d += end - start

            for i in range(reps):
                start = time.time()
                bi_dijkstra_priority(G, r, t)
                end = time.time()
                run_time_bi_d += end - start

        print("With n = ", n)
        print("dijkstra_priority time: ", run_time_d / reps)  # Print average run time
        print("bi_dijkstra_priority time: ", run_time_bi_d / reps)  # Print average run time

if __name__ == "__main__":
    dijkstra()