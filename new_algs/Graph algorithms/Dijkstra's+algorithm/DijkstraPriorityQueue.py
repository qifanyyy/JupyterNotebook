class DijkstraPriorityQueue:
	"""
	An augmented priority queue for use with Dijkstra's algorithm.
	"""	

	def __init__(self):
		"""
		Initializes a new Priority Queue for use with Dijkstra's algorithm (implemented as a heapmap).
		"""
		self.heapList = [0]
		self.size = 0
		# A map from an element to its index in our implicit heap representation.
		self.element_map = {}

	def __len__(self):
		return self.size

	def build_heap(self, kv_list):
		"""
		Populate internal values with elements from kv_list and heapify.

		@param	kv_list		The list of kv_pairs to include in our heap
		"""
		self.heapList = [0] + kv_list
		self.size = len(kv_list)
		# A map from an element to its index in our implicit heap representation.		
		self.element_map = {}
		for idx in xrange(1, self.size):
			self.element_map[self.heapList[idx][1]] = idx
		self.heapify()

	def heapify(self):
		"""
		Heapifies the heapList.
		"""
		for i in xrange(self.size / 2, 0, -1):
			self.percolateDown(i)

	def insert(self, key, value):
		"""
		Inserts a key-value pair into the priority queue while maintaining the heap properties.

		@param		key 	The key through which we'll maintain heap operations
		@param		value 	The value associated with that key
		"""
		self.size += 1
		self.heapList.append([key, value])
		# Only works if there are no duplicate keys. (Functional for Dijkstra b/c graph nodes are unique.)
		self.element_map[value] = self.size
		# Heapify up.
		self.percolateUp(self.size)

	def percolateUp(self, i):
		"""
		Ensures that the heap element at i maintains the heap property with respect to its ancestors.

		@param 		i 		The index at which we begin the "heapify up" operation.
		"""
		while i / 2 > 0:
			# print "i/2", i / 2
			# print "i/2", "i", self.heapList[i / 2][0], self.heapList[i][0]
			# Compare current node's heap key with its parent (available at idx i/2).
			if self.heapList[i / 2][0] > self.heapList[i][0]:
				# print True
				# Update the element map in anticipation of the swap.
				self.element_map[self.heapList[i][1]] = i / 2
				self.element_map[self.heapList[i / 2][1]] = i
				# Swap current element with its parent.
				temp = self.heapList[i / 2]
				self.heapList[i / 2] = self.heapList[i]
				self.heapList[i] = temp
			else: 
				break
			i /= 2

	def deleteMin(self):
		"""
		Deletes the element with the lowest-valued key from the heap and returns the associated k-v pair.		
		"""
		# Swap the minimum valued element with the element at the end.		
		temp = self.heapList[1]
		self.heapList[1] = self.heapList[self.size]
		self.heapList[self.size] = temp

		# Delete the minimum element.
		retVal = self.heapList.pop()
		self.size -= 1

		# Update the element map accordingly.
		del self.element_map[retVal[1]]

		if self.size:
			self.element_map[self.heapList[1][1]] = 1

		# Heapify down.
		self.percolateDown(1)
		return retVal

	def percolateDown(self, i):
		"""
		Ensures that the heap element at i maintains the heap property with respect to its descendants.

		@param 		i 		The index at which we begin the "heapify down" operation.		
		"""
		while i * 2 <= self.size:
			min_child_idx = self.findMinChild(i)
			if self.heapList[min_child_idx][0] < self.heapList[i][0]:
				# Update the element map in anticipation of the swap.
				self.element_map[self.heapList[i][1]] = min_child_idx
				self.element_map[self.heapList[min_child_idx][1]] = i

				# Swap elements.
				temp = self.heapList[i]
				self.heapList[i] = self.heapList[min_child_idx]
				self.heapList[min_child_idx] = temp
			else: 
				break
			i = min_child_idx

	def findMinChild(self, i):
		"""
		Determines the index of the child of self.heapList[i] with minimum priority.

		@param		i 		The index in the implicit heap whose children we will compare
		@return 			The index of the child of element at "i" whose priority is smaller
		"""
		if i * 2 == self.size:
			return self.size
		if self.heapList[i * 2][0] < self.heapList[i * 2 + 1][0]:
			return i * 2
		return i * 2 + 1

	def update_priority(self, value, new_priority):
		"""
		Updates the existing (priority, value) pair in the heapList with a new priority.

		@param 		value 			The node in the graph whose associated key priority we wish to modify
		@param		new_priority	The new priority for that node in the graph
		"""
		if value in self.element_map:
			idx = self.element_map[value]
			self.heapList[idx][0] = new_priority
			self.percolateUp(idx)	
