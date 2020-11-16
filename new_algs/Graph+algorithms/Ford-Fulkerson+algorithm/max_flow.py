import numpy as np


def find_augmenting_path_and_update(res, graph, flow_graph):
    '''
    Complexity is not O(E) due to adjaceny matrix implementation. (Do not keep track of set of edges)
    Completxity is O(V*V)
    '''
    backtrack = np.zeros(res.shape[0], np.int)
    visited = np.zeros(res.shape[0], np.int)
    flow = np.zeros(res.shape[0], np.int)
    flow[0] = 10000

    # find path using dfs
    node_stack = [0]

    flow_val = 0

    while(len(node_stack)):
        # get the top node
        node = node_stack.pop()
        visited[node] = 1

        # get all child nodes
        for i in xrange(res.shape[0]):
            if res[node][i] and not visited[i]:
                node_stack.append(i)
                backtrack[i] = node
                flow[i] = min(flow[node], res[node][i])

                # check whether target node
                if i == res.shape[0] - 1:
                    # to break the outer loop
                    node_stack = []
                    flow_val = flow[i]
                    break

    if not flow_val:
        return 0

    # update the residual network
    curr_node = res.shape[0] - 1

    while(curr_node != 0):
        prev_node = backtrack[curr_node]

        if graph[prev_node][curr_node]:
            flow_graph[prev_node][curr_node] += flow_val
        else:
            flow_graph[curr_node][prev_node] -= flow_val

        res[prev_node][curr_node] -= flow_val
        res[curr_node][prev_node] += flow_val
        curr_node = prev_node
    
    return flow_val


def find_max_flow(graph):
    # let's initialize the residual network
    res = graph.copy()
    flow_graph = np.zeros(res.shape, np.int)

    max_flow = 0

    while(True):
        flow_val = find_augmenting_path_and_update(res, graph, flow_graph)
        if not flow_val:
            break
        max_flow += flow_val

    return max_flow, flow_graph


# let's take a toy example
# graph of 6 nodes, 0 - source, 5 - target
# adjaceny matrix representation is used

graph = np.zeros((6,6), np.int)

# now add the flow capacities
graph[0][1] = 16
graph[0][2] = 13
graph[1][3] = 12
graph[2][1] = 4
graph[2][4] = 14
graph[3][5] = 20
graph[3][2] = 9
graph[4][3] = 7
graph[4][5] = 4

# find the max flow
max_flow, flow_graph = find_max_flow(graph)
print("Max flow: " + str(max_flow))
print(flow_graph)