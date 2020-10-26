#Authored by: Pranav Subramanian and Will Seiple
#following: https://julie-jiang.github.io/image-segmentation/
#per https://brilliant.org/wiki/edmonds-karp-algorithm/, decided to use an adjacency matrix

from ui import pickImage
from graph import *
from PIL import Image
import numpy as np
import math
import sys

def penalty(u, v, sigma):
    ''' Computes boundary penalty given two Vertex objects
        Input: u - a Vertex object
               v - a Vertex object
               sigma - a parameter to adjust the output of this function to something "workable", determined to be about 100000
        Output: boundary penalty - int
    '''
    return int(100*math.exp((-(u.get_data()-v.get_data())**2)/(2*sigma**2))) #this boundary penalty was from: https://julie-jiang.github.io/image-segmentation/

def intensity(rgb):
    ''' Gets the intensity of an rgb array
        Input: rgb - an array of 3 rgb values (i.e. [255, 255, 255])
        Output: intensity - a 1D value corresponding to the greyscale value of the rgb array
    '''
    return 0.2126 * rgb[0] ** 2.2 + 0.7152 * rgb[1] ** 2.2 + 0.0722 * rgb[2] ** 2.2 #this was from: https://stackoverflow.com/questions/687261/converting-rgb-to-grayscale-intensity

def image_to_array(filename):
    ''' Converts image to a 2D list of RGB values (sub-arrays)
        Input: filename - an image file name or path
        Ouput: array - a 2D list representation of the image, with each element as an rgb array of 3 values
    '''
    im = Image.open(filename, 'r')
    return np.asarray(im)

def add_vertices(graph, image_array):
    ''' Adds vertices from an array of image to our implementation of the graph
        Input: graph - an instance of the Graph class
               image_array - an array of image values
    '''
    im = image_array
    width, height = im.shape[1], im.shape[0]
    for row in range(0,height):
        for col in range(0,width):
            v = Vertex((row,col), intensity(im[row][col])) #makes a vertex out of each pixel, with its name set to a tuple of its coordinates, and its data set to its intensity
            graph.add_vertex(v)
 
def add_edges(graph, image_array):
    ''' Adds the edges from an array of our image to our implementation of the graph
        Input: graph - an instance of the Graph class
               input_array - an array of image values
    '''
    im = image_array
    width, height = im.shape[1]-1, im.shape[0]-1
    for vertex_pos in graph.vertices.keys(): #goes through all vertices, and adds edges linking each Vertex representing a pixel to its four direct neighbors, with the edge weight set to the boundary penalty function between the two's intensities
        if vertex_pos[0] < height:
            graph.add_edge(vertex_pos, (vertex_pos[0]+1, vertex_pos[1]), penalty(graph.vertices[vertex_pos],graph.vertices[(vertex_pos[0]+1, vertex_pos[1])], 100000))
        if vertex_pos[1] < width:
            graph.add_edge(vertex_pos, (vertex_pos[0], vertex_pos[1]+1), penalty(graph.vertices[vertex_pos],graph.vertices[(vertex_pos[0], vertex_pos[1]+1)], 100000))
        if vertex_pos[0] > 0:
            graph.add_edge(vertex_pos, (vertex_pos[0]-1, vertex_pos[1]), penalty(graph.vertices[vertex_pos],graph.vertices[(vertex_pos[0]-1, vertex_pos[1])], 100000))
        if vertex_pos[1] > 0:
            graph.add_edge(vertex_pos, (vertex_pos[0], vertex_pos[1]-1), penalty(graph.vertices[vertex_pos],graph.vertices[(vertex_pos[0], vertex_pos[1]-1)], 100000))

def add_source_sink(graph, source, sink):
    ''' Adds the sources and sinks to the graph
        Input: graph - an instance of the Graph class
               source - an array of tuples, holding source coordinates and a preset edge weight of 10000
               sink - an array of tuples, holding sink coordinates and a preset edge weight of 10000
    '''
    s = Vertex("Source")
    t = Vertex("Sink")
    graph.add_vertex(s)
    graph.add_vertex(t)

    for edge in source:
        #edge[0] describes the name of the neighboring vertex
        #edge[1] describes the weight, set by default to the maximum, of 100
        print "SOURCE TO: " + str(edge)
        print graph.vertices["Source"]
        print graph.vertices[(1,1)]
        print graph.add_directed_edge("Source", edge[0], edge[1])
    
    for edge in sink:
        #edge[0] describes the name of the neighboring vertex
        #edge[1] describes the weight, set by default to the maximum, of 100
        graph.add_directed_edge(edge[0], "Sink", edge[1])


