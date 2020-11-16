#PROGRAM: Python code to implement Prim's algorithm. The program takes a graph and finds the shortest distance from source vertex to other vertices.

#OUTPUT: compiles, gives correct reply

#TOP learnings:
#1. Creating different operations using dictionaries
#2. Using global variables

'''
algorithm logic:
1) Assign a distance value (from source vertex) to all vertices in the input graph. 
Initialize all distance values as INFINITE. Assign distance value as 0 for the source vertex so that it is picked first. (This is the first 'u')

2) Pick a vertex u which has minimum distance value, and which has not yet been picked.

3) Update distance value of all adjacent vertices of u. To update the distance values, iterate through all adjacent vertices.
For every adjacent vertex v, if sum of distance value of u (from source) and weight of edge u-v, is less than the distance value of v,
then update the distance value of v.

methods:

1) Create a dict distValueDicto.

2) def findingMinVertex (self, distValueDicto):
Method takes a graph, a vertex and a dictionary containing distance values of vertices.
            It updates the distance values of vertices the given vector is conected to.
            Returns nothing.
        
3) def distValUupdater

'''
from refGrAndVerBig2 import Graph
from refGrAndVerBig2 import Vertex

class djik():
    
    def findingMinVertex (self, distValueDicto):
        ''' Method takes a dict of vertices and their currently assumed "distance values" ie. distances from a source vertex.
            Returns the vertex with the least "distance value".
        '''
        #step 1: make a copy of the received dict so that original dict is unaltered
        tmpDicto = distValueDicto.copy()

        #step 2:delete the min vertices from the dict that have already been selected
        #this "for" loop is run as many times as the function "findingMinVertex" has been called previously
        for i in range (counter):
        #this is the "global" counter, which has been initialized to 0 in the main program
            for i in tmpDicto.keys():
                if tmpDicto[i] == min (tmpDicto.values()):
                    del tmpDicto[i]
                    break
            print ("inside counter.. this key and its value will be deleted")
            print (i)
            
        #step 3:find the new min vertex and return it
        for i in tmpDicto.keys(): 
             if tmpDicto[i] == min (tmpDicto.values()):
                 break
                 #del distValueDicto[i] #now removing this
        global counter
        counter = counter + 1
        return i

    def distValUpdater (self, grapho,  vertexU, distValueDicto):
        ''' Method takes a graph, a vertex and a dictionary containing "distance values" of vertices.
            It updates the distance values of vertices the given vector is conected to.
            Returns nothing.
        '''
        for i in grapho.vertList[vertexU].connectedTo.keys():
             if distValueDicto [vertexU]  + grapho.vertList[vertexU].connectedTo[i] < distValueDicto [i.id]:
                 distValueDicto [i.id] = distValueDicto [vertexU]  + grapho.vertList[vertexU].connectedTo[i]

        #remark! the first VertexU to be provided is always 0, giving some other vertex doesn't change anything.


#MAIN PROGRAM:

#creating a graph on which the djikstra's algorithm will be applied.
g = Graph()
for i in range(6):
    g.addVertex(i)

g.addEdge(0,1,5)
g.addEdge(0,5,2)
g.addEdge(1,2,4)
g.addEdge(2,3,9)
g.addEdge(3,4,7)
g.addEdge(3,5,3)
g.addEdge(4,0,1)
g.addEdge(5,4,8)
g.addEdge(5,2,1)

for v in g:
    for w in v.getConnections(): 
        print("( %s , %s, %s )" % (v.getId(), w.getId(), v.getWeight(w) ))  #yea! working!

distValueDicto = {}
#keys have vertex id no and values have "distance value" corresponding to the id.

#initializing distValueDicto
distValueDicto[0] = 0
for i in range (1,g.numVertices):
    distValueDicto[i] = 1000 #1000 is infinity

print ("will print initial distValueListo:")
print (distValueDicto)

d = djik()

counter = 0

for i in range (g.numVertices):
    minVertex = d.findingMinVertex (distValueDicto)
    print(minVertex )

    d.distValUpdater(g,minVertex,distValueDicto)

    print ("distValueDicto-transition copy after applying distValUpdater method is:")
    print (distValueDicto)

print ("will print final distValueListo:")
print (distValueDicto)

'''
OUTPUT:
( 0 , 5, 2 )
( 0 , 1, 5 )
( 1 , 2, 4 )
( 2 , 3, 9 )
( 3 , 5, 3 )
( 3 , 4, 7 )
( 4 , 0, 1 )
( 5 , 4, 8 )
( 5 , 2, 1 )
will print initial distValueListo:
{0: 0, 1: 1000, 2: 1000, 3: 1000, 4: 1000, 5: 1000}
0
distValueDicto-transition copy after applying distValUpdater method is:
{0: 0, 1: 5, 2: 1000, 3: 1000, 4: 1000, 5: 2}
inside counter.. this key and its value will be deleted
0
5
distValueDicto-transition copy after applying distValUpdater method is:
{0: 0, 1: 5, 2: 3, 3: 1000, 4: 10, 5: 2}
inside counter.. this key and its value will be deleted
0
inside counter.. this key and its value will be deleted
5
2
distValueDicto-transition copy after applying distValUpdater method is:
{0: 0, 1: 5, 2: 3, 3: 12, 4: 10, 5: 2}
inside counter.. this key and its value will be deleted
0
inside counter.. this key and its value will be deleted
5
inside counter.. this key and its value will be deleted
2
1
distValueDicto-transition copy after applying distValUpdater method is:
{0: 0, 1: 5, 2: 3, 3: 12, 4: 10, 5: 2}
inside counter.. this key and its value will be deleted
0
inside counter.. this key and its value will be deleted
5
inside counter.. this key and its value will be deleted
2
inside counter.. this key and its value will be deleted
1
4
distValueDicto-transition copy after applying distValUpdater method is:
{0: 0, 1: 5, 2: 3, 3: 12, 4: 10, 5: 2}
inside counter.. this key and its value will be deleted
0
inside counter.. this key and its value will be deleted
5
inside counter.. this key and its value will be deleted
2
inside counter.. this key and its value will be deleted
1
inside counter.. this key and its value will be deleted
4
3
distValueDicto-transition copy after applying distValUpdater method is:
{0: 0, 1: 5, 2: 3, 3: 12, 4: 10, 5: 2}
will print final distValueListo:
{0: 0, 1: 5, 2: 3, 3: 12, 4: 10, 5: 2}

'''
