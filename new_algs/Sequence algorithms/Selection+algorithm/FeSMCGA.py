import   sys, math, random

# Read data in the simplest possible way
def	read_data(file):
	f = open(file, "r")
	x = f.readlines()
	f.close()
	Classes = []
	D = []
	for i in range(len(x)):
		xx = x[i].split(' ')
		tmp = []
		for j in range(len(xx) - 1):
			tmp.append(float(xx[j]))
		D.append(tmp)
		Classes.append(int(xx[len(xx) - 1]) )
	return [D, Classes]


def	read_names(file):
	f = open(file, "r")
	x = f.readlines()
	f.close()
	Names = []
	for i in range(len(x)):
		Names.append(x[i][0:len(x[i]) - 1])

	return Names

def	is_in(a, L):
	ln = len(L)
	for i in range(ln):
		if a == L[i]:
			return 1
	return -1

def	construct_population(K, ni, dim, vMIF, mxx, mnn, nc):
	Pop = []
	ran = mxx - mnn
	for i in range(ni):
		atributes = []
		nA = int(random.random() * (K - 1)) + 2
		for j in range(nA):
			atr = int(random.random() * (dim - 1))
			r = random.random()
			while is_in(atr, atributes) == 1 or r > ( (vMIF[atr] - mnn)/ran) + 0.01:
				atr = int(random.random() * (dim - 1))
				r = random.random()
			atributes.append(atr)
		Pop.append(atributes)
	return Pop


def   distance(V1, V2, dim):
	dd = 0.0
	for i in range(dim):
		dd = dd + abs(V1[i] - V2[i])
	return dd

def   diameter(dim, Dx, Ind, diam):
	if diam == 1:
	# The farthest possible points in the space
		mn = [100000000.0] * dim
		mx = [-100000000.0] * dim
		nl = len(Dx)
		D = []
		for i in range(nl):
			tmp = []
			for j in range(dim):
				a = Ind[j]
				tmp.append(Dx[i][a])
			D.append(tmp)

		for i in range(dim):
			for j in range(nl):
				if D[j][i] < mn[i]:
					mn[i] = D[j][i]
				if D[j][i] > mx[i]:
					mx[i] = D[j][i]

		Vmin = []
		Vmax = []
		for i in range(dim):
			Vmin.append(mn[i])
			Vmax.append(mx[i])
		dd = distance(Vmin, Vmax, dim)
	else:
		# the farthest points in the space
		mx = -10000000000.0
		nl = len(Dx)
		for i in range(nl):
			for j in range(i + 1, nl):
				dd = distance(Dx[i], Dx[j], dim)
				if dd > mx:
					mx = dd
		dd = mx
		
	return dd

def	sel(Di, Ind):
	nl = len(Ind)
	Dx = []
	for i in range(nl):
		Dx.append(Di[Ind[i]])
	return Dx

def   distance_matrix(dim, D, Ind):
	nl = len(D)
	DM = [None] * nl
	for i in range(nl):
		DM[i] = [0.0] * nl
	for i in range(nl):
		for j in range(i + 1, nl):
			V1 = sel(D[i], Ind)
			V2 = sel(D[j], Ind)
			dd = distance(V1, V2, dim)
			DM[i][j] = dd
			DM[j][i] = dd
	return DM

def   largest_distance(D, Label, c):
	W = []
	nl = len(Label)
	for i in range(nl):
		if Label[i] == c:
			W.append(i)
	mx = -100000000.0
	for i in range(len(W)):
		for j in range(i, len(W)):
			if D[W[i]][W[j]] > mx:
				mx = D[W[i]][W[j]]
	return mx

