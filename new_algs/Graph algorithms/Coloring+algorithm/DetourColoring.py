#DetourColoring.py
#Non-functioning code, see algo.tex for pseudo
import networkx as nx
import numpy as np
import itertools
import sys
import os
from tqdm import *
import DetourMatrix as dm

global edges
edges = dict()

#To generate path edges
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

#To remove nesting on lists
def flatten(listOfLists):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(listOfLists)

def getPaths(d,key):
    dictPath = d[vertexPairs[key]]
    pfun = lambda x : x[0]
    paths = map(pfun,dictPath)
    return paths

def getColors(d,key):
    dictcolors = d[vertexPairs[key]]
    pfun = lambda x : x[1]
    colors = map(pfun,dictcolors)
    return colors

def updateColors(d,key,index,newColors):
    for i in d[key]:
        colorSet = i[index][1]
        colorSet |= newColors

#For debugging
def mapWhat(x):
    print( x)

def updateValues(x):
    getItems = lambda x:x.items()
    newDict = map(getItems,x)
    return newDict


def SearchFunction(y):
    colorsOnY = y["colors"]
    numColors = len(colorsOnY)
    edgesOnY = (x for x in y.keys() if not x=="colors")

    #updateValues = lambda (x,y):x.update(y)
    for a in KPaths:
        for b in KPaths[a]:
            val = {q:y[q] for q in y if q in b}
            #print( val)
            b.update(val)
            #def ReColor:
    #print( KPaths)
    for a in KPaths:
        for b in KPaths[a]:
            #print( b)
            vals = {x for x in b.values() if type(x)==int}
            vals = set(vals) - set([0])
            #print( vals)
            del b["colors"]
            b.update({"colors":vals})
            #print( b)

def updateEdgeAndColors(edge,color,numOfColors):
    for i in KPaths.values():
        print(i)
        for j in i:
            print(edges)
            if edge in j and "colors" in j:
                if color in j["colors"] or edge in edges:
                    print(color)
                    print("that color is already on the path")
                    return False
                FormCol = j["colors"]
                FormCol |= set([color])
                j.update({"colors":FormCol})
                j.update({edge:color})
                return True
            elif not edge in edges and numOfColors < k:
                print("this edge needs a new color")
                newColors=CK-set(edges.values())
                j.update({edge:list(newColors)[0]})
                return True
                #FormCol = j["colors"]
                #FormCol |= set([color])
                #j.update({"colors":FormCol})
                #j.update({edge:color})
                #return True
                #print j
                
def removeEdges(dic):
    Keys = set(KPaths.keys())
    ComKeys = set(dic.keys())
    Values = KPaths.values()
    ComValues = set(dic.values())
    
def IterateColors():
    firstPath = KPaths.values()[0][0]
    print("")
    print("the paths")
    for i in KPaths.values()[0]:
        print(i)
    print("")
    print("looking at vertex pair:")
    print( KPaths.keys()[0])
    print( "")
    pathcolors = firstPath["colors"]
    print( "colors on the path")
    if len(pathcolors)>=k:
        print( "k colors already between these vertices")
        return
    print( pathcolors)
    print( "")
    del firstPath["colors"]
    global inc
    
    for i in firstPath:
        inc = 0
        print( "")
        print( "We're looking at edge:")
        print( i)
        print( "")
        colorset = CK
#        print( list(CK-pathcolors))
        consideredcolor = list(
            CK-pathcolors
        )[0]
        while not updateEdgeAndColors(i,consideredcolor,len(pathcolors)):
            print( "entering the loop")
            print( list(colorset-pathcolors))
            print( inc)
            #print( pathcolors)
            consideredcolor = list(
                colorset-pathcolors
            )[inc]
            inc += 1
        for j in KPaths.values():
            for h in j:
                print( h)
                if "colors" in h and i in h:
                    if not consideredcolor in h["colors"]:
                        print( "the considered color")
                        print( consideredcolor)
                        print( "updating colors")
                        h.update({i:consideredcolor})
                        h.update({"colors":h["colors"] | set([consideredcolor])})
                        edges.update({i:h[i]})
                        del h[i]
                    else:
                        #updateEdgeAndColors(i,consideredcolor,inc)
                        """
                        print( "the considered color")
                        print( consideredcolor)
                        print( "updating colors")
                        h.update({i:consideredcolor})
                        h.update({"colors":h["colors"] | set([consideredcolor])})
                        edges.update({i:h[i]})
                        del h[i]
                        #print( h)
                        """
        firstPath.update({i:consideredcolor})
        inc += 1
        pathcolors |= set([consideredcolor])
    
    firstPath.update(
        {"colors":pathcolors}
    )
    

    
