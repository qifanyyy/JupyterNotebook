#implementation of dijkstra's algorithm

from math import inf

def dijkstra(graph, start, end):
    """Return the result of dijkstra algorithm

    Parameters:
    -----------
    graph: the graph will be used for apply the algorithm (list of list)
    start: the index of the node will be used to start (int)
    end: the index of the node will be used to end (int)

    Returns:
    --------
    path: a list with the shortest path to go from start to end (list)
    total_cost: the most optimized cost to go from start to end (int)

    """


    #init S ensemble with start_node inside
    S = [start]
    #defin V ensemble with all node of graph
    V = [x for x in range(len(graph))]
    #init distance dictionnary
    distance = {}
    #init previous history dictionnary
    previous = {}

    #init all of node distances to inf exept for start node
    for v in V:
        if v != start:
            distance[v] = inf

    #loop until S != V
    while len(S) != len(V):
        #for all element of V exept for the element which are in S
        for v in (set(V)-set(S)):
            #init uc as the last element added in S
            uc = S[-1]

            #if uc == 0 that signified we are in the start node
            if uc == 0:

                #add set uc as previous[v] if the new distance if shortest than the current
                if 0+graph[uc][v] < distance[v]:
                    previous[v] = uc

                #set the v distance as the min beetween the current v distance and the edge of uc and v.
                distance[v] = min(distance[v], 0+graph[uc][v])

            else:
                #add set uc as previous[v] if the new distance if shortest than the current
                if distance[uc]+graph[uc][v] <distance[v]:
                    previous[v] = uc
                #set the v distance as the min beetween the current v distance and the distance of u + the edge of uc and v.
                distance[v] = min(distance[v], distance[uc]+graph[uc][v])

        #find the node with the shortest distance
        #init vmin as inf
        vmin = inf
        x = inf
        #loop for all v in V / S
        for v in (set(V)-set(S)):
            #if v distance <  vmin
            if distance[v] < vmin:
                vmin = distance[v]
                # x = the node with the shortest distance
                x = v


        # UPDATE STATEMENT
        # define new uc as x
        uc = x
        # add new uc to S
        S.append(uc)

    #define total_cost to cost of the ending distance
    total_cost= distance[end]
    #init shortest path
    path = []

    #loop to insert in path the previous node from end's node
    while(end != start):
        path.insert(0, end)
        end = previous[end]
    path.insert(0, start)

    #return the shortest_way and total cost of dijkstra from start to end
    return path, total_cost
