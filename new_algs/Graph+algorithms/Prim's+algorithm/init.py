import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import datetime
from itertools import combinations,chain

def file_handling():
	file1=open('eil101.tsp','r')

	Name=file1.readline().split()[2]
	Comment=file1.readline().strip().split()[2:]
	Comment=Comment[0]+' '+Comment[1]+' '+Comment[2]
	Type=file1.readline().split()[2]
	Dimension=file1.readline().split()[2]
	Edge_weight_type=file1.readline().split()[2]

	file1.readline()
	nodelist=[]
	N=int(Dimension)
	for i in range(0,N):
		x,y=file1.readline().split()[1:]
		nodelist.append((float(x),float(y)))

	file1.close()
	filename=Name
	return nodelist,filename

def generate_data(n):
	arr=np.random.rand(n,2)
	arr=arr*100
	return arr

def euclid_dist(x1,y1,x2,y2):
	dist=sqrt((x1-x2)**2+(y1-y2)**2)
	return int(dist)

def edgedict(nodelist):
	
	edges={}
	for i in range(0,len(nodelist)-1):
		for j in range(i+1,len(nodelist)):
			(x1,y1)=nodelist[i]
			(x2,y2)=nodelist[j]
			edges[i,j]=euclid_dist(x1,y1,x2,y2)
			edges[j,i]=edges[i,j]
	return edges

def nearest(last,unvisited,edges):
	near=unvisited[0]
	min_dist=edges[last,near]
	for i in unvisited[1:]:
		if edges[last,i]<min_dist:
			near=i
			min_dist=edges[last,near]
	return near

def nearest_neighbour(nodelist,i,edges):
	unvisited=list(range(len(nodelist)))
	unvisited.remove(i)
	last=i
	tour=[i]
	while unvisited!=[]:
		next=nearest(last,unvisited,edges)
		tour.append(next)
		unvisited.remove(next)
		last=next
	return tour

def length(tour,edges):
	tour_length=edges[tour[-1],tour[0]]
	for i in range(1,len(tour)):
		tour_length+=edges[tour[i],tour[i-1]]
	return tour_length


def plot_graph(nodelist,visited):
	for i,txt in enumerate(nodelist):
		plt.scatter(nodelist[i][0],nodelist[i][1])
		#plt.annotate(txt,(nodelist[i][0],nodelist[i][1]))
	for i in range(0,len(visited)):
		plt.plot((nodelist[visited[i][0]][0],nodelist[visited[i][1]][0]),(nodelist[visited[i][0]][1],nodelist[visited[i][1]][1]))
	plt.show()

def graph_mst(opt_tour,nodelist):
	x_coords=[]
	y_coords=[]
	for i in opt_tour:
		x_coords.append(nodelist[i][0])
		y_coords.append(nodelist[i][1])
	for i,txt in enumerate(opt_tour):
		plt.plot(x_coords,y_coords)
		plt.scatter(x_coords,y_coords)
		#plt.annotate(txt,(x_coords[i],y_coords[i]))
	plt.show()

def edgedict2(nodelist):
	weights=[]
	nodes=[]
	for i in range(0,len(nodelist)-1):
		for j in range(i+1,len(nodelist)):
			(x1,y1)=nodelist[i]
			(x2,y2)=nodelist[j]
			nodes.append((i,j))
			weights.append(euclid_dist(x1,y1,x2,y2))
	nodes=np.array(nodes)
	weights=np.array(weights).reshape(-1,1)
	final=np.concatenate((nodes,weights),axis=1)
			#edges[j,i]=edges[i,j]
	return final

def mst_length(visited,nodelist):
	dist=[]
	for i in range(0,len(visited)):
		dist.append(euclid_dist(nodelist[visited[i][0]][0],nodelist[visited[i][0]][1],nodelist[visited[i][1]][0],nodelist[visited[i][1]][1]))
	length=sum(dist)
	return length

def check(nodelist,final):
	visited=[]
	visited_new=[]
	#print(nodelist)
	#print(final)
	final=list(final)
	while len(final)!=0:
		init_w=final[0][2]
		#print(init_w)
		for i in range(0,len(final)):
			if final[i][2]<=init_w:
				init_w=final[i][2]
				init_node=final[i]
				idx=i
	#	print(np.array(final))
		del final[idx]
		#final.pop(idx)
		visited.append(init_node[:2])
	visited=np.array(visited)
	final=np.array(final)
	visited=visited.tolist()
	data_list = visited
	all_triple_pairs = list(combinations(data_list, 3))
	digit_sets = [set(d for pair in trip for d in pair) for trip in all_triple_pairs]
	dup_inds = [i for i, s in enumerate(digit_sets) if len(s)==3]
	duplicates = [all_triple_pairs[i] for i in dup_inds]
	pairs_to_remove = [trip[-1] for trip in duplicates]
	answer = [pair for pair in data_list if pair not in pairs_to_remove]
	#print(answer)
	for p in answer:
	 	print(p)
	return answer

def main():
	t1=datetime.datetime.now()
	#n=200
	#nodelist=generate_data(n)
	#filename='200 random'
	nodelist,filename=file_handling()
	#nodelist=[(8,1),(3,5),(5,9),(1,4),(5,2)]
	#print(nodelist)
	#nodelist=[(8,-4),(5,9),(4,3),(2,6),(1,7),(9,2),(5,5),(8,3),(11,8),(6,14)]
	print(f'the total number of nodes are {len(nodelist)}')
	#final= edgedict2(nodelist)	
	#visited=check(nodelist,final)
	edges=edgedict(nodelist)
	lengths=[]
	tours=[]
	for i in range(0,len(nodelist)):
		tour=nearest_neighbour(nodelist,i,edges)
		tour_length = length(tour, edges)
		tours.append(tour)
		lengths.append(tour_length)
	idx=lengths.index(min(lengths))
	tour_length=min(lengths)
	opt_tour=tours[idx]
	#plot_graph(nodelist,visited)
	results(filename,tour_length,opt_tour,nodelist,t1)


def results(filename,tour_length,opt_tour,nodelist,t1):
	print(f'The optimal tour is {opt_tour}')
	print('-----')
	print(f"The length of the tour is {tour_length}")
	print('-----')
	t2=datetime.datetime.now()
	print(f'The time take is {t2-t1}')

	graph_mst(opt_tour,nodelist)
	file_out(filename,tour_length,opt_tour)

def file_out(filename,tour_length,opt_tour):
	f=open(f'{filename}.out.tour.adheesh','w+')
	f.write(f"NAME:{filename}.out.tour\n")
	f.write(f'COMMENT: Tour for {filename}.tsp (Length {tour_length})\n')
	f.write(f'TYPE: TOUR\n')
	f.write(f'DIMENSION:{len(opt_tour)}\n')
	f.write(f'TOUR SECTION:\n')
	for i in range(0,len(opt_tour)):
		f.write(f'{opt_tour[i]}\n')
	f.write(f'-1\n')
	f.write(f'EOF')



if __name__=='__main__':
	main()