def main():
    g = nx.cycle_graph(5)
    nodes = g.nodes()
    global vertexPairs
    #print((g.edges()))
    vertexPairs = list(
        itertools.combinations(
            nodes,
            2
        )
    )

    print( vertexPairs)
    
    global k
    k,P = dm.detour_matrix(g)
    global CK
    CK = set(
        range(
            1,
            2*k
        )
    )
    #print( 2*k-1)

    #generates edges as well as a color set
    dictMap = lambda y : [
        list(map(tuple,map(sorted,pairwise(y))))
    ]
    
    P_K = {
        x:map(dictMap,
              filter(
                  lambda i:len(i)-1 >= k,y)
        ) for x,y in P.iteritems()
    }
    
    #for i in P_K.values():
    #    print( i)
    #KPaths refers to the paths without k colors later on
    global KPaths
    KPaths = {x:map(
        dictMap,
        filter(
            lambda i:len(i)-1 == k,y
        )
    ) for x,y in P.iteritems()}

    KPaths = {x:y for x,y in KPaths.iteritems() if len(y)!=0}

    def colorMapping(y):
        newDict = dict()
        newList = list()
        for a in y:
            #print( a)
            for b in a:
                #print( b)
                newList.append(
                    dict(
                        zip(
                            a[0],
                            itertools.repeat(0,k)
                        )
                    )
                )
        return newList

    overVal = lambda x: KPaths[x]
    KPaths.update(
        dict(
            zip(
                KPaths.keys(),
                map(
                    colorMapping,
                    map(KPaths.get,KPaths.keys())
                )
            )
        )
    )

    global KPathsIte
    KPathsIte = KPaths.keys()
    global setOfPaths
    setOfPaths = KPaths.values()

    global firstpath
    
    firstpath = dict(zip(setOfPaths[0][0].keys(),range(1,k+1)))
    KPaths[KPathsIte[0]][0].update(firstpath)
    getValues = lambda x: {"colors":set(x.values())}    
    nonZeroDict = [q for q in setOfPaths if not 0 in map(getValues,q)]
    colorSet = [
        map(getValues,q)
        for q in setOfPaths
        for p in q
        if not 0 in getValues(p)]
    global UsedColors
    UsedColors = len(range(1,k+1))
    global conP
    conP = 1
    def consideredPaths(path):
        #print( setOfPaths)
        edges.update(path)
        KPathsIte = KPaths.keys()
        setOfPaths = KPaths.values()
        if "colors" in path:
            pathColors = path["colors"]
        else:
            pathColors = 0
        pathTup = {x
                   for x in path
                   if path[x]==0
        }
        if pathColors < k and pathColors > 0:
            firstpath = dict(
                zip(
                    [x for x in setOfPaths[0][0].keys() if not x == "colors"],
                    list(
                        sorted(
                            CK - path["colors"]
                        )
                    )[1:len(pathTup)]
                )
            )
            firstpath.update({"colors":setOfPaths[0][0]["colors"]})
            #print( firstpath)
            KPaths[KPathsIte[0]][0].update(firstpath)
        else:
            firstpath = dict(
                zip(
                    setOfPaths[0][0].keys(),
                    list(range(1,k+1))
                )
            )
        #print( KPaths)
        if conP:
           global conP
           conP = 0
           if "colors" not in path:
                path.update({"colors":set()})
                nonZeroDict = [q for q in setOfPaths if not 0 in map(getValues,q)]
                colorSet = [
                    map(
                        getValues,
                        q
                    ) for q in setOfPaths for p in q if not 0 in getValues(p)]
                #print( nonZeroDict)
                #print( colorSet)
                for i in range(len(nonZeroDict)):
                    for j in range(len(nonZeroDict[i])):
                        nonZeroDict[i][j].update(colorSet[i][j])
            #print( KPaths)
            #print( nonZeroDict)
            #print( colorSet)
                updatedDict = dict(
                    zip(
                            KPaths.keys(),
                            nonZeroDict
                        )
                    )
               #print( updatedDict)
                KPaths.update(updatedDict)
                for a in KPaths:
                    for b in KPaths[a]:
                        #print( b)
                        if b.get("colors") == None:
                            b.update({"colors":set()})
                        elif b.get("colors") == set([0]):
                            b.update({"colors":set()})
                        else:
                            continue
            #KPaths.update({KPaths.keys()[0]:path})
        #print( KPaths[KPaths.keys()[0]][0])
        #print( path["colors"])
        #if not conP:
            #print( KPaths)
        
        SearchFunction(path)

    #print( updatedDict)

    consideredPaths(firstpath)
    #print( KPaths)
    #SearchFunction(firstpath)
    #print( KPaths)
    
    #Initialization
    global VerticesWithkColors
    VerticesWithkColors = dict([])
    
    def UpdateVertices():
        VerticesWithkColors.update({KPathsIte[0]:KPaths[KPathsIte[0]]})
        del KPaths[KPathsIte[0]]
        KPathsIte.pop(0)
        
    #UpdateVertices()
    def filterByNoColors():
        for x in KPaths:
            for b in KPaths[x]:
                bCol = b["colors"]
                bNew =  {p:0 for p in b if b[p] == 0}
                #print( bNew)
                b.clear()
                b.update({"colors":bCol})
                b.update(bNew)

                
    filterByNoColors()
    for i in KPaths:
        print( i)
    print( "")
    print( "The edges with colors")
    print( "")
    print( edges)
    print( "")
    while KPaths:
        IterateColors()
      #  print( VerticesWithkColors)
        UpdateVertices()
    print( "")
    print( "The vertices with k colors")
    print( "")
    for i in VerticesWithkColors:
        print( i)
        print( VerticesWithkColors[i])
    #print( KPaths)
    finalEdgeColors = dict([])
    for i in VerticesWithkColors:
        for j in range(len(VerticesWithkColors[i])):
            finalEdgeColors.update(VerticesWithkColors[i][j])

    #print( finalEdgeColors)
    print( "")
    print( edges)
if __name__ == "__main__":
    main()
