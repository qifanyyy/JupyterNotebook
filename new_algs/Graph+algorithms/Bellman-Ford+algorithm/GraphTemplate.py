import math

# NO ADDITIONAL LIBRARIES HAVE TO BE USED FOR THE ASSIGNMENT

class GraphTemplate(object):
    _nodes = []               #! list of NodeTemplate ONLY
    _minPriorityQueue = None  #! reference to MinHeapTemplate

    def __init__(self):
        pass

    # TODO: implement additional constructors
    # TODO: implement method for adding a node
    # TODO: implement method for removing a node
    # TODO: implement Prim
    # TODO: implement Bellman-Ford
    # TODO: implement methods for manipulating the parent and distance

class NodeTemplate(object):
    label = ""          #! string
    adjacentNodes = {}  #! dict of pairs (NodeTemplate : float) 
    parent = None       #! reference to NodeTemplate
    distance = math.inf #! number (float), aka key

    def __init__(self):
        pass
    
    def __init__(self, labelN, adjacentNod):
        pass
    # TODO: implement additional constructors
    # TODO: implement method for adding a connection
    # TODO: implement method for removing a connection
    # TODO: implement methods for manipulating the parent and distance

class MinHeapTemplate(object):
    root = None #! reference to MinHeapNode

    def __init__(self):
        pass

    # TODO: implement method for restructuring the min-priority Queue
    # TODO: implement method for extracting the smaller element from the min-priority Queue

class MinHeapNode(object):
    node    = None  #! reference to NodeTemplate
    parent  = None  #! reference to MinHeapNode
    left    = None  #! reference to MinHeapNode
    right   = None  #! reference to MinHeapNode

    def __init__(self):
        pass

    # TODO: implement additional constructors