import sys
import os
import prettytable
import random

#generate system
def generateSystem():
    global amountOfNodes
    global minAmountOfedged
    global maxAmountOfedged
    global minAmountOfFlow
    global maxAmountOfFlow
    global sourceNode
    global endNode
    global totalAmountOfEdges

    system = []
    i = 0
    while i < amountOfNodes:
        newNode = []
        g = 0
        while g < amountOfNodes:
            newNode.append(0)
            g = g +1
            
        #add edges if not end node
        if i is not endNode:
            amountOfEdges = random.randint(minAmountOfedged,maxAmountOfedged)
            totalAmountOfEdges = totalAmountOfEdges + amountOfEdges
            k=0
            randomPoints = random.sample([x for x in range(amountOfNodes) if x not in [i, sourceNode]],amountOfEdges)
            while k < amountOfEdges:
                pipeValue = random.randint(minAmountOfFlow,maxAmountOfFlow)
                newNode[randomPoints[k]] = pipeValue
                k = k + 1            
        system.append(newNode)
        i = i +1
    return system

#Edmonds-Karp Algorithm
def printPartOne(wave):
    global sourceNode
    global endNode
    global iteration
    file.write("PART 1. Data\n")
    file.write("1.1 System\n")
    
    printSystem()
    
    file.write("1.2 Begin and endnode\n Beginnode = " + str(sourceNode) + " \n Endnode   = " + str(endNode) + "\n\n")
    file.write("Part 2. Trace\n\n")
    file.write("wave " + str(iteration) + " . Current paths:\n")
    file.write("\t 1) " + str1.join(str(v) for v in wave[0]) + ". Continue.")

def printPartThree(maximumFlow):
    global amountOfNodes
    global totalAmountOfEdges

    file.write("\nPART 3. Result\n")
    file.write("3.1 maximum complexity\n")
    file.write("complexity is: O((m*m)*n) where m is total amount of edges and n is amount of vertices/nodes.\n")
    calculatedMaxComplexity = (totalAmountOfEdges*totalAmountOfEdges)*amountOfNodes
    file.write("("+str(totalAmountOfEdges) + "*" + str(totalAmountOfEdges) + ") * " + str(amountOfNodes) + "= " + str(calculatedMaxComplexity) + "\n\n")
    file.write("3.2 Amount of iterations\n")
    file.write("In total there were " + str(countIterations) + " iterations\n\n")
    file.write("3.3 MaximumFlow\n The maximum flows is " + str(maximumFlow)+".\n\n")
    file.write("3.4 FollowedPaths\n")
    i = 0
    while i < len(usedPaths):
        file.write("\t"+str(i)+") " + str1.join(str(v) for v in usedPaths[i]) + ".\n")
        i = i+ 1
    file.write("\n3.5 System after subtractions\n")
    printSystem()

    
def printSystem():
    global nodes
    header = ["Y/X",""]
    for i in range(len(nodes[0])):
        header.append(i)
    table = prettytable.PrettyTable(header)

    for i in range(len(nodes[1])):
        row = [i,""]
        for n in nodes[i]:
            row.append(n)
            
        table.add_row(row)
    file.write(str(table) + "\n")

def getAllAdjecentNodes(indexOfNode):
    global nodes
    allAdjecentNodes = []
    i = 0
    while i < len(nodes):
        node = nodes[i]    
        if(node[indexOfNode]> 0):
            allAdjecentNodes.append(i)
        i = i + 1
    return allAdjecentNodes

def alterNodes(wave):
    global nodes
    global sourceNode
    global usedPaths
    global countIterations

    deletedPaths = []

    g = 0

    while g < len(wave):
        countIterations = countIterations + 1
        index = g +1
        path = wave[g]
        if path[-1] in path[:-1]:
            file.write("\t "+str(index)+") " + str1.join(str(v) for v in path) + ".Error. Loop Found. Delete this path\n")
            deletedPaths.append(path)
        elif path[-1] == sourceNode:
            file.write("\t "+str(index)+") " + str1.join(str(v) for v in path) + ". Endnode Found. Subtract path from system.\n")
            path.reverse()

            #get all values
            i = 0
            values = []
            while i < len(path) -1:
                values.append(nodes[path[i]][path[i+1]])
                i = i +1
            #find bottleneck
            minValue = min(values)

            #change values
            i = 0
            while i < len(path) - 1:
                nodes[path[i]][path[i+1]] = nodes[path[i]][path[i+1]]-minValue
                i = i+1
            
            usedPaths.append(path)
            deletedPaths.append(path)
        else:
            path.reverse()
            i = 0
            values = []
            while i < len(path) -1:
                values.append(nodes[path[i]][path[i+1]])
                i = i +1
            #find out if there is a value set on 0
            minValue = min(values)
            path.reverse()
            if minValue == 0:
                file.write("\t "+str(index)+") " + str1.join(str(v) for v in path) + ".Error. Value of zero in path. subtract path from system.\n")
            else:
                file.write("\t "+str(index)+") " + str1.join(str(v) for v in path) + ". Continue.\n")
        g = g+1

    for path in deletedPaths:
        wave.remove(path)
    return wave


def bfs(wave):
    global nodes
    global iteration
    
    iteration = iteration+1
    newWave = []
    for path in wave:
        lastIndex = path[-1]
        allPossibleMoves = getAllAdjecentNodes(lastIndex)
        for possibleMove in allPossibleMoves:
            addMove = []
            for x in path:
                addMove.append(x)
            addMove.append(possibleMove)
            newWave.append(addMove)
    if len(newWave) > 0:
        file.write("\n\nwave " + str(iteration) + " . Current paths:\n")
        newWave = alterNodes(newWave)
        if len(newWave) > 0:
            bfs(newWave)
        else:
            file.write("\n\n Search finished \n")

"""file name and delete already exsisting data in file"""
fileName = "maxFlowAlgotirhmResult.txt"
file = open(fileName,"a")
file.truncate(0)
    

#variables for generating a system
amountOfNodes = 20 #Must be higher then 2
minAmountOfedged = 2 #Must be higher then 1
maxAmountOfedged = 4 #Must be lower then the maximum amount of nodes
minAmountOfFlow = 100 #Must be higher then 0
maxAmountOfFlow = 105 # must be higher then 0

# choose which node is the sourceNode and end node. 
sourceNode = 1# must be inside the amount of nodes -1 because of list starts a 0
endNode = 2 # must be inside the amount of nodes -1 because of list starts a 0
    
#non-changable variables
totalAmountOfEdges = 0
maximumFlow = 0
leftOverlowAfterAlgorithm = 0
usedPaths = []
wave = [[endNode]]
iteration = 0
str1 = ", "
countIterations = 0


# make a capacity graph
nodes = generateSystem()

for node in nodes:
    maximumFlow = maximumFlow + node[endNode]

#print starting data
printPartOne(wave)
#start algorithm
bfs(wave)


for node in nodes:
    leftOverlowAfterAlgorithm = leftOverlowAfterAlgorithm + node[endNode]
maximumFlow = maximumFlow - leftOverlowAfterAlgorithm

#print results
printPartThree(maximumFlow)

file.close()
os.startfile(r"C:\Users\berend\Documents\Erasmus\algorithm analysis\maxFlowAlgotirhmResult.txt")
