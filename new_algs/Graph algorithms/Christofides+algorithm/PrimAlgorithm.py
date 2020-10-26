import sys
import matplotlib.pyplot as plt

class PrimAlgorithm: 

	def __init__(self, vertices): 
		self.V = len(vertices[0])
		self.graph = vertices

	# A utility function to print the constructed MST stored in parent[] 
	def printMST(self, parent): 
		print("Edge \tWeight")
		for i in range(1, self.V): 
			print(parent[i], "-", i, "\t", self.graph[i][ parent[i] ] )

	# A utility function to find the vertex with  
    # minimum distance value, from the set of vertices  
    # not yet included in shortest path tree 
	def minKey(self, key, mstSet): 

		min = sys.maxsize   

		for v in range(self.V): 
			if key[v] < min and mstSet[v] == False: 
				min = key[v] 
				min_index = v 

		return min_index 

	# Function to construct and print MST for a graph  
    # represented using adjacency matrix representation 
	def primMST(self): 

		key = [sys.maxsize] * self.V 
		parent = [None] * self.V 
		
		key[0] = 0
		mstSet = [False] * self.V 

		parent[0] = -1 

		for cout in range(self.V): 

			u = self.minKey(key, mstSet) 

			mstSet[u] = True
            
			for v in range(self.V): 
				if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]: 
						key[v] = self.graph[u][v] 
						parent[v] = u 
						
		return parent
