import math
import random
import subprocess
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

# AUTHOR: Luis Enrique Neri Pérez
# Copyright 2019

# This is an implementation of Kirkpatrick's Simulated Annealing that solves
# the Traveling Salesman Problem for 100 cities.

global toursGraphs
toursGraphs = []
global timesArr
timesArr = []


def install():
    if 'networkx' not in sys.modules:
        subprocess.call([sys.executable, "-m", "pip", "install", 'networkx'])
    if 'matplotlib' not in sys.modules:
        subprocess.call([sys.executable, "-m", "pip", "install", 'matplotlib'])


def read(file):
    file = open(file, 'r')
    lines = file.readlines()
    tours = []

    for l in lines:
        s1 = l.split(",")
        name = s1[0]

        s2 = s1[1].split("(")
        x = int(s2[1])

        s2 = s1[2].split(")")
        y = int(s2[0])

        tours.append(City(x, y, name))
    return tours


def plotNode(tour, i):
    G = nx.Graph()
    lst = {}

    for n in tour:
        G.add_node(str(n.name))
        lst[n.name] = (n.x, n.y)

    for n in range(0, len(tour) - 1):
        nodo = tour[n]
        G.add_edge(nodo.name, tour[n + 1].name, weight=getDistance(nodo, tour[n + 1]))

    nodo = tour[len(tour) - 1]
    G.add_edge(nodo.name, tour[0].name, weight=getDistance(nodo, tour[n + 1]))

    plt.title("Simulated Annealing - Length: " + str(int(getLength(tour))) + " Temperature: " + str(timesArr[i]))
    nx.draw(G, lst, node_size=40, font_size=8)
    nx.draw_networkx_edges(G, lst)

    plt.draw()
    plt.show()


def plot():
    global toursGraphs
    global timesArr

    i = 0
    for tour in toursGraphs:
        if i % 100 == 0:
            plotNode(tour, i)
            plt.draw()
            plt.pause(0.00000000000000001)
            plt.clf()
        i += 1


class City:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.min = 1000000


class Tour:
    def __init__(self, tourList):
        self.tour = tourList

    def get(self):
        return self.tour

    def set(self, newTour):
        self.tour = newTour


def getNewTour(tour):
    i = random.randint(0, len(tour) - 2)
    j = i
    while (i == j):
        j = random.randint(i, len(tour) - 1)

    newTour = []
    for t in range(0, len(tour)):
        if t <= i or t >= j:
            newTour.append(tour[t])
        else:
            newTour.insert(i, tour[t])
    return newTour


def acceptanceProbability(curr, new, t):
    return math.exp((-new + curr) / t) > random.random()

def getDistance(c1, c2):
    return math.sqrt((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2)


def getLength(tour):
    sum = getDistance(tour[-1], tour[0])
    for i in range(0, len(tour) - 1):
        sum += getDistance(tour[i], tour[i + 1])

    return sum

def openFile(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def getNamesList(tours):
    lista = []
    for i in tours:
        lista.append(i.name)
    output = open("ShortestRoute.txt", "w")
    for i in lista:
        output.write(i +"\n")
    output.close()
    openFile("ShortestRoute.txt")
    return list

def anneal():
    install()
    list = read("Cities.txt")
    currTour = Tour(list)

    plt.ion()

    tMax = 100
    tMin = 0.1
    alpha = 0.99995

    while tMax > tMin:

        tMax *= alpha

        newTour = getNewTour(currTour.tour)

        cGlobal = getLength(currTour.tour)
        nGlobal = getLength(newTour)

        if cGlobal > nGlobal:
            currTour.set(newTour)

        elif cGlobal < nGlobal:
            if acceptanceProbability(cGlobal, nGlobal, tMax):
                currTour.set(newTour)

        toursGraphs.append(currTour.tour)
        timesArr.append(tMax)

    getNamesList(currTour.tour)
    plot()
    return currTour

anneal()