# An implementation of Kosaraju's algorithm to find
# strongly connected components of directed graph.

from collections import defaultdict

g = defaultdict(list)			# Stores graph
g_reversed = defaultdict(list)	 	# Graph with reversed edges
connected = defaultdict(list)	 	# Contains lists of strongly connected nodes(after execution of the algorithm)
explored = defaultdict(int)		# Flags for exploring graph
reverse_finish = {}			# Mapping of finishing time of first pass to nodes

t = 0		# Number of nodes processed
s = 0		# Current source vertex


# dfs(), dfs_loop(): functions for the first pass through the graph
# dfs_g_rev(), dfs_loop_g_rev(): functions for the second pass through the graph

def dfs(g, v):
	global t
	explored[v] = 1
	connected[s].append(v)
	for j in g[v]:
		if not explored[j]:
			dfs(g, j)


def dfs_loop(g):
	global s
	s = 0
	i = len(g)
	while i > 0:
		if not explored[reverse_finish[i]]:
			s = reverse_finish[i]
			dfs(g, s)
		i = i - 1
	explored.clear()


def dfs_g_rev(g, v):
	global t
	explored[v] = 1
	for j in g[v]:
		if not explored[j]:
			dfs_g_rev(g, j)
	t = t + 1
	reverse_finish[t] = v


def dfs_loop_g_rev(g):
	global t
	t = 0
	i = len(g)
	while i > 0:
		if not explored[i]:
			dfs_g_rev(g, i)
		i = i-1
	explored.clear()


with open('test.txt', 'r') as inputFile:
	for line in inputFile:
		u = int(line.split()[0])
		v = int(line.split()[1])
		g[u].append(v)
		g_reversed[v].append(u)

dfs_loop_g_rev(g_reversed)
dfs_loop(g)

result = [a for a in connected.values()]
print(result)


# provided test file test.txt
#
# 1 7
# 4 1
# 7 9
# 9 6
# 3 9
# 6 3
# 8 2
# 2 5
# 5 8
# 7 4
# 6 8
#
# e.g: 1 7 denotes a directed edge from node 1 to 7

# expected output
# [[8, 2, 5], [9, 6, 3], [7, 4, 1]]
# the above is a list of nodes that are strongly connected

