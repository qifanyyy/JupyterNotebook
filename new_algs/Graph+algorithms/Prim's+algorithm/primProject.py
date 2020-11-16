# this block imports packages needed by the Graph and Weighted_Graph classes.  
# Just run it.
import numpy as np
import networkx as nx
# %matplotlib inline
import matplotlib.pyplot as plt

class Graph(object):
    
    def __init__(self, *args):
 
        self.edge_list_file = ''
        self.edge_set = set()
        self.vertex_set = set()

        # 1 or 2 arguments may be passed.
        # if 1, it can either be a edge list file or an edge set
        if(len(args)==1):
            # if the argument is a string, read the edges from the file
            if(type(args[0]) is str):
                self.edge_list_file = args[0]
                self.edge_set = self.set_edges_from_file()
                self.update_vertices()
            
            # if the argument is a set, set the edge_set and create a 
            # vertex set from the endpoints of the edges+
            elif(type(args[0]) is set):
                self.edge_set = args[0]
                self.update_vertices()

        # if 2 arguments are passed, the first should be the vertex set
        # and the second the edge_set
        elif(len(args)==2):
            self.vertex_set = args[0]
            self.edge_set = args[1]
    
    def set_edges_from_file(self):
        """ Returns the set of edges """
        edge_set = set()
        edge_list = np.loadtxt(self.edge_list_file, int)   # numpy 2-d array
        for row in edge_list:
            e = (row[0],row[1])
            edge_set.add(e)     # Assign keys and values
        return edge_set
        
    
    def update_vertices(self):
        """ Returns the set of vertices """
        for e in self.edge_set:
            self.vertex_set = self.vertex_set.union(e)
   
    def add_edge(self,e):
        """ Add an edge to the graph """
        self.edge_set.add(e)
        self.update_vertices()
    
    def copy(self):
        """ Make a copy of the graph """
        edges = self.edge_set.copy()
        vertices = self.vertex_set.copy()
        return Graph(vertices, edges)
    
    def is_tree(self):
        """ Return True if the graph is a tree, False otherwise based on the |V|=|E|+1 criterion"""
        return (len(self.vertex_set) == len(self.edge_set)+1)
    
    def spans(self,H):
        """ Return True if self spans the graph H , False otherwise """
        return self.vertex_set == H.vertex_set
    
    def draw_graph(self):
        """ This function is used to visualize your graph. The functions
            used inside are from the networkx library. """
        
        G = nx.Graph()
        G.add_nodes_from(self.vertex_set)
        G.add_edges_from(self.edge_set)
        pos=nx.spring_layout(G) # positions for all nodes
        nx.draw_networkx_nodes(G,pos,node_size=250) # nodes
        nx.draw_networkx_edges(G,pos,edgelist=G.edges(),width=1) # edges
        nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
        plt.axis('off')
        plt.show()
        
    def draw_subgraph(self, H):
        """ This function is used to visualize your weighted graph. The functions
            used inside are from the networkx library. """
        
        G = nx.Graph()
        G.add_nodes_from(self.vertex_set)
        G.add_edges_from(self.edge_set)

        S = nx.Graph()
        S.add_nodes_from(H.vertex_set)
        S.add_edges_from(H.edge_set)


        pos=nx.spring_layout(G) # positions for all nodes
        nx.draw_networkx_nodes(G,pos,node_size=250) # nodes
        nx.draw_networkx_nodes(G,pos, nodelist = S.nodes(),node_size=400)
        nx.draw_networkx_edges(G,pos,edgelist=G.edges(),width=1) # edges
        nx.draw_networkx_edges(G,pos,edgelist=S.edges(), color = 'red' ,width=5)
        
        # labels
        nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
        plt.axis('off')
        plt.show()        


