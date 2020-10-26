import math
import collections
#Implementation of the data structure Heap
class heap(object):
	def __init__(self):
		self.hdict=dict()
		self.name="Hrishi"
		self.s=0
		self.A=[]
		self.p=dict()
	
	
	def heapify_up(self,i):
		
		while (i>1):
			j=int(i/2) 
			if (self.hdict.get(self.A[i-1])<self.hdict.get(self.A[j-1])):
				temp=self.A[i-1]
				self.A[i-1]=self.A[j-1]
				self.A[j-1]=temp
				self.p.update({(self.A[i-1]):i})
				self.p.update({(self.A[j-1]):j})
				i=j
				
			else:
				break
				
	
	def insert(self,edge,key_value):
		
		self.s=self.s+1
		self.A.append(edge)
		#print self.A
		
		#print self.s
		
		self.p.update({edge:self.s})
		#print self.p
		self.hdict.update({edge:key_value})
		self.heapify_up(self.s)
		
	def extract_min(self):
		
		ret=self.A[0]
		del self.p[self.A[0]]
		self.A[0]=self.A[self.s-1]
		self.A.pop(self.s-1)
		#print self.A
		
		self.p.update({(self.A[0]):1})
		self.s=self.s-1
		if (self.s >=1):
			self.heapify_down(1) 
		return ret

	def heapify_down(self,i):
		
		while (2*i<=self.s):
			if (2*i==self.s)or(self.hdict.get(self.A[2*i-1])<=self.hdict.get(self.A[2*i-1+1])):
				j=2*i
			else:
				j=2*i+1
			if(self.hdict.get(self.A[j-1])<self.hdict.get(self.A[i-1])):
				temp=self.A[i-1]
				self.A[i-1]=self.A[j-1]
				self.A[j-1]=temp
				
				self.p.update({(self.A[i-1]):i})
				self.p.update({(self.A[j-1]):j})
				i=j
			else:
				break
				
				
		
		

def prim(graph,weight):
	mst=[]
	result=[]
	start=1
	visitcount=1
	visited=[1]
	h=heap()
	while(visitcount!=len(graph)):
		v=graph.get(start)
		n=len(v)
		for i in range(0,n):
			if (not (v[i] in visited)):
				edge=((start),v[i])
				key_value=weight.get((start,v[i]))
				h.insert(edge,key_value)
			
		m=h.extract_min()
		
		start=m[1]
		if not(start in visited):
			visited.append(start)
			#print visited
			#print m
			result.append(m)
			visitcount=visitcount+1
		
			
	sum=0
	for i in range(0,len(result)):
		l=result[i]
		sum=sum+weight.get((l[0],l[1]))
	
	print(sum)
		
	file2=open("output.txt",'a')
	sum=str(sum)
	file2.write(sum+"\n")
	for i in range(0,len(result)):
		l=result[i]
		file2.write(str(l[0])+" "+str(l[1])+"\n")
	
	
	
		
 
	

print("Project 1 \n")
file=open('input.txt','r')

#Extract the number of edges and vertices
first_line=file.readline()
first_line=first_line.rstrip()
ginfo=first_line.split()
v=int(ginfo[0])
e=int(ginfo[1])

weight=dict()
graph=dict()
for i in range(1,v+1):
	graph.update({i:[]})

#Extract the edges and weights and create a weight
for line in file:
	line=line.rstrip()
	parts=line.split()	
	
	if (int(parts[0])>int(parts[1])):
		temp=parts[0]
		parts[0]=parts[1]
		parts[1]=temp
		
	
	weight.update({((int(parts[0])),(int(parts[1]))):int(parts[2])})
	weight.update({((int(parts[1])),(int(parts[0]))):int(parts[2])})	

	graph[int(parts[0])].append(int(parts[1]))
	graph[int(parts[1])].append(int(parts[0]))
	
graph=collections.OrderedDict(sorted(graph.items()))

x=prim(graph,weight)	
inp=input("press any key")
		
		
	
	