def   smallest_distance(DM, Label, c, nc):
	W = []
	nl = len(Label)
	for i in range(nl):
		if Label[i] == c:
			W.append(i)

	mn = [100000000.0] * (nc)

	# obtain the minimum distance between vectors of class c and
	# vectors for classes c2, c2 != c.
	for i in range(len(W)):
		for j in range(nl):
			if int(Label[j]) != c:
				if DM[W[i]][j] < mn[int(Label[j])]:
					mn[int(Label[j])] = DM[W[i]][j]

	# The minimum distance
	mn_all = min(mn)

	return mn_all


def   evaluate(dim, D, Label, c, nc, Diam, alfa):
	ev = 0.0
	# First, obtain SL, the largest distance between elements of the same class
	SL = largest_distance(D, Label, c)
	#print "SL = ", SL
	# Then, obtain the smallest distance between a vector in class c and
	# a vector r in other class
	OS = smallest_distance(D, Label, c, nc)

	if Diam == 0.0:
		error = 1.0
	else:
		error = (alfa * (SL/Diam)) + (1.0 - alfa) * (1.0 - (OS / Diam))

	return error


def	evaluate_population(Population, ni, Dx, Classes, vectors_in_classes, nc, alfa):
	Ev = []
	Avg = 0.0
	Bst = -100.0
	for i in range(ni):
		# verify that the solution does not have repeated kinases
		exist = []
		bad = 0
		for j in range(len(Population[i])):
			if is_in(Population[i][j], exist) != -1:
				eval = 0.0
				bad = 1
				break
			exist.append(Population[i][j])
		if bad == 0:
			dim = len(Population[i])
			DM = distance_matrix(dim, Dx, Population[i])
			eval = 0.0
			Diam = diameter(dim, Dx, Population[i], diam)
			for c in range(nc):
				ev = evaluate(dim, DM, Classes, c, nc, Diam, alfa)
				eval = eval + ev
			eval = 1.0 - (eval / float(nc))

		if eval > Bst:
			Bst = eval
			who = i
		Avg = Avg + eval
		Ev.append(eval)

	Avg = Avg / ni
	return [Ev, Bst, Population[who], Avg]

# select individuals accordingly to their performance
def     select_population(Population, Ev, band, Best):
	tot = 0.0
	PS = len(Population)
	for i in range(len(Ev)):
		tot = tot + Ev[i]
	Ps = []
	t = 0.0
	for i in range(PS):
		Ps.append(t+(Ev[i]/tot))
		t = t + Ev[i]/tot
	New_P = [None] * PS
	#"""
	if band == 1:
		New_P[0] = Best
	for i in range(band, PS):
	#"""
		w = random.random()
		for j in range(len(Ps)):
			if w <= Ps[j]:
				New_P[i] = Population[j]
				break
	return New_P


def	cross_population(Pop, K):
	pairs = []
	N_pop = []
	ni = len(Pop)
	while len(pairs) < len(Pop):
		i = int(random.random()* ni)
		while is_in(i, pairs) == 1:
			i = int(random.random()* ni)
		j = int(random.random()* ni)
		while is_in(j, pairs) == 1:
			j = int(random.random()* ni)
		pairs.append(i)
		pairs.append(j)

		# chose a crossing point
		# the number of attributes of individual i
		na1 = len(Pop[i])
		# the number of attributes of individual i
		na2 = len(Pop[j])
		cp1 = int(random.random()* (na1 - 1)) + 1
		cp2 = int(random.random()* (na2 - 1)) + 1

		# a pair of new individuals
		ni1 = []
		ni2 = []
		# First new individual inherits from parent i from attribute 0 to attribute cp1
		for k in range(cp1):
			ni1.append(Pop[i][k])
		# And then from parent j from attribute cp2 to na2
		for k in range(cp2, na2):
			ni1.append(Pop[j][k])
		# Second new individual inherits from parent j from attribute 0 to attribute cp2
		for k in range(cp2):
			ni2.append(Pop[j][k])
		# And then from parent i from attribute cp2 to na2
		for k in range(cp1, na1):
			ni2.append(Pop[i][k])

		N1 = []
		mn = K
		if len(ni1) < K:
			mn = len(ni1)
		for i in range(mn):
			N1.append(ni1[i])
		N2 = []
		mn = K
		if len(ni2) < K:
			mn = len(ni2)
		for i in range(mn):
			N2.append(ni2[i])
		# New individuals go to new population
		# New individuals go to new population

		N_pop.append(N1)
		N_pop.append(N2)

	return N_pop


