#Authored by: Will Seiple
#borrowed graph implementation from: https://www.youtube.com/watch?time_continue=396&v=HDUzBEG1GlA&feature=emb_title

from prettytable import PrettyTable

class Vertex:
    def __init__(self, n, data=None, above=None, below=None, left=None, right=None):
        self.above = above
        self.below = below
        self.left = left
        self.right = right
        self.name = n
        self.data = data
        self.visited = False
    
    def get_data(self):
        ''' Getter for the data held by a Vertex
            Output: the data held by a Vertex
        '''
        return self.data
    
    def get_name(self):
        ''' Getter for the name of a Vertex
            Output: the name of a Vertex
        '''
        return self.name

    def __str__(self):
        ''' A string representation of a Vertex
            Output: a string representation of a Vertex
        '''
        return str((self.name,self.data))

class Graph:
    vertices = {}
    edges = []
    vertex_indices = {}
    index_to_vertex = {}

    def add_vertex(self, vertex):
        ''' Adds a vertex to the graph.
            Input: vertex - a Vertex object to be added
            Output: whether or not it was added
        '''
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            for row in self.edges:
                row.append(0)
            self.edges.append([0] * (len(self.edges)+1))
            self.vertex_indices[vertex.name] = len(self.vertex_indices) #since we go from a 2d representation of nxm pixels to a graph that's pxp, we need to map everything in nxm -> p; that mapping is assigned here
            self.index_to_vertex[len(self.vertex_indices)-1] = vertex.name
            return True
        return False
    
    def add_edge(self, u, v, weight=0):
        ''' Adds an undirected edge (more precisely, a pair of directed edges)
            Input: u,v - keys in vertices dict (name)
            Output: whether or not the edge could be added 
        '''
        if u in self.vertices and v in self.vertices:
            self.edges[self.vertex_indices[u]][self.vertex_indices[v]] = weight
            self.edges[self.vertex_indices[v]][self.vertex_indices[u]] = weight
            return True
        return False
    
    def add_directed_edge(self, u, v, weight=0):
        ''' Adds a directed edge
            Input: u,v - keys in vertices dict (name)
            Output: whether or not the edge could be added 
        '''
        print (u)
        print (v)
        print (u in self.vertices)
        print (v in self.vertices)
        if u in self.vertices and v in self.vertices:
            self.edges[self.vertex_indices[u]][self.vertex_indices[v]] = weight
            return True
        return False
    
    def print_graph(self):
        ''' Prints out a representation of the graph 
        '''
        listOfColumns = [self.index_to_vertex[i] for i in range(len(self.edges))]#sorted(self.vertex_indices)
        listOfColumns.insert(0, "from\\to")
        table = PrettyTable(listOfColumns)
        for i in range(len(self.edges)):
            vertex = self.index_to_vertex[i]
            row = [self.edges[i][j] for j in range(len(self.edges))]
            #print (str(v), str(self.index_to_vertex[i]), self.vertex_indices[v])
            row.insert(0, str(vertex))
            table.add_row(row)
        print (table)
        #for v, i in sorted(self.vertex_indices.items()):
        #    print str(v) + ' ',
        #    for j in range(len(self.edges)):
        #        print self.edges[i][j], 
        #    print(' ')   