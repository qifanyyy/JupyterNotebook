"""
    Author: Hsuan-Hau Liu
    Date:   June, 23rd, 2019
    Description: Find the optimal Yelp user community clustering using GN algorithm.
"""


from community_detection import gn, util

# PySpark import
from pyspark import SparkContext


def main():
    """ Main """
    context = SparkContext('local', 'GN')
    context.setLogLevel('OFF')

    # Read inputs
    threshold, input_name, b_output_name, c_output_name = util.parse_inputs()

    # Parse data
    data = util.parse_csv(context.textFile(input_name), header=True)
    user_set = util.build_user_set(data)
    graph, edges = util.build_social_graph(user_set, threshold)
    degree_table = util.build_degree_table(graph)
    adjacency_matrix = util.build_adjacency_matrix(edges)
    num_of_edges = len(edges)

    # calculate betweenness of the initial graph
    gn.calculate_betweenness(graph, edges)
    util.output_betweenness(b_output_name, util.convert_to_list(edges))

    # keep removing the edges with highest betweenness
    highest_modularity = -1.0
    optimal_communities = []
    while edges:
        communities = gn.find_communities(graph)
        modularity = gn.calculate_modularity(communities, degree_table, adjacency_matrix, num_of_edges)
        if modularity > highest_modularity:
            highest_modularity = modularity
            optimal_communities = communities

        util.remove_highest_edges(graph, edges)
        util.reset_betweenness(edges)
        if edges:
            gn.calculate_betweenness(graph, edges)

    util.sort_communities(optimal_communities)
    util.output_communities(c_output_name, optimal_communities)


if __name__ == '__main__':
    main()
