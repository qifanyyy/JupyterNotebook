
class grph:
    def __init__(self):
        self.no_nodes = 0
        self.a = []

    # takes a file path to build the graph from that source file
    def build(self, path):

        file = open(path, "r")
        package = file.readline()
        self.no_nodes = int(package[0])

        self.a = []
        for i in range(self.no_nodes):
            self.a.append([10000] * self.no_nodes)

        for line in file:
            package = line.split(' ')
            source = int(package[0])
            target = int(package[1])
            cost = int(package[2])

            self.a[source][target] = cost

        file.close()


# takes two vertices, the source and the destination of the path
# returns a message and a path, if any
def bellmanFord(graph, start, end):
    infinite = 1000
    distances = [infinite] * graph.no_nodes
    parent = [-1] * graph.no_nodes
    count = [0] * graph.no_nodes

    count[start] = 1
    distances[start] = 0

    # build the distance array and the counter array
    # we'll need the update variable outside the loop too
    update = None
    for it in range(graph.no_nodes):

        update = False
        for source in range(graph.no_nodes):
            for target in range(graph.no_nodes):

                # if the edges exists
                if graph.a[source][target] != infinite:

                    # try to use it to reduce some costs
                    current_distance = distances[target]
                    new_distance = distances[source] + graph.a[source][target]

                    if new_distance < current_distance:
                        distances[target] = new_distance
                        parent[target] = source
                        count[target] = count[source]
                        update = True
                    elif new_distance == current_distance:
                        count[target] += count[source]

            # If we didn't find something new to update, then break this loop and the outer loop
            if not update:
                break

        # also, if the above loop was broken, then it means that we don't have any
        # updates, so break the iteration's loop
        if not update:
            break

    # Check for negative cost cycle: only if the last iteration produced a new update,
    # we may encounter a negative cost cycle - we have to iterate one more time to be sure.
    # Otherwise, if we interrupt the loop before it's over, then there are definitely no
    # negative cost cycles.

    if update:
        for row in range(graph.no_nodes):
            for col in range(graph.no_nodes):
                if graph.a[row][col] != infinite and distances[col] > distances[row] + graph.a[row][col]:
                    return {"message": "negative cost cycle", "path": None,
                            "number of distinct walks of minimum cost": 0}

    # build the path
    path = []
    start_point = start
    end_point = end
    while end_point != start_point and end_point != -1:
        path.append(end_point)
        end_point = parent[end_point]

    # there is no path between these two vertices
    if end_point == -1:
        return {"message": "no negative cost cycles", "path": None,
                "number of distinct walks of minimum cost": 0}

    path.append(start_point)
    return {"message": "no negative cost cycles", "path": path,
            "number of distinct walks of minimum cost": count[end]}


# Topological sort
def tarjan(graph):
    visited = [0] * graph.no_nodes
    path = []

    for i in range(graph.no_nodes):
        if visited[i] == 0:
            if not dfs(graph, visited, path, i):
                return []
    return path[::-1]


# Depth-first search
def dfs(graph, visited, path, start):
    visited[start] = 1
    for i in range(graph.no_nodes):
        if graph.a[start][i] != 10000:
            if visited[i] == 1:
                return False
            elif visited[i] == 0:
                visited[i] = 1
                if not dfs(graph, visited, path, i):
                    return False
    visited[start] = 2
    path.append(start)
    return True


# longest walk
def longest_walk(graph, start, end):
    topological_sort = tarjan(graph)
    costs = [0] * graph.no_nodes

    i = 0
    while i < len(topological_sort) and topological_sort[i] != start:
        i += 1

    while i < len(topological_sort) and topological_sort[i] != end:

        vertex = topological_sort[i]

        for destination in range(graph.no_nodes):

            if graph.a[vertex][destination] != 10000:

                new_cost = costs[vertex]
                new_cost += graph.a[vertex][destination]
                if new_cost > costs[destination]:
                    costs[destination] = new_cost

        i += 1

    return costs[end]


# Floyd-Warshall algorithm
def floyd_warshall(graph, start, end):
    INF = 10000
    costs = graph.a

    for intermediary_node in range(graph.no_nodes):
        for a in range(graph.no_nodes):
            for b in range(graph.no_nodes):
                if costs[a][intermediary_node] != INF and costs[intermediary_node][b] != INF:
                    if costs[a][b] != INF:
                        costs[a][b] = min(costs[a][b], costs[a][intermediary_node] + costs[intermediary_node][b])
                    else:
                        costs[a][b] = costs[a][intermediary_node] + costs[intermediary_node][b]

    return costs[start][end]


class dict_grph:
    def __init__(self):
        self.no_nodes = 0
        self.a = {}

    # takes a file path to build the graph from that source file
    def build(self, path):

        file = open(path, "r")
        package = file.readline()
        self.no_nodes = int(package[0])
        self.a = {}

        for i in range(self.no_nodes + 1):
            self.a[i] = []

        for line in file:
            package = line.split(' ')
            source = int(package[0])
            target = int(package[1])
            cost = int(package[2])

            self.a[source].append((target, cost))

        file.close()


# Dijkstra's algorithm
def dijkstra(graph, start, end):
    infinity = 10000
    visited = [0] * graph.no_nodes
    parent = [-1] * graph.no_nodes
    costs = [infinity] * graph.no_nodes

    costs[start] = 0
    current_node = start

    while current_node != -1:

        visited[current_node] = 1

        min_cost_node = -1
        min_cost_edge = infinity
        for u in graph.a[current_node]:
            dest = u[0]
            edge = u[1]
            if costs[current_node] + edge < costs[dest]:
                parent[dest] = current_node
                costs[dest] = costs[current_node] + edge

            if edge < min_cost_edge and not visited[dest]:
                min_cost_edge = edge
                min_cost_node = dest

        current_node = min_cost_node

    # build the path
    path = []
    start_point = start
    end_point = end
    while end_point != start_point and end_point != -1:
        path.append(end_point)
        end_point = parent[end_point]

    if end_point == -1:
        return [], costs[end]

    path.append(start_point)
    return path, costs[end]

