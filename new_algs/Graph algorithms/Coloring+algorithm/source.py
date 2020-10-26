from graphio import show, read_edges
from coloring.random_search import Coloring
import networkx as nx


edges = read_edges('input.txt')
coloring = Coloring(nx.Graph(edges))
coloring.build(fit=3, steps=50)
show(edges, coloring.get_rgb_coloring(), message=f'colors amount = {coloring.fit}')
