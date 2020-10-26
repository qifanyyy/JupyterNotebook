#Name:Krishna Sreenivas Student ID-800984436
import sys
import os

class Heap(object):
    def __init__(self):
        self.items = [0] #Heap initialised with 0

    #Gets length of heap
    def __len__(self): 
        return len(self.items) - 1 

    #Returns the minimum child in heap i.e. root        
    def minimum_child(self, i):
        if i * 2 + 1 > len(self):
            return i * 2
        if self.items[i * 2] < self.items[i * 2 + 1]:
            return i * 2
        return i * 2 + 1            

    #Find the place for an item up in the heap
    def bubble_up(self):
        i = len(self)
        while i // 2 > 0:
          if self.items[i] < self.items[i // 2]:
              temp=self.items[i]
              self.items[i]=self.items[i//2]
              self.items[i//2]=temp            
          i = i // 2

    #Inserts element in the heap and heapifies by calling bubble_up
    def insert(self, k):
        self.items.append(k)
        self.bubble_up()

    #Find the place for an item down in the heap
    def bubble_down(self, i):
        while i * 2 <= len(self):
            mc = self.minimum_child(i)
            if self.items[i] > self.items[mc]:
                temp=self.items[i]
                self.items[i]=self.items[mc]
                self.items[mc]=temp
            i = mc

    #Build the heap and heapifiy the array list
    def construct_heap(self, alist):
        i = len(alist) // 2
        self.items = [0] + alist
        while i > 0:
            self.bubble_down(i)
            i = i - 1    
        
    #Pops outs the minimum element from the heap and heapifies by calling bubble_down    
    def pop_min(self):
        return_value = self.items[1]
        self.items[1] = self.items[len(self)]
        self.items.pop()
        self.bubble_down(1)
        return return_value
    

class Vertex:
    def __init__(self, vertex_name):
        self.id=vertex_name
        self.adjacent={}
        # Set distance to infinity for all nodes
        self.distance=sys.maxsize
        # Mark all nodes unvisited        
        self.visited=False  
        # Predecessor
        self.previous=None
        
    #Keeps track of visited vertices
    def set_visited(self):
        self.visited=True

    #To obtain the name of the vertex    
    def get_id(self):
        return self.id
        
    # To add neighbors to an vertex(adjacency)
    def add_neighbor(self, neighbor, weight, status):
        self.adjacent[neighbor.id]=[weight, status]

    #Obtains the parent of a vertex, needed in dijkstra's algorithm
    def set_previous(self, prev):
        self.previous=prev

    #Setting initial distances/transmit time
    def set_distance(self, dist):
        self.distance=dist

    #Needed to reset dijkstra's algorithm    
    def set_unvisited(self):
        self.visited=False
            
    #Obtain the distance/transmit time between source and dest vertex
    def get_weight(self, neighbor):
        return self.adjacent[neighbor][0]    
    
    #Obtaining the distance of vertex, needed in dijkstra's algorithm
    def get_distance(self):
        return self.distance
        
        
class Graph:
 
        #Adding edge to graph
    def add_edge(self, frm, to, cost, status):
        if frm not in self.vert_dict: #If source not in veritices dictionary
            self.add_vertex(frm)
        if to not in self.vert_dict: #If  destination not in vertices dictionary
            self.add_vertex(to)
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost, status) #If both are present
        
    #Constructor to initialise the attributes
    def __init__(self):
        self.vert_dict={} #dictionary of vertices
        self.num_vertices=0 #count of vertices
        self.vertices_status={} #status of vertices (up/down)

    #Setting the status of edge to DOWN
    def edge_down(self, frm, to):
        self.vert_dict[frm].adjacent[to][1]="DOWN"

    def isReachable(self,start,end): 
#        visited={}
        queue=[]
        if start or end not in self.vert_dict:
            print("No path exists")
        else:
            for node in self.vert_dict:
                self.vert_dict[node].visited=False
            queue.append(self.vert_dict[start])
            self.vert_dict[start].visited=True
            while queue:
                n=queue.pop(0)
                if n==end:
                    print("Path exists")
                for node in [key for key in list(self.vert_dict.keys()) if key!=start]:
                    if self.vert_dict[node].visited==False:
                        queue.append(node)
                        self.vert_dict[node].visited=True
       
    #Deleting edge from graph
    def delete_edge(self, frm, to):
        self.vert_dict[frm].adjacent.pop(to)

    #Setting the vertex to DOWN
    def vertex_down(self,vertex):
        self.vertices_status[vertex]="DOWN"

    #Needed for Dijkstra's 
    def shortest(self, target, path):
        #build shortest path by tracing predecessors
        if target.previous:
            path.append(target.previous.get_id())
            self.shortest(target.previous, path)
        return

    #Setting the status of edge to UP
    def edge_up(self, frm, to):
        self.vert_dict[frm].adjacent[to][1]="UP"

    #Shortest path using Dijkstra
    def dijkstra(self, start, target):
        p_q=Heap() #Initialize a priority queue
        start.set_distance(0) #Set distance of source to be 0
        unvisited_queue=[(self.vert_dict[v].get_distance(),self.vert_dict[v].get_id()) for v in self.vert_dict if self.vertices_status[v]=="UP"] #create list of unvisited vertices that are 'UP', with their distances
        p_q.construct_heap(unvisited_queue) #Add items from the unvisited queue to the priority queue
        while len(p_q)-1:
            #Get current Vertex object (min) from poped item
            current=self.get_vertex(p_q.pop_min()[1])
            current.set_visited() #set its status to visited
            #Loop over its adjacent nodes and calculate distances
            for next_node in current.adjacent:
                if self.vertices_status[next_node]=="UP" and current.adjacent[next_node][1]=="UP": #Check if vertex and edge are both up
                    next_node=self.get_vertex(next_node)
                    if next_node.visited: #If node has been visited move to next
                        continue
                    #Recalculate distances based on what is minimum
                    new_dist=current.get_distance()+float(current.get_weight(next_node.id))
                    if new_dist<next_node.get_distance():
                        next_node.set_distance(new_dist)
                        next_node.set_previous(current)
            #Pop all items from heap
            while len(p_q)-1:
                p_q.pop_min()
            #Rebuild the priority queue for next iteration
            unvisited_queue=[(self.vert_dict[v].get_distance(),self.vert_dict[v].get_id()) for v in self.vert_dict if not self.vert_dict[v].visited]
            p_q.construct_heap(unvisited_queue)


        
    #Adding new vertex
    def add_vertex(self, node):
        self.num_vertices=self.num_vertices+1
        new_vertex=Vertex(node)
        self.vert_dict[node]=new_vertex
        self.vertices_status[node]="UP" #initial status set to UP
        return new_vertex
    
    #Printing the graph in sorted order
    def print_graph(self):
        #for every vertex
        for vertex in sorted(list(self.vert_dict)):
            print(vertex, self.vertices_status[vertex])
            #for every adjacent node to vertex
            for node in sorted(list(self.vert_dict[vertex].adjacent.keys())):
                        print("  ",node,self.vert_dict[vertex].adjacent[node][0],self.vert_dict[vertex].adjacent[node][1])    

    #Setting the vertex up
    def vertex_up(self,vertex):
        self.vertices_status[vertex]="UP"
        
    #Fetching the vertex
    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None
             
grph=sys.argv[1] #Getting the graph file
#queries=sys.argv[2] #Getting the queries file
graph=Graph()

if os.path.getsize(grph)>0:
    f=open(grph, 'r')
    for line in f:
        line=line.split()
        #Bidirectional edges created all marked 'UP'
        graph.add_edge(line[0],line[1],line[2],"UP") #Initial edges are added in both directions.
        graph.add_edge(line[1],line[0],line[2],"UP")
    f.close()
else:
    print("File is empty!") #If file is empty error msg is printed
    exit(0)

         
#output_file=open(sys.argv[3], mode='w') #Create output.txt file for output
#if os.path.getsize(queries)>0: #Checking if file is not empty
#    f=open(queries, 'r')
#    for line in f: 
#        query=line.split() #Execute function according to first word in query
#        if query[0]=='print':
#            graph.print_graph()
#            print("Output written to file")
#        elif query[0]=='reachable':
#            graph.reachable()
#            print("Output written to file")
#        elif query[0]=='addedge':
#            graph.add_edge(query[1], query[2], query[3], "UP") #Edges marked 'UP' by default
#            print("Operation performed")
#        elif query[0]=='deleteedge':
#            graph.delete_edge(query[1], query[2])
#            print("Operation performed")
#        elif query[0]=='vertexup':
#            graph.vertex_up(query[1])
#            print("Operation performed")
#        elif query[0]=='vertexdown':
#            graph.vertex_down(query[1])
#            print("Operation performed")
#        elif query[0]=='edgedown':
#            graph.edge_down(query[1], query[2])
#            print("Operation performed")
#        elif query[0]=='quit':
#            exit(0)
#        elif query[0]=='edgeup':
#            graph.edge_up(query[1], query[2])
#            print("Operation performed")
#        elif query[0]=='path':
#            #Find shortest path from query[1] to query[2]
#            #Set all vertex to unvisited, infinite distance, and None as predecessor, initialisation of Dijkstras
#            for v in graph.vert_dict:
#                graph.vert_dict[v].set_unvisited()
#                graph.vert_dict[v].previous=None
#                graph.vert_dict[v].set_distance(sys.maxsize)      
#            #If either vertex is down output "Not reachable"
#            if graph.vertices_status[query[1]]=="DOWN" or graph.vertices_status[query[2]]=="DOWN":
#                print("Unreachable", file=output_file)
#                print("Output written to file")
#            else:
#                #Call dijkstras on the source and destination
#                graph.dijkstra(graph.get_vertex(query[1]), graph.get_vertex(query[2]))
#                target=graph.get_vertex(query[2])
#                path=[target.get_id()] #Store path as array
#                graph.shortest(target, path) # Calculate path
#                print(*path[::-1], "{0:.2f}".format(target.distance),sep=" ", file=output_file)
#                print("Output written to file")
#
#    f.close()
#else:
#    print("File is empty!")
#    exit(0)
#
##Closing the output file
#output_file.close()          
#        