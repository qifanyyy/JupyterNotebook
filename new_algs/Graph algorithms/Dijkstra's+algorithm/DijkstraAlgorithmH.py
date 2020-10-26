from graph_creationF import *
from heapq import *
from time import *


class DijkstraAlgorithmH(object):
	
	def __init__(self, init_node):
		self.initNode = init_node
		self.time = ''
		self.path = ''
	
	# param - a Node object
	def get_path(self, last_node):
		s = [last_node.getName()]
		while not last_node.prev is None:
			last_node = last_node.prev
			s.append(last_node.getName())
			
		s.reverse()
		# This is storing a path in it every single time. 
		# self.path will always be the path to the last node in the list.
		self.path = s

		
	def input_initNode(self):
		print "\nWhich node is the starting node?",
		n = raw_input()
		return n

	def get_time(self, start, end):
		self.time = "\nTime:" + str(end - start)

	def dijk_alg(self, g):	

                if self.initNode == None:
                        while True:
                                self.initNode = self.input_initNode()
                                if self.initNode in g.nodeList.keys():
                                        break

		
		#initNode = 'a'

		g.getNode(self.initNode).dist = 0

		heap = []
		
		start = time()

		for i in g.nodeList:
		  heappush(heap, g.getNode(i))

					
		while len(heap) > 0:
			heapify(heap)
			currNode = heappop(heap)
			#print currNode
			for n in currNode.neighbors:
				if n.dist > currNode.dist + currNode.getCost(n) or (n.dist == currNode.dist + currNode.getCost(n) and n.hop_count > currNode.hop_count + 1):
					n.dist = currNode.dist + currNode.getCost(n)
					n.prev = currNode
#					n.hop_count = currNode.hop_count + 1
					heappush(heap, currNode)
						
					
		# for i in g.nodeList:
			# print g.getNode(i)
		end = time()
		self.get_time(start, end)
		
		#print '\n{0:12} {1:7} {3:7} {2:10}'.format('Start/End:', 'Cost:', 'Path:', 'Hops:')
			
		for i in g.nodeList:
                        self.get_path(g.getNode(i))
                        print '('+self.initNode+','+g.getNode(i).getName()+')'
                        print "Cost: " + str(g.getNode(i).dist)
                        print "Hops: " + str(len(self.path)-1)
                        print "Path: " + str(self.path)

                #for i in g.nodeList:
			#self.get_path(g.getNode(i))
			#print '{0:12} {1:7} {3:7} {2:10}'.format('('+self.initNode+','+g.getNode(i).getName()+')', str(g.getNode(i).dist), str(self.path), str(len(self.path)-1))
			
		print "\n" + self.time
