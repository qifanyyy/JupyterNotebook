from four_color.InductionEngine import InductionEngine
from common.storage import SQLiteGraphStore
from common.multigraph import MultiGraph
from four_color.GraphMerger import GraphMerger
from common.storage import failed_graph_DB
from common.storage import snark_graph_DB
from common.storage import snark_graph_DB_2

import logging
import random
import json
import sys

import settings

random.seed(0)

logging.basicConfig(level=logging.DEBUG)


def readGraph(data):
    n, graph = readVertexData(data)
    edgedata = readEdgeData(graph,n)
    vertices = []
    for i in range(1,n+1):
        vertices.append({"x":0, "y":0, "name":i})
    edges = []
    index = 0
    for a in range(2,n+1):
        for b in range(1,a):
             if edgedata[index] == 1:
                 edges.append({"v1":a,"v2":b,"c1":-1,"c2":-1})
             index += 1
    return (vertices,edges)

    
def readVertexData(data):
    n = ord(data[0])
    if n == 126:
        x,y,z = data[1:3]
        graph = data[4:]
        n = (x-63)<<12 + (y-63)<<6 + z
    else:
        n = n - 63
        graph = data[1:]
    return (n, graph)
    
def readEdgeData(data,n):
    x = n * (n-1)/2
    edgedata = []
    for ch in data:
        if x <=0:
            break
        if x>=6:
            r=6
        else:
            r=x
        x -= r
        for i in range(5,5-r,-1):
            tmp = ord(ch) - 63
            edgedata.append( tmp>>i & 1)
    return edgedata


def read_graph_from_txt(path, graph_name):
# read a graph from a txt file. The 1st line is vertex #, the 2rd is the list of edges
    fin = open(path,'r')
    import ast
    a = fin.readlines()
    number_of_vertices = int(a[0])
    raw_edges = ast.literal_eval(a[1])
    vertices = []
    edges = []
    for index in range(1,number_of_vertices+1):
        vertices.append({"x":0,"y":0,"name":index})
    for each in raw_edges:
        edges.append({"v1":each[0],"v2":each[1],"c1":-1,"c2":-1})
    content = {"vertices":vertices,"edges":edges}
    g = MultiGraph.from_json(json.dumps(content))
    g.name = graph_name
    return g


gl = [18]

for n in gl:
    fin = open('C:/Users/temp-admin/Desktop/ove/data/snarks_graph6/snark{}_cyc4.g6'.format(n),'r')
    stri = fin.readline()
    num = 0
    while stri != "":
        num = num + 1
        print "New Graph: ", num 
        vertices, edges = readGraph(list(stri))
        content = {"vertices":vertices,"edges":edges}
        g = MultiGraph.from_json(json.dumps(content))
        graph_name = "snark{}_cyc4_{}".format(n, num)
        engine = InductionEngine(g)
        engine.edge_coloring()
     
        i = 0
        found = False
        for i in range(0, 10, 1):
            if engine.bicycle_layout():
                found = True
                break
            engine.edge_coloring()
        print "found bicycle"
        engine.find_petersen_subdivision()

        stri = fin.readline()
