
import numpy, random, tempfile, subprocess, shlex, heapq
from operator import itemgetter


class MatrixGraph:
    def __init__(self, matrix):
        self.matrix = matrix
        self.tree_edges = []

    def create_priority_queue(self, root):
        self.tree = []
        priority_queue = []
        priority_queue = self.update_priority_queue(priority_queue, root, None)
        self.total_cost = 0
        return priority_queue

    def create_heapqueue(self, root):
        heapqueue = []
        self.total_cost = 0
        self.tree = [root]
        self.tree_edges = []
        for neighbor, cost in self.get_neighbors(root):
     #   cost should be the first item in heapqueue because queue is sorted by the first item
            heapq.heappush(heapqueue, (cost, root, neighbor))
        return heapqueue

    def create_edges(self):
        self.colors = {}
        edges = []
        self.tree_edges = []
        self.total_cost = 0
        for node in xrange(len(self.matrix)):
            self.colors[node] = node

        for (node_1, node_2), cost in numpy.ndenumerate(self.matrix):
            if node_1 < node_2 and cost:
                edges.append((node_1, node_2, cost))
        edges = sorted(edges, key=itemgetter(2))
        return edges

    def display(self, filename):
        with tempfile.NamedTemporaryFile(delete=False) as tmpf:
            tmpf.write("graph Prim{\n node [fontname=\"Arial\"];\n")
            for node in xrange(len(self.matrix)):
                tmpf.write("node%d [label=\"%d\" style=filled fillcolor=white];\n" % (node, node))
            for (node_1, node_2, cost) in self.tree_edges:
                tmpf.write("node%d--node%d [label=\"%d\"];\n" % (node_1, node_2, cost))
            tmpf.write("}")

        cmd = "dot -Tpng -o %s %s" % (filename, tmpf.name)
        args = shlex.split(cmd)
        subprocess.Popen(args)
        return

    def get_neighbors(self, node):
        for n in range(len(self.matrix)):
            if n < node and self.matrix[n][node]:
                yield n, self.matrix[n][node]
            elif n > node and self.matrix[node][n]:
                yield n, self.matrix[node][n]

    def update_priority_queue(self, priority_queue, new_node, new_edge):
        for neighbor, cost in self.get_neighbors(new_node):
            if neighbor in self.tree:
                priority_queue.remove((min(new_node, neighbor), max(new_node, neighbor), cost))
            else:
                priority_queue.append((min(new_node, neighbor), max(new_node, neighbor), cost))

        if new_edge:
            self.tree_edges.append(new_edge)
            self.total_cost += new_edge[2]
        self.tree.append(new_node)
        return priority_queue

    def prim(self):
        priority_queue = self.create_priority_queue(0)
        while priority_queue:
            min_cost = -1
            min_edge = None
            for (node_1, node_2, cost) in priority_queue:
                if min_cost==-1 or min_cost>cost:
                    min_cost = cost
                    min_edge = (node_1, node_2, cost)
            new_node = min_edge[0] if min_edge[1] in self.tree else min_edge[1]
            self.update_priority_queue(priority_queue, new_node, min_edge)
        return self.total_cost

    def prim_with_heapqueue(self):
        heapqueue = self.create_heapqueue(0)
        while heapqueue:
            new_edge = heapq.heappop(heapqueue)
            (cost, node_1, node_2) = new_edge
            if (node_1 in self.tree and node_2 not in self.tree) or (node_2 in self.tree and node_1 not in self.tree):
                new_node = node_1 if node_2 in self.tree else node_2
                for new_neighbor, new_cost in self.get_neighbors(new_node):
                    if new_neighbor not in self.tree:
                        heapq.heappush(heapqueue, (new_cost, new_node, new_neighbor))
                self.tree.append(new_node)
                self.tree_edges.append((node_1, node_2, cost))
                self.total_cost += cost
        return self.total_cost

    def kruskal(self):
        edges = self.create_edges()
        while edges:
            (node_1, node_2, cost) = edges.pop(0)
            if not (self.colors[node_1]== self.colors[node_2]):
                node_color_1 = self.colors[node_1]
                node_color_2 = self.colors[node_2]
                new_color = min(node_color_1, node_color_2)
                for node in xrange(len(self.matrix)):
                    if self.colors[node]==node_color_1 or self.colors[node]==node_color_2:
                        self.colors[node] = new_color
                self.tree_edges.append((node_1, node_2, cost))
                self.total_cost += cost
        return self.total_cost


if __name__=='__main__':

    mylist = []
    nodes_numbers = 10
    for line in xrange(nodes_numbers):
        adjacency = []
        for neighbor in xrange(nodes_numbers):
            adjacency.append(numpy.random.choice([i for i in xrange(1, nodes_numbers+1)]) if line<neighbor else 0)
        mylist.append(adjacency)
    mg = MatrixGraph(mylist)
    print (mg.prim())
    mg.display('prim.png')
    print (mg.kruskal())
    mg.display('kruska.png')
    print (mg.prim_with_heapqueue())
    mg.display('heapqueue.png')

