import copy
import csv
import random
import time
from math import sqrt

from graph_impl.graph import Graph

from gabow_coloring import GabowColoringDFSMatching
from gabow_coloring import GabowColoringSplitMatching
from graph_impl.biprartite import Bipartite
from vizing_coloring import VizingColoring


#@timing
def gabow_split_stuff(graph):
    graph_to_gabow_split = copy.deepcopy(graph)
    gabow_start = time.time()
    gabowColoring = GabowColoringSplitMatching(graph)
    coloring = gabowColoring()
    gabow_end = time.time()
    return gabow_end - gabow_start


#@timing
def gabow_matching_stuff(graph):
    graph_to_gabow_mathcing = copy.deepcopy(graph)
    gabow_start = time.time()
    gabowColoring = GabowColoringDFSMatching(graph)
    coloring = gabowColoring()
    gabow_end = time.time()
    return gabow_end - gabow_start


#@timing
def vizing_stuff(graph):
    graph_to_vizing = copy.deepcopy(graph)
    vizing_start = time.time()
    vizingColoring = VizingColoring(graph)
    coloring = vizingColoring()
    vizing_end = time.time()
    return vizing_end - vizing_start


def perform_comparison(p, n_start, n_end, set_diff_coefficient, attempts_for_constant_n):
    results = []
    n_holder = [n for n in range(n_start, n_end)]
    count = 0
    for n in n_holder:
        for i in range(attempts_for_constant_n):
            set1 = set(range(n))
            set2 = set(range(n + 1, int(n * set_diff_coefficient)))
            used1 = {elem: False for elem in set1}
            used2 = {elem: False for elem in set2}
            edges = []
            degrees = {node: 0 for node in set1.union(set2)}
            for node1 in set1:
                p1 = random.randint(0, 100) / 100
                for node2 in set2:
                    if (random.randint(0, 100) / 100) < p*p1:
                        edges.append((node1, node2))
                        degrees[node1] += 1
                        degrees[node2] += 1
                        used1[node1] = True
                        used2[node2] = True
            degrees_list = [degrees[node] for node in degrees]
            avg_degree = sum(degrees_list) / len(degrees_list)
            simple = Graph(edges=edges)
            max_degree = simple.max_degree('degree')
            bipartite = Bipartite(edges=edges, v_one=set1, v_two=set2)
            # mulgraph = Multigraph(edges=edges, v_one=set1, v_two=set2)
            dev = [(degrees[node] - avg_degree)**2 for node in degrees]
            std = sqrt(sum(dev)/len(degrees_list))
            vizing_time = vizing_stuff(simple)
            split_time = gabow_split_stuff(bipartite)
            # matching_time = gabow_matching_stuff(mulgraph)
            iteration_result = (p, n, int(n*set_diff_coefficient), max_degree, avg_degree, std, len(edges), vizing_time, split_time)
            results.append(iteration_result)
            count+=1
            if count > 10:
                fname = 'output10062.csv'
                with open(fname, 'a', newline='') as f:
                    writer = csv.writer(f)
                    for row in results:
                        writer.writerow(row)
                results = []
                count = 0
                print(str(time.time()) + " " + str(iteration_result))

    return results

# for p in [0.2, 0.4, 0.6, 0.8]:
#     for k in [1.2, 1.5, 2, 3]:
#         perform_comparison(p, 20, 401, k, 3)

# for p in [0.2, 0.4, 0.6, 0.8]:
#     for k in [1.2, 1.5, 2]:
#         perform_comparison(p, int(10/p), int(301/p), k, 1)

# for p in [0.2]:
#     for k in [1.2, 1.5, 2]:
#         perform_comparison(p, 20, 801, k, 1)

for p in [0.4]:
    for k in [1.2, 1.5, 2]:
        perform_comparison(p, 501, 551, k, 1)

for p in [0.6]:
    for k in [1.2, 1.5, 2]:
        perform_comparison(p, 401, 501, k, 1)

for p in [0.8]:
    for k in [1.2, 1.5, 2]:
        perform_comparison(p, 301, 401, k, 1)