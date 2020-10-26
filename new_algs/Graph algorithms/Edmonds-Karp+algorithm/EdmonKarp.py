# Edmonds Karp Algorithm
def max_flow(G, s, t):
    n = len(G)  # Capacity matrix
    F = [[0] * n for i in range(n)]
    path = BreadthFirstSearch(G, F, s, t)
  #  print path
    while path != None:
        flow = min(G[u][v] - F[u][v] for u, v in path)
        for u, v in path:
            F[u][v] += flow
            F[v][u] -= flow
        path = BreadthFirstSearch(G, F, s, t)
    return sum(F[s][i] for i in range(n))  # Returning calculated Max Flow


def BreadthFirstSearch(G, F, s, t):
    queue = [s]
    paths = {s: []}
    if s == t:
        return paths[s]
    while queue:
        u = queue.pop(0)
        for v in range(len(G)):
            if(G[u][v]-F[u][v] > 0) and v not in paths:
                paths[v] = paths[u]+[(u, v)]
                print(paths)
                if v == t:
                    return paths[v]
                queue.append(v)
    return None

# Reading graph from file


def ParseGraph(filename):
    G = []
    with open(filename, 'r') as file_obj:
        for line in file_obj.readlines():
            Gline = line.split(",")
            G.append([int(i) for i in Gline])
        return G


# Parse capacity graph

# Program Driver
G = ParseGraph("flow_network.txt")
source = 0
sink = 5
max = max_flow(G, source, sink)

print("Edmond-Karp Max Flow Algorithm:")
print("Max Flow is: ", max)
