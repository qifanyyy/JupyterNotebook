"""
@author: David Lei
@since: 19/10/2017

"""

def find_connected_component(graph, visited, node, component_number):  # Modified dfs.
    for edge in graph.get_adjacent_edges(node):
        adj_node = edge.destination
        if visited[adj_node.index] == -1:  # Visit the node.
            visited[adj_node.index] = component_number
            find_connected_component(graph, visited, adj_node, component_number)

def connected_components(graph):
    nodes = graph.get_all_vertices()
    visited = [-1] * len(nodes)
    component_number = 0  # Label each component starting at 0.
    for node in nodes:
        if visited[node.index] == -1:  # Have not visited this node yet.
            visited[node.index] = component_number
            find_connected_component(graph, visited, node, component_number)
            # We have found all components reachable from node so increment component number to
            # find components reachable from another node, it is guaranteed a node can't be in 2 components
            # as otherwise find_connected_component() would have found it.
            component_number += 1
    return component_number, visited

if __name__ == "__main__":
    from algorithms_datastructures.graphs.implementations.adjacency_list import AdjacencyList

    graph = AdjacencyList(4)
    A = graph.add_vertex(0, "A")
    B = graph.add_vertex(1, "B")
    C = graph.add_vertex(2, "C")
    D = graph.add_vertex(3, "D")

    # Graph is just 4 nodes = 4 components.
    num_components, node_components = connected_components(graph)
    print("number of components %s is correct: %s" % (num_components, num_components == 4))
    print("node components: " + str(node_components))

    # Add edge b/w A and B.
    graph.add_edge(origin_vertex=A, destination_vertex=B)
    num_components, node_components = connected_components(graph)
    print("number of components %s is correct: %s" % (num_components, num_components == 3))
    print("node components: " + str(node_components))

    # Add edges b/w B and C and D and C. But D is not reachable from A, B or C so 2 components.
    graph.add_edge(origin_vertex=B, destination_vertex=C)
    graph.add_edge(origin_vertex=D, destination_vertex=C)
    num_components, node_components = connected_components(graph)
    print("number of components %s is correct: %s" % (num_components, num_components == 2))
    print("node components: " + str(node_components))

    # Add edge b/w C and D resulting in 1 component.
    graph.add_edge(origin_vertex=C, destination_vertex=D)
    num_components, node_components = connected_components(graph)
    print("number of components %s is correct: %s" % (num_components, num_components == 1))
    print("node components: " + str(node_components))