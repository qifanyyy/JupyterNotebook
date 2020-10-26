import numpy as np
import vertex as vtx
import graph as gp
def print_path(d,mat,s,t):
	path = []
	s = s-1
	t = t-1
	i = t
	max_bw = 100000000000000000
	path.append(i+1)
	while (i!=s):
		u=i
		#print 'u', u
		path.append(int(d[i]+1))
		i = d[i]
		v=i
		#print 'v', v
		#print 'wt', mat[u][v]
		if(mat[u][v]<max_bw):
			max_bw=mat[u][v]
	ret = ''
	for i in range(len(path)):
		ret = ret + str(path[len(path)-i-1]) + ' -> '
	#print
	#print 'max bw path =\n', ret 
	#print 'max bw = ', max_bw
	#print
	val =[ret,max_bw]
	return val

def algo1(g,s,t):
	#print '\ns', s, 't', t
	adj_list  = g[0]
	edge_wts = g[1]
	s = s-1
	t = t-1
	no_of_vertices = len(adj_list)
	bw = np.zeros(no_of_vertices)
	dad = np.zeros(no_of_vertices)
	status = []

	for i in range(no_of_vertices):
		status.append(-1) # -1 for unseen
	status[s] = 1 # 1 for in-tree

	bw[s] = 100000000000000 # +inf

	for i in range(len(adj_list[s])):
		w =  adj_list[s][i]

		w = w-1
		status[w] = 0 #fringe

		bw[w] = edge_wts[s][w]
		dad[w]=s
	
	while (status[t] != 1): #while t is not in-tree
		flag = 1

		# pick a fringe of the max bw
		m = -1
		max_bw_index = -1
		for i in range(len(status)):
			if(status[i] == 0): 
				if(bw[i]>m):
					m = bw[i]
					max_bw_index = i


		v = max_bw_index
		status[v] = 1
		for i in range(len(adj_list[v])):
			w =  adj_list[v][i]
			w = w-1
			if(status[w] == -1):#if unseen
				status[w] = 0 #make fringe
				bw[w] = min(bw[v], edge_wts[v][w])
				dad[w] = v
			else:
				if(status[w] == 0 and bw[w]< min(bw[v], edge_wts[v][w])):# if fringe
					bw[w] = min(bw[v], edge_wts[v][w])
					dad[w] = v
	return dad
	max_bw_path = print_path(dad,edge_wts,s+1,t+1)
	print
	print 'Using Dijkstras algo without heap'
	print 'max bw path in g from', s+1, 'to', t+1, 'is', ':', max_bw_path[0] 
	print 'max bw = ', max_bw_path[1]
	print

import heap as hp

def algo2(g,s,t):
	adj_list  = g[0]
	edge_wts = g[1]
	s = s-1
	t = t-1
	no_of_vertices = len(adj_list)
	dad = np.zeros(no_of_vertices)
	status = []
	bw = np.zeros(no_of_vertices)

	#max heap for maintaining fringes
	fringeHeap = hp.maxHeap()


	for i in range(no_of_vertices):
		status.append(-1) # -1 for unseen
	status[s] = 1 # 1 for in-tree

	
	bw[s] = 10000000000 # +inf
	fringeHeap.Insert(s, bw[s])


	# updating source node's neighbors
	fringeHeap.Delete(1)

	for i in range(len(adj_list[s])):
		w =  adj_list[s][i]
		#print w
		w = w-1
		status[w] = 0 #fringe
		bw[w] = edge_wts[s][w]
		fringeHeap.Insert(w, bw[w])
		dad[w]=s
	
	while (status[t] != 1): #while t is not in-tree
		flag = 1
		v = fringeHeap.Maximum();
		fringeHeap.Delete(1)
		status[v] = 1

		for i in range(len(adj_list[v])):
			w =  adj_list[v][i]
			w = w-1
			if(status[w] == -1):#if unseen
				status[w] = 0 #make fringe
				bw[w] = min(bw[v], edge_wts[v][w])
				fringeHeap.Insert(w, bw[w])
				dad[w] = v
			else:
				if(status[w] == 0 and bw[w]< min(bw[v], edge_wts[v][w])):#if fringe
					bw[w] = min(bw[v], edge_wts[v][w])
					fringeHeap.Insert(w, bw[w])#update it not insert
					dad[w] = v
	max_bw_path = print_path(dad,edge_wts,s+1,t+1)
	print
	print 'Using Dijkstras algo using heap'
	print 'max bw path in g from', s+1, 'to', t+1, 'is', ':', max_bw_path[0] 
	print 'max bw = ', max_bw_path[1]
	print

