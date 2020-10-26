""" GN algorithm helpers. """


from argparse import ArgumentParser
from itertools import combinations


def parse_inputs():
    """ Parser function to take care of the inputs """
    parser = ArgumentParser(description='Input filename and output filename')
    parser.add_argument('threshold', type=int,
                        help='Enter threshold.')
    parser.add_argument('input_file_name', type=str,
                        help='Enter the path of the input file.')
    parser.add_argument('betweenness_output_file_name', type=str,
                        help='Enter the path of the betweenness output file.')
    parser.add_argument('community_output_file_name', type=str,
                        help='Enter the path of the community output file.')
    args = parser.parse_args()

    return (args.threshold, args.input_file_name, args.betweenness_output_file_name,
            args.community_output_file_name)


def parse_csv(data, header=False):
    """ Parse CSV data in RDD """
    data = data.map(lambda x: x.split(','))
    if header:
        header = data.first()
        data = data.filter(lambda x: x != header)
    return data


def build_user_set(data):
    """ Build user dictionaries """
    return data.groupByKey()\
           .map(lambda x: (x[0], set(x[1])))\
           .collectAsMap()


def build_social_graph(users, threshold):
    """ Construct social graph """
    graph, edges = {}, {}
    for u_1, u_2 in combinations(users.keys(), 2):
        if len(users[u_1].intersection(users[u_2])) >= threshold:
            edges[tuple(sorted([u_1, u_2]))] = 0
            if u_1 not in graph:
                graph[u_1] = set()
            if u_2 not in graph:
                graph[u_2] = set()
            graph[u_1].add(u_2)
            graph[u_2].add(u_1)

    return graph, edges


def build_degree_table(graph):
    """ Construct a dictionary of degrees of each node """
    return {n: len(graph[n]) for n in graph}


def build_adjacency_matrix(edges):
    """ Construct the adjacency matrix of the original graph """
    return set(edge for edge in edges)


def remove_highest_edges(graph, edges):
    """ Remove edge(s) with the highest betweenness """
    maximum = 0.0
    for i in edges:
        maximum = max(maximum, edges[i])

    # find the set of edges with the highest betweenness
    edges_to_be_removed = []
    for edge, betweenness in edges.items():
        if betweenness == maximum:
            edges_to_be_removed.append(edge)

    # update edges and graph dictionaries
    for node_1, node_2 in edges_to_be_removed:
        graph[node_1].remove(node_2)
        graph[node_2].remove(node_1)
        del edges[(node_1, node_2)]


def convert_to_list(edges):
    """ Convert dictionary of edges to sorted list """
    res = [[key, value] for key, value in edges.items()]
    res.sort(key=lambda x: (-x[1], x[0]))
    return res


def reset_betweenness(edges):
    """ Reset the betweenness of each edge """
    for i in edges:
        edges[i] = 0


def sort_communities(communities):
    """ Sort communities in by size """
    for com in communities:
        com.sort()

    communities.sort()
    communities.sort(key=len)


def output_betweenness(filename, data):
    """ Save the output to a file """
    with open(filename, 'w') as write_file:
        for pair, value in data:
            write_file.write("('")
            write_file.write(pair[0])
            write_file.write("', '")
            write_file.write(pair[1])
            write_file.write("'), ")
            write_file.write(str(value))
            write_file.write("\n")


def output_communities(filename, data):
    """ Save the output to a file """
    with open(filename, 'w') as write_file:
        for community in data:
            write_file.write(", ".join([_quote(user) for user in community]))
            write_file.write("\n")


def _quote(user_id):
    """ Add quotation marks around the string """
    return "'" + user_id + "'"
