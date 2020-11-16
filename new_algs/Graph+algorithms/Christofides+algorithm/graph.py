
import math

class Graph:


    def __init__(self):
        # self.adjMatrix = [[]]
        # self.V = {}
        # self.graph = {"vertices":{},"edges":set([]),"weights":{} }
        self.vertices = {}
        self.edges = set()
        self.weights = {}

    def addEdge(self,v,u,w=-1): 
        vertixV = self.vertices[v]; 
        vertixU = self.vertices[u]; 
        if(w==-1):
            weight = self.dist(vertixV,vertixU)
        else:
            weight = w 

        if( (u,v,weight) in self.edges or (v,u,weight) in self.edges):
           return
        self.edges.add((v,u,weight)) 
        self.weights[(u,v)] = weight; 
        self.weights[(v,u)] = weight; 
        
        

    def addVertex(self,name,x=0,y=0): ## each vertex is defined by (name,x,y).
 
        self.vertices[name] = (x,y) ## save each vertex by it's name as KEY, with value of x,y cooridnates. 
        # self.vertices.append(name)

    def dist(self,v,u):
        res = math.sqrt( (v[0]-u[0])**2 + ( v[1]-u[1])**2 ) ## compute euclidean distance, because we have a metric graph. 
       
        return int(100*res)/100; 
    
    def weight(self,v,u) :
        return self.weights[ (v,u) ]
       


    def printGraph(self):
        print("vertices = ",self.vertices)
        print("Edges = " , self.edges); 
        print("--------------------------------------------------------------------------------")

    def toMatrix(self):    
        gMatrix = {}
        adj =[]
        
        

        for v in self.vertices.keys():
            gMatrix[v] = {}
            for u in self.vertices.keys():
                if((v,u) not in self.weights):
                    gMatrix[v][u] = 0
                else:
                    gMatrix[v][u] = self.weights[(v,u)]

    
        edgesList = list(gMatrix.values())
        
        for i in edgesList:
            adj.append(list(i.values()))
        return adj

    def getChar(self,ind): ## get vertrices names in this order -> "A" - "B"- "C" ........
        return  chr(ord("A")+ind)

    def toGraph(self,adjMatrix):
        newGraph = Graph(); 
        n = len(adjMatrix)

        for i in range(n):
            newGraph.addVertex(self.getChar(i))


        for i in range(n): 
            for j in range(i+1,n):  
                if(i != j):
                    newGraph.addEdge(self.getChar(i),self.getChar(j),adjMatrix[i][j])
        return newGraph; 