def algo3(g,s,t):
	list  = g[0]
	mat = g[1]
	no_of_vertices = len(list)
	edgesHeap = hp.maxHeap()
	for i in range(len(list)):
		for j in range(len(list[i])):

			u = i+1
			v = list[i][j] 
			wt = mat[i][list[i][j]-1]
			edgesHeap.Insert([u,v], wt)
	ret = edgesHeap.HeapSort()
	sorted_weights=ret[0]
	sorted_edges=ret[1]

	#print 'HeapSort of edges is done'

	b_l=[]
	V_1=[]

	for i in range(no_of_vertices+1):
		b_l.append(vtx.Vertex(i))

	for i in range(no_of_vertices+1):
		V_1.append(i)

	MST=gp.Graph(no_of_vertices)
	 
	MST.add_vertices(V_1[1:])
	p=[]
	rank = []
	dad = np.zeros(no_of_vertices+1)
	dad1 = np.zeros(no_of_vertices+1)

	for i in range(no_of_vertices+1):
		p.append(0)
		rank.append(0)
	
	#print 'Initialization is done'
	
	def Find(v):
		w=v;
		while(p[w]!=0):
			w=p[w]
		return w
	def Union(r1,r2):

		if(rank[r1] < rank[r2]):
			p[r1]=r2
		if(rank[r1] > rank[r2]):
			p[r2]=r1
		if(rank[r1] == rank[r2]):
			p[r1]=r2
			rank[r2] = rank[r2] + 1

	flag = []
	
	for i in range(no_of_vertices+1):
		flag.append(0)
	flag[0] = -1
	
	#print flag
	while(len(sorted_edges)!=0 and flag.count(1) != no_of_vertices):#Or all vertices are joined
		
		#print flag
		e = sorted_edges.pop(0)

		u=e[0]
		v=e[1]

		r_u=Find(u)
		r_v=Find(v)

		if( r_u != r_v ):

			dad[v] = u
			dad1[u]=v
			MST.add_edge_mst(b_l[u],b_l[v])
			flag[u]=flag[v]=1

			Union(r_u,r_v)

	#print 'MST generated'
	
	mst_adj_list = (MST.adjacencyList())

	mst_adj_list.insert(0,[])

	curr = s
	queue = []
	status = np.zeros(no_of_vertices+1)#un-visited

	status[s] = 1#in-tree
	queue.append(s)

	path =[]
	dad = np.zeros(no_of_vertices)
	
	#print 'BFS started'
	
	while(curr != t):

		curr = queue.pop(0)
		path.append(curr)

		for i in range( len(mst_adj_list[curr]) ):
			nxt  = mst_adj_list[curr][i]
			if(status[nxt] == 0):
				queue.append(nxt)
				status[nxt] = 1
				dad[nxt-1] = curr-1
	#print 'parent array generated for s to t path'
	max_bw_path = print_path(dad,mat,s,t)
	print
	print 'Using Kruskals algo'
	print 'max bw path in g from', s, 'to', t, 'is', ':', max_bw_path[0] 
	print 'max bw = ', max_bw_path[1]
	print

'''
import generate_graphs as gg
temp = gg.g_1(100)
temp = gg.g_2(100)

algo1(temp,2,5)
algo2(temp,2,5)
algo3(temp,2,5)
'''