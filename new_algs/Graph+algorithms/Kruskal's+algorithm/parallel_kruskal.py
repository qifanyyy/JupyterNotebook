#Rich Gioiosa
#This code is reelased under the BSD license as part of my final project
#for CSC503
#!/usr/bin/env python 
from psim import PSim
import time
import random
import sys

MAX_WEIGHT = 500

#Function to create a graph of n vertices with c randomly weighted
#connections. Graph will be in the form a of list of tuples.
#Tuple (a,b,c) such that a is a vertex, b is a vertex and c
#is the weight of the edge between them
def make_graph_tuple(n, c):
	count = c
	tuple_graph = []
	edges_so_far = []
	while count>0:
		vertex1 = random.randint(0,n-1)
		vertex2 = random.randint(0,n-1)
		#don't create any edges that point to the same vertex
		#and don't recreate another edge with a different weight
		#just try again, don't decrease counter
		if vertex1 != vertex2 and (vertex1,vertex2) not in edges_so_far and (vertex2,vertex1) not in edges_so_far:
			#create a random wieght from 1-MAX_WEIGHT
			weight = random.randint(1,MAX_WEIGHT)
			edge = (vertex1,vertex2,weight)
			tuple_graph.append(edge)
			edges_so_far.append((vertex1,vertex2))
			count = count-1
	return tuple_graph 

#serial Kruskal alorithm
def kruskal_serial(n, edges): 
	MST = []
	forest = []
	#create initial forest, each tree is one vertex
	for i in range(0,n-1):
		temp = []
		temp.append(i)
		forest.append(temp);
	#sort edges
	sorted_edges = edges
	quicksort_tuple_graph(sorted_edges)
	for e in sorted_edges:
		tree1 = []
		tree2 = []
		vertex1, vertex2, weight = e
		#find the trees the vertices belong to
		for j in range(0, len(forest)):
			if vertex1 in forest[j]:
				tree1_pos = j
				tree1 = forest[j]
			if vertex2 in forest[j]:
				tree2_pos = j
				tree2 = forest[j]
		#only add to MST if they are not already part of the same tree
		if tree1 != tree2:
			new_tree = []
			MST.append(e)
			#combine tree1 and tree 2 and add to forest
			#remove tree1 and tree2
			new_tree = tree1 + tree2
			forest[tree1_pos] = []
			forest[tree2_pos] = []
			forest.append(new_tree)
	return MST	
	
#serial Kruskal alorithm to pick up where the parallel algorithm left off
def kruskal_serial_cont(m,f,edges): 
	MST = m
	forest = f
	sorted_edges = edges
	for e in sorted_edges:
		tree1 = []
		tree2 = []
		tree1_pos = -1
		tree2_pos = -1
		vertex1, vertex2, weight = e
		#find the trees the vertices belong to
		for j in range(0, len(forest)):
			if vertex1 in forest[j]:
				tree1_pos = j
				tree1 = forest[j]
			if vertex2 in forest[j]:
				tree2_pos = j
				tree2 = forest[j]
		#only add to MST if they are not already part of the same tree
		if tree1 != tree2:
			new_tree = []
			MST.append(e)
			#combine tree1 and tree 2 and add to forest
			#remove tree1 and tree2
			new_tree = tree1 + tree2
			forest[tree1_pos] = []
			forest[tree2_pos] = []
			forest.append(new_tree)
	return MST	

#quicksort function to sort a list of tuples based on the weight
def quicksort_tuple_graph(edges,p=0,r=None):
	if r is None:
		r=len(edges)
	if p<r-1:
		q=partition(edges,p,r)
		quicksort_tuple_graph(edges,p,q)
		quicksort_tuple_graph(edges,q+1,r)
		
def partition(edges,i,j):
	t1,t2,x=edges[i]
	h=i
	for k in range(i+1,j):
		t3,t4,w = edges[k]
		if w<x:
			h=h+1
			edges[h],edges[k] = edges[k],edges[h]
	edges[h],edges[i] = edges[i],edges[h]
	return h

#get command line arguments for number of processors, 
#the number of vertices, and the number to edges in the graph
p = int(sys.argv[1]) #number of processor nodes
n = int(sys.argv[2]) #number of vertices 
e = int(sys.argv[3]) #number of edges
h = int(sys.argv[4]) #use additional hueristic methods
s = int(sys.argv[5]) #run in serial mode

print ('Command Line Options Entered')
print ('Number of Nodes (only applies to Parallel Kruskal MST): ', p)
print ('Number of Vertices in the Graph: ', n)
print ('Number of Edges in the Graph: ', e)
print ('Use heuristic methods (only applies to Parallel Kruskal MST)?: ', h)
print ('Run serial Kruskal MST?: ', s)

