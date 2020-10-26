'''
Here we'll code up Prim's minimum spanning tree algorithm.
The accompanying text file describes an undirected graph with integer edge costs. It has the format:

[number_of_nodes] [number_of_edges]
[one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
[one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
...

For example, the third line of the file is "2 3 -8874", indicating that there is an edge
connecting vertex #2 and vertex #3 that has cost -8874.

Do NOT assume that edge costs are positive, nor that they are distinct.

Run Prim's minimum spanning tree algorithm on this graph, and reported the
overall cost of a minimum spanning tree --- an integer, which may or may not be negative.

IMPLEMENTATION NOTES: This graph is small enough that the straightforward O(mn) time
implementation of Prim's algorithm should work fine. OPTIONAL: For an
additional challenge, try implementing a heap-based version. The simpler approach, which should
already give a healthy speed-up, is to maintain relevant edges in a heap (with keys = edge
costs). The superior approach stores the unprocessed vertices in the heap. Note this requires
a heap that supports deletions and requires one to maintain
some kind of mapping between vertices and their positions in the heap.
'''
import time


# Vertex class for undirected graphs
class Vertex():
    def __init__(self, key):
        self._key = key
        self._nbrs = {}

    def __str__(self):
        return '{' + "'key': {}, 'nbrs': {}".format(
            self._key,
            self._nbrs
        ) + '}'

    def add_nbr(self, nbr_key, weight=1):
        if (nbr_key):
            self._nbrs[nbr_key] = weight

    def has_nbr(self, nbr_key):
        return nbr_key in self._nbrs

    def get_nbr_keys(self):
        return list(self._nbrs.keys())

    def remove_nbr(self, nbr_key):
        if nbr_key in self._nbrs:
            del self._nbrs[nbr_key]

    def get_e(self, nbr_key):
        if nbr_key in self._nbrs:
            return self._nbrs[nbr_key]


# Undirected graph class
class Graph():
    def __init__(self):
        self._vertices = {}

    # 'x in graph' will use this containment logic
    def __contains__(self, key):
        return key in self._vertices

    # 'for x in graph' will use this iter() definition, where x is a vertex in an array
    def __iter__(self):
        return iter(self._vertices.values())

    def __str__(self):
        output = '\n{\n'
        vertices = self._vertices.values()
        for v in vertices:
            graph_key = "{}".format(v._key)
            v_str = "\n   'key': {}, \n   'nbrs': {}".format(
                v._key,
                v._nbrs
            )
            output += ' ' + graph_key + ': {' + v_str + '\n },\n'
        return output + '}'

    def add_v(self, v):
        if v:
            self._vertices[v._key] = v
        return self

    def get_v(self, key):
        try:
            return self._vertices[key]
        except KeyError:
            return None

    def get_v_keys(self):
        return list(self._vertices.keys())

    # removes vertex as neighbor from all its neighbors, then deletes vertex
    def remove_v(self, key):
        if key in self._vertices:
            nbr_keys = self._vertices[key].get_nbr_keys()
            for nbr_key in nbr_keys:
                self.remove_e(nbr_key, key)
            del self._vertices[key]

    def add_e(self, from_key, to_key, weight=1):
        if from_key not in self._vertices:
            self.add_v(Vertex(from_key))
        if to_key not in self._vertices:
            self.add_v(Vertex(to_key))

        self._vertices[from_key].add_nbr(to_key, weight)
        self._vertices[to_key].add_nbr(from_key, weight)

    def get_e(self, from_key, to_key):
        if from_key and to_key in self._vertices:
            return self.get_v(from_key).get_e(to_key)

    # adds the weight for an edge if it exists already, with a default of 1
    def increase_e(self, from_key, to_key, weight=1):
        if from_key not in self._vertices:
            self.add_v(Vertex(from_key))
        if to_key not in self._vertices:
            self.add_v(Vertex(to_key))

        weight_u_v = self.get_v(from_key).get_e(to_key)
        new_weight_u_v = weight_u_v + weight if weight_u_v else weight

        weight_v_u = self.get_v(to_key).get_e(from_key)
        new_weight_v_u = weight_v_u + weight if weight_v_u else weight

        self._vertices[from_key].add_nbr(to_key, new_weight_u_v)
        self._vertices[to_key].add_nbr(from_key, new_weight_v_u)

    def has_e(self, from_key, to_key):
        if from_key in self._vertices:
            return self._vertices[from_key].has_nbr(to_key)

    def remove_e(self, from_key, to_key):
        if from_key in self._vertices:
            self._vertices[from_key].remove_nbr(to_key)
        if to_key in self._vertices:
            self._vertices[to_key].remove_nbr(from_key)

    def for_each_v(self, cb):
        for v in self._vertices:
            cb(v)


