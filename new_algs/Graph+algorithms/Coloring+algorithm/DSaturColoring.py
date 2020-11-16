import networkx as nx
"""
Color graph such that no two adjacent nodes are colored with the same color.

Arguments: G - reference to networkx graph
Returns: listColors - list of lists, when coloring every list should be assigned different color

NOTE: G must be
        - undirected (directed G will be processed as undirected)
        - DeSatur Coloring Algorithm generally uses less colors than Greedy Coloring Algorithm
"""
def dsaturAlgorithm(G):
    # get list of unvisited nodes
    unvisited = []
    unvisited.extend(G.nodes())

    # find node with max neighbors
    maxNeighbors = 0
    for n in unvisited:
        if len(list(G.neighbors(n))) > maxNeighbors:
            maxNeighbors = len(list(G.neighbors(n)))
    # maximum number of colors
    maxColors = maxNeighbors + 1

    # create lists of colors
    listColors = []
    for i in range(0, maxColors - 1):
        newList = []
        listColors.append(newList)

    # while every node is not colored
    while len(unvisited) != 0:
        # highest saturation degree - number and list of nodes
        highestSADegree = -1
        nodesWithHighestSADegree = []
        # choose uncolored node with the highest number of different adjacent colors (saturation degree)
        # for every node N that is not colored
        for n in unvisited:
            # for every neighbor node of node N
            neighborColor = [] # keep track of colors of neighbouring nodes
            for neighbor in G.neighbors(n):
                # check if neighbor node was colored and get index of color
                neighborColored = False
                for color in listColors:
                    if neighbor in color:
                        colorIndex = listColors.index(color)
                        neighborColored = True
                        break
                # if node was colored and index of color is not in neighborColor
                if neighborColored == True and colorIndex not in neighborColor:
                    # add index of color to neighborColor
                    neighborColor.append(colorIndex)
            # get saturation degree of the node
            saturationDegree = len(neighborColor)
            # if SA of the node is higher that highestSA
            if saturationDegree > highestSADegree:
                # highestSA is equal to SA of the node
                highestSADegree = saturationDegree
                # clear nodesWithHighestSA and add there the node
                nodesWithHighestSADegree.clear()
                nodesWithHighestSADegree.append(n)
            # if SA of the node is the same as highestSA
            elif saturationDegree == highestSADegree:
                # add node to nodesWithHighestSADegree
                nodesWithHighestSADegree.append(n)
            # clear neighborColor list for next node
            neighborColor.clear()


        # if there is just one node that has the highest saturation degree
        if len(nodesWithHighestSADegree) == 1:
            nodeToColor = nodesWithHighestSADegree[0]
        # if more nodes have the same saturation degree, choose node with the highest degree (or one of them)
        else:
            highestDegree = -1
            for i in nodesWithHighestSADegree:
                if len(list(G.neighbors(i))) > highestSADegree:
                    highestSADegree = len(list(G.neighbors(i)))
                    nodeToColor = i


        # color nodeToColor
        for color in listColors:
            # for every neighbor check if it is not in color1, color2, ... colorM
            nInColor = False
            for n in list(G.neighbors(nodeToColor)):
                if n in color:
                    nInColor = True
                    continue
            # if no neighbor was in colorN, color node with colorN
            if nInColor == False:
                color.extend(nodeToColor)
                break

        # node was colored -> delete it from unvisited list
        unvisited.remove(nodeToColor)


    # compute how many colors were needed
    numberColors = maxColors
    for i in range(len(listColors)):
        if len(listColors[i]) == 0:
            numberColors = i
            break
    # delete unused color lists
    while len(listColors) > numberColors:
        listColors.pop(numberColors)

    return listColors

