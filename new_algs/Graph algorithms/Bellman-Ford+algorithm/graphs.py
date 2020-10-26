class Graph:
    """Adjacency-list representation of a graph"""
    def __init__(self, vertex_number):
        self.__adjacencies = [{} for _ in range(vertex_number)]

    def add_edge(self, a, b, length=1, undirected=True):
        self.__adjacencies[a][b] = length
        if undirected:
            self.__adjacencies[b][a] = length

    def adjacencies(self, vertex, with_length=False):
        return self.__adjacencies[vertex].items() if with_length else self.__adjacencies[vertex].keys()

    def get_vertex_number(self):
        return len(self.__adjacencies)


def has_path_to(graph, start_vertex, target_vertex):
    """Depth-First Search (DFS)"""
    def nested(current_vertex, explored):
        explored[current_vertex] = True
        if current_vertex == target_vertex:
            return True
        for adj_vertex in graph.adjacencies(current_vertex):
            if not explored[adj_vertex] and nested(adj_vertex, explored):
                return True
        return False
    return nested(start_vertex, [False] * graph.get_vertex_number())


def _get_path(vertex, predecessors):
        if vertex is None:
            return []
        path = _get_path(predecessors[vertex], predecessors)
        path.append(vertex)
        return path


def get_bfs_shortest_path_to(graph, start_vertex, target_vertex):
    """Breadth-First Search (BFS)"""
    from linkedlist import Queue

    predecessors = [None] * graph.get_vertex_number()  # previous vertex on the path

    to_explore = Queue()
    to_explore.enqueue(start_vertex)

    explored = [False] * graph.get_vertex_number()
    explored[start_vertex] = True

    while to_explore:
        current_vertex = to_explore.dequeue()
        for adj_vertex in graph.adjacencies(current_vertex):
            if not explored[adj_vertex]:
                predecessors[adj_vertex] = current_vertex
                if adj_vertex == target_vertex:
                    return _get_path(target_vertex, predecessors)
                explored[adj_vertex] = True
                to_explore.enqueue(adj_vertex)


def get_bellman_ford_shortest_path_to(graph, start_vertex, target_vertex):
    """Bellman-Ford shortest-path algorithm
    It is assumed that there are no negative cycles in the graph"""
    def relax(a, b, l):
        """Relax an edge from vertex a to vertex b of length l"""
        distance_through_edge = dist_to[a] + l
        if distance_through_edge < dist_to[b]:
            dist_to[b] = distance_through_edge
            predecessors[b] = a
            if not on_queue[b]:
                on_queue[b] = True
                to_explore.enqueue(b)

    import sys
    from linkedlist import Queue

    dist_to = [sys.maxsize] * graph.get_vertex_number()
    dist_to[start_vertex] = 0
    predecessors = [None] * graph.get_vertex_number()  # previous vertex on the path

    to_explore = Queue()
    to_explore.enqueue(start_vertex)
    on_queue = [False] * graph.get_vertex_number()
    on_queue[start_vertex] = True

    while to_explore:
        current_vertex = to_explore.dequeue()
        on_queue[current_vertex] = False
        for adj_vertex, edge_length in graph.adjacencies(current_vertex, True):
            relax(current_vertex, adj_vertex, edge_length)

    return _get_path(target_vertex, predecessors), dist_to[target_vertex]


def get_dijkstra_shortest_path_to(graph, start_vertex, target_vertex):
    """Dijkstra's shortest-path algorithm
    All edges are assumed to be non-negative"""
    def relax(a, b, l):
        """Relax an edge from vertex a to vertex b of length l"""
        distance_through_edge = dist_to[a] + l
        if distance_through_edge < dist_to[b]:
            dist_to[b] = distance_through_edge
            predecessors[b] = a
            if to_explore.get_key(b) is not None:
                to_explore.decrease_key(distance_through_edge, b)
            else:
                to_explore.push(distance_through_edge, b)

    import sys
    from heap import Heap

    dist_to = [sys.maxsize] * graph.get_vertex_number()
    dist_to[start_vertex] = 0
    predecessors = [None] * graph.get_vertex_number()  # previous vertex on the path

    to_explore = Heap()
    to_explore.push(0, start_vertex)

    while to_explore.size() > 0:
        _, current_vertex = to_explore.pop()
        for adj_vertex, edge_length in graph.adjacencies(current_vertex, True):
            relax(current_vertex, adj_vertex, edge_length)

    return _get_path(target_vertex, predecessors), dist_to[target_vertex]


def build_mst(graph):
    """Prim's MST algorithm; eager implementation
    Returns a set of MST edges"""
    from heap import Heap

    mst_edges = []
    mst_vertices = []
    predecessors = [None] * graph.get_vertex_number()  # previous vertex in the tree

    start_vertex = 0  # does not matter where we start building MST
    to_explore = Heap()  # values are vertex ids; keys are distances from the tree to the vertices
    to_explore.push(0, start_vertex)

    while to_explore.size() > 0:
        _, current_vertex = to_explore.pop()
        mst_vertices.append(current_vertex)
        if predecessors[current_vertex] is not None:
            mst_edges.append((predecessors[current_vertex], current_vertex) if predecessors[current_vertex] < current_vertex else (current_vertex, predecessors[current_vertex]))
        for adj_vertex, edge_length in graph.adjacencies(current_vertex, True):
            if adj_vertex in mst_vertices:
                continue
            adj_length = to_explore.get_key(adj_vertex)
            if adj_length is None:
                to_explore.push(edge_length, adj_vertex)
                predecessors[adj_vertex] = current_vertex
            elif edge_length < adj_length:
                to_explore.decrease_key(edge_length, adj_vertex)
                predecessors[adj_vertex] = current_vertex

    return set(mst_edges)
