# Prim's Algorithm uses to compute minimum spanning tree
# which means a min weight path go through every node in graph
# in given G(V,E), time complexity is O(|E|log|V|)
from PriorityQueue import PriorityQueue
def Prim(G):
    inf = float("+inf")
    cost = [inf] * len(G)
    prev = [None] * len(G)
    v0 = 0
    cost[v0] = 0
    Q = PriorityQueue()
    for i in range(len(cost)):
        Q.put(i, cost[i])
    while not Q.empty():
        u, c = Q.get()
        for w in range(len(G)):
            if G[u][w] and w in Q and G[u][w] < cost[w]:
                cost[w] = G[u][w]
                prev[w] = u
                Q.update(w, cost[w])
    return prev

def test():
    G = [[0, 5, 6, 4, 0, 0], [5, 0, 1, 2, 0, 0, 0], [6, 1, 0, 2, 5, 3],
         [4, 2, 2, 0, 0, 4], [0, 0, 5, 0, 0, 0, 4], [0, 0, 3, 4, 4, 0]]
    print(Prim(G))

if __name__=="__main__":
    test()