from DijkstraAlgorithmH import *
import pdb

class DPRRS(object):
	def __init__(self):
		self.da = DijkstraAlgorithmH()
		
	# node and neighbor are node objects
	def changeCost(self, node, neighbor):
		#node.changeNeighborCost(neighbor)
		node.removeNode()
	
	def removePath(self):
		i = 0
		while i < len(self.da.path) - 1:
			self.changeCost(g.getNode(self.da.path[i]), g.getNode(self.da.path[i+1]))
			self.changeCost(g.getNode(self.da.path[i+1]), g.getNode(self.da.path[i]))
			i = i +1
	
	def dprrs_alg(self):
		
		while True:
			try:
				print ("How many times do you want to run DPRRS?",)
				resp = raw_input()
				times = int(resp)
				break
			except ValueError:
				print ("That is not an int!")
		
		i = 0
		while i < times:
			self.da.dijk_alg()
			pdb.set_trace()
			# This is removing the last path recorded in path
			self.removePath()
			i = i + 1
		