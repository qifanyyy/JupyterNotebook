# Floyd's Algorithm uses to solve all-pair shortest paths problem for weight graph
# only with positive weight
def Floyd(G):
    n = len(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                G[i][j] = min(G[i][j], G[i][k] + G[k][j])
    return G

def test():
    n = float("+inf")
    W = [[0, 1, 1, 1, n], [1, 0, n, 1, 1], [1, n, 0, 1, n], [1, 1, 1, 0, 1], [n, 1, n, 1, 0]]
    print(Floyd(W))

if __name__=="__main__":
    test()