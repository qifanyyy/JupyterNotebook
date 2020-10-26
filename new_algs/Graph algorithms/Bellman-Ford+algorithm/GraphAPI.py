'''GraphAPI implementation
    bag: a bag of nodes in the graph
    adjacent: dictionary {node: list of neighbors of node}
'''
class Graph(object):

    '''constructor initialize bag and adjacent list'''
    def __init__(self):
        self.bag = []
        self.adjacent = {}
        self.edges = []

    '''method for adding node to the graph if it is not in the graph'''
    def addNode(self, node):
        if node not in self.bag:
            #add to the bag
            self.bag.append(node)   
            #add a empty adjacent list                  
            self.adjacent[node] = []

    '''add a weighted edge'''
    def addWeightedEdge(self, source, target, weight):
        if source not in self.bag or target not in self.bag:
            print "there is not such node"
        else:
            #element of adjacent list would be (neighbor, weight)
            self.adjacent.get(source).append((target, weight))
            self.edges.append((source, target, weight))

    
    '''given id, get the node'''
    def getNodebyID(self, id):
        if id in self.bag:
            return self.bag[self.bag.index(id)]
        
    '''print adjacent list 
        node [(neighbors, weight)...,]
    '''
    def toString(self):
        result = ""
        for node in self.bag:
            result += str(node) + "[" 
            for n in self.adjacent[node]:
                result += str(n)
            result += "] \n"
        return result


'''for testing
if __name__ =="__main__":
    graph =Graph()

    graph.addNode(1)
    graph.addNode(2)

    graph.addNode(3)

    graph.addWeightedEdge(3, 2, 10)

    print graph.toString()
    print graph.getNodebyID(2)
'''