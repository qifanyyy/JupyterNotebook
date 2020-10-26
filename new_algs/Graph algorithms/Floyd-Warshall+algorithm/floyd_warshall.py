# Floyd Warshall Algorithm
# Number of vertces
V = 20
# Definition of infinity, which does not connect
INF  = 99999

def floyd_warshall(graph):
    dist = [[[0 for z in range(V)] for j in range(V)] for i in range(V)]
    for i in range(V):
        for j in range(V):
            dist[i][j][0] = graph[i][j]

    for k in range(V):
        for i in range(V):
            for j in range(V):
                with_k = dist[i][k][0]+dist[k][j][0]
                if(with_k<dist[i][j][0]):
                    dist[i][j][0] = with_k
                    if dist[i][j][1] == 0:
                        dist[i][j][1] = k
                    else:
                        for n in range(V):
                            if dist[i][j][n] == 0:
                                dist[i][j][n] = k
                                break
    return dist

def print_matrix(dist):
    print("\nThe following matrix shows all minimum cost paths between any two cities.\n\n")
    for i in range(V):
        for j in range(V):
            if(dist[i][j][0] == INF):
                print("%5s" %("INF"),end = '|'),
            else:
                print("%5d" %(dist[i][j][0]),end = '|'),
            if j == V-1:
                print("\n---------------------------------------------------------------------------------------------------------------------------")

# Put your graph here
graph = [
    [0,INF,INF,861,INF,211,INF,INF,INF,586,INF,753,382,896,INF,INF,INF,INF,INF,INF],
    [INF,0,423,617,365,INF,INF,INF,INF,357,INF,INF,806,INF,INF,INF,INF,INF,INF,INF],
    [INF,423,0,554,359,INF,INF,INF,INF,306,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF],
    [861,617,554,0,INF,INF,INF,INF,INF,656,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF],
    [INF,365,359,INF,0,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF],
    [211,INF,INF,INF,INF,0,988,INF,293,102,INF,870,399,INF,INF,INF,INF,INF,INF,INF],
    [INF,INF,INF,INF,INF,988,0,228,43,INF,573,663,INF,INF,INF,INF,INF,INF,INF,INF],
    [INF,INF,INF,INF,INF,INF,228,0,801,INF,31,INF,INF,INF,INF,INF,INF,INF,INF,INF],
    [INF,INF,INF,INF,INF,293,43,801,0,724,927,936,INF,INF,696,INF,INF,INF,INF,INF],
    [586,357,306,656,INF,102,INF,INF,724,0,INF,736,672,804,INF,INF,INF,INF,INF,INF],
    [INF,INF,INF,INF,INF,INF,573,31,927,INF,0,634,INF,INF,927,INF,INF,INF,INF,INF],
    [753,INF,INF,INF,INF,870,663,INF,936,736,634,0,8,71,798,INF,713,INF,INF,INF],
    [382,806,INF,INF,INF,399,INF,INF,INF,672,INF,844,0,21,INF,299,INF,INF,INF,INF],
    [896,INF,INF,INF,INF,INF,INF,INF,INF,804,INF,71,21,0,244,447,726,INF,INF,INF],
    [INF,INF,INF,INF,INF,INF,INF,INF,696,INF,927,798,INF,244,0,INF,387,INF,INF,INF],
    [INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,299,447,INF,0,503,113,431,INF],
    [INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,713,INF,726,387,503,0,916,490,INF],
    [INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,113,916,0,980,326],
    [INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,431,490,980,0,455],
    [INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,326,455,0]
]

print('Add two cities to calculate the minnimum cost.')
a = int(input('a = '))
b = int(input('b = '))

intermadiate = []
for i in range(V):
    if (floyd_warshall(graph)[a][b][i] != 0 and i != 0):
        intermadiate.append(floyd_warshall(graph)[a][b][i])

print('The minimum cost between the city '+str(a)+' and the city '+str(b)+' is '+str(floyd_warshall(graph)[a][b][0])+', intermediate city = '+str(intermadiate))

print_matrix(floyd_warshall(graph))