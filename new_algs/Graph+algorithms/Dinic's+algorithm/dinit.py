from Data import graphs, init_residuals,Ds,breadth_first,Neighbours
import numpy as np

def max_flow_print(ID):
	s=Ds[ID]
	t=s+1
	flow=np.zeros((t+1,t+1))
	graph=graphs[ID]
	residual=init_residuals[ID]
	dist=1
	f= open('dinit_'+str(ID)+'.txt', 'w')
	while not(np.isinf(dist)):
		d=0
		while d<t+1:
			f.write(" ".join(map(str, residual[d])))
			f.write("\n")
			d+=1
		#find the shortest s-t path
		st_path,dist=breadth_first(residual,s,t)
		#find the maximum avaible flow
		i=0
		K=np.inf
		while i<np.size(st_path)-1:
			a=st_path.item(i)
			b=st_path.item(i+1)
			if graph.item((a,b))-flow.item((a,b)) < K :
				K=graph.item((a,b))-flow.item((a,b))
			i+=1
		#update residual and flow
		i=0
		while i<np.size(st_path)-1:
			a=st_path.item(i)
			b=st_path.item(i+1)
			#update flow
			flow.itemset((a,b),flow.item((a,b))+K)
			flow.itemset((b,a),flow.item((b,a))-K)
			#update residual
			if graph.item((a,b))==flow.item((a,b)):
				residual.itemset((a,b),0)
			elif flow.item((a,b))>0 :
				residual.itemset((b,a),1)
			i+=1
	d=0
	while d<t+1:
		f.write(" ".join(map(str, residual[d])))
		f.write("\n")
		d+=1
	f.close
	f1 = open('dinit_flow_'+str(ID)+'.txt', 'w')
	f1.write(str(np.sum(flow[s])))
	f1.close

def max_flow(ID):
	print('-')
	s=Ds[ID]
	t=s+1
	flow=np.zeros((t+1,t+1))
	graph=graphs[ID]
	residual=init_residuals[ID]
	neighbours=Neighbours[ID]
	t_visited=True
	while t_visited:
		#find the shortest s-t path
		st_path,t_visited=breadth_first(residual,neighbours,s,t)
		#find the maximum avaible flow
		i=0
		K=np.inf
		while i<np.size(st_path)-1:
			a=st_path.item(i)
			b=st_path.item(i+1)
			if graph.item((a,b))-flow.item((a,b)) < K :
				K=graph.item((a,b))-flow.item((a,b))
			i+=1
		#update residual and flow
		i=0
		while i<np.size(st_path)-1:
			a=st_path.item(i)
			b=st_path.item(i+1)
			#update flow
			flow.itemset((a,b),flow.item((a,b))+K)
			flow.itemset((b,a),flow.item((b,a))-K)
			#update residual
			if graph.item((a,b))==flow.item((a,b)):
				residual.itemset((a,b),0)
			elif flow.item((a,b))>0 :
				residual.itemset((b,a),1)
			i+=1
	return(np.sum(flow[s]))