def create_graph(graph, filename, source, sink):
    ''' Creates the graph
        Input: graph - an (empty) instance of the Graph class
               filename - the file name or file path of the image
               source - an array of tuples, holding source coordinates and a preset edge weight of 10000
               sink - an array of tuples, holding sink coordinates and a preset edge weight of 10000
    '''
    graph = Graph()
    image_array = image_to_array(filename)
    add_vertices(graph, image_array)
    add_edges(graph, image_array)
    add_source_sink(graph, source, sink)


def dfs(graph, resGraph):
    ''' Our method of finding an augmenting path in the residual graph, using a depth-first-search from source to sink
        Input: graph - an instance of the Graph class
               resGraph - a 2D list representing the residual graph
    '''
    #remember that the row signifies the "pointer" and the column signifies the "pointee"
    edges = graph.edges
    verts = graph.vertices

    #variables standard to a dfs
    source = (edges[-2], len(edges)-2)
    stack = []
    stack.append(source)
    
    pathTracker = {} #allows for tracking of paths, so that the obtained path can be traced from sink back to source; see https://stackoverflow.com/questions/12864004/tracing-and-returning-a-path-in-depth-first-search
    verts[graph.index_to_vertex[len(edges)-2]].visited = True #setting the source to visited
    allVisited = [verts[graph.index_to_vertex[len(edges)-2]]] #this array is maintained so we can easily reset the 'visited' state of every vertex at the end of execution

    while len(stack) > 0: #standard dfs
        top = stack.pop()
        for i in range(len(top[0])):
            #going through a list of neighbors, which looks like [0, 100, 0, 14, 0, etc...]
            if top[0][i] is 0: #i.e. no edge
                continue
            if verts[graph.index_to_vertex[i]].name is 'Sink': #i.e. we've finished!
                pathTracker[i] = top[1]
                break
            if not verts[graph.index_to_vertex[i]].visited: #i.e. an unvisited neighbor
                if edges[top[1]][i] - resGraph[top[1]][i] > 0: #see if there's flow left
                    stack.append((edges[i], i)) #if so, push it
                    #print (edges[i], i)
                    pathTracker[i] = top[1] #inspiration from here: https://stackoverflow.com/questions/12864004/tracing-and-returning-a-path-in-depth-first-search
                    verts[graph.index_to_vertex[i]].visited = True #mark visited after pushing
                    allVisited.append(verts[graph.index_to_vertex[i]])
    
    for x in allVisited: #clear visited, could've used a visited matrix as that would clear as soon as the method ended execution...
        #print x.name
        x.visited = False
    
    path = [] #finally, get the path
    current = len(edges)-1 #inspiration from here: https://stackoverflow.com/questions/12864004/tracing-and-returning-a-path-in-depth-first-search
    
    if current not in pathTracker: #this means if the sink isn't in pathTracker, implying no path from source to sink exists...
        return path #...return an empty array
    
    while (current != len(edges)-2): #otherwise, backtrack through the dict until you get to the source
        path.append(graph.index_to_vertex[current])
        current = pathTracker[current]
    path.append(graph.index_to_vertex[len(edges)-2]) #append the source

    return path


