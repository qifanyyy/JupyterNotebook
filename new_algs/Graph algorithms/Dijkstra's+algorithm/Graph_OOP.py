class Edge:
    def __init__(self, start, end, weight):
        self.__start = start
        self.__end = end
        self.__weight = weight

    def __str__(self):
        return ", ".join(str(item) for item in self.edge)

    @property
    def edge(self):
        return self.__start.name, self.__end.name, self.__weight

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def weight(self):
        return self.__weight


class Vertex:
    def __init__(self, name):
        self.__name = name
        self.__in_edges = []
        self.__out_edges = []
        self.cost = None
        self.previous_edge = None

    def __str__(self):
        return str(self.properties)

    def add_edge(self, edge):
        if edge.start == self:  # Loops will be recorded as out-edges, but not in-edges
            self.__out_edges.append(edge)
        elif edge.end == self:
            self.__in_edges.append(edge)
        else:  # Edges that do not touch this vertex are invalid
            raise ValueError("Not a valid edge for this vertex.")

    def remove_edge(self, edge):
        if edge.start == self:
            self.__out_edges.remove(edge)
        elif edge.end == self:
            self.__in_edges.remove(edge)
        else:  # Edges that do not touch this vertex are invalid
            raise ValueError("Not a valid edge for this vertex.")

    @property
    def degree(self):
        return len(self.__in_edges) + len(self.__out_edges)

    @property
    def in_edges(self):
        return self.__in_edges

    @property
    def out_edges(self):
        return self.__out_edges

    @property
    def name(self):
        return self.__name

    @property
    def properties(self):
        return self.__name, self.cost


