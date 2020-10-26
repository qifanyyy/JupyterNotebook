# Areege Chaudhary
# 10197607
# I confirm that this submission is my own work and is consistent with the Queen's regulations on Academic Integrity.

import random

def constructRandomGraph(n):
        vSet = []

        #makes empty lists in array
        for i in range(n): 
                vSet.append([])
                
        #creates a random graph represented by an adjacency matrix
        for i in range(2, n): 
                x = random.randint(1, i-1) 
                for j in range(x): 
                    nodeConnect = random.randint(0, n-1)
                    weight = random.randint(10, 100) 
                    vSet[i].append((nodeConnect, weight)) 
                    vSet[nodeConnect].append((i, weight))
                    
        #converting from adjacency list to adjacency matrix
        matrix = []
        for i in range(n):
                tempMatrix = []
                for j in range(n):
                        tempMatrix.append(0)
                matrix.append(tempMatrix)
        for i in range(n):
                for j in range(len(vSet[i])):
                        matrixConnect = vSet[i][j][0]
                        matrixWeight = vSet[i][j][1]
                        matrix[i][matrixConnect] = matrixWeight
        return(matrix)

def BFS(G):
        v = random.randint(0,len(G)-1) #chooses random start vertex
        total = 0 
        
        Q = [] #create an empty queue
        visited = [] #will keep track of visited vertices
        for i in range(0,len(G)): #one element per vertex
                visited.append(0)
        visited[v] = 1 #mark starting vertex as visited
        Q.append(v) #add starting vertex to queue

        while (len(Q) != 0): #while queue is not empty
                x = Q.pop(0) #remove first element from queue
                for y in range(0, len(visited)):
                        if ((G[x][y] > 0) and (visited[y] == 0)):
                                visited[y] = 1
                                Q.append(y)
                                total += G[x][y]
        return(total)

def Prim(G):
        total = 0
        startVertex = random.randint(0,len(G)-1) #random starting vertex
        
        #row 1 is "Still in R"
        #row 2 is the connector vertex
        #row 3 is the cost
        
        #creating array full of empty elements
        A = [[],[],[]]
        for x in range(0,3):
                for y in range(0,len(G)):
                        A[x].append("empty")

        A[0][startVertex] = "N" #starting vertex is not in R

        for i in range(1,len(G)):
                A[0][i] = "Y" 
                A[2][i] = 1000 #1000 represents infinity

        #for each neighbor y of vertex 0
        for i in range(0,len(G)):
                if (G[0][i] > 0):
                        A[1][i] = startVertex
                        A[2][i] = G[startVertex][i]
                        
        T = [0] #T represents the tree that we are growing
        chosen_edges = []
        while (len(T) < len(G)):
                min = 1000 #set minimum to highest possible value @ infinity
                for i in range(0,len(G)):
                        if ((A[0][i] == "Y") and (A[2][i] < min)):
                                min = A[2][i]
                                x = i
                T.append(x)
                chosen_edges.append((x,A[1][x]))
                total += A[2][x]
                A[0][x] = "N"

                #for each neighbor y of vertex x (3)
                for y in range(0,len(G)):
                        if (G[x][y] > 0):
                                if ((A[0][y] == "Y") and (G[x][y] < A[2][y])):
                                        A[1][y] =  x
                                        A[2][y] = G[x][y]
        return(total)
        
def experiment():
        n = [20, 30, 40, 50, 60]
        k = 1000
        for x in range(len(n)):
                sum = 0
                for y in range(0,k):
                        graph = constructRandomGraph(n[x])
                        B = BFS(graph)
                        P = Prim(graph)
                        Diff = ((B/P) - 1) * 100 #diff is the percentage by which B is larger than P
                        sum += Diff
                avg = sum/k
                print("Average of Diff for n = " + str(n[x]) + ": " + str(avg)) 

experiment()
