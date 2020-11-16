import logging
import os

from Models.Edge import Edge
from Models.Graph import Graph
from Models.Node import Node
import re


class FileController:
    MAX_IDENT = 2  # Maximum length of the node identifier
    MAX_ITEMS = 100  # Maximum number of imported items
    MAX_COST = 30  # Maximum edge cost value
    MAX_NODE_ID = 40  # Maximum node id value

    @classmethod
    def is_path_valid(cls, path):
        """
        Checks if the passed path is valid
        :param path: The path to check
        :return: Boolean: True on valid, false on invalid
        """
        # if path is empty, it is not a valid path
        if path is None:
            return False

        # check if the file exists and that it is accessible
        try:
            if os.path.exists(path):
                file = open(path, 'r')  # opening with write deletes the file contents!
                file.close()
                return True
            else:
                return False
        except OSError:
            # Cannot open the file
            print('[ERROR] The path \'', path, '\' is not a valid path or the file does not exist.')
            return False
        except TypeError:
            # Path is not of type string or os.path, should never happen
            print("[FATAL] Path is in an invalid type!")
            return False

    def import_file_to_graph(self, inputpath):
        """
        Decodes a text file into a Graph object
        :param inputpath: path to definition file
        :return: graph: Imported Graph object
        """
        with open(inputpath, 'r') as file:
            graph = Graph()
            entries = 0
            lines = file.readlines()

            # Check if the file has the correct format:
            # Graph [name] { ... } with // comments allowed
            contents = ""
            for line in lines:
                contents += line
            # set flag re.DEBUG as additional parameter to debug this regex
            match = re.match("(\/\/.*)*Graph\s.+\s{[\s\S]*}", contents)
            if match is None:
                logging.error("The file format is not valid! Check the import specification for the correct format.")
                exit(2)

            # Read the file line by line
            for line in lines:
                if entries >= self.MAX_ITEMS:
                    logging.error("File is too long! Aborting import.")
                    exit(2)

                if line.startswith('//') or line.find(';') == -1:
                    # line is a comment or not a definition
                    continue

                if line.find('-') == -1:
                    # line is a node definition
                    key = line[0: line.find('=')].strip()
                    value = line[line.find('=') + 1:line.find(';')].strip()
                    graph.nodes.append(Node(value, key))
                    logging.debug('Node definition found: %s | %s', value, key)
                elif line.find('-') != -1:
                    # line is an edge definition
                    frm = line[0: line.find('-')].strip()
                    to = line[line.find('-') + 1: line.find(':')].strip()
                    cost = line[line.find(':') + 1:line.find(';')].strip()
                    graph.edges.append(Edge(frm, to, int(cost)))
                    logging.debug('Edge definition found: %s | %s | %s', frm, to, cost)

                entries += 1

            for node in graph.nodes:
                logging.debug('%s - %s', node.node_id, node.name)

            for edge in graph.edges:
                logging.debug('%s - %s: %s', edge.frm, edge.to, edge.cost)

            file.close()
        return graph

    def validate_imported_data(self, graph):
        """
        Validates the data with the set constants. Exits on invalidity
        :param graph: Graph to validate
        """
        # Assert that all node definitions are valid
        for node in graph.nodes:
            # Assert that the node names are not longer than the global setting MAX_IDENT
            if len(node.node_id) > self.MAX_IDENT:
                logging.error("Node has a name longer than MAX_IDENT (%s): '%s' with Node ID %s",
                              self.MAX_IDENT, node.name, node.node_id)
                exit(2)
            # Assert that the node ids are not greater than the global setting MAX_NODE_ID
            if int(node.node_id) > self.MAX_NODE_ID:
                logging.error("Node has an ID value greater than MAX_NODE_ID (%s): '%s' with Node ID %s",
                              self.MAX_NODE_ID, node.name, node.node_id)
                exit(2)
            if not graph.find_edges_for_node(node):
                logging.error("Node has no edges that connect to it: '%s' with Node ID %s",
                              node.name, node.node_id)
                exit(2)

        # Assert that all edge dfinitions are valid
        for edge in graph.edges:
            # Assert that every edge has a source and destination that exists
            if graph.find_node_by_name(edge.frm) is None or graph.find_node_by_name(edge.to) is None:
                logging.error("Edge references to a node that does not exist: '%s' to '%s' with cost '%s'",
                              edge.frm, edge.to, edge.cost)
                exit(2)
            # Assert that the cost of every edge is not greater than the global setting MAX_COSTS
            if edge.cost > self.MAX_COST:
                logging.error("Edge has a cost value greater than MAX_COST: '%s' to '%s' with cost '%s'",
                              edge.frm, edge.to, edge.cost)
                exit(2)
            # Assert that there are no duplicate edges
            for existing_edge in graph.edges:
                if(edge.to == existing_edge.frm) and (edge.frm == existing_edge.to):
                    logging.error("Edge has a disallowed duplicate: '%s' to '%s' with cost '%s'",
                                  edge.frm, edge.to, edge.cost)
                    exit(2)

        # Assert that graph is connected
        visited = [graph.nodes[0]]
        logging.debug("Visited: %s", visited)
        # Start at one node and add every reachable node from there (repeat for every reachable node)
        for node in visited:
            edges = graph.find_edges_for_node(node)
            for edge in edges:
                if edge.to != node.name:
                    next_node = graph.find_node_by_name(edge.to)
                else:
                    next_node = graph.find_node_by_name(edge.frm)
                if next_node not in visited:
                    visited.append(next_node)
        # If all reachable, visited nodes are less than all nodes in the graph, the graph is not fully connected
        if len(visited) < len(graph.nodes):
            logging.error("Graph is not fully connected!")
            exit(2)

    @classmethod
    def export_result_to_file(cls, result, exportpath):
        """
        Writes the result of the algorithm to a file
        :param result: Nodes List to export
        :param exportpath: True if successful, False if invalid path or writing failed
        :return:
        """
        # Create a new file at given path, catch if not a valid path
        try:
            file = open(exportpath, 'w+')
            # Dump the contents of the graph object into the file
            file.write("Name\tID\tCost to Root\tNext Hop to Root\tBroadcast Count\n")
            for node in result:
                if node.next_hop.cost == -1:
                    next_hop = "Is Root"
                else:
                    next_hop = (node.next_hop.frm + "->" + node.next_hop.to + ": " + str(node.next_hop.cost))
                file.write(node.name + "\t\t" +
                           node.node_id + "\t" +
                           str(node.cost) + "\t\t\t\t" +
                           "%-15s" % next_hop + "\t\t" +
                           str(node.count) + "\n")
            file.close()
            return True
        except IOError:
            print('[ERROR] Could not write to file', exportpath, ". Is it a valid file?")
            return False
