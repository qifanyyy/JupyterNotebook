"""

	created by: masphei @2013
	contact: masphei@gmail.com
	description: PythonFlow class is an implementation of Ford-Fulkerson algorithm which is found in Introduction to Algorithm 3rd Edition. There are several ways of modification to build the program as my thought.
	
"""

import timeit

class PythonFlow:
	# PythonFlow implement Ford-Fulkerson method to maximize flow on graph problems. 
	# example of input text:
	#
	# 0 16 13 0 0 0 
	# 0 0 0 12 0 0
	# 0 4 0 0 14 0
	# 0 0 9 0 0 20
	# 0 0 0 7 0 4
	# 0 0 0 0 0 0
	#
	# (do not forget to put last enter)
    def __init__(self):
		# graph G network
		self.graph = []
		# flow f network
		self.flow = []
		# residual f' network
		self.residual = []
		# total flow which can be retrieved
		self.total_flow = 0
		#file name
		self.file_name = "D:/Copy/Coding/GitHub/PythonFlow/bipartite.txt"
		
		self.load_file()
		# self.print_graph(self.graph)
		row = [0] # source
		for x in range(len(self.graph)):
			self.graph[x].insert(0, 0)
			if x < len(self.graph)/2:
				self.graph[x].append(0)
				row.append(1)
			else:
				self.graph[x].append(1)
				row.append(0)
		row.append(0) # sink
		self.graph.insert(0, row)
		self.graph.append([0 for x in range(len(self.graph)+1)])
		# self.print_graph(self.graph)
		
		self.init_flow()
		self.update_residual()
	
	#input graph from specified file
    def load_file(self):
		counter_row = 0
		counter_col = 0
		row = []
		number = ""
		#iterate whole lines
		for line in open(self.file_name):
			#iterate each character
		    for char in line:
				if char == "\n":
					counter_col += 1
					row.append(int(number.strip()))
					self.graph.append(row)
					row = []
					number = ""
				elif char == " ":
					row.append(int(number.strip()))
					number = ""
				elif char != " ":
					number += char
	
	#initializing flow network
    def init_flow(self):
		number = []
		for element in self.graph:
			for value in element:
				number.append(0)
			self.flow.append(number)
			number = []
			
	#update residual network value based on current flow
    def update_residual(self):
		number = []
		self.residual = []
		for x in range(len(self.graph)):
			for y in range(len(self.graph[x])):
				number.append(self.graph[x][y] - self.flow[x][y])
			self.residual.append(number)
			number = []

    def main_algorithm(self):
		best_path = self.find_best_path()
		# iterate until no augmenting paths exist, it gives sign for maximum flow f
		while len(best_path)!= 0:
			self.apply_path(best_path)
			self.update_residual()
			best_path = self.find_best_path()
		
    def apply_path(self, path):
		cost = self.get_minimum_cost_flow(path)
#		print "applying cost:",cost
		self.total_flow += cost
		source = 0
		for x in path:
			self.flow[source][x] += cost
			source = x
		self.update_residual()
	
    def find_best_path(self):
		# best path is obtained by doing bfs to reveal all available paths and greedy to choose the best path
		# assume that there is no antiparallel edges
		# this method chooses the best path from options
		self.options = []
		self.get_path(0, [])
		if len(self.options) >0:
			self.cost = []
			min_index = -1
			max_flow = 0
			# do such a greedy to get the maximum impact
			for x in range(len(self.options)):
				min = self.get_minimum_cost_flow(self.options[x])
				if max_flow < min:
					max_flow = min
					min_index = x
#			print "Best augmenting path: ",self.options[min_index], "with cost: ", max_flow
			return self.options[min_index]
		else:
			return []
		
	# find the minimum cost flow from augmenting paths
    def get_minimum_cost_flow(self, path):
		source = 0
		min = 9999
		for x in path:
			if min > self.residual[source][x]:
				min = self.residual[source][x]
			source = x
		return min
		
	# get list of available paths from particular vertex
    def get_path(self, vertex, paths):
		options = self.get_options(vertex)
		sink_index = len(self.graph[0]) - 1
		if vertex == sink_index and len(options) == 0:
			self.options.append(paths)
		else:
			# testing: counter = 0
			# testing: while len(self.options) == 0 and counter < len(options):
				# testing: x = options[counter]
			for x in options:
				if x not in paths:
					# generate new path
					new_path = []
					for y in paths:
						new_path.append(y)
					new_path.append(x)
					# iteratively find paths
					self.get_path(x, new_path)			
				# testing: counter += 1
	
	# permute available vertices to generate path
    def get_options(self, initial_vertex):
		retval = []
		index = 0
		for x in self.graph[initial_vertex]:
			if index != initial_vertex and self.residual[initial_vertex][index]!=0:
				retval.append(index)
			index += 1
		return retval
	
	# print graph
    def print_graph(self, graph):
		for x in range(len(graph)):
			print graph[x]

# example of usage
flow = PythonFlow()
print "This is Graph G:"
flow.print_graph(flow.graph)
start = timeit.default_timer()
flow.main_algorithm()
stop = timeit.default_timer()
print "This is Flow f:"
flow.print_graph(flow.flow)
print "This is Residual f':"
flow.print_graph(flow.residual)
print "Total flow: ", flow.total_flow
print "time elapsed: ", (stop - start), " seconds"