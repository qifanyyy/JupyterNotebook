import re
from string import Template
import numpy
from node import Node
import math

class Graph:
	def __init__(self, path="", *ns):
		self.root = None
		self.spaningTree = {}
		self.height = 0
		self.nodes = []
		self.labels = {}
		self.colorsStats = []
		self.bestColoringN = 100000
		self.bestColoringNodes = {}
		self.rounds=100

		if len(ns) > 0:
			for n in ns:
				self.nodes.append(n)
				self.labels[n.id]=str(n.id)
		elif len(path) > 0:
			self.buildByFile(path)
		self.adjMatrix = numpy.zeros((len(self.nodes), len(self.nodes)), dtype=numpy.int)
		for n in self.nodes:
			adj = n.getNeighbors()
			self.adjMatrix[n.id][adj] = 1
		self.minSpanningTree()

	def evalQuality(self, colors):
		quality = 0
		for n, c in zip(self.nodes, colors):
			n.color = c
		for n in self.nodes:
			quality += n.colorMark()
		return quality

	def startRunning(self, r=100, p=0.4):
		self.rounds = r
		for n in self.nodes:
			n.rcvStartMsg(int(math.ceil(r*p)))

	def runColoring(self):
		self.nodes.sort()
		for i in range(self.rounds):
			for n in self.nodes:
				n.occurEvent(i)
			self.updateBestColoring()
			self.doStat()
			self.nodes.sort()

	def doStat(self):
		stats = open("graphstats.txt", 'a')
		thetas = {}
		line = ""
		for i, n in enumerate(self.nodes):
			line += "{{{0}}} ".format(i)
			thetas[n.id] = n.theta

		keys = sorted(thetas.keys())
		values = list(thetas.values())
		line = line.format(*values)
		stats.write(line)
		stats.write("\n")


	def updateBestColoring(self):
		colors = set()
		for n in self.nodes:
			colors.add(n.color)
		self.colorsStats.append(len(colors))
		
		if (self.bestColoringN > len(colors) and self.checkValidColoring()):
			self.bestColoringN = len(colors)
			for n in self.nodes:
				self.bestColoringNodes[n.id]=n.color
			f = open("{0}.dot".format(self.bestColoringN), 'w')
			f.write(str(self))
			f.close()
		
	def checkValidColoring(self):
		for n in self.nodes:
			if not n.hasValidColor():
				return False
		return True

	def buildByFile(self, path):
		labelnodes = {}
		f = open(path, "r")
		f.readline()
		for edge in f:
			ns = list(re.findall(r'\d+', edge))
			for a, b in zip(ns[0:len(ns)-1], ns[1:len(ns)]):
				if a in labelnodes:
					n = labelnodes[a]
					if b in labelnodes:
						n.add(labelnodes[b])
					else:
						n2 = Node()
						labelnodes[b] = n2
						n.add(n2)
				else:
					n = Node()
					labelnodes[a] = n
					if b in labelnodes:
						n.add(labelnodes[b])
					else:
						n2 = Node()
						labelnodes[b] = n2
						n.add(n2)
		f.close()
		self.nodes = list(labelnodes.values())
		self.labels = {labelnodes[k].id: k for k in list(labelnodes.keys())}

	def __str__(self):
		l = str(list(self.labels.values()))
		strg = "graph G {\ngraph [concentrate=true, overlap=\"prism\"];\n"
		strg += 'node [width=\"0.15\", height=\"0.15"];'
		for n in self.nodes:
			strg += format(n, l)
		strg += "}\n"
		return strg

	def showColoringStats(self):
		print("Round\tnb Colors")
		i=0
		for stat in self.colorsStats:
			print(str(i)+"\t"+str(stat))
			i+=1
		
	def minSpanningTree(self):
		tree = []
		edgeSet = []
		for i, head in enumerate(numpy.nditer(self.adjMatrix, flags=['external_loop'], order='F')):
			tails = numpy.arange(len(self.nodes))
			tails = tails[(head > 0)]
			for t in tails:
				edgeSet.append((i,t))

		self.root = edgeSet[0][0] 
		tree.append(self.root)
		self.spaningTree[self.root] = []
		connected = True
		for h, t in edgeSet:
			if not h in tree:
				self.spaningTree[h] = []
				tree.append(h)
				connected = False
			if not t in tree or not connected:
				if not t in tree:
					if not h in self.spaningTree.keys():
						self.spaningTree[h] = []
					self.spaningTree[h].append(t)
					tree.append(t)
				else:
					if not t in self.spaningTree.keys():
						self.spaningTree[t] = []
					self.spaningTree[t].append(h)
					connected = True

		hs = numpy.zeros(len(self.nodes), numpy.int)
		hs[list(self.spaningTree.keys())[0]] += 1
		for n in iter(self.spaningTree.keys()):
			hs[self.spaningTree[n]] = 1 + hs[n]
		self.height = numpy.amax(hs)