def edmondsKarp(graph, resGraph):
    ''' A method that runs the actual Edmonds-Karp Algorithm.
        Input: graph - an instance of the Graph class
               resGraph - a 2D list representing the residual graph
    '''
    path = dfs(graph, resGraph) #this gets you the path, but its reversed. We handle that in the loop, by switching the order of the vertex indices when finding edge weights (i.e. graph.edges[graph.vertex_indices[path[x+1]]][graph.vertex_indices[path[x]]])
    #print path
    while('Sink' in path): #while an 'augmenting path' exists in the residual graph
        #print "EdmondsKarp" #for testing
        edges = [(graph.vertex_indices[path[x+1]],graph.vertex_indices[path[x]]) for x in range(len(path)-1)]
        edges.reverse() #this gets all the edges in a simple tuple format, with integers representing the indices they correspond to in the adjacency matrix, and put in sequential order, as the dfs returns a reversed path
        minCap = min([graph.edges[edge[0]][edge[1]] - resGraph[edge[0]][edge[1]] for edge in edges]) #find the minimum residual capacity
        for edge in edges:
            #(u,v) += minCap
            resGraph[edge[0]][edge[1]] += minCap
            #(v,u) -= minCap
            resGraph[edge[1]][edge[0]] -= minCap
        
        path = dfs(graph, resGraph) #update the path


def findCut(graph, resGraph):
    ''' A breadth-first traversal from the source to all edges that arent at capacity, making huge list of vertices/pixels that are in the source segment
        Input: graph - an instance of the graph class
               resGraph - a 2D list representing the residual graph, AFTER Edmonds-Karp has been run.
    '''
    print "Here" #for testing
    pixels = [graph.vertices[graph.index_to_vertex[len(graph.edges)-2]]] #a list of all the pixels
    
    #variables standard to a bft
    q = []
    source = (graph.edges[-2],len(graph.edges)-2)
    q.append(source)   

    while len(q) > 0:
        top = q.pop(0)
        for i in range(len(top[0])):
            if top[0][i] is not 0: #want to filter all the neighbors of the source in the residual graph such that we only go for neighbors where an edge exists, there is capacity left, and it hasn't been visited (i.e. it is a part of the source segment)
                if top[0][i] - resGraph[top[1]][i] > 0: #could've easily made this 1 if statement, but splitting it like this improved readability and facilitated debugging
                    if not graph.vertices[graph.index_to_vertex[i]].visited:
                        pixels.append(graph.vertices[graph.index_to_vertex[i]]) #it is part of the source segment!
                        q.append((graph.edges[i], i))#if so, push it
                        graph.vertices[graph.index_to_vertex[i]].visited = True #mark visited after pushing
    print [str(x) for x in pixels]
    return pixels

# Reversing a list using reversed() - https://www.geeksforgeeks.org/python-reversing-tuple/
def Reverse(tuples): 
    new_tup = () 
    for k in reversed(tuples): 
        new_tup = new_tup + (k,) 
    return new_tup 


if __name__ == "__main__":
    #get the image, sources, and sinks
    pre_sources, pre_sinks, filename, dimensions = pickImage()

    filename = "C:\Users\prana\Documents\image_segmentation\image_segmentation\imeg2.png"
    dimensions = (10,8)

    #print pre_sources
    pre_sources = [x[::-1] for x in pre_sources]
    #print pre_sources
    
    #print pre_sinks
    pre_sinks = [x[::-1] for x in pre_sinks]
    #print pre_sinks

    pre_sources = ["5,8"]
    pre_sinks = ["3,2", "4,6"]

    #converts the coordinates from pickImage() to a format that can be easily converted to a Vertex
    sources = [((int(x.split(",")[0]), int(x.split(",")[1])),10000) for x in pre_sources] 
    
    sinks = [((int(x.split(",")[0]), int(x.split(",")[1])),10000) for x in pre_sinks]

    print sources
    print sinks

    #create the graph
    graph = Graph()
    create_graph(graph, filename, sources, sinks)

    #and the residual graph
    residualGraph = [[0 for x in range(len(graph.edges))] for y in range(len(graph.edges))]

    #graph.print_graph()
    #print residualGraph

    #run Edmonds-Karp
    edmondsKarp(graph, residualGraph)

    #finally, the bft that gets all vertices associated with pixels in the source segment/foreground
    source_pixels = findCut(graph, residualGraph)

    #finally, create and save an image that has a blue sink segment (a blue background) and a red source segment (a red foreground)
    segmented = Image.new('RGB', dimensions, color = (0, 0, 255))
    for i in source_pixels:
        if not i.name == "Source":
            print Reverse(i.name)
            segmented.putpixel(Reverse(i.name), (255, 0, 0))
    segmented.save("segmented.png")


    

