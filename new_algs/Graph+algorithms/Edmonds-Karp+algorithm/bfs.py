# my implementation of BFS version
def find_path(self, source, sink, path):
    queue = [(source, path)]
    while queue:
        (source, path) = queue.pop(0)
        for edge in self.get_edges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and edge not in path and edge.redge not in path:
                if edge.sink == sink:
                    return path + [edge]
                else:
                    queue.append((edge.sink, path + [edge]))
