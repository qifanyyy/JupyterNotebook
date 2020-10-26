'''

Kruskal's and Prim's Algorithms

'''


# Imports
from queue import Queue


# Boiler plate

# dictionary reversal alg
drev = lambda dct: dict([(v, k) for k,v in dct.items()])

# Dictionary sorting function
sortD = lambda dct: [drev(dct)[i] for i in sorted([v for _, v in dct.items()])]

# removing items from an array
def strip(arr:list, *items)->list: 
	for item in items: 
		arr.pop(arr.index(item))

	return arr




# Main graph
class Graph:
	def __init__(self, edges: dict): # edge is input as {"x-y":4, "a-b":6, etc.}
		self.getVertexPair = lambda edge: edge.replace(" ", "").split("-")

		self.edges = edges		
		self.edge_name = [k for k, _ in edges.items()]
		self.vertices = self.getVertices(self.edge_name)
		self.vNeighbours = self.getNeighbours(self.edge_name) # vertex neighbours
		

	def getVertices(self, gr): # get vertices from list of edges
		vertices = []
		
		for edge in gr:
			a, b = self.getVertexPair(edge)

			if a not in vertices: vertices.append(a)
			if b not in vertices: vertices.append(b)

		return vertices

	def getNeighbours(self, gr): # gets vertex neighbours
		dct = dict([(v, []) for v in self.vertices])

		for edge in self.edges:
			a, b = self.getVertexPair(edge)

			if a not in dct[b]: dct[b].append(a)
			if b not in dct[a]: dct[a].append(b)

		return dct

	def addEdge(self, name, weight):
		self.edges[name] = weight
		self.edge_name = [k for k, _ in self.edges.items()]
		self.vertices = self.getVertices(self.edge_name)
		self.vNeighbours = self.getNeighbours(self.edge_name)

	def __str__(self):
		return f"{self.edges}"

	def __repr__(self):
		return f"[{', '.join([e for e, _ in self.edges.items()])}]"



	# boolean version of breadth first search
	# O(V+E)
	def bfs(self, start, end) -> bool: # check if 2 nodes are already connected
		try:
			Q = Queue(limit=len(self.edges.items())*2) # Vertex Queue
			discovered = dict([(v, False) for v in self.vertices])
			parent = dict([(v, None) for v in self.vertices])

			Q.enqueue(start)
			discovered[start] = True
			found = False

			while len(Q) > 0 and not found:
				v = Q.dequeue()

				for u in self.vNeighbours[v]:
					if not discovered[u] and not found:
						Q.enqueue(u)
						discovered[u] = True
						parent[u] = v
						found = True if u == end else found

			if found:return True # there is a path
			else:return False # there is no path

		except KeyError:
			return False




	def kruskal(self): # find a min-spanning tree within a graph
		available_edges = sortD(self.edges) # sorts the edges by edge weight
		unvisited = [v for v in self.vertices] # unvisited vertices list
		valence = dict([(v, 0) for v in unvisited]) # list of valences of all the vertices
		Tree = Graph({}) # this is a graph of the min-spanning tree

		for edge in available_edges: # iterates through every edge (lowest weight val -> highest weight val)
			x, y = self.getVertexPair(edge) # x and y are the start an end points of each edge
			
			if x in unvisited or y in unvisited:
				Tree.addEdge(edge, self.edges[edge])
				if x in unvisited: strip(unvisited, x) # removes x from "unvisited" list, marking it as visited
				if y in unvisited: strip(unvisited, y) # removes y from "unvisited" list, as above

			elif not Tree.bfs(x, y): # do a BFS and if val == False then carry on
				Tree.addEdge(edge, self.edges[edge])


		return Tree



	def getNearestEdge(self, tree): # O(VE + EV^2+ VE^2)
		nearest = [None, None]

		for vertex in tree.vertices: # O(V)
			a = [edge for edge, _ in self.edges.items() if vertex in edge]# O(E)
			for edge in a: # O(E)
				x, y = self.getVertexPair(edge)

				if not tree.bfs(x,y): # O(V+E)
					if nearest[1] == None: nearest = [edge, self.edges[edge]]
					elif self.edges[edge] < nearest[1] and edge not in tree.edge_name: nearest = [edge, self.edges[edge]]

		return nearest[0]


	# Prim's algorithm
	def prim(self, start): # O(ElogV)
		tree = Graph({})
		tree.vertices.append(start)

		while len(tree.vertices) < len(self.vertices):
			s = self.getNearestEdge(tree)
			tree.addEdge(s, self.edges[s])


		return tree



		

# Runtime
if __name__ == "__main__":
	a = Graph({
		
		"a-b":4.6, 
		"a-g":2.3,
		"a-h":1.8,

		"b-c":2.4,
		"b-d":3.5,
		"b-f":3.4,

		"c-d":3.1,
		"c-h":5.2,

		"d-e":3.7,

		"e-f":2.8,

		"f-g":8.7,

		"g-h":2.5
		
		})

	print(a.vertices)
	print(repr(a.kruskal()))
	print(repr(a.prim("a")))