# Heap class
# input: order is 0 for max heap, 1 for min heap
class Heap():
    def __init__(self, order=1):
        self._heap = []
        self._min_heap = order

    def __str__(self):
        output = '['
        size = len(self._heap)
        for i, v in enumerate(self._heap):
            txt = ', ' if i is not size - 1 else ''
            output += str(v) + txt
        return output + ']'

    # input: parent and child nodes
    def _is_balanced(self, p, c):
        is_min_heap = p <= c
        return is_min_heap if self._min_heap else not is_min_heap

    def _swap(self, i, j):
        # bookkeeping for Prim's MST algorithm:
        # global heap_i
        # u = self._heap[i]
        # v = self._heap[j]
        # heap_i[u] = j
        # heap_i[v] = i

        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    # input: parent and child indices
    def _sift_up(self, p_i, c_i):
        if p_i == -1:
            return 0
        p = self._heap[p_i]
        c = self._heap[c_i]

        while (not self._is_balanced(p, c)):
            p_i = (c_i - 1) // 2
            self._swap(c_i, p_i)
            c_i = p_i
            if c_i is 0:
                break
            p = self._heap[(c_i - 1) // 2]

    # input: parent and child indices
    def _sift_down(self, p_i, c_i):
        while (c_i and not self._is_balanced(self._heap[p_i], self._heap[c_i])):
            self._swap(p_i, c_i)
            p_i = c_i
            c_i = self._get_swapped_child_index(p_i)

    def get_root(self):
        try:
            return self._heap[0]
        except KeyError:
            return None

    def get_node(self, key):
        try:
            return self._heap[key]
        except KeyError:
            return None

    def get_nodes(self):
        return self._heap

    def insert(self, node):
        self._heap.append(node)
        node_i = len(self._heap) - 1

        # bookkeeping for Prim's MST algorithm:
        # global heap_i
        # heap_i[node] = node_i

        self._sift_up((node_i - 1) // 2, node_i)

    # input: parent index
    # output: index of smaller or greater child, one index if other DNE, or None
    def _get_swapped_child_index(self, p_i):
        size = len(self._heap)
        i = p_i * 2 + 1
        j = p_i * 2 + 2
        if size <= i:
            return None
        elif size <= j:
            return i

        if self._heap[i] > self._heap[j]:
            return j if self._min_heap else i
        else:
            return i if self._min_heap else j

    def _extract_root(self):
        if self._heap:
            self._swap(0, len(self._heap) - 1)
            root = self._heap.pop()
            self._sift_down(0, self._get_swapped_child_index(0))
            return root

    # extracts minimum value in O(logn) time
    def extract_min(self):
        if not self._min_heap:
            raise ValueError('Only min heaps support extract_min')
        return self._extract_root()

    # extracts maximum value in O(logn) time
    def extract_max(self):
        if self._min_heap:
            raise ValueError('Only max heaps support extract_max.')
        return self._extract_root()

    # deletes node from anywhere in heap in O(logn) time
    # input: key (i.e. index) of node to delete
    def delete(self, key):
        self._swap(key, len(self._heap) - 1)
        removed = self._heap.pop()

        p_i = (key - 1) // 2
        if not self._is_balanced(self._heap[p_i], self._heap[key]):
            self._sift_up(p_i, key)
        else:
            self._sift_down(p_i, key)

        return removed

    # initializes a heap in O(n) time
    def heapify(self):  # to do
        return self._heap


# Global variables
G = Graph()
H = Heap()
X = {1: 1}  # vertices spanned by tree T
# heap_i = {}  # tracks index of vertices in heap


# input: filename
# output: Graph
def create_graph(filename):
    global G
    with open(filename) as f_handle:
        f_handle.readline()
        for line in f_handle:
            edge = line.split()
            u = int(edge[0])
            v = int(edge[1])
            cost = int(edge[2])
            G.add_e(u, v, cost)
    return G


# input: graph T (assumed to be a minimum spanning tree)
# output: cost of MST
def calc_cost(T):
    cost = 0
    G_keys = T.get_v_keys()
    for v_k in G_keys:
        v = T.get_v(v_k)
        nbr_keys = v.get_nbr_keys()
        for nbr_k in nbr_keys:
            cost += v.get_e(nbr_k)
    return cost // 2


# input: heap key (vertex) to update, u edge cost which may decrease v's position in heap
# def update_heap_key(v, u_v_cost):
#     global H, heap_i

#     v_heap_i = heap_i[v]
#     if u_v_cost < H.get_node(v_heap_i):
#         H.delete(v_heap_i)  # delete at index i the vertex v in heap
#         insert_i = H.insert(u_v_cost)
#         heap_i[v] = insert_i


# input: vertices to update [optional]
# output: updated heap
def calc_heap(vertices):
    global G, H, X, heap_i
    G_keys = G.get_v_keys()
    for v in G_keys:
        if v not in X:
            u_keys = list(filter(lambda u: u in X, G.get_v(v).get_nbr_keys()))
            u_edges = list(map(lambda u: G.get_e(u, v), u_keys))
            # print('v: ', v)
            # print('u_keys: ', u_keys)
            # print('u_edges: ', u_edges)
            min_u_cost = min(u_edges) if u_edges else 1000000
            H.insert(min_u_cost)
            # print('min_u_cost: ', min_u_cost)
            # print('H: ', H)
            # print('heap_i: ', heap_i)
    return H


# output: minimum spanning tree
def minimum_spanning_tree():
    global G, H, X, heap_i
    T = Graph()
    # H = calc_heap(G)

    num_vertices = len(G.get_v_keys())
    while len(X.keys()) != num_vertices:
        min_cost = 1000000
        min_e = None
        for v_k in X:
            v = G.get_v(v_k)
            nbr_keys = filter(lambda k: k not in X, v.get_nbr_keys())
            for nbr_k in nbr_keys:
                cost = v.get_e(nbr_k)
                if cost < min_cost:
                    min_cost = cost
                    min_e = [v_k, nbr_k]
        u, v = min_e[0], min_e[1]
        T.add_e(u, v, G.get_e(u, v))
        X[v] = 1

    return T


def main():
    # Expected example overall cost of MST = 14
    create_graph('minimum_spanning_tree_ex.txt')
    # print(G)

    start = time.time()
    mst = minimum_spanning_tree()
    result = calc_cost(mst)
    print('result: ', result)
    print('elapsed time: ', time.time() - start)


main()
