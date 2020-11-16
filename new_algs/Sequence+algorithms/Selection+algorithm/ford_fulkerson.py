"""
@author: David Lei
@since: 5/10/2017

Implementation of ford_fulkerson to find max flow.
"""
from algorithms_datastructures.graphs.implementations.adjacency_list import AdjacencyList

def find_path_dfs(residual_network, source, target, edge_list, visited):
    if source == target:
        return edge_list
    visited[source.index] = 1  # Note source.index is just an index.
    for edge in residual_network.get_adjacent_edges(source):
        if edge.residual_capacity <= 0:
            continue
        if visited[edge.destination.index] != 1:

            found_path = find_path_dfs(residual_network, edge.destination, target, edge_list + [edge], visited)
            if found_path:
                return found_path

def ford_fulkerson(flow_network, residual_network, source, target, num_nodes, residual_source, residual_target):
    visited = [0 for _ in range(num_nodes)]
    augmenting_path = find_path_dfs(residual_network, residual_source, residual_target, [], visited) # List of chosen edges.
    augmented_path_flows = []
    while augmenting_path:

        print("Augmenting path found: %s" % source.rep, end="")
        for edge in augmenting_path:
            print("->%s" % edge.destination.rep, end="")
        print()

        # The flow of the path is defined as the min flow through all edges in the path.
        flow_of_augmented_path = min(edge.residual_capacity for edge in augmenting_path)
        augmented_path_flows.append(flow_of_augmented_path)

        for residual_edge in augmenting_path:
            original_edge = flow_network.find_edge(residual_edge.origin, residual_edge.destination)
            if not original_edge:
                raise ValueError("Missing edge? How did this happen")
            # Add the flow to the original graph, greedly use that path.
            original_edge.flow += flow_of_augmented_path
            # Remove the flow from the residual graph edges with residual_capacity == flow of aug path will be saturated.
            residual_edge.residual_capacity -= flow_of_augmented_path

        # Get next augmenting path.
        visited = [0 for _ in range(num_nodes)]
        augmenting_path = find_path_dfs(residual_network, residual_source, residual_target, [], visited) # List of chosen edges.

    # Get the overall flow == max flow == sum of flow in edges, the edges in the original network now have max flow.
    print("Computing max flow from flows of augmented paths")
    print(sum(augmented_path_flows))

    max_flow_s = 0
    print("Computing max flow from Source")
    for edge in flow_network.get_adjacent_edges(source):
        max_flow_s += edge.flow
    print(max_flow_s)

    target_incoming_edges = []

    print("Finding chosen edges")
    seen_edges = set()
    edges = flow_network.get_adjacent_edges(source)
    for edge in edges:
        print("%s->%s: f=%s" % (edge.origin.rep, edge.destination.rep, edge.flow))
        if edge.destination != target:
            for next_edge in flow_network.get_adjacent_edges(edge.destination):
                if not next_edge in seen_edges:
                    edges.append(next_edge)
                    seen_edges.add(next_edge)
        else:
            target_incoming_edges.append(edge)

    max_flow_t = 0
    print("Computing max flow from Target")
    for edge in set(target_incoming_edges):
        max_flow_t += edge.flow
    print(max_flow_t)

    if not (max_flow_t == max_flow_s == sum(augmented_path_flows)):
        raise ValueError("Wrong max flow?")
    return max_flow_t

# ------------------------------------------------- driver functions ---------------------------------------------------

