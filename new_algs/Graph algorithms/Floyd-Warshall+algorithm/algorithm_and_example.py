
# coding: utf-8

# In[1]:


# # Python Program for Floyd Warshall Algorithm 
# This code is contributed by Nikhil Kumar Singh(nickzuck_007) and modified by Zhenhui Peng (penguinzhou) to report the matrix in between

import numpy as np

  
# Define infinity as the large enough value. This value will be 
# used for vertices not connected to each other 
INF  = 99999
  
# Solves all pair shortest path via Floyd Warshall Algorithm 
def floydWarshall(graph): 
    # # Number of vertices in the graph 
    V = len(graph[0])
    """ dist[][] will be the output matrix that will finally 
        have the shortest distances between every pair of vertices """
    """ initializing the solution matrix same as input graph matrix 
    OR we can say that the initial values of shortest distances 
    are based on shortest paths considering no  
    intermediate vertices """
    dist = map(lambda i : map(lambda j : j , i) , graph) 
      
    """ Add all vertices one by one to the set of intermediate 
     vertices. 
     ---> Before start of an iteration, we have shortest distances 
     between all pairs of vertices such that the shortest 
     distances consider only the vertices in the set  
    {0, 1, 2, .. k-1} as intermediate vertices. 
      ----> After the end of a iteration, vertex no. k is 
     added to the set of intermediate vertices and the  
    set becomes {0, 1, 2, .. k} 
    """
    for k in range(V): 
  
        # pick all vertices as source one by one 
        for i in range(V): 
  
            # Pick all vertices as destination for the 
            # above picked source 
            for j in range(V): 

                # If vertex k is on the shortest path from  
                # i to j, then update the value of dist[i][j] 
                dist[i][j] = min(dist[i][j] , dist[i][k]+ dist[k][j]) 
        print("The %d th matrix" % (k+1))
        print(np.array(dist)) 
        
# A utility function to print the solution 
def printSolution(dist): 
    print("Following matrix shows the shortest distances between every pair of vertices") 
    for i in range(V): 
        for j in range(V): 
            if(dist[i][j] == INF): 
                print("%7s" %("INF"))
            else: 
                print("%7d\t" %(dist[i][j]))
            if j == V-1: 
                print("")

# Driver program to test the above program 
# Let us create the following weighted graph 
graph = [[0, INF, INF, INF, 7, INF, INF, 1, INF], 
         [INF, 0, INF, INF, INF, 7, INF, INF, 6], 
         [INF, -2, 0, INF, INF, INF, INF, INF, 9], 
         [-3, INF, INF, 0, INF, INF, INF, INF, 1], 
         [INF, 3, INF, INF, 0, INF, INF, INF, INF],
         [INF, INF, 4, INF, INF, 0, INF, INF, INF],
         [INF, INF, 5, -2, INF, INF, 0, INF, INF],
         [INF, INF, INF, 5, INF, INF, INF, 0, INF],
         [5, INF, INF, INF, -2, INF, 3, INF, 0]
        ] 
# Print the solution 
floydWarshall(graph); 
# Note: if the value of dist[i][j] is very large, then it is INF


# In[2]:


# Python Program for divide-and-conqure dynamic programming method to solve all pairs shortest path problem
# This code is modified by Zhenhui Peng (penguinzhou) to deal with the 2nd dynamic programming method to solve all pairs shortest path problem
import numpy as np
import math
  
# Define infinity as the large enough value. This value will be 
# used for vertices not connected to each other 
INF  = 99999

dist_array = []
# Solves all pair shortest path via dcDP Algorithm 
def dcDP(graph): 
    # Number of vertices in the graph 
    V = len(graph[0])
    s = math.ceil(V**0.5)
    dist = map(lambda i : map(lambda j : j , i) , graph) 
    # Store the array in between
    dist_array.append(dist)
    for m in range(int(s)): 
        dist = dist_array[m]
        dist_new = np.zeros((V, V), dtype=np.int)
#         if 2^(m+1) > V:
#             break
        # pick all vertices as source one by one 
        for i in range(V): 
            # Pick all vertices as destination for the 
            # above picked source 
            for j in range(V): 
                dist_new[i][j] = INF
                for k in range(V): 
                    if (dist[i][k]+ dist[k][j]) < dist_new[i][j]:
                        dist_new[i][j] = dist[i][k]+ dist[k][j]
        dist_array.append(dist_new)
        print("The {} th matrix".format(2**(m+1)))
        print(dist_new)
  
  
# A utility function to print the solution 
def printSolution(dist): 
    print("Following matrix shows the shortest distances between every pair of vertices") 
    for i in range(V): 
        for j in range(V): 
            if(dist[i][j] == INF): 
                print("%7s" %("INF"))
            else: 
                print("%7d\t" %(dist[i][j]))
            if j == V-1: 
                print("")

# Driver program to test the above program 
# Let us create the following weighted graph 
graph = [[0, INF, INF, INF, 7, INF, INF, 1, INF], 
         [INF, 0, INF, INF, INF, 7, INF, INF, 6], 
         [INF, -2, 0, INF, INF, INF, INF, INF, 9], 
         [-3, INF, INF, 0, INF, INF, INF, INF, 1], 
         [INF, 3, INF, INF, 0, INF, INF, INF, INF],
         [INF, INF, 4, INF, INF, 0, INF, INF, INF],
         [INF, INF, 5, -2, INF, INF, 0, INF, INF],
         [INF, INF, INF, 5, INF, INF, INF, 0, INF],
         [5, INF, INF, INF, -2, INF, 3, INF, 0]
        ] 
# Print the solution 
dcDP(graph); 
# This code is contributed by Nikhil Kumar Singh(nickzuck_007) 

