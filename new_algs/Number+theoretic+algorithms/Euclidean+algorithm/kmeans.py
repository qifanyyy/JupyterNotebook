import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance as d


def printVals(KMap):
    print("Cluster Points")
    for center in range(0, k):
        temp = pd.DataFrame(KMap[KMap.K == center][['x', 'y']])
        print(center, "   ", temp.index.values)


def calcuateSSE(k, KMap, centroids):
    SSElist = []
    for center in range(0, k):
        SSE = 0
        temp = pd.DataFrame(KMap[KMap.K == center][['x', 'y']])
        for index in temp.index.values:
            SSE += d.euclidean(temp.loc[[index]], centroids.loc[[center]]) ** 2
        SSElist.append(SSE)
    print("Value of Sum of Squared Error (SSE): ", sum(SSElist))


def main(k, inputpath, outputpath):
    # inputpath = "C:/Users/ather/Desktop/data.csv"
    # outputpath = "C:/Users/ather/Desktop/results.txt"
    data = pd.read_csv(inputpath, delimiter="\t", index_col='id')

    centroids = pd.DataFrame(np.random.uniform(low=0.3, high=0.9, size=(k, 2)))
    centroids.columns = ['x', 'y']

    plt.scatter(data['x'], data['y'])
    plt.scatter(centroids['x'], centroids['y'], marker="o")
    for loops in range(1, 25):
        i = 0
        kloc = []
        temploc = 0

        # for points in data:
        for j in range(0, 100):
            locdist = []
            loc = 1
            for c in range(0, k):
                reldist = d.euclidean(data.loc[[j]], centroids.loc[[c]])
                locdist.append(reldist)
                if loc > reldist:
                    loc = reldist
                    temploc = i
                i = i + 1
            kloc.append(temploc)
            i = 0

        K = pd.DataFrame({'K': kloc})

        KMap = pd.concat([K, data], axis=1)

        meanlist = pd.DataFrame()

        for i in range(0, k):
            meanlist = meanlist.append(KMap[KMap.K == i][['x', 'y']].mean(0), ignore_index=True)
        meanlist = meanlist.fillna(0.3)
        if meanlist.equals(centroids):
            # print(loops, "Exiting")
            break
        centroids = meanlist

    printVals(KMap)
    calcuateSSE(k, KMap, centroids)
    plt.scatter(centroids['x'], centroids['y'], s=50, marker="x", c='r')

    plt.show()


k = int(sys.argv[1])
inputpath = sys.argv[2]
outputpath = sys.argv[3]
file = open(outputpath, "w+")
sys.stdout = file
main(k, inputpath, outputpath)
file.close()
