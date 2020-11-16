import copy


#==============================================================================================================================#
    #==========================================  Bellman-Ford algorithm  ==================================================#
#==============================================================================================================================#       


class broute:
    # The class broute implements Bellman-Ford routing algorithm. It only has two attributes to store the route from o to d in the graph A, 
    # and the minimum cost of the travel. v for route and c for minimum cost. 
    def __init__ (self):
        self.v = []
        self.c = 0

    def bellman_ford (self,A, o, d):
        start = min(o,d) - 1          # For the convenience of the routing we assume o start is smaller node than

        destination = max(o,d) - 1    # the destination (e.g. 5 -> 6 and 6 -> 5 have identical cost and route
                                      # but the order is always ascending)

        visited = []                  # Keep track of visited nodes in order 

        self.v = [0] * (len(A) + 1)     # Store the predecessors from node 1 to length of A. For example vector[3] = 2
                                        #iff the node 3 has a minimum cost link to node 2
                                        # By default v[o] = 0 meaning the origin node itself has predecessor of 0

        matrix = copy.deepcopy(A)         

        infinite_weight = float("inf")

        ## Convert the cost of any unconnected node from start to infinity (initially, cost = 0). If connected, then we simply copy the cost into matrix. 
        for i in range(0,len(matrix)):
            for j in range(0,len(matrix[i])):
                if matrix[i][j] == 0:
                    matrix[i][j] = infinite_weight

        ## Initialization  
        distances = matrix[start]       # Distances have cost to connected node and unconnected node from the start node.      
        distances[start] = 0            # Start node is 0 distance from itself.

        for i  in range(1,len(self.v)):     #  Initially, all other nodes except the start node have predecessor as the start node.
            if i != start + 1:
                self.v[i] = start+1
            else:
                self.v[i] = 0
                
        print("Node 1 \tNode 2 \tNode 3 \tNode 4 \tNode 5 \tNode 6")
        
        

        # From start node, we find the cost to every other node by updating cost if there's any cheaper route via the nodes connected to start node.
        # If any, update and keep searching until we find all paths to all nodes with the cheapest cost possible.
        for v in range(0, len(matrix)):
            for x in range (0, len(matrix[v])):
                if distances[x] > distances[v] + matrix[v][x]:
                    distances[x] = distances[v] + matrix[v][x]
                    self.v[x+1] = v + 1
                print("("+ str(distances[x]) + "," + str(self.v[x+1]) + ")", end="\t")
            print("\n")

        
        # Trace back the route from destination to start and record the sequence in the list
        # Reverse the array to properly format the vector from start to destination.
        temp = []
        predecessor = destination + 1
        while (predecessor != start+1):
            temp.append(predecessor)
            predecessor = self.v[predecessor]
        temp.append(start+1)
        temp.reverse()
        self.v = temp
        self.c = distances[destination]

        return (self.v, self.c)

                 
        

