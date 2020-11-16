import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import pylab

pause_time = 0.001
total_frame = 50
V = 20
INF = 99999
edge_weight = [1,2,3,4,5,6,7,8,9,10,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF]
pylab.ioff()
pylab.show()

# Solves all pair shortest path via Floyd Warshall Algorithm 
def floydWarshall(graph): 
	dist = map(lambda i : map(lambda j : j , i) , graph) 
	for k in range(V): 
		# pick all vertices as source one by one 
		for i in range(V): 
			# Pick all vertices as destination for the above picked source 
			for j in range(V): 
				# If vertex k is on the shortest path from 
				# i to j, then update the value of dist[i][j] 
				dist[i][j] = min(dist[i][j] , 
								dist[i][k]+ dist[k][j] 
								) 
	# print dist[0][11]
	printSolution(dist) 

def printSolution(dist): 
	print ("Following matrix shows the shortest distances\ between every pair of vertices" )
	for i in range(V): 
		for j in range(V): 
			if(dist[i][j] == INF): 
				print ("%7s" %("INF"),) 
			else: 
				print ("%7d\t" %(dist[i][j]),) 
			if j == V-1: 
				print ("" )

def get_graph(graph):
	# generating graph object
	G=nx.Graph()
	G.add_nodes_from(range(0,V))
	for i in range(V):
		for j in range(V):
			if i!=j:
				if graph[i][j]!=INF:	
					G.add_edge(*[i,j], label='graph[i][j]')
	return G


fig = pylab.figure()
for i in range(total_frame):
	# print i
	graph = a = [[0] * V for i in range(V)]
	for i in range(V):
		for j in range(V):
			if i!=j:	
				graph[i][j] = random.choice(edge_weight) 
	# floyd matrix			
	floydWarshall(graph); 
	# displaying graph
	G = get_graph(graph)
	labels = range(V)
	nx.draw(G,pos=nx.circular_layout(G))
	nx.draw_networkx_labels(G,label=labels,pos=nx.circular_layout(G),font_size=16)

	fig.canvas.draw()
	# pylab.draw()
	plt.pause(pause_time)
	fig.clf()
