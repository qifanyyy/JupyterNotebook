# Solution of Assignment 2 of EE6108
# A Python implement of Bellman-Ford Algorithm.
# by GUO DONGFANG, G1801224L, MSc of CommEng, EEE, NTU

# Class to represent a graph
class Graph:
    def __init__(self, nodes):
        self.N = nodes  # No. of nodes
        self.graph = []

    # A function to add an edge to graph (unidirectional, from u to v)
    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])      # u:parent node, v:current node w:distance

    # A function to generate the lines of the output table
    def line_list(self, dist, next_node, iteration):
        line_head = 'Iter'+str(iteration)
        line_list = [line_head]
        for i in range(self.N):
            routing = "(" + str(next_node[i]) + ", " + str(dist[i]) + ")"
            line_list.append(routing)
        return line_list

    # Bellman-Ford algorithm
    # Find shortest distances from all the nodes to the target
    def bellmanford(self, target):
        # Initialize distances from target to all other nodes as infinite, target to target as O
        # and the parent nodes of all other nodes as -1, of target as itself.
        dist = [float("Inf")] * self.N
        next_node = [int(-1)] * self.N
        dist[target] = int(0)
        next_node[target] = target
        parent_set_iter = [target]
        # Initialization of the output lines
        output_iter = 0
        output_lines = []
        line = self.line_list(dist, next_node, output_iter)
        output_lines.append(line)

        # Relax all edges |N| - 1 times.
        # Update dist value and parent index of the adjacent nodes of
        # the chosen nodes. Only consider those nodes still in queue
        for i in range(self.N - 1):
            parent_set = list(parent_set_iter)           # the parent set only change once per iteration!
            for u, v, w in self.graph:
                if u in parent_set:
                    # use a temp parent set to avoid instant updates
                    # of parent nodes set before one iteration is done
                    parent_set_iter.append(v)
                    parent_set_iter = list(set(parent_set_iter))
                    if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        next_node[v] = u
            output_iter = output_iter + 1
            line = self.line_list(dist, next_node, output_iter)
            if (line[1:] == output_lines[-1][1:]) is False:
                output_lines.append(line)
            # print(parent_set, next_node, dist)

        # Output the result into the txt, in a table form as the PPT shows.
        f = open(table_path,'w')
        # Make the table header
        header = "Iterations"
        for i in range(self.N):
            node_name = "Node" + str(i)
            header = header + '\t' + node_name
        f.write(header+'\n')
        # Write the routing information
        for row in output_lines:
            row_str = "\t".join(row)
            f.write('\n')
            f.write(row_str)
        f.close()
        print("The result has been printed in the ./OUTPUT_bellmanford.txt ! Check it out :)")


# Configuration of path
graph_path = './INPUT_bellmanford.txt'          # path of input graph
table_path = './OUTPUT_bellmanford.txt'          # path of output table

# Read the txt to get the input graph.
with open(graph_path, 'r') as f:
    graph = []
    data = f.readlines()
    for line in data:
        line_data = line.split()
        line_data = list(map(int, line_data))
        graph.append(line_data)
    num_nodes = len(graph)

# Read the txt to get the input graph.
# In this case, switch the adjacency matrix to the adjacency list(edges)
# The edges should be bidirectional !
g = Graph(num_nodes)
for i in range(len(graph)):
    for j in range(len(graph[0])):
        if graph[i][j] != 0:
            u = i
            v = j
            w = graph[i][j]
            g.add_edge(u, v, w)

# Input the target node
print("-----a Python implement of BELLMAN-FORD algorithm-----")
print("-----------------by GUO DONGFANG----------------------")
print("Please make sure the adjacency matrix of your graph has been correctly written into ./INPUT_bellmanford.txt!")
print("There are totally {} nodes in your input graph.".format(len(graph)))
target = input("Please input your target node (choose from 0 to {}):".format(len(graph)-1))

# Run! and output the solution table
g.bellmanford(int(target))
input("Press Enter to exit.")