def	mutate_population(Pop, pm, dim, K, vMIF, mxx):
	# there are several mutation mechanisms...
	# Change an attribute for another
	N_pop = []
	for i in range(len(Pop)):
		ni = []
		na = len(Pop[i])
		for j in range(na):
			p = random.random()
			if p < pm:
				atr = int(random.random() * (dim - 1))
				r = random.random()
				while atr == Pop[i][j] or r > (vMIF[atr]/mxx) + 0.01:
				#while atr == Pop[i][j] or r > vMIF[atr] + 0.01:
					atr = int(random.random() * (dim - 1))
					r = random.random()
				ni.append(atr)
			else:
				ni.append(Pop[i][j])
		N_pop.append(ni)

	# What about adding a new attribute
	for i in range(len(N_pop)):
		if len(N_pop[i]) < K:
			p = random.random()
			if p < pm:
				atr = int(random.random() * (dim - 1))
				r = random.random()
				while is_in(atr, N_pop[i]) == 1 or r > vMIF[atr] + 0.01:
					atr = int(random.random() * (dim - 1))
					r = random.random()
				N_pop[i].append(atr)
	
	return N_pop


def	write_data(file, Best, D, nv, Z, Best_ev, K, Lbs, Names, epochs, ni):
	f = open(file, "w")
	dim = len(Best)
	f.write(str(dim))
	f.write("\n")
	f.write("#")
	for j in range(dim):
		#f.write(str(Best[j]))
		f.write(str(Names[Best[j]]))
		f.write(" (")
		f.write(str(Best[j]))
		f.write(") ")
	f.write(str(Best_ev))
	f.write(" max K: ")
	f.write(str(K))
	f.write(" ni: ")
	f.write(str(ni))
	f.write(" epochs: ")
	f.write(str(epochs))
	f.write("\n")
	for i in range(nv):
		for j in range(dim):
			Atr = Best[j]
			#f.write(str(D[Atr][i]))
			f.write(str(D[i][Atr]))
			f.write(" ")
		#f.write(str(Z[i]))
		f.write(Lbs[i])
		f.write("\n")
	f.close()

def	read_labels(file):
	cont = 1
	Lbs = []
	f = open(file, "r")
	x = f.readlines()
	for i in range(len(x)):
		xx = x[i].split('\n')
		Lbs.append(xx[0])
	return Lbs


def	average_size(Pop):
	AVG = 0.0
	ln = len(Pop)
	for i in range(ln):
		AVG = AVG + len(Pop[i])
	AVG = AVG / ln
	return AVG


def	write_vmd(file, vMD, Names):
	f = open(file, "w")
	for i in range(len(vMD)):
		f.write(Names[i])
		f.write(" ")
		f.write(str(vMD[i]))
		f.write("\n")
	f.close()

def	different_instances(L):
	n = 1
	nl = len(L)
	for i in range(1, nl):
		if L[i] != L[i-1]:
			n = n + 1
	return n


def	distance_vector(A, B, dim):
	d = 0.0
	for i in range(dim):
		d = d + abs(A[i] - B[i])
	return d


def	dist_individual_variables(nc, dim, Dx, Classes, alfa):
	EV = []
	for i in range(dim):
		DM = distance_matrix(1, Dx, [i])
		eval = 0.0
		Diam = diameter(1, Dx, [i], diam)
		for c in range(nc):
			print "Var ", i, " class ", c
			ev = evaluate(1, DM, Classes, c, nc, Diam, alfa)
			eval = eval + ev
		eval = 1.0 - (eval / float(nc))
		print "Variable ", i, " C = ", eval
		EV.append(eval)

	return EV


