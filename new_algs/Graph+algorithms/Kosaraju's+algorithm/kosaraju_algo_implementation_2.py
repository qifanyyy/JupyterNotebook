# Created By Parth Dani
# Date 24/05/2020

from collections import defaultdict

TOTAL_NODES = 0
VERTEX = 0
GRAPH = defaultdict(list)
GRAPH_REVERSED = defaultdict(list)
RESULT_SCC = defaultdict(list)
VISITED = defaultdict(int)
FINISHING_TIME = {}


def depth_first_search(graph, vertex):
    global TOTAL_NODES
    VISITED[vertex] = 1
    RESULT_SCC[VERTEX].append(vertex)
    for j in graph[vertex]:
        if not VISITED[j]:
            depth_first_search(graph, j)


def depth_first_search_util(graph):
    global VERTEX
    VERTEX = 0
    i = len(graph)
    while i > 0:
        if not VISITED[FINISHING_TIME[i]]:
            VERTEX = FINISHING_TIME[i]
            depth_first_search(graph, VERTEX)
        i = i - 1
    VISITED.clear()


def depth_first_search_reverse(graph, vertex):
    global TOTAL_NODES
    VISITED[vertex] = 1
    for j in graph[vertex]:
        if not VISITED[j]:
            depth_first_search_reverse(graph, j)
    TOTAL_NODES = TOTAL_NODES + 1
    FINISHING_TIME[TOTAL_NODES] = vertex


def depth_first_search_util_reverse(graph):
    global TOTAL_NODES
    TOTAL_NODES = 0
    i = len(graph)
    while i > 0:
        if not VISITED[i]:
            depth_first_search_reverse(graph, i)
        i = i - 1
    VISITED.clear()


with open('test_data_implementation_2.txt', 'r') as file:
    for line in file:
        head = int(line.split()[0])
        tail = int(line.split()[1])
        GRAPH[head].append(tail)
        GRAPH_REVERSED[tail].append(head)

depth_first_search_util_reverse(GRAPH_REVERSED)
depth_first_search_util(GRAPH)

for i in RESULT_SCC.values():
    print(i)
