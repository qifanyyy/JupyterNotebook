from DijkstraPriorityQueue import DijkstraPriorityQueue as dpq

def valid_within_bounding_box(start, end, pt):
	if end is None:
		return True
	small_x, large_x = min(start[0], end[0]), max(start[0], end[0])
	small_y, large_y = min(start[1], end[1]), max(start[1], end[1])
	return pt[0] <= large_x and pt[0] >= small_x and pt[1] <= large_y and pt[1] >= small_y 

def shortest_path(adj_list, source, end=None):
	"""
	Runs Dijkstra's algorithm on the graph represented by adj_list. 

	@param		adj_list	A dictionary mapping each node to a list of (neighbor, edge_weight)
	@param		source		the source node from which to begin our search
	@return		dist 		a dictionary mapping each node to its distance from "source"
	@return		p 			a "node to parent" mapping which can be traversed to yield the paths themselves
	"""
	dist = {}
	p = {}
	for node in adj_list:
		if valid_within_bounding_box(source, end, node):
			dist[node] = float("inf")
			p[node] = None
	dist[source] = 0

	priority_queue = dpq()
	priority_queue.build_heap([[v, k] for k, v in dist.items()])

	while len(priority_queue) > 0:
		# print priority_queue.heapList		
		curr = priority_queue.deleteMin()[1]
		if curr == end:
			return dist, p
		# print curr
		for nbr, wt in adj_list[curr]:
			# print nbr, wt, wt+dist[curr], dist[nbr]
			if valid_within_bounding_box(source, end, nbr) and wt + dist[curr] < dist[nbr]:
				dist[nbr] = wt + dist[curr]
				p[nbr] = curr
				priority_queue.update_priority(nbr, dist[nbr])
	return dist, p


def main():
	"""
	Executes the application.
	"""
	adj_list = {1: [(2, 15), (3, 71)],
				2: [(3, 7), (4, 1)],
				3: [(4, 19)],
				4: [(3, 1)]}
	print shortest_path(adj_list, 1)
	

if __name__ == "__main__":
	main()