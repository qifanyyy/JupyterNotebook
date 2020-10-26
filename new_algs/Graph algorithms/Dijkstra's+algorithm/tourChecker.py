# 
#        Checks if the output is a valid path
#     Usage: python tourChecker.py input_file output_file
#     Note : input_fie and tn_graph.txt must be in the valid format
# 
import sys
import networkx as nx

GRAPH_FILE = 'tn_graph.txt'

cities   = []
path     = []
no_nodes = 0
no_edges = 0
G = nx.Graph()

def readInput(inputFile):
	with open(sys.argv[1]) as f:
		f.readline().strip()
		for line in f:
			cities.append(int(line))


def readGraph(graph_file):
	with open(graph_file) as f:
		no_nodes = int(f.readline().strip())    # No of nodes
		[f.readline() for i in range(no_nodes)]

		no_edges = int(f.readline().strip())
		for i in range(no_edges):
			l = f.readline().split()
			node1 = int(l[0])
			node2 = int(l[1])
			weigh = G.get_edge_data(node1, node2)
			if weigh is None:
				G.add_edge(node1, node2, dist=float(l[3]))
			else:
				G[node1][node2][WEI] = min(weigh[WEI], float(l[3]))


def readOutput(output_file):
	with open(output_file) as f:
		for line in f:
			path.append(int(line.strip()))


def inSequence():
	i = 0
	for j in path:
		if j == cities[i]:
			i += 1
		if i == len(cities):
			break;

	if i == len(cities):
		return True
	return False


def getDistance():
	distance = 0.0
	node1 = path[0]
	for i in path[1:]:
		edge = G.get_edge_data(node1, i)
		if edge is None:
			print 'Invalid edge detected (', node1, ', ', i, ')'
			sys.exit(0)

		distance += edge['dist']
		node1 = i

	return distance


def validateOutput():
	if path[0] != cities[0] or path[-1] != cities[0]:
		print '[!] Error in starting point or ending point'
		sys.exit(0)

	if not inSequence():
		print '[!] Cities not visited in sequence'
		sys.exit(0)


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Usage: '+sys.argv[0]+' input_file output_file'
		sys.exit(0)

	readInput(sys.argv[1])
	readGraph(GRAPH_FILE)
	readOutput(sys.argv[2])
	validateOutput()
	distance = getDistance()
	print '[+] Nodes are valid'
	print '[i] Length of the path: ', distance