class Graph:
    def __init__(self):
        self.__vertices = []
        self.__vertex_names = dict()

    def __str__(self):
        if self.is_simple():
            return self.adj_mat_string
        else:
            return self.edge_list_string

    def add_vertex(self, name):
        if name not in self.__vertex_names:
            self.__vertices.append(Vertex(name))
            self.__vertex_names[name] = len(self.__vertices) - 1

    def get_vertex(self, name, get_index=False):
        index = self.__vertex_names[name]
        if get_index:
            return self.__vertices[index], index
        else:
            return self.__vertices[index]

    """
    Add edge to the graph.
    Should be given in the form [start_name, end_name, weight].
    """
    def add_edge(self, start, end, weight):
        # Add vertices of edges if not already in graph
        self.add_vertex(start)
        self.add_vertex(end)

        # Construct new edge
        start = self.get_vertex(start)
        end = self.get_vertex(end)
        new_edge = Edge(start, end, weight)

        # Add edges to Vertex class instances
        start.add_edge(new_edge)
        if start != end:  # If the edge is a loop, only add it once
            end.add_edge(new_edge)

    def is_adjacent(self, vertex_one, vertex_two):
        vertex_one = self.get_vertex(vertex_one)
        vertex_two = self.get_vertex(vertex_two)
        for out_edge in vertex_one.out_edges:
            if out_edge.end == vertex_two:
                return True
        for in_edge in vertex_one.in_edges:
            if in_edge.start == vertex_two:
                return True
        return False

    def find_edges(self, start, end, weight=None):
        start = self.get_vertex(start)
        end = self.get_vertex(end)
        target_edge = Edge(start, end, weight)

        if weight is None:
            def same_edge(edge1, edge2): return edge1.end == edge2.end
        else:
            def same_edge(edge1, edge2): return edge1.end == edge2.end and edge1.weight == edge2.weight

        found_edges = []
        for test_edge in start.out_edges:
            if same_edge(test_edge, target_edge):
                found_edges.append(test_edge)
        return found_edges

    def remove_edges(self, start, end, weight=None):
        edges = self.find_edges(start, end, weight)
        for edge in edges:
            edge.start.remove_edge(edge)
            edge.end.remove_edge(edge)

    def remove_vertex(self, vertex_name):
        vertex, index = self.get_vertex(vertex_name, get_index=True)

        # Remove edges from connecting vertices
        for edge in vertex.out_edges:
            edge.end.remove_edge(edge)
        for edge in vertex.in_edges:
            edge.start.remove_edge(edge)

        # delete the vertex
        # TODO: Adjust indices of other vertices after deleted vertex is popped. Write test cases.
        self.__vertices.pop(index)
        del self.__vertex_names[vertex_name]

    def is_simple(self):
        for vertex in self.__vertices:
            for out_index_1 in range(len(vertex.out_edges)):

                # Check for loops
                if vertex.out_edges[out_index_1].end == vertex:
                    return False

                # Check for multiple edges
                for out_index_2 in range(out_index_1 + 1, len(vertex.out_edges)):
                    if vertex.out_edges[out_index_1].end == vertex.out_edges[out_index_2].end:
                        return False
        return True

    def dijkstra_shortest_path(self, start, end):

        def swap_values(in_list, idx1, idx2):
            temp = in_list[idx1]
            in_list[idx1] = in_list[idx2]
            in_list[idx2] = temp

        def sort_single_item(in_list, key=None, sort_index=None):
            # If a key is not given, construct the key to return it's argument.
            if key is None:
                def key(x): return x

            if sort_index is None or sort_index < 0 or sort_index >= len(in_list):
                sort_index = len(in_list) - 1

            while key(in_list[sort_index - 1]) > key(in_list[sort_index]) and sort_index > 0:
                swap_values(in_list, sort_index - 1, sort_index)
                sort_index -= 1

        """
        Explore graph, assign costs to vertices from start to end until path to the end is found.
        """
        def assign_costs(start, end):
            start.cost = 0
            priority_queue = [start]
            while priority_queue[0] != end:
                # Get vertex with the minimum cost
                curr_vertex = priority_queue[0]

                # Calculate costs for adjacent vertices, insert into priority queue in sorted order by cost.
                for out_edge in curr_vertex.out_edges:
                    next_vertex = out_edge.end
                    route_cost = curr_vertex.cost + out_edge.weight
                    sort_index = None

                    # Case where adjacent vertex has not been encountered yet.
                    if next_vertex.cost is None:
                        # calculate cost
                        next_vertex.cost = route_cost
                        next_vertex.previous_edge = out_edge
                        # Add to priority queue, sort by cost
                        priority_queue.append(next_vertex)

                    # Case where adjacent vertex already has a larger cost.
                    elif route_cost < next_vertex.cost:
                        # Update with the smaller cost
                        next_vertex.cost = route_cost
                        next_vertex.previous_edge = out_edge
                        # Update priority queue.
                        # It is guaranteed that next_vertex is in the priority queue. It could not have already been
                        # popped from the priority queue, as it must have a larger cost than curr_vertex.
                        sort_index = priority_queue.index(next_vertex)

                    # Case where adjacent vertex already has a smaller cost.
                    # Don't calculate new cost, don't change priority queue.

                    sort_single_item(priority_queue, key=lambda vertex: vertex.cost, sort_index=sort_index)

                # All costs calculated, remove current vertex from priority queue.
                priority_queue.pop(0)

                # Repeat until the next vertex is the end vertex, so no shorter path to the end can be found

        """
        Finds the shortest path from start to end.
        precondition: Must have already assigned costs to vertices from start to end
        """
        def find_shortest_path(start, end):
            shortest_path_vertices = []
            shortest_path_edges = []
            curr_vertex = end

            # Backtrack until the current vertex is the start vertex.
            while curr_vertex.cost > 0:
                shortest_path_vertices.append(curr_vertex)
                shortest_path_edges.append(curr_vertex.previous_edge)
                curr_vertex = curr_vertex.previous_edge.start

            # Order the shortest path so it goes from start to end.
            shortest_path_vertices.append(start)
            shortest_path_vertices.reverse()
            shortest_path_edges.reverse()

            return shortest_path_vertices, shortest_path_edges

        # TODO: Fix this so it doesn't need to go through every vertex, only the ones seen
        def reset_vertex_data(vertices):
            for vertex in vertices:
                if vertex.cost is not None:
                    vertex.cost = None

        # Get references to start and end vertices.
        start = self.get_vertex(start)
        end = self.get_vertex(end)

        # Find shortest path from start to end.
        reset_vertex_data(self.__vertices)
        assign_costs(start, end)
        path_vertices, path_edges = find_shortest_path(start, end)
        return path_vertices, path_edges, end.cost

    @property
    def adjacency_matrix(self):
        adj_mat = []
        for row_idx in range(len(self.__vertices)):
            adj_mat.append([0] * len(self.__vertices))
        for vertex in self.__vertices:
            row_idx = self.__vertex_names[vertex.name]
            for out_edge in vertex.out_edges:
                col_idx = self.__vertex_names[out_edge.end.name]
                adj_mat[row_idx][col_idx] = out_edge.weight
        return self.vertex_names, adj_mat

    @property
    def adj_mat_string(self):
        name_list, adj_mat = self.adjacency_matrix
        out_string = " ".join([" "] + ["|"] + name_list) + "\n" + "_ "*(len(name_list)+2) + "\n"
        for row_idx in range(len(adj_mat)):
            out_string += " ".join([name_list[row_idx]] + ["|"] + [str(char) for char in adj_mat[row_idx]]) + "\n"
        return out_string

    @property
    def edge_list(self):
        edges = []
        for vertex in self.__vertices:
            for out_edge in vertex.out_edges:
                edges.append(out_edge.edge)
        return edges

    @property
    def edge_list_string(self):
        edges = ""
        for vertex in self.__vertices:
            for out_edge in vertex.out_edges:
                edges += str(out_edge) + "\n"
        return edges

    @property
    def vertex_names(self):
        return list(self.__vertex_names.keys())


######################################################################################################

if __name__ == '__main__':
    G = Graph()
    edge_list = (("A", "B", 3),
                 ("B", "C", 4),
                 ("B", "D", 2),
                 ("A", "D", 20),
                 ("A", "E", 1),
                 ("C", "E", 6),
                 ("D", "E", 5),
                 ("C", "C", 1))  # Add edge list here
    for input_edge in edge_list:
        G.add_edge(*input_edge)
    print(G)
    print(G.adj_mat_string)
    print(G.edge_list_string)
    print("Simple? " + str(G.is_simple()))
