#superclass for directed graphs with weighted edges.
class Graph():
	def __init__(self, matrix):
		self.data = matrix
	
	#use slices to get weights along a path:
	def __getitem__(self, path):
		i = 0
		result = []
		while i+1 < len(path):
			result.append(self.data[path[i]][path[i+1]])
			i = i+1
		return result
		
	def __setitem__(self, path, values):
		i = 0
		while i+1 < len(path):
			self.data[path[i]][path[i+1]] = values[i]
			i = i+1

	def __len__(self):
		return len(self.data)

	def link(self, from_node, to_node, weight = 1):
		self.data[from_node][to_node] = weight
	
	def get_outflow(self, node):
		return self.data[node]
		
	def get_inflow(self, node):
		return [each_row[node] for each_row in self.data]
		
	def add_node(self, loc):
		filler = [0 for _ in self.data]
		self.data.insert(loc,filler)
		for each_row in self.data:
			each_row.insert(loc,0)
	
	def dim(self):
		return range(0,len(self.data))
		
	def get_successors(self, node):
		results = []
		for i in self.dim():
			if self.data[node][i] != 0:
				results.append(i)
		return results


#Network tracks both routes and flow, each of which are instances of Graph.
class Network():
	def __init__(self, matrix, starts, ends):
		self.data = Graph(matrix)
		self.starts = starts
		self.ends = ends
		self.augment()
		
		#initialize zero matrix for tracking flow through network:
		self.flow = Graph([[0 for _ in self.data.dim()] for _ in self.data.dim()])
		
	def augment(self):
		self.data.add_node(0) #prepend node
		self.data.add_node(len(self.data)) #append node
		
		#all node labels are now off by 1:
		self.starts = [each + 1 for each in self.starts]
		self.ends = [each + 1 for each in self.ends]
		
		self.start = 0 #initial node label
		self.end = len(self.data) - 1 #final node label
		
		starts_outflow = []
		for each in self.starts:
			m = sum(self.data.get_outflow(each))
			starts_outflow.append(m)
		m = sum(starts_outflow)
		
		ends_inflow = []
		for each in self.ends:
			n = sum(self.data.get_inflow(each))
			ends_inflow.append(n)
		n = sum(ends_inflow)
		
		for each in self.starts:
			self.data.link(self.start,each,m)
			
		for each in self.ends:
			self.data.link(each,self.end,n)

	def flow_thru_path(self, path):
		f = min(self.get_residual_flow(path))
		self.update_flow(path, f)

	def get_residual_flow(self, path):
		#self.data[path] - self.flow[path]
		return [x-y for (x,y) in zip(self.data[path], self.flow[path])]

	def update_flow(self, path, water):
		#flow water down the path
		#self.flow[path] += self.flow[path] + water
		stream = [water] * len(path)
		self.flow[path] = [x+y for (x,y) in zip(self.flow[path], stream)]
	
	#returns a list of successor nodes with positive residual flow capacity remaining.
	def get_residual_successors(self, node):
		residuals = [x-y for (x,y) in zip(self.data.get_outflow(node), self.flow.get_outflow(node))]
		result = []
		for ind, val in enumerate(residuals):
			if val != 0:
				result.append(ind)
		return result
	
	#BFS on residual network. Returns dict of traversal history.
	def BFS(self, start, end):
		Q = [start]
		discovered = [start]
		pred = {}
		#instead of relying on defaultdict:
		for each_node in self.data.dim():
			pred[each_node] = None
		while Q:
			v = Q.pop(0)
			if v == end:
				return pred
			else:
				for each in self.get_residual_successors(v):
					if each not in discovered:
						discovered.append(each)
						pred[each] = v
						Q.append(each)
		#no paths found from start to end:
		return None

#the core loop for the algorithm:
def edmondsKarp(matrix, starts, ends):
	network = Network(matrix, starts, ends)
	path = network.BFS(network.start, network.end)
	while path:
		path = build_path(path, network.start, network.end)
		network.flow_thru_path(path)
		path = network.BFS(network.start, network.end)
	return network.flow, network.flow.get_inflow(network.end)
	
#turns the dict result from BFS into an actual path:
def build_path(path,start,end):
	result = [end]
	pred = end
	while pred != start:
		pred = path[pred]
		result.insert(0,pred)
	return result