def make_networks_mathspace():
    # https://mathspace.co/learn/world-of-maths/networks/network-flow-18724/network-flow-1289/
    flow_network = AdjacencyList(4)
    A = flow_network.add_vertex(index=0, rep='A')
    B = flow_network.add_vertex(index=1, rep='B')
    D = flow_network.add_vertex(index=2, rep='D')
    C = flow_network.add_vertex(index=3, rep='C')
    flow_network.add_edge(origin_vertex=A, destination_vertex=B, capacity=12, flow=0)
    flow_network.add_edge(origin_vertex=A, destination_vertex=D, capacity=9, flow=0)
    flow_network.add_edge(origin_vertex=D, destination_vertex=B, capacity=8, flow=0)
    flow_network.add_edge(origin_vertex=B, destination_vertex=C, capacity=15, flow=0)
    flow_network.add_edge(origin_vertex=D, destination_vertex=C, capacity=11, flow=0)

    residual_network = AdjacencyList(4)
    Ar = residual_network.add_vertex(index=0, rep='A')
    Br = residual_network.add_vertex(index=1, rep='B')
    Dr = residual_network.add_vertex(index=2, rep='D')
    Cr = residual_network.add_vertex(index=3, rep='C')
    residual_network.add_edge(origin_vertex=Ar, destination_vertex=Br, residual_capacity=12, flow=0)
    residual_network.add_edge(origin_vertex=Ar, destination_vertex=Dr, residual_capacity=9, flow=0)
    residual_network.add_edge(origin_vertex=Dr, destination_vertex=Br, residual_capacity=8, flow=0)
    residual_network.add_edge(origin_vertex=Br, destination_vertex=Cr, residual_capacity=15, flow=0)
    residual_network.add_edge(origin_vertex=Dr, destination_vertex=Cr, residual_capacity=11, flow=0)
    return flow_network, residual_network, A, C, Ar, Cr

def make_networks_basic_test():
    # A simple linear chain network showing that edges S->A and B->T will be restricted by the min flow in an edge in the augmenting path.
    flow_network = AdjacencyList(4)
    S = flow_network.add_vertex(index=0, rep='S')
    A = flow_network.add_vertex(index=1, rep='A')
    B = flow_network.add_vertex(index=2, rep='B')
    T = flow_network.add_vertex(index=3, rep='T')
    flow_network.add_edge(origin_vertex=S, destination_vertex=A, capacity=50, flow=0)
    flow_network.add_edge(origin_vertex=A, destination_vertex=B, capacity=2, flow=0)
    flow_network.add_edge(origin_vertex=B, destination_vertex=T, capacity=50, flow=0)

    residual_network = AdjacencyList(4)
    Sr = residual_network.add_vertex(index=0, rep='S')
    Ar = residual_network.add_vertex(index=1, rep='A')
    Br = residual_network.add_vertex(index=2, rep='B')
    Tr = flow_network.add_vertex(index=3, rep='T')
    residual_network.add_edge(origin_vertex=Sr, destination_vertex=Ar, residual_capacity=50)
    residual_network.add_edge(origin_vertex=Ar, destination_vertex=Br, residual_capacity=2)
    residual_network.add_edge(origin_vertex=Br, destination_vertex=Tr, residual_capacity=50)
    return flow_network, residual_network, S, T, Sr, Tr

def make_networks():
    # Modeling 2nd graph from with max flow of 17: https://www.hackerearth.com/practice/algorithms/graphs/maximum-flow/tutorial/
    flow_network = AdjacencyList(6)
    S = flow_network.add_vertex(index=0, rep='S')
    A = flow_network.add_vertex(index=1, rep='A')
    B = flow_network.add_vertex(index=2, rep='B')
    C = flow_network.add_vertex(index=3, rep='C')
    D = flow_network.add_vertex(index=4, rep='D')
    T = flow_network.add_vertex(index=5, rep='T')
    # Set all flows to 0.
    SA = flow_network.add_edge(origin_vertex=S, destination_vertex=A, capacity=10, flow=0)
    AC = flow_network.add_edge(origin_vertex=A, destination_vertex=C, capacity=8, flow=0)
    CT = flow_network.add_edge(origin_vertex=C, destination_vertex=T, capacity=10, flow=0)
    AB = flow_network.add_edge(origin_vertex=A, destination_vertex=B, capacity=2, flow=0)
    SB = flow_network.add_edge(origin_vertex=S, destination_vertex=B, capacity=8, flow=0)
    BC = flow_network.add_edge(origin_vertex=B, destination_vertex=C, capacity=6, flow=0)
    BD = flow_network.add_edge(origin_vertex=B, destination_vertex=D, capacity=7, flow=0)
    DT = flow_network.add_edge(origin_vertex=D, destination_vertex=T, capacity=10, flow=0)

    # Make residual graph.
    residual_network = AdjacencyList(6)
    Sr = residual_network.add_vertex(index=0, rep='S')
    Ar = residual_network.add_vertex(index=1, rep='A')
    Br = residual_network.add_vertex(index=2, rep='B')
    Cr = residual_network.add_vertex(index=3, rep='C')
    Dr = residual_network.add_vertex(index=4, rep='D')
    Tr = residual_network.add_vertex(index=5, rep='T')
    # All edges have residual capacity = capacity of edge - flow, all flow is 0 to start.
    SAr = residual_network.add_edge(origin_vertex=Sr, destination_vertex=Ar, residual_capacity=10, flow=0)
    ACr = residual_network.add_edge(origin_vertex=Ar, destination_vertex=Cr, residual_capacity=8, flow=0)
    CTr = residual_network.add_edge(origin_vertex=Cr, destination_vertex=Tr, residual_capacity=10, flow=0)
    ABr = residual_network.add_edge(origin_vertex=Ar, destination_vertex=Br, residual_capacity=2, flow=0)
    SBr = residual_network.add_edge(origin_vertex=Sr, destination_vertex=Br, residual_capacity=8, flow=0)
    BCr = residual_network.add_edge(origin_vertex=Br, destination_vertex=Cr, residual_capacity=6, flow=0)
    BDr = residual_network.add_edge(origin_vertex=Br, destination_vertex=Dr, residual_capacity=7, flow=0)
    DTr = residual_network.add_edge(origin_vertex=Dr, destination_vertex=Tr, residual_capacity=10, flow=0)
    return flow_network, residual_network, S, T, Sr, Tr

