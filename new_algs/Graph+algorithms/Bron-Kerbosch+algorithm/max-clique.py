from graph_generator import read_graph, random_graph
from writer import write_results
import time
import sys

filename = "data/" + sys.argv[1]
vertices = 5
random = False

if len(sys.argv) >= 3:
    vertices = int(sys.argv[2])
    random = sys.argv[3].lower() == 'true'


def get_edge_count(graph):
    edges = 0
    for node in graph:
        edges += len(node.neighbors)
    return edges / vertices


def check_if_clique(clique):
    i = 1
    for node in clique:
        if i != len(clique):
            if clique[i] in node.neighbors:
                i += 1
                continue
            else:
                return False
    return True


all_cliques = []


#       poaibiai          P                    R              X
def find_cliques(potential_clique=[], remaining_nodes=[], skip_nodes=[], depth=0):
    if len(remaining_nodes) == 0 and len(skip_nodes) == 0:
        all_cliques.append(potential_clique)
        return 1

    cliques_found = 0
    for node in remaining_nodes:
        new_potential_clique = potential_clique + [node]
        new_remaining_nodes = [n for n in remaining_nodes if n in node.neighbors]
        new_skip_list = [n for n in skip_nodes if n in node.neighbors]
        cliques_found += find_cliques(new_potential_clique, new_remaining_nodes, new_skip_list, depth + 1)

        remaining_nodes.remove(node)
        skip_nodes.append(node)
    return cliques_found


def measure_algorithm():
    took_times = []
    avg_edges = []
    for i in range(int(sys.argv[4])):
        nodes = random_graph(vertices)
        print('Searching for max clique of graph with ' + str(vertices) + ' vertices')
        start = time.time()
        cliques_count = find_cliques(remaining_nodes=nodes[:])
        end = time.time()

        took_times.append(end - start)
        avg_edges.append(get_edge_count(nodes))
        print(str(i) + ': Finding clique with ' + str(vertices) + ' vertices took ' + str(end - start) + ' seconds')

    return [sum(took_times) / len(took_times), int(sum(avg_edges) / len(avg_edges)), cliques_count]


all_nodes = []
if len(sys.argv) == 5:
    [avg_runtime, edges, cliques] = measure_algorithm()
    write_results([str(vertices), str(round(avg_runtime, 2)), str(edges), str(cliques)])
    print()
else:
    if random:
        all_nodes = random_graph(vertices)
    else:
        all_nodes = read_graph(filename)
    find_cliques(remaining_nodes=all_nodes[:])
    print(all_cliques)
