import xml.etree.ElementTree as ET
import math
import heapq
from heapq import heapify, heappop

EarthRadius = 6371.0 / 1.60934

def distanceBetween(node1, node2):
    """
    Uses the haversine formula to calculate the approximate distance between
    two nodes
    """
    sinLat = math.pow(math.sin((node1.Lat - node2.Lat)/2), 2)
    cosLat1 = math.cos(node1.Lat)
    cosLat2 = math.cos(node2.Lat)
    sinLong = math.pow(math.sin((node1.Lon - node2.Lon)/2), 2)
    return 2 * EarthRadius * math.asin(math.sqrt(sinLat + cosLat1 * cosLat2 * sinLong))


class Graph(object):
    """
    The Graph class is built from an OSM file from the openstreetmap.org site

    Nodes will be a hash table of all node elements from the graph file where the key
    will be the id from the OSM file and the value will be a Node object

    Edges will be a hash table of all way elements from the graph file where the key
    will be the id with a segment number added since a way has multiple nodes in it
    and the value will be an Edge object.
    """

    def __init__(self, path):
        """
        Path is expected to be a XML file from openstreetmap.org
        """
        tree = ET.parse(path)
        root = tree.getroot()
        self.buildNodes(root)
        self.buildEdges(root)
        self.removeNodesWithNoEdges()

    def buildNodes(self, root):
        self.Nodes = {}
        for nodeElem in root.findall('./node'):
            node = Node(nodeElem)
            self.Nodes[node.Id] = node

    def buildEdges(self, root):
        """
        Builds edges for all ways that have a name - this will skip ways that
        are parking lots and other things that aren't of interest
        """
        self.Edges = {}
        for wayElem in root.findall("./way/tag[@k='name']/.."):
            self.buildEdgesFromWay(wayElem)

    def buildEdgesFromWay(self, wayElem):
        """
        Builds all the edges for a way element
        """
        prevNode = None
        edgeNbr = 1
        edgeId = wayElem.get('id')
        name = wayElem.find("./tag[@k='name']").get('v')
        for ndElem in wayElem.findall('./nd'):
            node = self.Nodes[ndElem.get('ref')]
            if node != None:
                if prevNode != None:
                    edge = Edge(edgeId, name, prevNode, node, edgeNbr)
                    self.Edges[edge.Id] = edge
                    edgeNbr += 1
                prevNode = node

    def removeNodesWithNoEdges(self):
		# the values method in Python 3 is an iterator, so
		# need to gather the list of nodes to be deleted
		# and remove them in a separate loop
        toBeDeleted = []
        for n in self.Nodes.values():
            if len(n.Edges) == 0:
                toBeDeleted.append(n.Id)
				
        for id in toBeDeleted:
                del self.Nodes[id]
                
    def StartNode(self):
        """
        The corner of Reade and Main
        """
        return self.Nodes['179660855']

    def EndNode(self):
        """
        corner of Univserstity Blvd & Felton - near IWU
        """
        return self.Nodes['300906742']

    def NearEndNode(self):
        """
        corner of Berry and South 3rd Street - a near point for testing
        """
        return self.Nodes['179661822']

class Node(object):
    """
    The Node class has the following properties:
    Id - id from the OSM file
    Lat - latitude (lat) from the OSM file converted to float and radians
    Lon - longitude (lon) from the OSM file converted to float and radians
    Edges - all edges connected to the node
    """

    def __init__(self, ndElem):
        self.Id = ndElem.get('id')
        self.Lat = math.radians(float(ndElem.get('lat')))
        self.Lon = math.radians(float(ndElem.get('lon')))
        self.Edges = []

    def addEdge(self, edge):
        self.Edges.append(edge)

    ################ added by Dustin #####################
    def connectedTo(self,node):
        for edge in self.Edges:
            if edge.otherNode(node):
                return True
        return False

    def getNeighbors(self):
        neighbors = []
        for edge in self.Edges:
            neighbors.append(edge.otherNode(self).Id)
        return neighbors

    def lengthTo(self,node):
        if self.connectedTo(node):
            for edge in self.Edges:
                if edge.otherNode(node):
                    return edge.Length
        else:
            return None

    def getEdge(self,node):
        if self.connectedTo(node):
            for edge in self.Edges:
                if edge.otherNode(node):
                    return edge.Name
        else:
            return None
    #######################################################

