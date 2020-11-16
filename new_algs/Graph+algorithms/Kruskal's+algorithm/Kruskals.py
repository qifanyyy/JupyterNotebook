import xml.dom.minidom
from GraphsandTrees.Dijkstra.dijkstra import Vertex, VertexCost, Edge


class Partition:
    def __init__(self, size):
        self.data = list(range(size))

    def sameSetAndUnion(self, i, j):
        rooti = i
        rootj = j

        while rooti != self.data[rooti]:
            rooti = self.data[rooti]


        while rootj != self.data[rootj]:
            rootj = self.data[rootj]

        if rooti != rootj:
            self.data[rooti] = rootj
            return False

        return True


def main():
    # We must read in the graph.xml file first to set up our edges and vertices
    xmldoc = xml.dom.minidom.parse('GraphsandTrees/Dijkstra/graph.xml')
    vertexElements = xmldoc.getElementsByTagName("Vertex")
    edgeElements = xmldoc.getElementsByTagName("Edge")
    # dict of vertexIds:vertexObjs
    vertexIdVertexObjDict = {}

    startingVertex = None
    # get vertexIds, add to vertexIdVertexObjDict
    for s in vertexElements:
        vertexId = int(s.attributes['vertexId'].value)
        x = s.attributes['x'].value
        y = s.attributes['y'].value
        label = int(s.attributes['label'].value)
        vertexObj = Vertex(vertexId, x, y, label)
        if label == 0:
            vertexObj.updateCost(0)
            vertexObj.setPrevious(0)
            startingVertex = VertexCost(0, vertexId)
        vertexIdVertexObjDict[vertexId] = vertexObj

    # get edge weights
    edgeLst = []
    for j in edgeElements:
        vertex1 = int(j.attributes['tail'].value)
        vertex2 = int(j.attributes['head'].value)
        weight = float(j.attributes['weight'].value)
        edgeLst.append(Edge(vertex1, vertex2, weight))

    # add Edge object to appropriate vertex
    for edge in edgeLst:
        vertex1 = edge.getV1()
        vertex2 = edge.getV2()
        vertexIdVertexObjDict[vertex1].addEdge(edge)
        vertexIdVertexObjDict[vertex2].addEdge(edge)


    # Where Kruskal's algorithm really starts
    edgeLst.sort()
    spanningTree = []
    partition = Partition(len(vertexIdVertexObjDict))
    edgeIndex = 0

    while len(spanningTree) + 1 < len(vertexIdVertexObjDict) and edgeIndex < len(edgeList):
        edge = edgeLst[edgeIndex]
        if not partition.sameSetAndUnion(edge.getV1(), edge.getV2()):
            # Add them to the spanning tree
            spanningTree.append(edge)
        edgeIndex += 1

    # for edge in spanningTree:
    #     edge.draw(turtle, vertexDict, color="orange", width=1)



if __name__ == "__main__":
    main()