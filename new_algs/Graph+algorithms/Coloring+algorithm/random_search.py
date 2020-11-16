from random import shuffle
from coloring.mixins import RandomSearchingToolsMixin, GetColoringMixin


class Coloring(RandomSearchingToolsMixin, GetColoringMixin):

    def __init__(self, graph):
        self.graph = graph
        self.nodes = self.graph.nodes
        self.edges = graph.edges
        self.node_color = {}
        self.fit = None
        self.rgb = None
        self.rgb_coloring = None

    def build(self, fit, steps=1):
        colors = list(range(len(self.nodes)))
        self.mutate(colors)
        valid_config = {}
        for step in range(steps):
            if self.is_coloring_valid():
                if self.fitness() <= fit:  # минимизация
                    self.fit = self.fitness()
                    return None
                valid_config = self.node_color
                self.mutate(colors)
            else:
                self.node_color = valid_config
                colors = list(valid_config.values())
                shuffle(colors)  # если этого не сделать, то цвета будут возвращаться в том же порядке
                # и в итоге реузльтат не изменится
        if not self.is_coloring_valid():
            self.node_color = valid_config
        self.fit = self.fitness()
        return None