def make_networks_example():
    # Network based on: https://www.youtube.com/watch?v=rLIR89YyNjg&ab_channel=A%26A
    flow_network = AdjacencyList(6)
    A = flow_network.add_vertex(index=0, rep='A')
    B = flow_network.add_vertex(index=1, rep='B')
    C = flow_network.add_vertex(index=2, rep='C')
    D = flow_network.add_vertex(index=3, rep='D')
    E = flow_network.add_vertex(index=4, rep='E')
    F = flow_network.add_vertex(index=5, rep='F')
    flow_network.add_edge(origin_vertex=A, destination_vertex=B, capacity=16, flow=0)
    flow_network.add_edge(origin_vertex=B, destination_vertex=C, capacity=12, flow=0)
    flow_network.add_edge(origin_vertex=B, destination_vertex=D, capacity=4, flow=0)
    flow_network.add_edge(origin_vertex=A, destination_vertex=D, capacity=5, flow=0)
    flow_network.add_edge(origin_vertex=C, destination_vertex=D, capacity=9, flow=0)
    flow_network.add_edge(origin_vertex=C, destination_vertex=F, capacity=5, flow=0)
    flow_network.add_edge(origin_vertex=D, destination_vertex=E, capacity=20, flow=0)
    flow_network.add_edge(origin_vertex=C, destination_vertex=E, capacity=7, flow=0)
    flow_network.add_edge(origin_vertex=E, destination_vertex=F, capacity=20, flow=0)

    # Residual network:
    residual_network = AdjacencyList(6)
    Ar = residual_network.add_vertex(index=0, rep='A')
    Br = residual_network.add_vertex(index=1, rep='B')
    Cr = residual_network.add_vertex(index=2, rep='C')
    Dr = residual_network.add_vertex(index=3, rep='D')
    Er = residual_network.add_vertex(index=4, rep='E')
    Fr = residual_network.add_vertex(index=5, rep='F')
    residual_network.add_edge(origin_vertex=Ar, destination_vertex=Br, residual_capacity=16, flow=0)
    residual_network.add_edge(origin_vertex=Br, destination_vertex=Cr, residual_capacity=12, flow=0)
    residual_network.add_edge(origin_vertex=Br, destination_vertex=Dr, residual_capacity=4, flow=0)
    residual_network.add_edge(origin_vertex=Ar, destination_vertex=Dr, residual_capacity=5, flow=0)
    residual_network.add_edge(origin_vertex=Cr, destination_vertex=Dr, residual_capacity=9, flow=0)
    residual_network.add_edge(origin_vertex=Cr, destination_vertex=Fr, residual_capacity=5, flow=0)
    residual_network.add_edge(origin_vertex=Dr, destination_vertex=Er, residual_capacity=20, flow=0)
    residual_network.add_edge(origin_vertex=Cr, destination_vertex=Er, residual_capacity=7, flow=0)
    residual_network.add_edge(origin_vertex=Er, destination_vertex=Fr, residual_capacity=20, flow=0)

    return flow_network, residual_network, A, F, Ar, Fr

