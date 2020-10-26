'''
It is an additional module, not essential. Feel free to ignore this module.
This module is for free designed methods of construct bridgeless cubic graphs.
Feel free to modify or add now methods as long as you know what you are doing.
'''

from four_color.InductionEngine import InductionEngine
from common.storage import SQLiteGraphStore
from common.multigraph import MultiGraph
from four_color.GraphMerger import GraphMerger
from common.storage import failed_graph_DB
from common.storage import snark_graph_DB
from settings import count_utility

import logging
import random
import json
import sys

import settings

random.seed(0)

logging.basicConfig(level=logging.DEBUG)


graph1 = MultiGraph()

for i in range(1, 31, 1):
	graph1.add_vertex(i)
	graph1._positions[i] = (0, 0)

##########
for i in range(1, 15, 1):
	e_id = graph1.add_edge(i, i + 1)
	edge = graph1.get_edge(e_id)
	edge.color = i % 2 + 1

e_id = graph1.add_edge(1, 15)
edge = graph1.get_edge(e_id)
graph1.set_color(e_id, 1, 1)
graph1.set_color(e_id, 15, 2)


for i in range(16, 30, 1):
	e_id = graph1.add_edge(i, i + 1)
	edge = graph1.get_edge(e_id)
	edge.color = i % 2 + 1

e_id = graph1.add_edge(16, 30)
edge = graph1.get_edge(e_id)
graph1.set_color(e_id, 16, 2)
graph1.set_color(e_id, 30, 1)


##############################
elist = []

elist.append(graph1.add_edge(2,17))
elist.append(graph1.add_edge(5,20))
elist.append(graph1.add_edge(8,23))
elist.append(graph1.add_edge(1,15))
elist.append(graph1.add_edge(3,14))
elist.append(graph1.add_edge(4,13))
elist.append(graph1.add_edge(6,12))
elist.append(graph1.add_edge(7,11))
elist.append(graph1.add_edge(9,10))
elist.append(graph1.add_edge(16,30))
elist.append(graph1.add_edge(18,29))
elist.append(graph1.add_edge(19,28))
elist.append(graph1.add_edge(21,27))
elist.append(graph1.add_edge(22,26))
elist.append(graph1.add_edge(24,25))

for x in elist:
	graph1.get_edge(x).color = 3

#failed_graph_DB.add_graph("graph1",graph1.to_json())
engine = InductionEngine(graph1)
if engine.bicycle_algorithm() == False:
        print "haha not resolved"
else:
        print "resolved"

