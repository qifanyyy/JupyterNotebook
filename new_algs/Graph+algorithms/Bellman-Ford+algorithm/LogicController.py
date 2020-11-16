import logging
from typing import List

from Models.Graph import Graph
from Models.Node import Node


class LogicController:
    def minimize_graph(self, graph):
        """
        Minimizes the passed graph with the modified Bellman-Ford algorithm
        :param graph: The graph to minimize
        :returns: List<Node>: The result (all nodes with minimal weight to root etc)
        """
        logging.debug('Starting modified Bellman-Ford algorithm with %s nodes and %s edges...',
                      len(graph.nodes), len(graph.edges))

        # Repeat for every node in the graph
        for curr_node in graph.nodes:
            self.broadcast(graph, curr_node)

        # Print the graph and return the updated nodes
        self.print_result(graph.nodes)
        return graph.nodes

    def broadcast(self, graph, curr_node):
        """
        Broadcasts a message (root_id and cost) to the neighboring nodes of curr_node
        :param graph: The graph in which the node sits
        :param curr_node: The current broadcasting node
        """
        logging.debug("Current node (%s = %s) is broadcasting...", curr_node.name, curr_node.root_id)
        # Broadcast cost and root_id to next node of every edge of the current node
        current_edges = graph.find_edges_for_node(curr_node)
        curr_node.count += 1
        for edge in current_edges:
            # Find the node the edge points to
            if edge.frm == curr_node.name:
                next_node = graph.find_node_by_name(edge.to)
            else:
                next_node = graph.find_node_by_name(edge.frm)
            logging.debug("Sending root_id %s and cost %s to next_node (%s = %s)...",
                          curr_node.root_id, curr_node.cost, next_node.name, next_node.root_id)

            # Calculate the new cost to root
            curr_cost = curr_node.cost + edge.cost

            # Update cost and root_id (only if next_node id is greater curr_node id)
            if next_node.root_id > curr_node.root_id:
                logging.debug("next_node root_id %s is larger than curr_node root id %s, updating values...",
                              next_node.root_id, curr_node.root_id)
                next_node.root_id = curr_node.root_id
                next_node.cost = curr_cost
                next_node.next_hop = edge
                logging.debug("Node %s now has root_id %s and cost %s",
                              next_node.name, next_node.root_id, next_node.cost)
                self.broadcast(graph, next_node)
            # Update cost of root node only if it is smaller than the current cost of the next node
            elif (next_node.root_id == curr_node.root_id) and (curr_cost < next_node.cost):
                logging.debug("next_node root_id %s is smaller or equal to curr_node root id %s with smaller cost, "
                              "updating...",
                              next_node.root_id, curr_node.root_id)
                next_node.cost = curr_cost
                next_node.next_hop = edge
                logging.debug("Node %s now has root_id %s and cost %s",
                              next_node.name, next_node.root_id, next_node.cost)
                self.broadcast(graph, next_node)

    @classmethod
    def print_result(cls, nodes):
        """
        Print passed nodes list in a very pretty way
        :param nodes: The nodes to print
        """
        logging.info("Nodes with smallest cost to root %s:", min(nodes, key=lambda x: x.node_id).name)
        print("Name\tID\tCost to Root\tNext Hop to Root\tBroadcast Count")
        nodes_str = ""
        for node in nodes:
            if node.next_hop.cost == -1:
                next_hop = "Is Root"
            else:
                next_hop = (node.next_hop.frm + "->" + node.next_hop.to + ": " + str(node.next_hop.cost))
            nodes_str += (node.name + "\t" +
                          node.node_id + "\t" +
                          str(node.cost) + "\t\t" +
                          "%-15s" % next_hop + "\t\t" +
                          str(node.count) + "\n")
        print(nodes_str)
