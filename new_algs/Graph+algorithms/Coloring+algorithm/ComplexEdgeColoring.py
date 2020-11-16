from common.path import create_path
import random

import logging

logger = logging.getLogger(__name__)


class EdgeColoring(object):
    def __init__(self, graph):
        self.__graph = graph
        self.__kempe = KempeEngine(graph)

    # don't delete this part, the original one passed from Guan
    def run(self, limit=200):
        self.__kempe.run()
        last = self.__graph.num_errors
        while limit > 0 and last > 0:
            self.__kempe.run()
            if self.__graph.num_errors >= last:
                limit = limit - 1
                self.random_split()
            last = self.__graph.num_errors
        if self.__graph.num_errors > 0:
            self.__kempe.run()
            #print self.__graph.to_json()
            print ("Proper Edge Coloring of G' not found!!!")
            return False
        return True

    def another_run(self, limit = 400):
        times = limit
        self.__kempe.run()
        last = self.__graph.num_errors
        while times > 0 and last > 0:
            self.__graph.random_color()
            self.__kempe.run()
            last = self.__graph.num_errors
            times = times - 1
        if last > 0:
            #print "Proper edge coloring not found!"
            return False
        return True

    '''def run(self, limit=400):
        times = limit
        self.__kempe.run()
        last = self.__graph.num_errors
        while limit > 0 and last > 0:
            self.__kempe.run()
            if self.__graph.num_errors >= last:
                limit = limit - 1
                self.random_split()
            else:
                limit = times
                last = self.__graph.num_errors
        if last > 0:
            print "Proper Edge Coloring of G' not found!!!"
     '''      

    def random_split(self):
        break_times = 60
        # random break
        errors = list(self.__graph.errors)
        for i in xrange(break_times):
            edge = random.choice(errors)
            (link, dc) = edge.links
            c1 = link.color
            vertex = link.vertex
            colors = [link.color for link in vertex.links]
            colors = filter(lambda c: c != c1, colors)
            if len(colors) == 0:
                break
            c2 = random.choice(colors)
            vertex.swap_colors(c1, c2)


class KempeEngine(object):
    def __init__(self, graph):
        """
        :type graph: Graph
        :param graph: Graph to work on
        """
        self.graph = graph

    def run(self):
        """
        Run Kempe Path Algorithm
        """
        for edge in self.graph.edges:
            self.run_on_edge(edge)

    def run_on_edge(self, edge):
        """
        Run Kempe Path Algorithm on an error edge.

        :returns:
            length of path involved - If error is reduced
            -length of path involved - If no error is reduced
        """
        # not an error, stop
        if not edge.is_error():
            return -1

        (a, b) = edge.get_endpoints()
        ca = edge.get_link(a).color
        cb = edge.get_link(b).color
        if random.random() < 0.5:
            p = create_path(self.graph, a, cb, ca)
        else:
            p = create_path(self.graph, b, ca, cb)
            # meet start edge, stop
        if p.is_closed():
            return -len(p)
            # flip whole path
        p.swap_colors(ca, cb)
        return len(p)
