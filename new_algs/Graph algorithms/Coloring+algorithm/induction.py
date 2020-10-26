from common.storage import *
from common.multigraph import MultiGraph
from four_color.GraphMerger import GraphMerger
from four_color.InductionEngine import InductionEngine
from four_color.some_methods import *

import logging
import random
import json
import time
import sys


random.seed()

logging.basicConfig(level=logging.DEBUG)

start = time.time()

fin = open('D:/graphdata/result_{}.txt'.format(12),'r')
#n = 20
#fin = open('C:/Users/temp-admin/Desktop/ove/data/snarks_graph6/snark{}_cyc4.g6'.format(n),'r')

stri = fin.readline()
num = 0

stats = dict()

#results = open('D:/Google Drive/ove/results.txt', 'a')

#results.write("new run:\n")
#results.write(fin.name + "\n")
#rnd = 50
#results.write("rounds: " + str(rnd) + "\n")
#last = 0
#tt = 0
while stri != "":
        num = num + 1
        #if num < last + tt:
        #        continue
        #last = num
        #tt = random.randint(20, 100)
        print "New Graph: ", num 
        vertices, edges = readGraph(list(stri))
        content = {"vertices":vertices,"edges":edges}
        #print json.dumps(content,indent=4)
        #g = MultiGraph.from_json(json.dumps(content))
        g1 = MultiGraph.from_json(json.dumps(content))
        #g2 = MultiGraph.from_json(json.dumps(content))
        #g3 = MultiGraph.from_json(json.dumps(content))
        #(g12, temp) = GraphMerger.single_vertex_merge(g1, g2)
        #(g123, temp) = GraphMerger.single_vertex_merge(g12, g3)
        #graph_name = "snark{}_cyc4_{}".format(n, num)
        engine = InductionEngine(g1)
        engine.add_to_DB()
        #engine.check_critical()
        #stats[num] = engine.stat_test(rnd)
        #engine.test_vertex_edge_merge(5000)
        stri = fin.readline()

'''a, b, c = 0, 0, 0
for temp in stats:
        
        rate, tt = stats[temp]
        if tt != "NA":
                c += 1
                a += rate
                b += tt
print float(a/c), float(b / c)
results.write(repr(stats))
results.write("\n")
'''
end = time.time()
print "running time: ", (end - start) / 60, "minutes\n"
#results.write("running time: " +str( round((end - start) / 60, 2)) + "minutes")
#results.write("\n\n")

#results.close()

