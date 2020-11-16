"""
@author-Aayushi Srivastava
This code generates Chordal Graphs using Minimum Degree Vertex heuristic.
"""
import random
import numpy as np

import itertools
import copy

import networkx as nx
import matplotlib.pyplot as plt
import sys

class ChordalVert:
	def __init__(self, noNodes, noEdges, m_vert=0):
		"""function to initialize the variables in the instance of a ChordalGraph"""
		self.noNodes = noNodes
		self.noEdges = noEdges
		self.vertexList = []
		self.GEdgeList = []
		self.HEdgeList = [] #HEdgeList
		self.G = {}
		self.H = {}
		#self.R = {}
		self.neb = [] 
		self.m_vert = m_vert
		self.minv = {}
		self.neb = []
		self.NEdgeList = []
		#self.S = {}
		#self.SEdgelist = []

	def ArbitraryGraph(self):
		"""function to create arbitrary graph"""
		self.G = nx.dense_gnm_random_graph(self.noNodes, self.noEdges)
		#self.G = {0: [15], 1: [8, 2, 3, 10], 2: [1, 10, 5, 6], 3: [1, 15], 4: [5], 5: [2, 4, 6, 15], 6: [9, 2, 12, 5], 7: [8, 11, 13], 8: [1, 14, 7], 9: [10, 6, 15], 10: [1, 2, 12, 13, 9], 11: [7], 12: [10, 13, 6], 13: [10, 15, 12, 7], 14: [8, 15], 15: [0, 3, 5, 9, 13, 14]}

		if type(self.G) is not dict:
			self.G = nx.to_dict_of_lists(self.G)
				
		for i in range(0, self.noNodes):
			self.vertexList.append(i)
		for key, value in self.G.iteritems():
			for v in value:
				if key<v:
					e = []
					e.append(key)
					e.append(v)
					self.GEdgeList.append(e)
		
		self.G = nx.Graph(self.G)
		connComp = sorted(nx.connected_components(self.G))
		self.G = nx.to_dict_of_lists(self.G)
		
		connComp = list(connComp)
		noOFConnComp = len(connComp)
		if noOFConnComp > 1:
			print ("Here we are")
			print (connComp)
			self.G = nx.Graph(self.G)
			self.plotArbitraryGraph(self.G)
			j = 0
			while j < noOFConnComp - 1:
				u = random.choice(list(connComp[j%noOFConnComp]))
				v = random.choice(list(connComp[(j+1)%noOFConnComp]))
				self.addAnEdge(self.G, self.GEdgeList, u, v)
				j = j + 1
		print (str(self.G))
		self.G = nx.Graph(self.G)
		self.plotArbitraryGraph(self.G)
		#print "see"
		self.G = nx.to_dict_of_lists(self.G)


		 
	def addAnEdge(self, graphToAdd, edgeListToAdd, v1, v2):
		"""function to add an edge in the graph"""
		graphToAdd = nx.to_dict_of_lists(graphToAdd)
		graphToAdd[v1].append(v2)
		graphToAdd[v2].append(v1)
		e = []
		e.append(v1)
		e.append(v2)
		edgeListToAdd.append(e)


	def plotArbitraryGraph(self, graphToDraw):
		"""function to plot graphs"""	
		self.HEdgeList = copy.deepcopy(self.GEdgeList)
		self.H = copy.deepcopy(self.G)	
		graphToDraw = nx.to_dict_of_lists(graphToDraw)
		#print "HEY"
		#print type(graphToDraw)
		edges = 0
		for node, degree in graphToDraw.iteritems():
			edges += len(degree) 
		print (type(self.G))
		print (self.G)
	
		
		GD = nx.Graph(graphToDraw)
		pos = nx.spring_layout(GD)
		print ("\nArbitrary Graph: "+str(self.G))
		print ("\nNo. of edges in the Arbitrary Graph: "+ str(edges/2))
		#plt.title("Arbitrary Graph")
		nx.draw(GD, pos, width=8.0,alpha=0.5,with_labels = True)
		plt.draw()
		plt.show()
		#plt.savefig('Arbitrary_Graph.png')
		self.H = nx.to_dict_of_lists(self.H)
		#self.H = nx.Graph(self.H)
		#print "see graph det",self.H

		#self.ChordalCheck(self.G)
		self.createChrdG()


	def createChrdG(self):
		"""function to start MDV"""
		self.HEdgeList = copy.deepcopy(self.GEdgeList)
		self.H = copy.deepcopy(self.G)
		self.H = nx.Graph(self.H)

		print ("Start Minimum Vertex Process")
		self.Minvertex(self.vertexList,self.HEdgeList,self.H)
		self.FinalGraph(self.G,self.NEdgeList,self.vertexList)
		print ("End Minimum Vertex Process")
		return True
		#self.FinalGraph(self.G,self.NEdgeList,self.vertexList)

	def Minvertex(self,vertexList,edgeList, graphtoCons):
		"""MDV Algorithm"""
		graphtoCons = nx.Graph(graphtoCons)
		self.H = nx.Graph(self.H)
		#isChordal = False
		#self.H = nx.Graph(self.H)
		random.shuffle(vertexList)
		self.H = nx.Graph(self.H)
		for v in vertexList:
			#print "check type"
			#print type(self.H)
			self.H = nx.Graph(self.H)
			dv = list(self.H.degree(self.H)) #list of tuples
			#print "see the list:"
			print (dv)
		#pd = len(dv)
		#print pd
			#print self.HEdgeList
			dvdict = dict(dv)
			#print "Dictionary of node-degree is", dvdict
			self.minv = dict(sorted(dvdict.items(), key=lambda kv:(kv[1], kv[0])))
			#print "Sorted dictionary of node-degree:",self.minv
			self.H = nx.to_dict_of_lists(self.H)
			#print "The dictionary looks like:", self.H
			mincp = copy.deepcopy(self.minv)
			try:
				for key,value in mincp.iteritems():
					if value < 2:
				#del minv[key]
						self.minv.pop(key)
				#print "Deleted"
				#print "Updates:",self.minv
				graphtoCons = nx.Graph(graphtoCons)
				self.H = nx.Graph(self.H)
				nodeH = self.H.nodes()
				#print "Old Nodes are:",nodeH
				#print "New nodes are",list(self.minv)
				self.H.add_nodes_from(list(self.minv))
				self.H.remove_nodes_from(list(list(set(nodeH) - set(list(self.minv)))))
				self.H = nx.to_dict_of_lists(self.H)
				#print "New Dictionary:",self.H
				self.m_vert = min(self.minv.keys(), key=(lambda k:self.minv[k]))
				#print type(self.m_vert)
				print ("Minimum degree vertex is:",self.m_vert)
				#print type(self.H)
				self.H = nx.Graph(self.H)
				#self.H = nx.Graph(self.H)
				print ("The chosen Minimum vertex is", self.m_vert)
				
				self.neb = list(self.H.neighbors(self.m_vert))
				print ("Neighbors of the chosen vertex are:",self.neb)
				neblen = len(self.neb)
				
				self.H = nx.Graph(self.H)
				self.H.remove_node(self.m_vert)
				self.neighbcomp(self.m_vert,self.H)

				self.H = nx.Graph(self.H)
			except ValueError as e:
				print ("Dictionary is Empty now")
				break
		#self.FinalGraph(self.G,self.NEdgeList,self.vertexList)

	def neighbcomp(self,chosvert,graphtoRecreate):
		"""Add edges amongst neighbors"""
		#eb = 0
		self.H = nx.Graph(self.H)
		nebcomb = list(itertools.combinations(self.neb,2))
		#print "See combinations:",nebcomb
		for p in nebcomb:
			v1 =  p[0]
			v2 = p[1]
			#print p
			if self.H.has_edge(*p) :
				#print p
				#print "Already edge is there"
				continue
			else:
				self.H.add_edge(*p)
				#print "Check this"
				self.NEdgeList.append(p)
				#print "My list", self.NEdgeList
				continue
		print ("Edges added using Minimum Degree",len(self.NEdgeList))

		self.H= nx.to_dict_of_lists(self.H)
		#print "See change",self.H
		#self.graphtoRecreate = nx.to_dict_of_lists(graphtoRecreate)

	#def FG(self):
		#print "Run the graph once:"
		#self.FinalGraph(self.G,self.NEdgeList,self.vertexList)
		
	

	def FinalGraph(self,graphVerify,newaddedgelist,vertexlist):
    		# """To plot chordal graph"""
		print ("EdgeList verifying",newaddedgelist)
		print ("Total Edges added in Minimum Degree Process is ",len(newaddedgelist))
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)

		B = copy.deepcopy(self.G)
		B = nx.Graph(B)
		B.add_nodes_from(vertexlist)
		B.add_edges_from(newaddedgelist)
		B = nx.to_dict_of_lists(B)
		print ("see B", B)
		##Recognition----
		graph = nx.Graph(B)
		print (type(B))
		if nx.is_chordal(graph):
			print ("IT IS CHORDAL")
		else :
			print ("NO IT IS NOT CHORDAL")
		print ("Draw graph")
		nx.draw_networkx_nodes(GD, pos, nodelist=vertexlist, node_color='red', node_size=300, alpha=0.8,label='Min degree')	
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newaddedgelist, width=8.0, alpha=0.5, edge_color='blue',label='Min degree')
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		plt.show()	



"""Input from Command PRompt"""			
val1 = int(raw_input("Enter no. of nodes:"))
val2 = int(raw_input("Enter no. of edges:"))
gvert = ChordalVert(val1,val2)
gvert.ArbitraryGraph()
#gvert.FG()