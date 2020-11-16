from graphics import *
from enum import Enum

class Color(Enum):
    no_color = 0
    red = 1
    green = 2
    blue = 3
    purple = 4

    def color_to_string(self):
        if self is Color.no_color:
            return "gray"
        if self is Color.red:
            return "red"
        if self is Color.green:
            return "green"
        if self is Color.blue:
            return "blue"
        if self is Color.purple:
            return "purple"

class Map():
    def __init__(self, graph):
        self.graph = graph
        self.num_colored = 0

    def clean_map(self):

        self.num_colored = 0

        for pt in self.graph:
            pt.color = 0
            pt.conflicts = 0
            pt.color_reads = 0
            pt.color_writes = 0

    def draw_graph(self, win):
        graph = self.graph
        for pt in graph:
            circ = Circle(pt.pt, 6)
            circ.setFill("black")
            circ.draw(win)
            for edge in pt.edges:
                edge.ln.draw(win)

    def draw_poly(self, win):
        graph = self.graph
        for pt in graph:
            poly = pt.poly
            col_enum = Color(pt.color)
            poly.setFill(col_enum.color_to_string())
            poly.draw(win)

    def count_reads_writes(self):
        reads = 0
        writes = 0
        for pt in self.graph:
            reads = reads + pt.color_reads
            writes = writes + pt.color_writes

        return [reads, writes]


class graph_edge():
    def __init__(self, ln, start_point, end_point, distance, if_checked=False):
        self.ln = ln
        self.start_point = start_point
        self.end_point = end_point
        self.distance = distance
        self.checked = if_checked
        self.theta = 0

class graph_point(object):
    def __init__(self, pt, color=None, poly=None):
        self.map = None
        self.pt = pt
        self.neighbors = []
        self.edges = []
        self._color = color
        self.conflicts = 0

        self.color_reads = 0
        self.color_writes = 0

        self.poly = poly
        self.all_edges = []
        self.triangles=None

    @property
    def color(self):
        self.color_reads = self.color_reads + 1

        return self._color


    @color.setter
    def color(self, value):
        self.color_writes = self.color_writes + 1


        self._color = value

    # Returns true if any neighbors have conflicting colors
    def has_conflicting_neighbors(self):

        return any(pt.color == self.color for pt in self.neighbors)




