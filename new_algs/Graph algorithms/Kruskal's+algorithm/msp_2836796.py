import sys
import Graph

def Kruskal(graph):
	sets = []
	results = []
	for i in range(graph.count):
		sets.append(set([i]))
	for edge in graph.edges:
		if edge.node1 not in sets[edge.node2] and edge.node2 not in sets[edge.node1]:
			results.append(edge)
			sets[edge.node2].add(edge.node1)
			sets[edge.node1].add(edge.node2)
			for i in sets[edge.node1]:
				sets[i] = sets[i].union(sets[edge.node1])
			for i in sets[edge.node2]:
				sets[i] = sets[i].union(sets[edge.node2])
	return results

def main():
	if(len(sys.argv) < 2):
		print("Usage: python msp_2836796.py input_n.txt > output_n.txt")
		sys.exit()
	myGraph = Graph.read_file(sys.argv[1])
	results = Kruskal(myGraph)

	for result in results:
		print(result)

if __name__ == '__main__':
	main()