from resources.partial_tree import Graph, determine_partial_tree, all_paths_of_length_k, kruskal, prim

g = Graph()
g.build("../input_files/partial_tree_graph1.in")

partial_tree = Graph(g.nodes)
determine_partial_tree(g, partial_tree)

print(partial_tree.__dict__)
print(all_paths_of_length_k(partial_tree, 1, 7))

g.build("../input_files/partial_tree_graph2.in")
print("\nKruskal's algorithm: ")
print(kruskal(g))

print("\nPrim's algorithm: ")
prim(g, 3)
