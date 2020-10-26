"""
@author: David Lei
@since: 20/10/2017

Based on https://www.youtube.com/watch?v=5xosHRdxqHA&ab_channel=BoQian
"""
from algorithms_datastructures.distjoint_set.distjoint_set import DistjointSet
from algorithms_datastructures.graphs.implementations.structures import Edge
from algorithms_datastructures.graphs.implementations.structures import Vertex

def kruskals(nodes, edges):
    mst = []
    distjoint_set = DistjointSet()
    djs_index_map = distjoint_set.make_set(nodes, return_mapping=True)  # DistjointSetNode.data now points to a Vertex.
    edges.sort(key=lambda e:e.weight)  # Sort edges by weight, min is first.
    for edge in edges:
        src = edge.origin
        dst = edge.destination
        if distjoint_set.find_compressed(djs_index_map[src]) != distjoint_set.find_compressed(djs_index_map[dst]):
            # These two vertices are not connected yet, we found the min edge that connects them.
            # Merge in disjoint set.
            distjoint_set.union_by_size(djs_index_map[src], djs_index_map[dst])
            # Add to mst.
            mst.append(edge)
    return mst

if __name__ == "__main__":
    nodes = ["a", "b", "f", "c", "d", "e"]
    node_mappings = {rep: Vertex(x=i, rep=rep) for i, rep in enumerate(nodes)}
    nodes = list(node_mappings.values())
    nodes.sort(key=lambda n:n.rep)  # Sort by representation which is a character.

    input_edges = [
        ("a", "f", 2), ("a", "b", 4), ("b", "f", 5),
        ("b", "c", 6), ("c", "f", 1), ("c", "d", 3),
        ("d", "e", 2), ("f", "e", 4)
    ]

    edges = []

    for src, dst, weight in input_edges:
        # Undirected graph.
        forwards = Edge(origin=node_mappings[src], destination=node_mappings[dst], weight=weight)
        backwards = Edge(origin=node_mappings[dst], destination=node_mappings[src], weight=weight)
        edges.append(forwards)
        edges.append(backwards)

    mst = kruskals(nodes, edges)
    print("Minimum spanning tree")
    for edge in mst:
        print("%s -> %s cost: %s" % (edge.origin.rep, edge.destination.rep, edge.weight))