# the number of different classes (cancer cell lines)
def	different_instances(Z):
	lz = len(Z)
	Classes = []
	for i in range(lz):
		if is_in(Z[i], Classes) == -1:
			Classes.append(Z[i])
	return Classes

def	vectors_in_each_class(Classes, nc, Dx):
	vectors_in_class = [None] * nc
	for i in range(nc):
		vectors_in_class[i] = []
	nd = len(Dx)
	for i in range(nd):
		cl = int(Classes[i])
		vectors_in_class[cl].append(i)
	return vectors_in_class

"""
This program searches the attribute space for a list (subspace) of up to K attributes such that distance between vectors of the same class is
minimun and distance between centroids for different classes is maximum.
An extensive search (brute force) is not possible as the number of permutations grows as A^K, where A is the number of attributes (dimension)a. Thus,
an heuristic search is requiered. We implemented a genetic algorithm to search
for that space
"""
Dt = read_data(sys.argv[1])
D = Dt[0]
dim = len(D[0])
Classes = Dt[1]
Names = read_names(sys.argv[8])

# the different classes
diff_classes = different_instances(Classes)
# the number of different classes
nc = len(diff_classes)

alfa = float(sys.argv[10])
diam = int(sys.argv[11])
# Number of vectors
nv = len(D)
# Maximum number of attributes in solutions
K = int(sys.argv[2])
# number of individuals in the population
ni = int(sys.argv[3])

# The vectors in each class
vec = vectors_in_each_class(Classes, nc, D)

# Dist_clusters for each variable
# the number of classes
print "Computing C for individual variables"
vMD = dist_individual_variables(nc, dim, D, Classes, alfa)
mxx = max(vMD)
mnn = min(vMD)
write_vmd(sys.argv[9], vMD, Names)

print "Creating initial solutions..."
Population = construct_population(K, ni, dim, vMD, mxx, mnn, nc)
av = average_size(Population)

epochs = int(sys.argv[4])
pm = float(sys.argv[5])

band = 0
Best_ev = -100.0
Best = []
delta = 40
AVG = []
ult = 10
# The labels
Lbs = read_labels(sys.argv[6])

Dx = D
for i in range(epochs):
	print "Evaluating solutions in epoch ", i
	Ev = evaluate_population(Population, ni, Dx, Classes, vec, nc, alfa)
	print "gen = ", i, " avg = ", Ev[3]

	AVG.append(Ev[3])
	if Ev[1] > Best_ev:
		Best_ev = Ev[1]
		Best = Ev[2]
	if i % 10 == 0:
		print "Gen = ", i, " Best gen = ", Ev[1], " Avg = ", Ev[3]
		print "Best = ", Best, " Ev = ", Best_ev
	S_Population = select_population(Population, Ev[0], band, Ev[2])
	C_Population = cross_population(S_Population, K)
	M_Population = mutate_population(C_Population, pm, dim, K, vMD, mxx)
	Population = [None] * ni
	for j in range(ni):
		Population[j] = M_Population[j]
	if i > delta and AVG[i] <= AVG[i-delta] and band == 0 and ult + delta < i:
		print "MUT CAT"
		PM = pm
		pm = pm * 4
		band = 1
		tm = 0
	if band == 1:
		if tm > 5:
			print "Mut nrm"
			pm = PM
			band = 0
			ult = i
		else:
			tm = tm + 1

	if i % 10 == 0:
		av = average_size(Population)
		print "av = ", av
	if i % 10 == 0 and i > 0:
	#if i % 20 == 0 and i > 0:
		write_data(sys.argv[7], Best, Dx, nv, Classes, Best_ev, K, Lbs, Names, i, ni)

write_data(sys.argv[7], Best, Dx, nv, Classes, Best_ev, K, Lbs, Names, i, ni)