class Edge(object):
    """
    The Edge class has the following properties:
    Id - id from the OSM file plus a sequence number for uniqueness
    Name - name of the street
    NodeStart - starting node for edge
    NodeEnd - ending node for edge
    Length - estimated length of edge
    All edges are considered bi-directional - use otherNode method to
    find the opposite node given either one.
    """

    def __init__(self, edgeId, name, nodeStart, nodeEnd, edgeNbr):
        self.Id = edgeId + "_" + str(edgeNbr)
        self.Name = name
        self.NodeStart = nodeStart
        nodeStart.addEdge(self)
        self.NodeEnd = nodeEnd
        nodeEnd.addEdge(self)
        self.Length = distanceBetween(nodeStart, nodeEnd)

    def otherNode(self, node):
        if node == self.NodeStart:
            return self.NodeEnd
        elif node == self.NodeEnd:
            return self.NodeStart
        return None


######################Added by Dustin#################################
    
def reconstruct_path(cameFrom,current_node,path):
    if current_node in cameFrom:
        p = reconstruct_path(cameFrom,cameFrom[current_node],path)
        p.append(current_node)
        return p
    else:
        path.append(current_node)
        return path

def OS(openSet):
    x = []
    for i in openSet:
        x.append(i[1])
    return x

def short_path(graph,start,goal,heuristic):
    path = []
    closedSet = []
    cameFrom = {}
    g_score = {start.Id:0}
    f_score = {start.Id:g_score[start.Id] + heuristic(start,goal)}
    openSet = [ ( f_score[start.Id] , start.Id ) ,]
    
    while len(openSet) > 0:
        heapify(openSet)
        current = heappop(openSet)[1]
        if current == goal.Id:
            return [reconstruct_path(cameFrom,goal.Id,path),f_score,openSet,closedSet]
        closedSet.append(current)
        for neighbor in graph.Nodes[current].getNeighbors():
            if neighbor in closedSet:
                continue
            tentative_g_score = g_score[current] + graph.Nodes[current].lengthTo(graph.Nodes[neighbor])

            if neighbor not in OS(openSet) or tentative_g_score < g_score[neighbor]:
                cameFrom[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(graph.Nodes[neighbor],goal)
                if neighbor not in OS(openSet):
                    openSet.append((f_score[neighbor],neighbor))
    return False

def dijkstra(start,goal):
    return 0

def print_results(graph,info):
    print("Distance from TU to IWU: ",info[1][graph.EndNode().Id])
    print("Number of nodes in path: ",len(info[0]))
    print("Number of nodes handled: ",len(info[3]))
    print("Number of nodes found not handled: ",len(info[2]))
    
    print("Path to Take:")
    x = []
    for i in range(len(info[0])-1):
        if graph.Nodes[info[0][i]].getEdge(graph.Nodes[info[0][i+1]]) not in x:
            print("\t",graph.Nodes[info[0][i]].getEdge(graph.Nodes[info[0][i+1]]))
            x.append(graph.Nodes[info[0][i]].getEdge(graph.Nodes[info[0][i+1]]))
    print()
    
########################################################################
            
if __name__ == "__main__":
    graph = Graph("upland.osm")
    print("number of nodes", len(graph.Nodes))
    print("number of edges", len(graph.Edges))
    print()
    
    info = short_path(graph,graph.StartNode(),graph.EndNode(),distanceBetween)
    print("A* Results")
    print_results(graph,info)
    
    info = short_path(graph,graph.StartNode(),graph.EndNode(),dijkstra)
    print("Dijkstra Results")
    print_results(graph,info)
    input()
    
            
