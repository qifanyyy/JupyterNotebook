# WarShall algorithm uses to compute transitive closure
# which means can we go from i to j directly or through k
# time complexity is O(n^3), which n is the amount of nodes
# in sparse graph, use DFS may be better
def WarShall(G):
    n = len(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                G[i][j] = G[i][j] or (G[i][k] and G[k][j])
    return G

    # code in the lecture but doesn't work
    # n = len(G)
    # R = []
    # for i in range(n+1):
    #     t = []
    #     for j in range(n):
    #         t.append([0]*n)
    #     R.append(t)
    # R[0] = G
    # for k in range(n+1):
    #     for i in range(n):
    #         for j in range(n):
    #             R[k][i][j] = R[k-1][i][j] or (R[k-1][i][k-1] and R[k-1][k-1][j])
    # return R[n]

def test():
    A = [[0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1], [0, 0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0]]
    print(WarShall(A))
    # simple test
    # B = [[0, 1, 1],[1, 0, 0],[0, 1, 0]]
    # print(WarShall(B))
if __name__=="__main__":
    test()