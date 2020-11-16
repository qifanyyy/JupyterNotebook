from graph import *
try:
    import cPickle as pickle
except:
    import pickle
import random
import argparse
import os

PATH = "graphs\\"

def pickleGraphList(G, f):
    file = open(f, 'ab')
    pickle.dump(G, file)
    file.close()

def genGraph(num, edgeCap, weightMax, weightMin = 1):
    G = Graph(V=[],E=[],directed = True)
    for i in range(0, num):
        G.addVertex(i)

    for i in range(0, len(G.V)):
        if i < len(G.V) - 1:
            u = G.V[i]
            v = G.V[i+1]
        else:
            u = G.V[-1]
            v = G.V[0]
        # print(v.value)
        G.addEdge(u, v, random.randint(weightMin, weightMax))
    for u in G.V:
        for i in range(edgeCap - 1):
            success = False
            while not success:
                v = G.V[random.randint(0,len(G.V)-1)]

                if u == v:
                    continue

                edge = Edge(u,v,random.randint(weightMin, weightMax))
                same = False

                for e in G.getAdj(u):
                    if edge.equals(e):
                        same = True
                        break

                if not same:
                    G.addEdge(edge.u, edge.v, weight = edge.weight)
                    success = True
    return G


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('v', action='store', type = int, help='Number of vertices in the generated graph')
    parser.add_argument('max', action='store', type = int, help='Maximum weight for a given edge')
    parser.add_argument('--min', dest='min', type = int, action='store', default=1, help='Minimum value for a given edge (default = 0)')
    parser.add_argument('f', action='store', type = str, help='File name')
    return parser.parse_args()

def main():
    args = parse()
    # os.remove(PATH + str(args.f))
    print("Generating data set " +  args.f + "...")
    for i in range(1, args.v+1):
        print("Generating graph with edge cap " + str(i) + "...")
        G = genGraph(i, 1, args.max, args.min)
        print("Generation complete.")
        print("Saving to file...")
        pickleGraphList(G, PATH + str(args.f))
        print("File saved.")
        G = None
    print("Data set generated and saved.")


main()
