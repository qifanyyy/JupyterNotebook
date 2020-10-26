#!/usr/bin/python
from collections import deque
import sys
import argparse
from util import helper
import time
'''
	@Author: Emmanuel John (emmanuj)
'''

#read arguments
parser = argparse.ArgumentParser(description='Maximum network flow Solver')
parser.add_argument("-o","--output", help="Output file to write solution (Output is in DIMACS format)")
parser.add_argument("-i","--infile", help="Input graph file. Graph must be in DIMACS format", type=argparse.FileType('r'))
args = parser.parse_args()

vertex = [] # adjacency list (list of list)
cap = [] # list of dict of capacities
flow = [] # flow of edge (a,b): also list of dict, initially set to 0
level = [] #initialize this to length of the graph and set to zero
path = [] #prev node of a. initially set to none
numnodes =0

#initialize adjacency list and other program params
vertex, cap, flow, level, path, numnodes = helper.init(args, vertex, cap, flow, level, path, numnodes)

#creates level graph using bfs search
def createLevelGraph(source, sink):
	queue = deque([])
	queue.append(source)
	for l in range(len(level)):
		level[l] = 0
	level[source] = 1
	while queue:
		cur = queue.popleft()
		for i in range(len(vertex[cur])):
			nb = vertex[cur][i] #ith neighbor
			if((cap[cur][nb] - flow[cur][nb] > 0) and level[nb] == 0 ):
				queue.append(nb)
				level[nb] = level[cur] + 1
	return 	level[sink] != 0

#compute blocking flows with DFS
def createBlockingFlow(source, sink):
	fl = 0
	stack = [] #using a list with stack operations
	visited_nodes = []
	for l in range(len(vertex)):
		visited_nodes.append(0)
	stack.append(source)
	run = 0
	while stack:
		cur = stack[-1] #top
		if(cur != sink ):#advance step
			j = 0
			while j < len(vertex[cur]) and stack[-1] == cur:
				nb = vertex[cur][j]
				if visited_nodes[nb] == 1 or level[nb] != level[cur] + 1:
					j = j + 1
					continue
				if cap[cur][nb] - flow[cur][nb] > 0:			
					stack.append(nb)
					path[nb] = cur
				j = j + 1
			if stack[-1] == cur: #at already visited node. Need this to avoid infinite loop
				stack.pop()
				visited_nodes[cur] = 1	
		else:#augment step
			F = 1000000000
			bottleneck = None
			c = sink
			#find min(p)
			while c != source:
				F = min(F, (cap[path[c]][c] - flow[path[c]][c]) if (path[c] >= 0) else flow[c][-path[c]])
				c = abs(path[c])
			
			c = sink
			#update p as f = f + f'
			while c != source:
				flow[path[c]][c] = flow[path[c]][c] + F
				if (cap[path[c]][c] - flow[path[c]][c] == 0):
					bottleneck = path[c]
				c = abs(path[c])
			#retreat step
			while (stack and stack[len(stack) -1] != bottleneck):
				stack.pop();
			fl = fl+F
		run = run + 1
	return fl

#main module
def Dinic(source, sink):
	f  = 0
	while createLevelGraph(source, sink):
		f = f + createBlockingFlow(source, sink)
	return f

max_flow = Dinic(0,len(vertex) -1)
helper.writeGraph(args, vertex, flow, max_flow)
