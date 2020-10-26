import matplotlib.pyplot as plt
import json
import argparse

INPUTPATH = "data\\"
OUTPUTPATH = "visualization\\"

def jsonToDict(file):
    data = {}
    with open(INPUTPATH + file, "r") as input:
        data = json.load(input)
    return data

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('f', action='store', type = str, help='Input file name')
    parser.add_argument('o', action='store', type = str, help='Output file name')
    return parser.parse_args()

def main():
    args = parse()
    print("Reading in data from " + args.f + "...")
    data = jsonToDict(args.f)
    print("Data read.")

    print("Parsing X axis...")
    x1 = data["edges"]
    print("Parsing Y axis...")
    y1 = data["dijkstra"]
    y2 = data["bellmanford"]
    y3 = data["yen"]
    y4 = data["fibonacciheap"]
    print("Axes parsed.")

    name = args.o.split(".")[0] + "-all"
    print("Plotting graph...")
    plt.plot(x1, y1, label="Dijkstra", color="b")
    plt.plot(x1, y2, label="Bellman-Ford", color="orange")
    plt.plot(x1, y3, label="FibonacciHeap", color="g")
    plt.plot(x1, y4, label="Yen", color="r")
    print("Graph plotted.")
    plt.legend(loc='best')
    print("Generating graph labels...")
    plt.xlabel("Edges")
    plt.ylabel("Times (ms)")
    plt.title(name.upper())
    print("Labels generated.")

    print("Saving to " + name + ".png...")
    plt.savefig(OUTPUTPATH + name + ".png", bbox_inches="tight")
    print("File saved.")

    plt.close()

    name = args.o.split(".")[0] + "-df"
    print("Plotting graph...")
    plt.plot(x1, y1, label="Dijkstra", color="b")
    plt.plot(x1, y3, label="FibonacciHeap", color="g")
    print("Graph plotted.")
    plt.legend(loc='best')
    print("Generating graph labels...")
    plt.xlabel("Edges")
    plt.ylabel("Times (ms)")
    plt.title(name.upper())
    print("Labels generated.")

    print("Saving to " + name + ".png...")
    plt.savefig(OUTPUTPATH + name + ".png", bbox_inches="tight")
    print("File saved.")

    plt.close()

    name = args.o.split(".")[0] + "-by"
    print("Plotting graph...")
    plt.plot(x1, y2, label="Bellman-Ford", color="orange")
    plt.plot(x1, y4, label="Yen", color="r")
    print("Graph plotted.")
    plt.legend(loc='best')
    print("Generating graph labels...")
    plt.xlabel("Edges")
    plt.ylabel("Times (ms)")
    plt.title(name.upper())
    print("Labels generated.")

    print("Saving to " + name + ".png...")
    plt.savefig(OUTPUTPATH + name + ".png", bbox_inches="tight")
    print("File saved.")

    plt.close()

    name = args.o.split(".")[0] + "-dfy"
    print("Plotting graph...")
    plt.plot(x1, y1, label="Dijkstra", color="b")
    plt.plot(x1, y3, label="FibonacciHeap", color="g")
    plt.plot(x1, y4, label="Yen", color="r")
    print("Graph plotted.")
    plt.legend(loc='best')
    print("Generating graph labels...")
    plt.xlabel("Edges")
    plt.ylabel("Times (ms)")
    plt.title(name.upper())
    print("Labels generated.")

    print("Saving to " + name + ".png...")
    plt.savefig(OUTPUTPATH + name + ".png", bbox_inches="tight")
    print("File saved.")
main()
