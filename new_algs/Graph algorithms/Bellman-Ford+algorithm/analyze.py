from graph import *
try:
    import cPickle as pickle
except:
    import pickle
import variants
import argparse
import time
import json

INPUTPATH = "graphs\\"
OUTPUTPATH = "data\\"

def readGraphList(f):
    file = open(INPUTPATH + f, 'rb')
    G = pickle.load(file)
    file.close()
    return G

def writeData(data, file):
    with open(OUTPUTPATH+file, "w") as output:
        json.dump(data, output, indent = 4)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('f', action='store', type = str, help='Input file name')
    parser.add_argument('o', action='store', type = str, help='Output file name')
    return parser.parse_args()

def getTimeDijkstra(G):
    avg = 0
    for i in range(0,10):
        start = round(time.clock() * 10000)
        variants.dijkstra(G, G.V[0])
        end = round(time.clock() * 10000)
        avg += (end-start)
    avg = avg / 10
    return avg

def getTimeYen(G):
    avg = 0
    for i in range(0,10):
        start = round(time.clock() * 10000)
        variants.Yen(G, G.V[0])
        end = round(time.clock() * 10000)
        avg += (end-start)
    avg = avg / 10
    return avg

def getTimeFib(G):
    avg = 0
    for i in range(0,10):
        start = round(time.clock() * 10000)
        variants.fibDijkstra(G, G.V[0])
        end = round(time.clock() * 10000)
        avg += (end-start)
    avg = avg / 10
    return avg

def getTimeBellmanFord(G):
    avg = 0
    for i in range(0,10):
        start = round(time.clock() * 10000)
        variants.bellmanFord(G, G.V[0])
        end = round(time.clock() * 10000)
        avg += (end-start)
    avg = avg / 10
    return avg

def main():
    data = {"vertices":0, "dijkstra": [], "bellmanford": [], "fibonacciheap": [], "yen": [], "edges": []}
    args = parse()

    print("Beginning to calculate run times...")

    inputdata = open(str(INPUTPATH + args.f),"rb")
    index = 1
    try:
        while True :
            try:
                print("Loading graph data...")
                G = pickle.load(inputdata)
                print("Loading Complete.")

                data["vertices"] = len(G.V)
                data["edges"].append(len(G.E))

                print("Graph " + str(index) + " out of " + str((int(data["vertices"])-1))+ " info: \n\tDirected: " + str(G.directed) + "\n\tVertex Count: " + str(len(G.V)) + "\n\tEdge Count: " + str(len(G.E)))
                print("Calculating average time for shortest path...")

                avg = getTimeDijkstra(G)
                data["dijkstra"].append(avg)
                print("Dijkstra Run Time: ", data["dijkstra"][-1])

                avg = getTimeFib(G)
                data["fibonacciheap"].append(avg)
                print("Fibonacci Heap Run Time: ", data["fibonacciheap"][-1])

                avg = getTimeBellmanFord(G)
                data["bellmanford"].append(avg)
                print("Bellman-Ford Run Time: ", data["bellmanford"][-1])

                avg = getTimeYen(G)
                data["yen"].append(avg)
                print("Yen Run Time: ", data["yen"][-1])

                G = None
                index+=1
            except EOFError:
                break
    finally:
        inputdata.close()

    print("Finished calculations.")

    print("Writing data to " + args.o + "...")
    writeData(data, args.o)
    print("Data written.")


main()
