from itertools import cycle
from random import random


class RandomSearchingToolsMixin:

    def mutate(self, colors, i=0):
        colors.pop(i)
        color = cycle(colors)
        self.node_color = {node: next(color) for node in self.nodes}

    def fitness(self):
        return len(set(self.node_color.values()))

    def is_coloring_valid(self):
        for i, j in self.edges:
            if self.node_color[i] == self.node_color[j]:
                return False
        return True


class GetColoringMixin:

    def get_rgb_coloring(self):
        if not self.rgb:
            self.rgb = {color: ((color / len(self.nodes)) * random(), random(), random()) for color in self.node_color.values()}
        if not self.rgb_coloring:
            self.rgb_coloring = {node: self.rgb[self.node_color[node]] for node in self.nodes}
        return self.rgb_coloring

    def get_int_coloring(self):
        return self.node_color

    def get_rgb_colors(self):
        return self.rgb

    def get_int_colors(self):
        return list(self.node_color.values())
