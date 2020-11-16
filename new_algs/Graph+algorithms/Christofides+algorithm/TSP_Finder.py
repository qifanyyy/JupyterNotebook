from Graph import Graph
import GraphAlgo
import random
import time 
import pandas as pd;
import copy
import networkx as nx
import matplotlib.pyplot as plt

def main():
    
    print("Enter choice")
    print("1: Read input from file, adjancey matrix (Check example.txt for format)")
    print("2: Generate random amount of vertrices with random coodinates")
    choice = int(input());
    
    if choice == 1:
        print("Root will be the vertex of the first index")
        fileName = input("Enter the name of your file, or enter 0 to see an example file (example.txt) ")
        if fileName == "0":
            fileName = 0

        g = fillGraph(fileName)
        root = "A"

    else:
        n = int(input("Enter number of verteices to test:"))
        g = generate_random(n); 
        root = "1"
        
    startTime = time.time();
    sol = solve(g,root)
    finishTime = time.time(); 
    print("Path Found:")
    printPath(sol[-1])
    print("Cost:" ,sol[1])
    print("Time taken:" ,(finishTime -startTime),"seconds")
    drawGraphSol(g,sol[-1]);
    print("A picture has been draw to file named Path.png, greens edges indicate the path (starting from vertex '1') ")

def solve(g,root):
    sol  = GraphAlgo.Christofides(g,root)
    return sol
    


def fillGraph(fileName = 0):
    if(fileName==0):
        fileName= "example.txt";

    ins = open(fileName, "r" )
    data = []
    for line in ins:
        number_strings = line.split() # Split the line on runs of whitespace
        numbers = [int(n) for n in number_strings] # Convert to integers
        data.append(numbers) # Add the "row" to your list.
    g = Graph()
    finalG = g.toGraph(data);
    return finalG

def drawGraphSol(g,sol):
    print(sol)
    tempNx = nx.Graph()
    tempNx.add_weighted_edges_from(g.edges)

    nxSol = nx.Graph();
    nxSol.add_weighted_edges_from(g.edges)
    
    for u,v,edata in nxSol.edges(data=True):
        edata["color"] = 'r'

    for i in  range(len(sol)-1):
        for u,v,edata in nxSol.edges(data=True):
                if( (sol[i] == v and sol[i+1] == u)  or ( sol[i+1]==v and sol[i] == u) ):
                    edata["color"] = "g";
                    break;
                
    edges = nxSol.edges()
    colors = [nxSol[u][v]['color'] for u,v in edges]
    weights = [nxSol[u][v]['weight'] for u,v in edges]
    pos = nx.circular_layout(nxSol)
    nx.draw(nxSol, pos, edges=edges, edge_color=colors,with_labels = True,edge_labels = weights)
    ## labels = nx.get_edge_attributes(nxSol,'weight')
    ## nx.draw_networkx_edge_labels(nxSol,pos,edge_labels=labels)


    plt.savefig("Path.png")


def generate_random(size):
    randomGraph = Graph()
    for i in range(size):
        x = random.randint(0,10000)
        y = random.randint(0,10000)
        randomGraph.addVertex(str(i+1),x,y)
    
    for v in randomGraph.vertices:
        for i in range(size):
            u = str(i+1)
            if v == u:
                continue
            randomGraph.addEdge(v,u)

    return randomGraph

def test_data(n,dataIndex,df):
    cost = 0;
    timeTaken = 0; 
    sumTimes=0

    numOftimesToAverage = 3;
    curGraph= generate_random(n) 
    for i in range(numOftimesToAverage):  ## test each graph 3 times.... to get the average time 
        graphToTest = copy.deepcopy(curGraph)
        start = time.time()
        sol = solve(graphToTest,"1")    
        end = time.time()-start
        sumTimes += end
    
    timeTaken = sumTimes / numOftimesToAverage
    cost = sol[1]


    df.loc[dataIndex] = [n,int(cost),int(timeTaken*100000)/100.0]; 
    if( (dataIndex+1) % 10 == 0):
        df.to_csv(str(int(time.time()))+"-iteration-"+str(dataIndex)+".txt", index=False) #

def testSetOfVertices(numOfVertrices, incrementEachTime):
    df = pd.DataFrame(columns=["Number of ","Path Cost", "Time Taken(ms)"])
    numOfVertrices = 5; 
    for i in range(100):
        test_data(numOfVertrices,i,df)
        numOfVertrices +=incrementEachTime;

    df.to_csv(str(int(time.time()))+"-iteration-"+".txt", index=False) #

def printPath(pathList):
    s =""
    for i in pathList:
        s+=i+" -> "
    s = s[0:(len(s)-4)];
    print(s)

if __name__ == "__main__":
    main()