class Weighted_Graph(Graph):
    
    def __init__(self, *args):
        
        self.edge_list_file = ''
        self.edge_dict = {}
        self.edge_set = set()
        self.vertex_set = set()
        
        # 1 or 2 arguments may be passed.
        # if 1, it can either be a edge list file or an edge dictionary
        if(len(args)==1):
            # if the argument is a string, read the edges from the file
            if(type(args[0]) is str):
                self.edge_list_file = args[0]
                self.edge_dict = self.set_edge_dict_from_file()
                self.edge_set = set()
                self.update_edges()
                self.vertex_set = set()
                self.update_vertices()
            
            # if the argument is a dictionary, set the edge dictionary and create a 
            # edge set from the dictionary and a vertex set from the edge set.
            elif(type(args[0]) is dict):
                self.edge_dict = args[0]
                self.edge_set = set()
                self.update_edges()
                self.vertex_set = set()
                self.update_vertices()

        # if 2 arguments are passed, the first should be the vertex set
        # and the second the edge dictionary
        elif(len(args)==2):
            self.vertex_set = args[0]
            self.edge_dict = args[1]
            self.edge_set = set()
            self.update_edges()

            
    def set_edge_dict_from_file(self):
        """ Reads in the edge list from the provided directory address and 
            creates a edge dictionary where the keys are the edges and values
            are the corresponding edge weights. In particular, to access the
            value of edge (a,b), simply type edge_dict[(a,b)]"""
        edge_dict = dict()                                 # dict()=empty dictionary
        edge_list = np.loadtxt(self.edge_list_file, int)   # numpy 2-d array
        for row in edge_list:
            edge_dict[(row[0], row[1])] = row[2]           # Assign keys and values
        return edge_dict
    
    
    def update_edges(self):
        """ Returns the set of edges """
        self.edge_set = set(self.edge_dict.keys())
        
    def copy(self):
        """ Make a copy of the graph """
        
        # if the edge list file has been defined, create the new graph from that
        if(self.edge_list_file):
            return Weighted_Graph(self.edge_list_file)
        # otherwise create the graph from the edge_dict and vertex_set
        else:
            edge_dict = self.edge_dict.copy()
            vertices = self.vertex_set.copy()
            return Weighted_Graph(vertices, edge_dict)
        
 
    def add_edge(self,e,w):
        """ add an edge with a weight """
        self.edge_dict[e] = w
        self.update_edges()
        self.update_vertices()
    
    def draw_graph(self):
        """ This function is used to visualize your weighted graph. The functions
            used inside are from the networkx library. """
        
        G = nx.read_edgelist(self.edge_list_file, nodetype=int, data=(('weight',float),))
        e=[(u,v) for (u,v,d) in G.edges(data=True)]
        pos=nx.spring_layout(G) # positions for all nodes
        nx.draw_networkx_nodes(G,pos,node_size=250) # nodes
        nx.draw_networkx_edges(G,pos,edgelist=e,width=1) # edges

        # labels
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        plt.axis('off')
        plt.show()
        
    def draw_subgraph(self, H):
        """ This function is used to visualize your weighted graph. The functions
            used inside are from the networkx library. """
        
        G = nx.read_edgelist(self.edge_list_file, nodetype=int, data=(('weight',float),))
        e1=[(u,v) for (u,v,d) in G.edges(data=True)]
        e2= [e for e in e1 if e in H.edge_set]
        v1 =[v for v in H.vertex_set]
        pos=nx.spring_layout(G) # positions for all nodes
        nx.draw_networkx_nodes(G,pos,node_size=250) # nodes
        nx.draw_networkx_nodes(G,pos, nodelist = v1,node_size=400)
        nx.draw_networkx_edges(G,pos,edgelist=e1,width=1) # edges
        nx.draw_networkx_edges(G,pos,edgelist=e2, color = 'red' ,width=5)
        
        # labels
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        plt.axis('off')
        plt.show()

def incident_edges(G,T):
    ''' return the set of all edges from graph G that are incident with tree T'''
    
    # initialize an empty set incidentEdges 
    incidentEdges = set()
    
    # for every vertex v in T check all edges e in G.  
    # if v is an endpoint of e, add e to incidentEdges
    for v in T.vertex_set:
        for e in G.edge_set:
            if v in e:
                incidentEdges.add(e)
    
    # return indicent edges that are not already edges in T 
    return incidentEdges - T.edge_set

def valid_edges(G,T):
    ''' return the set of all edges e from G where T+e is a tree and e is not already an edge of T'''

     # get a set incident of all edges in G incident with T
    incidentEdges = incident_edges(G,T)
    
    # initialize an empty set valid 
    valid = set()
    
    # check all edges e in incident.  if T+e is a tree, add e to valid
    # Hint: test e using a copy of T
    for e in incidentEdges:
        Tcopy = T.copy()
        Tcopy.edge_set.add(e)
        for v in e:
            Tcopy.vertex_set.add(v)
        if (Tcopy.is_tree()):
            valid.add(e)
    # return all of the valid edges   
    return valid

def weight(e,G):
    ''' return the weight of an edge in a weighted graph G '''
    return G.edge_dict[e]

def min_valid_edge(G,T):
    ''' return the edge e from graph G with minimum weight where T+e is a tree '''
 
    # get a set all edges e in G where T+e is a tree
    valid = valid_edges(G,T)
    
    # initialize min_edge to be a random edge in valid 
    min_edge = valid.pop()
   
    # check all valid edges e.  if the weight of e is less than the weight of min_edge, update minEdge = e 
    for e in valid:
        if (weight(e,G) < weight(min_edge,G)):
            min_edge = e
   
    # return min_edge
    return min_edge

def prim(G):
    ''' Use Prim's algorithm to find a MST for the graph G '''    

    # Initialize tree T with a single vertex and no edges 
    v = next(iter(G.vertex_set))
    vset = set()
    vset.add(v)
    e = {}
    T = Weighted_Graph(vset,e)
    
    # while the vertex set of T is smaller than the vertex set of G, 
    # (i.e. while the vertex set of T is a proper subset of the 
    #  vertex set of G), find the edge e with minimum weight so that  
    # T+e is a tree. Then update T = T+e '''
    while(not T.spans(G)):
        next_edge = min_valid_edge(G,T)
        next_edge_weight = weight(next_edge, G)
        T.add_edge(next_edge, next_edge_weight)
                   
    # return T 
    return T

G = Weighted_Graph('test2.txt')
T = prim(G)
G.draw_subgraph(T)