#run the serial Kruskal Algorithm if chosen
if s == 1:
	serial_graph = make_graph_tuple(n,e)
	#start the timer
	st = time.time()
	MST = kruskal_serial(n, serial_graph)
	print (MST)
	#stop timer
	#print 'Total Time: ',(time.time() - st)
else:
	comm = PSim(p) #create nodes, node 0 is the master	
	#master node	
	if comm.rank == 0:
		#the master node creates the initial graph
		the_graph = make_graph_tuple(n,e)
		#start the timer
		st = time.time()
		
		#break up edges and send to other worker nodes to
		#sort the edges by weight
		num_edges = e / p
		#node 0's edges to sort
		local_edges_to_sort = the_graph[0:num_edges] 
		for i in range (1,p):
			comm.send(i, the_graph[num_edges*i:(num_edges*i)+num_edges])
		#sort own local piece
		quicksort_tuple_graph(local_edges_to_sort)
		
		#now receive sorted pieces from worker nodes
		sorted_edges_to_merge = []
		sorted_edges_to_merge.append(local_edges_to_sort)
		for j in range (1,p):
			sorted_edges_to_merge.append(comm.recv(j))
		#merge sorted edges from workers into 1 sorted list
		sorted_edges = []
		for k in range (0,e):
			smallest = MAX_WEIGHT+1
			smallest_pos = -1
			for m in range(0,p):
				if len(sorted_edges_to_merge[m]) > 0: #check for empty list		
					t1,t2,weight = sorted_edges_to_merge[m][0]
					if weight<smallest:
						smallest = weight
						smallest_pos = m
			#next smallest weight found, add to final list
			if len(sorted_edges_to_merge[smallest_pos]) > 0:
				sorted_edges.append(sorted_edges_to_merge[smallest_pos].pop(0))			
	#worker node		
	else:
		#recieve edges from master, sort them by weight, and send back
		local_edges_to_sort = comm.recv(0)
		#print 'I am ', comm.rank, ' and I got ', local_edges_to_sort
		quicksort_tuple_graph(local_edges_to_sort)
		comm.send(0, local_edges_to_sort)
		
	#master node creates the initial forest, partition it, and send to the worker nodes
	if comm.rank == 0:
		num_trees = n/(p-1) #the master is not getting a forest, use p-1
		the_forest = []
		for i in range(0,n):
			temp = []
			temp.append(i)
			the_forest.append(temp);
		for k in range (1,p):
			comm.send(k, the_forest[(num_trees*(k-1)):(num_trees*(k-1))+num_trees])
			#print 'send to ', k, the_forest[(num_trees*(k-1)):(num_trees*(k-1))+num_trees]
	#worker gets it's part of the forest
	else:
		the_forest = comm.recv(0)
		#print 'I am ', comm.rank, ' and my forest is ', the_forest
		
		
	#master now starts to move through the sorted list of edges
	if comm.rank == 0:
		MST = [] #minimum spanning tree to return
		total_worker_trees = 0
		edges_processed = 0;
		cont_parallel = True
		cont_serial = False
		while cont_parallel:
			#for i in sorted_edges:
			if len(sorted_edges)==0:
				cont_parallel = False
			else:
				curr_edge = sorted_edges.pop(0)
				#command for workers to be sent with message
				cmnd = 1 
				v1, v2, w = curr_edge 
				#send the vertices to the workers so they can search their local forest 
				comm.one2all_broadcast(0,(cmnd,v1,v2))
				add = False
				send_union_tree = False
				#if vertices are in different worker's forests, must get the rank of the 
				#worker with vertex_1 and both trees to union and send to that worker
				worker = -1
				half_tree_1 = []
				half_tree_2 = []
				#loop through all of the worker responses
				for r in range(1,p):
					total_worker_trees = 0
					resp = comm.recv(r)
					if resp[0] == 0:
						b=1
						#print 'worker: ', r, ' does not have these vertices in their forest'
					elif resp[0] == 1:
						add = True
						send_union_tree = True
						if h==1:
							half_tree_1 = resp[2]
						else:
							half_tree_1 = resp[1]
						worker = r
						#print 'worker: ', r, ' has vertex 1, tree ', half_tree_1
					elif resp[0] == 2:
						if h==1:
							half_tree_2 = resp[2]
						else:
							half_tree_2 = resp[1]
						add = True
						#print 'worker: ', r, ' has vertex 2, tree ', half_tree_2
					elif resp[0] == 3:
						#print 'worker: ', r, ' has both vertex 1 and vertex 2 '
						add = True
					elif resp[0] == 4:
						b=1
						#print 'worker: ', r, ' has both vertx 1 and vertex 2 in the same tree '
					
					#If using the heuristics option
					#check the number of worker trees to see if it is now more efficient to switch
					#to the serial agorithm on the master(each worker only has 1 or 2 trees)
					if h == 1:
						total_worker_trees = total_worker_trees + resp[1]
						
				#process results of the workers
				#vertex_1 and vertex_2 are in 2 different trees, add to MST	
				if add: 
					MST.append(curr_edge) 
				#need to send a new tree to the worker who had vertex_1
				if send_union_tree:
					union_tree = half_tree_1 + half_tree_2
					comm.send(worker, (3, union_tree, 0))
					#print 'sent ', union_tree, 'to worker ', worker
				#check to stop for heuristic option
				if h==1 and total_worker_trees <= p-1*2:
					cont_parallel = False
					cont_serial = True
				
		#If using heuristics option, check to see if it is time to switch to the serial
		#algorithm on the master node, if so, collect all trees from workers and continue
		if h==1 and cont_serial:
			new_forest = []
			print ('There are ', p-1, ' workers, but only ', total_worker_trees, 'trees left. Switching to serial Kruskal MST Algorithm.')
			comm.one2all_broadcast(0,(4,0,0))
			#collect the worker forests
			for w in range(1,p):
				worker_trees = comm.recv(w)
				new_forest = new_forest+worker_trees
			#stop the workers
			comm.one2all_broadcast(0,(2,0,0))
			MST = kruskal_serial_cont(MST,new_forest,sorted_edges)
		#print MST
		#stop timer
		print ('Total Time: ',(time.time() - st))
	else:
		#get first command from the master, should be to search for vertices
		go = True
		recv_mesg = comm.recv(0)
		cmnd,v1, v2 = recv_mesg
		while go:
			#print 'worker:', comm.rank, 'received this command ',cmnd
			#master wants the worker to search his forest for these vertices
			if cmnd == 1:
				#search the local forest for these vertices, set mesg var for 1 of 5
				#outcomes to send to the master, 1) vertices are not in forest 2) vertex_1 is in 
				#one tree 3) vertex_2 is in one tree 4)both vertices are in 2 different trees 
				#5) both vertices are in the same tree
				found_1 = 0
				found_2 = 0
				result = 0
				mesg = []
				#search through the trees in the forest for the vertices
				for t in the_forest:
					#print 'worker:', comm.rank, 'search for vertex', v1, 'this is t:',t
					if v1 in t:
						found_1 = 1
						tree_1 = t
					if v2 in t:
						found_2 = 1
						tree_2 = t
				#prepare message back to master with search results
				#doesn't have either vertex in the forest
				if found_1==0 and found_2==0:
					result = 0
				#has vertex_1
				elif found_1 == 1 and found_2 == 0:
					result = 1
				#has vertex_2
				elif found_1 == 0 and found_2 == 1:
					result = 2
				#has both vertices in different trees
				elif found_1 == 1 and found_2 == 1 and tree_1 != tree_2:
					result = 3
				#has both vertices in the same tree
				elif found_1 == 1 and found_2 == 1 and tree_1 != tree_2:
					result = 4
				
				mesg.append(result)
				
				#If using the heuristics option:
				#inform the master about the number of trees in the forest
				#add that to the message as well
				if h==1:
					mesg.append(len(the_forest))
				
				#send back tree info for master node to union if this worker found 1 tree
				#or perform union if both vertices are in this forest
				if result == 1:
					mesg.append(tree_1)
					the_forest.remove(tree_1)
				elif result == 2:
					mesg.append(tree_2)
					the_forest.remove(tree_2)
				#perform union and create new tree
				elif result == 3:
					union_tree = tree_1 + tree_2
					#print 'here is my new union tree ', union_tree
					the_forest.remove(tree_1)
					the_forest.remove(tree_2)
					the_forest.append(union_tree)
				#print 'worker:', comm.rank, 'here is my mesg to master', mesg
				comm.send(0, mesg)
			#the master wants the worker to stop listening for instructions, his work is done
			elif cmnd == 2:
				go = False
				#print 'worker: ', comm.rank, ' The master says it is quitting time'
			#the master has a new tree for the worker to add to their forest
			elif cmnd == 3:
				the_forest.append(v1)
				#print 'worker: ', comm.rank,' the master says to add ', v1, 'to my forest'
			#send forest to master
			elif cmnd == 4:
				comm.send(0, the_forest)
				#print 'worker: ', comm.rank,' the master want my whole forest:', the_forest
				
			#get next command from master
			if go:	
				recv_mesg = comm.recv(0)
				cmnd, v1, v2 = recv_mesg


	





			