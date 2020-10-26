import networkx as nx

"""
Color graph such that no two adjacent nodes are colored with the same color.
Arguments: G - reference to networkx graph
Returns: listColors - list of lists, when coloring every list should be assigned different color

NOTE: G must be
        - undirected (directed G will be processed as undirected)
        - order of nodes in which greedy algorithm process them is random
"""
def greedyAlgorithm(G):
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
    for i in range(0, maxColors):
        newList = []
        listColors.append(newList)

    # while every node is not colored
    while len(unvisited) != 0:
        # choose next node in queue
        node = unvisited[0]

        for color in listColors:
            # for every neighbor check if it is not in color1, color2, ... colorM
            nInColor = False
            for n in list(G.neighbors(node)):
                if n in color:
                    nInColor = True
                    continue
            # if no neighbor was in colorN, color node with colorN
            if nInColor == False:
                color.extend(node)
                break

        # node was colored -> delete it from unvisited queue
        del unvisited[0]

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

"""
- coloring is NP complete problem (approximate algorithm to solve it)
- edge and face coloring are similar
- chromatic number - smallest number of colors needed 

Application of Graph Coloring
- making schedule or time table
- sudoku
- mobile radio frequency assignment
- bipartite graphs - if 2-colorable -> bipartite
- map coloring
"""