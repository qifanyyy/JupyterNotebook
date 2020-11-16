from common.path import create_path
from common.TreeNode import TreeNode
from four_color.ComplexEdgeColoring import KempeEngine
import random
import itertools
import unittest
import logging

logger = logging.getLogger(__name__)


class InspectorEngine(object):
    def __init__(self, graph):
        self.graph = graph
        self.removed = None

    def check_pentagon(self, pentagon):
        count = 0
        for (a, b) in itertools.combinations(pentagon, 2):
            if self.graph.get_edge(a, b) is not None:
                count += 1
        if count == 5:
            for k in xrange(5):
                a = pentagon[k]
                b = pentagon[(k + 1) % 5]
                if self.can_remove(pentagon, a, b):
                    return True
        return False

    def find_pentagon(self):
        for vertex in self.graph.vertices:
            root_node = TreeNode(vertex.id)
            nodes = [root_node]
            while len(nodes) > 0:
                node = nodes.pop(0)
                path = node.get_path()
                v_a_id = node.value
                v_a = self.graph.get_vertex(v_a_id)
                for v_b in v_a.neighbors:
                    if not v_b.id in path and len(path) < 5:
                        child = TreeNode(v_b.id)
                        node.add_child(child)
                        nodes.append(child)
                    elif len(path) == 5 and v_b == vertex:
                        # check path
                        # a valid pentagon has not internal edges on itself
                        if self.check_pentagon(path):
                            return path
        return None

    def can_remove(self, pentagon, a, b):
        vertices = set([])
        neighbors = filter(lambda k: k != b, self.graph.get_neighbors(a))
        if len(neighbors) != 2 or self.graph.has_edge(neighbors[0], neighbors[1]):
            return False
        vertices.update(neighbors)
        neighbors = filter(lambda k: k != a, self.graph.get_neighbors(b))
        if len(neighbors) != 2 or self.graph.has_edge(neighbors[0], neighbors[1]):
            return False
        vertices.update(neighbors)
        if len(vertices) != 4:
            return False
        return True

    def remove_edge(self, pentagon):
        assert self.removed is None
        # try to find an edge that can be removed
        for k in xrange(5):
            a = pentagon[k]
            b = pentagon[(k + 1) % 5]
            if self.can_remove(pentagon, a, b):
                self.graph.remove_edge_by_endpoint(a, b)
                c, d = self.graph.contract_vertex(a)
                e, f = self.graph.contract_vertex(b)
                # ensure that c, e are on the pentagon
                if not c in pentagon:
                    c, d = d, c
                if not e in pentagon:
                    e, f = f, e
                    #
                # c----a----d
                #      | <= removed
                # e----b----f
                #
                # c, a, b, e are on the pentagon
                self.removed = ((c, a, d), (e, b, f))
                return True
        return False

    def check_cycles(self):
        ((c, a, d), (e, b, f)) = self.removed
        if self.graph.get_color(c, d) != self.graph.get_color(e, f):
            self.put_back_edge()
            return False
        self.put_back_edge()
        self.last_removed = ((c, a, d), (e, b, f))
        c0 = self.graph.get_color(c, a)
        colors = [1, 2, 3]
        colors.remove(c0)
        c1, c2 = tuple(colors)
        # try 1st
        self.graph.set_color(a, c, c1)
        self.graph.set_color(b, e, c1)
        self.graph.set_color(a, b, c2)
        self.graph.set_color(b, a, c2)
        p1 = create_path(self.graph, self.graph.get_edge(a, c), a, c0, c1)
        p2 = create_path(self.graph, self.graph.get_edge(b, e), b, c0, c1)
        if not p1.is_closed() or not p2.is_closed():
            return False
        self.bicycle_configs = [(c0, c1, c2, p1, p2)]
        # try 2nd
        self.graph.set_color(a, c, c2)
        self.graph.set_color(b, e, c2)
        self.graph.set_color(a, b, c1)
        self.graph.set_color(b, a, c1)
        p1 = create_path(self.graph, self.graph.get_edge(a, c), a, c0, c2)
        p2 = create_path(self.graph, self.graph.get_edge(b, e), b, c0, c2)
        if not p1.is_closed() or not p2.is_closed():
            return False
        self.bicycle_configs.append((c0, c2, c1, p1, p2))
        return True

    def put_back_edge(self):
        assert self.removed is not None
        ((c, a, d), (e, b, f)) = self.removed
        c1 = self.graph.get_color(c, d)
        c2 = self.graph.get_color(e, f)
        self.graph.remove_edge_by_endpoint(c, d)
        self.graph.remove_edge_by_endpoint(e, f)
        self.graph.add_vertex(a)
        self.graph.add_vertex(b)
        self.graph.add_edge(a, b)
        self.graph.add_edge(a, c)
        self.graph.add_edge(a, d)
        self.graph.set_color(a, d, c1)
        self.graph.set_color(d, a, c1)
        self.graph.set_color(c, a, c1)
        self.graph.add_edge(b, e)
        self.graph.add_edge(b, f)
        self.graph.set_color(e, b, c2)
        self.graph.set_color(f, b, c2)
        self.graph.set_color(b, f, c2)
        self.removed = None

    def contract(self):
        print (self.graph.to_json())
        assert len(self.bicycle_configs) == 2

        for k in range(2):
            # color
            ((c, a, d), (e, b, f)) = self.last_removed
            c0, c1, c2, p1, p2 = self.bicycle_configs[k]
            print (len(p1), len(p2))
            cycle = []
            cycle.extend(p1)
            cycle.extend(p2)
            # re-color
            self.graph.set_color(a, c, c1)
            self.graph.set_color(b, e, c1)
            self.graph.set_color(a, b, c2)
            self.graph.set_color(b, a, c2)
            chords_map = {}
            for v in cycle:
                chord = self.find_chord(v, cycle, c0, c2)
                if len(chord) > 2:
                    chords_map[chord[0]] = chord[-1]
            print ('00000000000000')
            print (self.graph.to_json())
            to_remove = filter(lambda v: not v.id in cycle, self.graph.vertices)
            for v in to_remove:
                print ('remove %d' % v.id)
                self.graph.remove_vertex(v.id)
            print ('1111111111111')
            print (self.graph.to_json())
            for a in chords_map:
                b = chords_map[a]
                if a > b:
                    self.graph.add_edge(a, b)
                    self.graph.set_color(a, b, c2)
                    self.graph.set_color(b, a, c2)
            print ('!!!')
            print (self.graph.to_json())
            self.graph.validate()


    def dump_chord(self, chord):
        print (chord[0],)
        for i in xrange(len(chord) - 1):
            a = chord[i]
            b = chord[i + 1]
            c1 = self.graph.get_color(a, b)
            c2 = self.graph.get_color(b, a)
            print ('-(%d,%d)-%d' % (c1, c2, b),)
        print ('\n')

    def find_chord(self, v, cycle, x0, x1):
        """
        :param v: the vertex id of the starting vertex
        :param x1: the chord's color
        :rtype: list of ints
        """
        assert v in cycle
        chord = [v]
        v = self.graph.get_vertex(v)
        if v is None:
            return []
        while True:
            u = v.get_neighbor_edge_by_color(x1)
            assert self.graph.get_color(v.id, u.id) == x1
            chord.append(u.id)
            if u.id in cycle:
                break
            x0, x1 = x1, x0
            v = u
        return chord


