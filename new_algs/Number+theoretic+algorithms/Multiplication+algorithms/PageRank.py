# AUTHOR: Luis Enrique Neri Pérez
# AUTHOR: Gerardo Arturo Valderrama Quiróz
# Copyright 2019

# This is an implementation of Google's Googles Algorithm to get
# the most relevant nodes.

rep = 0
outlinks = {}
inlinks = {}
pagerank = {}
Prev = {}
rank = {}


def inputProcessing():
    print("Paste the nodes with the following format (V1,E1), ... , (Vn,En):")
    print("EJ. (1,2), (1,3), (3,1), (3,2), (3,5), (4,5), (4,6), (5,4), (5,6), (6,4)\n")
    links = input("Nodes: ")

    global rep
    rep = int(input("How many times the algorithm will be repeated?: "))
    saving = False
    for i in range(0, len(links) - 1):
        if (links[i] == '('):
            saving = True;
            continue
        elif (links[i] == ')'):
            saving = False
            continue
        elif (saving):
            pair = links[i:i + 3]
            if (int(pair[0]) not in outlinks.keys()):
                lista = []
                lista.append(int(pair[2]))
                outlinks[int(pair[0])] = lista
            else:
                key = int(pair[0])
                listaAct = outlinks.get(key)
                listaAct.append(int(pair[2]))
                outlinks.update({int(pair[0]): listaAct})
            if (int(pair[2]) not in inlinks.keys()):
                lista = []
                lista.append(int(pair[0]))
                inlinks[int(pair[2])] = lista
            else:
                key = int(pair[2])
                listaAct = inlinks.get(key)
                listaAct.append(int(pair[0]))
                inlinks.update({int(pair[2]): listaAct})
            saving = False
        else:
            continue

    keys = inlinks.keys()
    for key in keys:
        pagerank[key] = 1 / len(keys)


def copyPrevPageRank():
    keysP = inlinks.keys()
    for keyP in keysP:
        prevValue = pagerank[keyP]
        Prev[keyP] = prevValue


def PageRankFormula(currNode):
    parts = inlinks[currNode]
    pr = 0
    for value in parts:
        pr += Prev[value] / len(outlinks[value])
    pagerank[currNode] = pr


def PageRank():
    global pagerank, Prev, outlinks, inlinks, rep
    rep = 0
    outlinks = {}
    inlinks = {}
    pagerank = {}
    Prev = {}
    inputProcessing()
    print("\nTABLE\n")
    print("ROUND 0")
    print(pagerank)
    copyPrevPageRank()
    for i in range(1, rep + 1):
        for node in pagerank.keys():
            PageRankFormula(node)
        print("ROUND " + str(i))
        print(pagerank)
        copyPrevPageRank()
    createRanking()
    printRanking()


def createRanking():
    global rank
    rank = {}
    prValues = []
    for key in pagerank.keys():
        prValues.append(pagerank[key])
    prValues.sort()
    prValues.reverse()
    for prValue in prValues:
        for key in pagerank.keys():
            if prValue == pagerank[key]:
                if prValue not in rank:
                    lista = []
                    lista.append(key)
                    rank[prValue] = lista
                    continue
                else:
                    listaAct = rank.get(prValue)
                    if key not in listaAct:
                        listaAct.append(key)
                        listaAct.sort()
                        outlinks.update({prValue: listaAct})
            else:
                continue


def printRanking():
    print("\nPAGE  RANKING\n")
    keys = rank.keys()
    place = 1
    for key in keys:
        for value in rank[key]:
            print("#" + str(place) + ": Node " + str(value))
        place += 1


def main():
    print("\nPAGE RANK\n")
    PageRank()

    repeat = input("\nDo you want to restart the program?[y/n]")
    if repeat == "y":
        main()
    else:
        print("Thanks for using our program!!")


main()
