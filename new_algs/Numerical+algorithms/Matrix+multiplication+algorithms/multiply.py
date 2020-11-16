import numpy as np
from scipy.sparse import dok_matrix

# def get_hashtable_node_count(root):
# 	table = dict()
# 	queue = [root]
# 	counter = 0

# 	while queue:
# 		node = queue.pop(0)

# def get_ith_basis_vec(i, N):
# 	vec = np.zeros(N)
# 	vec[i] = i
# 	return vec

# def is_leaf(node):
# 	#not sure abt the suffix-trees api but here is a possible implementation
# 	return not node.left and not node.right

# def fill_phi(node, phi, counter):
# 	if is_leaf(node):
# 		vec = get_ith_basis_vec(node.index, N) #assuming node has attribute index, may need to use an extern data structure
# 		phi[:][counter] = vec
# 	else:
# 		for child in node.children:
# 			fill_phi(child, phi, )	

#sigma notation labeled (5) in the paper
# def get_sum5(node, squigglyV, N, node_uids):
# 	queue = [node]
# 	sumvec = np.zeros(N)

# 	while not queue.empty():
# 		curr = queue.pop(0)
# 		for value, child in curr.childen.items():
# 			if is_leaf(child) and child not in squigglyV:
# 				sumvec += get_ith_basis_vec(node_uids[child], N)
# 			else:
# 				queue.append(child)

# #havent run yet!!!
# def get_phi(squigglyV, N, listoflevels, node_uids):
# 	#squigglyV is a set of nodes, N is the dimension (num docs), listoflevels is varun's BF traversal, node_uids is 
# 	#the map fron node to its unqiue identifier
# 	V_caret = squigglyV
# 	V_caret.add(listoflevels[0][0])

# 	numNodes = listoflevels[-1][-1][1] + 1 #counter starts at 0
# 	phi = dok_matrix((N,numNodes - 1), dtype=np.int)
# 	#phi = np.zeros((N,numNodes - 1)) #ignore the root

# 	#start looping from the back
# 	for i in range(len(listoflists), 1, -1): #skip the root, that's why we end at 1 instead of 0
# 		level = listoflevels[i]
# 		for node, count in level:
# 			if node not in squigglyV: continue #accounted for by other nodes
# 			counter -= 1 #adjust indexing 
# 			if is_leaf(node):
# 				vec = get_ith_basis_vec(node_uids[node], N)
# 				phi[:][counter] = vec
# 			else:
# 				phi[:][counter] = get_sum_5(node, squigglyV, N, node_uids)
# 				#double check dafuq
# 	return phi

#### Kevin's way

def populate_phi(phi, node, counter, squigglyV, node_uids):
	queue = [node]
	#sumvec = np.zeros(N)

	while not queue.empty():
		curr = queue.pop(0)
		for value, child in curr.childen.items():
			if is_leaf(child) and child not in squigglyV:
				phi[node_uids[child], counter] = 1
			else:
				queue.append(child)


def get_phi_as_dok(squigglyV, listoflevels, node_uids):
	#squigglyV is a set of nodes, N is the dimension (num docs), listoflevels is varun's BF traversal, node_uids is 
	#the map fron node to its unqiue identifier
	V_caret = squigglyV
	V_caret.add(listoflevels[0][0])

	numNodes = listoflevels[-1][-1][1] + 1 #counter starts at 0
	phi = dok_matrix((N,numNodes - 1), dtype=np.int32)

	#start looping from the back
	for i in range(len(listoflists), 1, -1): #skip the root, that's why we end at 1 instead of 0
		level = listoflevels[i]
		for node, count in level:
			if node not in squigglyV: continue #accounted for by other nodes
			counter -= 1 #adjust indexing 
			if is_leaf(node):
				phi[node_uids[node], counter] = 1
			else:
				populate_phi(phi, node, counter, squigglyV, node_uids)
	return phi


def get_squiggly_X(root, listoflevels, X, Phi):
	# root - root of the tree
	# listoflevels - another format of the tree
	# X - N-gram matrix (filled w integers)
	# get Phi from the method above

	numNodes = listoflevels[-1][-1][1] + 1 #counter starts at 0
	squigglyX = np.zeros((N,numNodes - 1)) #ignore the root

	for i in range(len(listoflists), 1, -1): #skip the root, that's why we end at 1 instead of 0
		level = listoflevels[i]
		for node, count in level:
			squigglyX[count] = Phi[count] + sum([Phi[child.count] for child in node.children()]) #ASSUMING there is
			# a count variable in each node and has method .children()

	return squigglyX	

def main():
	return 0

if __name__ == '__main__':
	main()