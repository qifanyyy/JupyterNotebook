from collections import defaultdict
import sys, threading
import concurrent.futures

# necessary for large graphs
sys.setrecursionlimit(3000000)  
threading.stack_size(67108864) 


def main():   
    G = Graph(875714)
    with open('SCC.txt', 'r') as file:
            for line in file.readlines():
                    u, v = line.strip().split(" ")
                    G.addEdge(int(u), int(v))
    # G.printGraph()
    print(calculateSCC(G, 5))
    

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = defaultdict(list)
        self.graphTranspose = defaultdict(list)
    
    def addEdge(self,u,v):
        self.graph[u].append(v)
        self.graphTranspose[v].append(u)

    def printGraph(self):
        return print(self.graph)


def dfs(G, v, visited, scc_list):
    # mark the current node as visited
    visited[v] = True
    scc_list.append(v)
    # recurse for all vertices adjacent to this vertex
    for i in G[v]:
        if visited[i] == False:
            dfs(G, i, visited, scc_list)


# fill the stack starting from the smallest finishing time
def finishingTime(Grev, v, visited, stack):
    # mark the current node as visited
    visited[v] = True
    # recurse for all vertices adjacent to this vertex
    for i in Grev[v]:
        if visited[i] == False:
            finishingTime(Grev, i, visited, stack)
    stack.append(v)


# find all strongly connected components with Kosaraju's two-pass algotithm
def scc(G):
    stack = []
    scc_dict = {}

    # mark all vertices as not visited
    visited = [False]*(G.vertices + 1)

    # get transposed graph with all arcs reversed
    # fill the stack starting from the smallest finishing time
    for i in list(G.graphTranspose):
        if visited[i] == False:
            finishingTime(G.graphTranspose, i, visited, stack)
        
    # mark all vertices as not visited
    visited = [False]*(G.vertices + 1)

    # run dfs again in the order defined by stack
    while stack:
        i = stack.pop()
        if visited[i] == False:
            # i is the leader, list contains the connected nodes
            scc_dict[i] = []
            dfs(G.graph, i, visited, scc_dict[i])
    
    return scc_dict


# calculate the top n SCC
def calculateSCC(G, n):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(scc, G)
        scc_dict = future.result()
    # scc_dict = scc(G)
    length = []
    for key in scc_dict.keys():
        length.append(len(scc_dict[key]))
    length.sort(reverse=True)
    return length[:n]


if __name__ == "__main__":
    main()