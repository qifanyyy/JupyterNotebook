import random
import sys


MIN_THRESH, MAX_THRESH = 1, 100

def create_regular_ring_lattice(N, d):
	adjacency_list = [[] for _ in range(N)]
	adjacency_matrix = [[False for _ in range(N)] for _ in range(N)]
	left = d / 2
	right = (d + 1) / 2
	for v in range(N):
		for i in range(1, 1 + d / 2):
			u1, u2 = (v - i) % N, (v + i) % N
			adjacency_matrix[v][u1], adjacency_matrix[u1][v] = True, True
			adjacency_matrix[v][u2], adjacency_matrix[u2][v] = True, True
			#if d % 2 == 1:
				#u1 = (v + d/2 + 1) % N
				#adjacency_matrix[v][u1], adjacency_matrix[u1][v] = True, True
	for v in range(N):
		for u in range(N):
			if adjacency_matrix[u][v]:
				adjacency_list[u].append(v)
	return adjacency_list, adjacency_matrix

def select_new_random_edge(u, v, adjacency_matrix):
	new_v = u
	#for i in range(N):
		#print(adjacency_matrix[i])
	while(new_v == u or adjacency_matrix[u][new_v]):
		assert (len(adjacency_matrix) >= 1)
		new_v = random.randint(0, len(adjacency_matrix) - 1)
		assert(new_v < len(adjacency_matrix))

		#print("u ", u, " v ", v, " new v", new_v)
	adjacency_matrix[u][v], adjacency_matrix[u][new_v] = False, True
	adjacency_matrix[v][u], adjacency_matrix[new_v][u] = False, True

def threshold(N, _min, _max):
	return [random.randint(_min, _max) for v in range(N)]

def cost_to_infect(N, adjacency_list):
	res = [1] * N
	for v in range(N):
		if not len(adjacency_list[v]) <= 1:
			res[v] = random.randint(1, len(adjacency_list[v]))
	return res

def create_files(filename, adjacency_list, f, b):
	N, M = len(adjacency_list), 0
	str_adj = ""
	str_b_f = ""
	for v in range(N):
		str_b_f += str(b[v]) + " " + str(f[v]) + "\n"
		for u in adjacency_list[v]:
			if v < u:
				str_adj += str(v) + " " + str(u) + "\n"
				M += 1
	with open(filename, "w") as myfile:
		myfile.write(str(N) + " " + str(M) + "\n" + str_b_f + str_adj)
	print("created")

def small_world_random_graph(N, density, p):
	adjacency_list, adjacency_matrix = create_regular_ring_lattice(N, density)
	for u in range(N):
		for v in range(N):
			if not adjacency_matrix[u][v]:
				continue
			#print(u, ", ", v)
			if random.uniform(0, 1) < p:
				select_new_random_edge(u, v, adjacency_matrix)
	adjacency_list = [[v for v in range(N) if adjacency_matrix[u][v]] for u in range(N)]
	f = threshold(N, MIN_THRESH, MAX_THRESH)
	b = cost_to_infect(N, adjacency_list)
	filename = "small_world-N" + str(N) +"-d" + str(density) + "-p" + str(p) + "-s" + str(seed)
	create_files(filename, adjacency_list, f, b)


if __name__ == "__main__":
	if (len(sys.argv) != 5):
		print("small_world_random_graph <N> <density> <p> <seed>")
		exit(0)
	N = int(sys.argv[1])
	density = int(sys.argv[2])
	p = float(sys.argv[3])
	seed = int(sys.argv[4])
	random.seed(seed)
	small_world_random_graph(N, density, p)
