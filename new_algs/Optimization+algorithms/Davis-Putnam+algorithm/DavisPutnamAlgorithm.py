
def copy_list(S):
	copy = []
	for i in range(len(S)):
		copy.append([])
		for x in range(len(S[i])):
			copy[i].append(S[i][x])
	return copy

def lit_check(atoms,S):
	sol = []
	for i in range(0,atoms):
			b = None
			for j in range(0,len(S)):
				if i in S[j] :
					if b == None:
						b = i
					elif b == i:
						continue
					elif b != i:
						b= None
						break
				elif -i in S[j]:
					if b== None:
						b = -i
					elif b == -i:
						continue
					elif b != -i:
						b = None
						break
			if b != None:
					return b
	return None

def obvious_assign(L,V):
	if L > 0:
		V[L] = 1
	else:
		V[-L] = -1
	return V

def propogate(A,S,V):
	i=0
	while i < len(S):
		if A in S[i] :
			S.pop(i)
			i -=1
		elif -A in S[i]:
			S[i].remove(-A)
		i +=1
	return S

def DP(atoms, S):
	V = [0]*(atoms)
	return dpAlg(atoms,S,V)


def dpAlg(atoms, S,V):
	bo = True
	n=0
	while (bo):
		bo = False
		#Base of recursion: Success or Failure
		if len(S) == 0:
			#for i in range(0,atoms):
			#	if V[i]==0:
			#		V[i]=1
			return V
		else:
			for i in range(0,len(S)):
				if len(S[i]) == 0:
					return None

		#Simple cases
		#Pure literal
		lit = lit_check(atoms,S)
		if lit != None:
			bo = True
			V = obvious_assign(lit,V)
			j = 0
			while j < len(S):
				if lit in S[j]:
					S.pop(j)
					j -= 1
				j +=1
			continue
		
		#Forced Assignment
		for i in range(0, len(S)):
			if len(S[i]) == 1:
				obvious_assign(S[i][0],V)
				S = propogate(S[i][0],S,V)
				bo = True
				break
		

	#Pick atom, try assignment
	Vnew = list(V)
	i = 0
	while(Vnew[i] != 0):
		i+=1
	Vnew[i] = 1
	
	
	S1 = copy_list(S)
	S1 = propogate(i,S1,Vnew)
	Vnew = dpAlg(atoms,S1,Vnew)
	
	if Vnew != None:
		return Vnew

	V[i] = -1
	S = propogate(-i,S,V)
	return dpAlg(atoms,S,V)


#C = [[-3,-1,5],[3,2],[-5,2],[-4,-2],[-1,-4,-5],[3,4,5],[-5,4] ]
#Sol = DP(6,C)
#print(Sol)


		
