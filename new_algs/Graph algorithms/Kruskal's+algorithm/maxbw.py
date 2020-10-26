import heap
import graph
import array
import uf 

def dkt(G, s_label, t_label, use_heap=1):
	"""
	Using Dijkstra's algorithm to find the MAX_BANDWIDTH from source to destination.
	G is a graph represented by adjacency list, 
	the labels for vertices in which must be consecutive positive integers.
	s_label is the unique label for source vertex
	t_label is the unique label for destination vertex
	"""
	if(use_heap != 1):
		return dkt_no_heap(G, s_label, t_label)
	h = heap.Heap(G.V, [])
	parent = array.array('I', [0] * (h.max_size + 1))
	for v in G.adj_list[1:]:
		h[v.label] = 0
		parent[v.label] = 0
	h[s_label] = graph.MAX_EDGE_WEIGHT 
	while (h.has(t_label) ):
		u_label_weight = h.pop()
		if(h[u_label_weight[0]] == 0): break
		u = G[u_label_weight[0]]
		for v_label_weight in u.list:
			new_bandwidth = min(h[u_label_weight[0]], v_label_weight[1])
			if(new_bandwidth > h[v_label_weight[0]]):
				h[v_label_weight[0]] = new_bandwidth
				parent[v_label_weight[0]] = u_label_weight[0]
	return [h[t_label], parent]

def dkt_no_heap(G, s_label, t_label):
	h = array.array('I', [0]* (G.V + 1))
	s = array.array('c', ['0']* (G.V + 1))
	parent = array.array('I', [0] * (G.V + 1))
	for v in G.adj_list[1:]:
		h[v.label] = 0
		s[v.label] = '1'
		parent[v.label] = 0
	h[s_label] = graph.MAX_EDGE_WEIGHT
	while (s[t_label] == '1'):
		max_w = h[0]
		max_w_i = 0 
		for i in range(1,G.V+1):
			if(s[i] == '1' and h[i] > max_w):
				max_w = h[i]
				max_w_i = i
		u_label_weight = [max_w_i, max_w];
		s[u_label_weight[0]] = '0'
		if(h[u_label_weight[0]] == 0): return [0, parent]
		u = G[u_label_weight[0]]
		for v_label_weight in u.list:
			new_bandwidth = min(h[u_label_weight[0]], v_label_weight[1])
			if(new_bandwidth > h[v_label_weight[0]]):
				h[v_label_weight[0]] = new_bandwidth
				parent[v_label_weight[0]] = u_label_weight[0]
	return [h[t_label], parent]

def krsk(G, s_label, t_label):
	"""
	Using Kruskal's algorithm to find the maximal bandwidth problem
	"""
	parent = array.array('I', [0] * (G.V + 1))
	mst = map(graph.Vertex, range(0, G.V + 1)) 
	e = G.edge_list()
	h = heap.Heap(len(e[1]) - 1, e[1][1:], "max")
	for v in G.adj_list[1:]:
		v.make_set()
	while( h.size > 1 and uf.find(G[ s_label ]) != uf.find(G[ t_label ]) ):
		[key, value] = h.pop()
		u = uf.find( e[0][key][0] )
		v = uf.find( e[0][key][1] )
		if(u != v):
			mst[ e[0][key][0].label ].add_adjacency_vertex( e[0][key][1].label, h[key])
			mst[ e[0][key][1].label ].add_adjacency_vertex( e[0][key][0].label, h[key])
			uf.union(u, v)
	if(uf.find(G[ s_label ]) != uf.find(G[ t_label ]) ):
		return [0, parent]
	else:
		max_bandwidth = dfs(graph.Graph(mst), s_label, t_label, graph.MAX_EDGE_WEIGHT, parent)
		return [max_bandwidth, parent]
def dfs(G, s, t, bw, p):
	for adj in G[s].list:
		if(adj[0] == t):
			return min(bw, adj[1])
		if(p[ adj[0] ] == 0):
			p[ adj[0] ] = s
			ret = dfs(G, adj[0] , t, min(bw, adj[1]), p)
			if(ret != -1):
				return ret 
	return -1