class InspectorTest(unittest.TestCase):
    def setUp(self):
        from common.multigraph import MultiGraph
        import json

        data = {
            'edges': [
                {'v1': 1, 'v2': 2, 'c1': 1, 'c2': 1},
                {'v1': 1, 'v2': 3, 'c1': 1, 'c2': 1},
                {'v1': 1, 'v2': 6, 'c1': 1, 'c2': 1},
                {'v1': 2, 'v2': 3, 'c1': 1, 'c2': 1},
                {'v1': 2, 'v2': 6, 'c1': 1, 'c2': 1},
                {'v1': 3, 'v2': 4, 'c1': 1, 'c2': 1},
                {'v1': 4, 'v2': 5, 'c1': 1, 'c2': 1},
                {'v1': 5, 'v2': 1, 'c1': 1, 'c2': 1},
                {'v1': 5, 'v2': 2, 'c1': 1, 'c2': 1},
            ],
            'vertices': [
                {'x': 0, 'y': 0, 'name': 1},
                {'x': 0, 'y': 0, 'name': 2},
                {'x': 0, 'y': 0, 'name': 3},
                {'x': 0, 'y': 0, 'name': 4},
                {'x': 0, 'y': 0, 'name': 5},
                {'x': 0, 'y': 0, 'name': 6},
            ],
        }
        graph = MultiGraph.from_json(json.dumps(data))
        self.inspector = InspectorEngine(graph)

    def test_find_pentagon(self):
        self.assertEqual(5, len(self.inspector.find_pentagon()), "pentagon not found")
