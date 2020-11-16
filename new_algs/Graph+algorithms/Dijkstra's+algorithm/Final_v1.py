

class Building:

    def __init__(self, name):
        self.name = name


class TransportNetwork:
    def __init__(self, graph):
        self.graph = graph

    """
    Finds smallest path from connecting paths
    @param total_costs: dictionary of towns and their current distances from destination
    @param visited: list of Building objects already visited
    return node: next smallest path from connecting paths
    """
    def find_smallest_path(self, total_costs, visited):
        min_dist = None
        next_node = None
        for key in total_costs:  # searches through total_costs to find smallest int stored
            if key not in visited:
                if min_dist is None:
                    min_dist = total_costs.get(key)
                    next_node = key
                else:
                    if total_costs.get(key) is not None:
                        if total_costs.get(key) < min_dist:
                            min_dist = total_costs.get(key)
                            next_node = key
        return next_node

    """
    Runs Dijsktra's Algorithm to find shortest path to the destination from all Buildings
    @param destination: dictionary of towns and their current distances from destination
    return total_costs: dictionary of total distance from Building to Destination
    return prev_nodes: dictionary of Buildings in the path to get to the destination
    """
    def dijkstra(self, destination):

        total_costs = {}  # will contain total distance of each node from destination
        prev_nodes = {}  # will contain previous nodes for each node to get to destination
        queue = []  # next nodes to go through
        visited = []  # nodes already visited

        visited.append(destination)
        total_costs.update({destination: 0})
        prev_nodes.update({destination: None})

        for key in self.graph:  # Sets every distance besides Destination to None and previous nodes to None
            if key is not destination:
                total_costs.update({key: None})
                prev_nodes.update({key: None})

        for pair in self.graph.get(destination):  # assigns distance to Destination's connecting buildings
            total_costs[pair[0]] = pair[1]
            prev_nodes[pair[0]] = destination

        next_node = self.find_smallest_path(total_costs, visited)

        queue.append(next_node)

        while visited.__len__() != self.graph.__len__():
            current_node = queue[0]
            # Relaxation
            for pair in self.graph.get(current_node):  # assigns distance to directly connecting buildings
                if pair[0] not in visited:
                    if total_costs[pair[0]] is None:
                        total_costs[pair[0]] = total_costs[current_node] + pair[1]  # Adds distance if distance is None
                        prev_nodes[pair[0]] = current_node
                    elif total_costs[current_node] + pair[1] < total_costs[pair[0]]:
                        total_costs[pair[0]] = total_costs[current_node] + pair[1]  # Adds distance if distance is less
                        prev_nodes[pair[0]] = current_node

            visited.append(current_node)
            queue.remove(current_node)
            queue.append(self.find_smallest_path(total_costs, visited))

        return total_costs, prev_nodes

    """
    Finds path from one Building to Another calling Dijkstra and returns list of path and total distance
    @param start: town to start from
    @param destination: town to get to
    return distance: shortest distance from start to destination 
    return path: list of Buildings in the path
    """
    def path_from_to(self, start, destination):
        total_costs, prev_nodes = self.dijkstra(destination)
        current = start
        path = []
        distance = total_costs[start]

        path.append(start)  # Creates the path list from prev_nodes dictionary
        while current != destination:
            path.append(prev_nodes[current])
            current = prev_nodes[current]

        return distance, path

    """
    Returns path in string form
    @param path: list of each Building in the path
    return path_str: list changed into a string
    """
    def return_path(self, path):
        path_str = ""
        for i in range(0, len(path)):
            path_str += path[i].name + " - "

        return path_str
