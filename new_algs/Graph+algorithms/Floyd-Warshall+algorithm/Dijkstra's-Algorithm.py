# Dijkstra's Algorithm uses to compute "all shortest path from a fixed start node"
# just like to find all shortest paths from node A to others
# Time complexity O(|E|log|V|)
from PriorityQueue import PriorityQueue
def Dijkstra(G, v0):
    inf = float("+inf")
    dist = [inf] * len(G)
    prev = [None] * len(G)
    dist[v0] = 0
    Q = PriorityQueue()
    for i in range(len(dist)):
        Q.put(i, dist[i])
    while not Q.empty():
        u,d = Q.get()
        for w in range(len(G)):
            if G[u][w] and w in Q and dist[u] + G[u][w] < dist[w]:
                dist[w] = dist[u] + G[u][w]
                prev[w] = u
                Q.update(w, dist[w])
    return dist


def test():
    G = [[0, 0, 4, 1, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 3],
         [0, 2, 1, 0, 4, 5], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0]]
    print(Dijkstra(G, 0))

if __name__=="__main__":
    test()