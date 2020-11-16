
"""Python Breadth-First Search implementation. It can check if a graph is connected.
It can also count distance between points. It's modified to take advantage of
adjacency list format, which is used on couple other occasions.
Usage examples:

>>> G = adl('cities.txt')
>>> bfs(G, 'Chicago')
Connected graph. Total points: 15. BFS explored: 15

>>> G = adl('cities.txt', bonus_key='dist')
>>> print(bfs(G, 'Chicago', 'Paris', pre_explored=['dist'], dist='dist'))
('Chicago', 'Paris', 5)

>>> G = adl('cities.txt', bonus_key='dist')
>>> print(bfs(G, 'Warsaw', 'Tokyo', pre_explored=['dist'], dist='dist'))
('Warsaw', 'Tokyo', 2)

>>> G = adl('cities.txt', bonus_key='dist')
>>> print(bfs(G, 'Warsaw', 'Tokyo', pre_explored=['dist', 'Rome'], dist='dist'))
('Warsaw', 'Tokyo', 4)
"""

from collections import deque
from adjacency_list import adl


def bfs(graph, start_node, end_node=None, pre_explored=(), dist=''):
    """Breadth-First Search. Counts node distance between start_node and end_node.
    Takes adjacency list representation of a graph in form of a dictionary of
    nested dictionaries. Key name for holding a distance can be set in dist parameter
    and is expected to be present in a graph. Some points can be ignored if specified
    in pre_explored parameter.
    """
    Q = deque([start_node])
    explored = {start_node}.union(set(pre_explored))
    while Q:
        v = Q.popleft()
        for u in graph[v]:
            if u not in explored:
                explored.add(u)
                Q.append(u)
                if dist:
                    graph[u][dist] = graph[v][dist] + 1
        if end_node and end_node == v and dist:
            return start_node, v, graph[v][dist]

    explored = explored.difference(pre_explored)
    if len(explored) < len(graph):
        print('Disconnected graph. Total points: {}. BFS explored: {}'
              .format(len(graph), len(explored)))
    else:
        print('Connected graph. Total points: {}. BFS explored: {}'
              .format(len(graph), len(explored)))

    return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
