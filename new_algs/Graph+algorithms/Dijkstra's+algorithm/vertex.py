import sys;

class Vertex(object):

	def __init__(self,name):
		self.name = name;
		self.visited = False;
		self.predecessor = None;
		self.adjacenciesList=[];
		self.minDistance = sys.maxsize;

	def __cmp__(self, otherVertex):
		return self.tmp(self.minDistance, otherVertex.minDistance)
	
	def __lt__():
		selfPriority = self.minDistance;
		othePriority = other.minDistance;
		return selfPriority < othePriority;
