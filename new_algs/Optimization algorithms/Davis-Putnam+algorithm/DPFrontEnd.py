import sys,DavisPutnamAlgorithm,DPBackEnd

input_file = sys.argv[1]
input_string = open(input_file,"r")


try:
	k=0
	registers = 0
	start_vals= []
	end_vals = []

	#print('flow 1')
	
	i = 0
	for line in input_string:
		split_line = line.split()
		if (len(split_line) % 2 != 0) and i<2:
			print(split_line)
			raise IOError
		if i ==0:
			registers = int(len(split_line)/2)+1
			start_vals = []
			for x in range(1,len(split_line),2):
				start_vals.append(split_line[x])
			end_vals=[-1]*registers
		elif i == 1:
			for x in range(0,len(split_line),2):
				end_vals[int(split_line[x])] = split_line[x+1]
			end_vals.pop(0)
		elif i == 2:
			k = int(split_line[0])
		elif i>3:
			raise IOError
		i +=1
	
	#print('flow 2')

	vals=[]
	for x in range(0,len(start_vals)):
		if start_vals[x] not in vals:
			vals.append(start_vals[x])

	#Atoms
	atoms = [0]
	val_stop = 0
	for t in range(0,k+1):
		for r in range(1,registers):
			for v in vals:
				tup = (r,v,t)
				atoms.append(tup)
				val_stop += 1
	assign_stop = val_stop
	for t in range(0,k):
		for ra in range(1,registers):
			for rb in range(1,registers):
				if ra != rb:
					tup = (ra,rb,t)
					atoms.append(tup)
					assign_stop +=1

	#print('flow 3, Uniqueness')
	
	clauses = []
	#Uniqueness Axiom
	ii = 0
	for t in range(0,k+1):
		for v in vals:
			for r in range(1,registers):
				tup = (r,v,t)
				index = atoms.index(tup)
				for vb in vals:
					if v != vb:
						tup1 = (r,vb,t)
						i = atoms.index(tup1)
						c = [-index,-i]
						clauses.append(c)
						ii +=1

	

	#Positive Effects of Actions Axiom
	for t in range(0,k):
		for v in vals:
			for ra in range(1,registers):
				tup1 = (ra,v,t+1)
				index = atoms.index(tup1)
				for rb in range(1,registers):
					if ra != rb:
						tup2 = (ra,rb,t)
						i1 = atoms.index(tup2)
						tup3 = (rb,v,t)
						i2 = atoms.index(tup3)
						#print('not ',tup2, ' or not ', tup3,'or ',tup1)
						c = [-i1,-i2,index]
						clauses.append(c)
						ii+=1



	#Incompatible Assignment Axiom
	for t in range(0,k):
		for ra in range(1,registers):
			for rb in range(1,registers):
				for rc in range(1,registers):
					if ra != rb and rb != rc and ra != rc:
						tup = (ra,rb,t)
						index = atoms.index(tup)
						tup = (rb,ra,t)
						i1 = atoms.index(tup)
						tup = (ra,rc,t)
						i2 = atoms.index(tup)
						tup = (rb,rc,t)
						i3 = atoms.index(tup)
						c = [-index,-i1]
						clauses.append(c)
						c = [-index,-i2]
						clauses.append(c)
						c = [-index,-i3]
						clauses.append(c)
						ii+=3
	


	#Frame Axiom
	for t in range(0,k):
		for ra in range(1,registers):
			for v in vals:
				tup = (ra,v,t)
				index1 = atoms.index(tup)
				tup = (ra,v,t+1)
				index2 = atoms.index(tup)
				c = [-index1,index2]
				for rb in range(1,registers):
					if ra != rb:
						tup = (ra,rb,t)
						c.append(atoms.index(tup))
				clauses.append(c)
				ii+=1

	


	#Starting and Ending States
	for r in range(1,registers):
		tup = (r,start_vals[r-1],0)
		index1 = atoms.index(tup)
		#print('start ',tup)
		c1 = [index1]
		clauses.append(c1)
		if (end_vals[r-1] != -1):
			tup = (r,end_vals[r-1],k)
			index2 = atoms.index(tup)
			#print('goal ',tup)
			c2 = [index2]
			clauses.append(c2)

	
	#print('flow 4', len(atoms))

	#print(atoms)

	#Using DPAlgorithm and output solution
	solution = DavisPutnamAlgorithm.DP(len(atoms),clauses)
	if solution != None:
		#print(solution)
		DPBackEnd.back_out(solution,atoms,val_stop,assign_stop,k)
	else:
		print('None')
		text_file = open("DPSolution.txt","w")
		text_file.write('None')
		text_file.close()



		


except IOError:
	print ("Error, program spec input file has odd numbered first or second line or more than three lines in text")