def make_networks_codeforces():
    flow_network = AdjacencyList(4)
    one = flow_network.add_vertex(index=0, rep='(1)')
    two = flow_network.add_vertex(index=1, rep='(2)')
    three = flow_network.add_vertex(index=2, rep='(3)')
    four = flow_network.add_vertex(index=3, rep='(4)')
    flow_network.add_edge(origin_vertex=one, destination_vertex=two, capacity=10, flow=0)
    flow_network.add_edge(origin_vertex=one, destination_vertex=three, capacity=10, flow=0)
    flow_network.add_edge(origin_vertex=two, destination_vertex=three, capacity=1, flow=0)
    flow_network.add_edge(origin_vertex=two, destination_vertex=four, capacity=10, flow=0)
    flow_network.add_edge(origin_vertex=three, destination_vertex=four, capacity=10, flow=0)

    residual_network = AdjacencyList(4)
    one_r = residual_network.add_vertex(index=0, rep='(1)')
    two_r = residual_network.add_vertex(index=1, rep='(2)')
    three_r = residual_network.add_vertex(index=2, rep='(3)')
    four_r = residual_network.add_vertex(index=3, rep='(4)')
    residual_network.add_edge(origin_vertex=one_r, destination_vertex=two_r, residual_capacity=10, flow=0)
    residual_network.add_edge(origin_vertex=one_r, destination_vertex=three_r, residual_capacity=10, flow=0)
    residual_network.add_edge(origin_vertex=two_r, destination_vertex=three_r, residual_capacity=1, flow=0)
    residual_network.add_edge(origin_vertex=two_r, destination_vertex=four_r, residual_capacity=10, flow=0)
    residual_network.add_edge(origin_vertex=three_r, destination_vertex=four_r, residual_capacity=10, flow=0)

    return flow_network, residual_network, one, four, one_r, four_r

if __name__ == "__main__":
    # Test simple linear network.
    print("\n\t\t~~~ Test 1 ~~~")
    flow_network, residual_network, source, target, residual_source, residual_target = make_networks_basic_test()
    max_flow = ford_fulkerson(flow_network, residual_network, source, target, 6, residual_source, residual_target)
    print("max flow: %s, expected: 2" % max_flow)
    print("Passed: %s" % (max_flow == 2))

    # Test 2nd graph from https://www.hackerearth.com/practice/algorithms/graphs/maximum-flow/tutorial/
    print("\n\t\t~~~ Test 2 ~~~")
    flow_network, residual_network, source, target, residual_source, residual_target = make_networks()
    max_flow = ford_fulkerson(flow_network, residual_network, source, target, 6, residual_source, residual_target)
    print("max flow: %s, expected: 17" % max_flow)
    print("Passed: %s" % (max_flow == 17))

    # Test graph from https://www.youtube.com/watch?v=rLIR89YyNjg&ab_channel=A%26A
    print("\n\t\t~~~ Test 3 ~~~")
    flow_network, residual_network, source, target, residual_source, residual_target = make_networks_example()
    max_flow = ford_fulkerson(flow_network, residual_network, source, target, 6, residual_source, residual_target)
    print("max flow: %s, expected: 21" % max_flow)
    print("Passed: %s" % (max_flow == 21))

    # Test graph from https://mathspace.co/learn/world-of-maths/networks/network-flow-18724/network-flow-1289
    print("\n\t\t~~~ Test 4 ~~~")
    flow_network, residual_network, source, target, residual_source, residual_target = make_networks_mathspace()
    max_flow = ford_fulkerson(flow_network, residual_network, source, target, 6, residual_source, residual_target)
    print("max flow: %s, expected: 21" % max_flow)
    print("Passed: %s" % (max_flow == 21))

    # Test from code forces network flow applications A.
    print("\n\t\t~~~ Test 5 ~~~")
    flow_network, residual_network, source, target, residual_source, residual_target = make_networks_codeforces()
    max_flow = ford_fulkerson(flow_network, residual_network, source, target, 4, residual_source, residual_target)
    print("max flow: %s, expected: 20" % max_flow)
    print("Passed: %s" % (max_flow == 20))