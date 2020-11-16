from sys import stdin
from DP import dp

#Front_End
# create atoms, create index link to atoms 
def create_atoms(start, goal, k):
	atoms = {}
	atoms2num = {}
	#atom1: value(r,v,i)
	for i in range(k+1):
		for reg in start.keys():
			for v in start.values():
				atoms[len(atoms) + 1] = ("Value", reg, v, i)
				atoms2num[("Value", reg, v, i)] = len(atoms) 


	#atom2: Assign(rA,rB,i)
	for i in range(k):
		for rA in start.keys():
			for rB in start.keys():
				if rA != rB:
					atoms[len(atoms) + 1] = ("Assign", rA, rB, i)
					atoms2num[("Assign", rA, rB, i)] = len(atoms)

	return atoms, atoms2num 

#create cnfs 
def create_CNF(atoms2num, start, goal, k):
	cnfs = []

	#unique value
	for i in range(k+1):
		for reg in start.keys():
			for valx in start.values():
				for valy in start.values():
					if valy != valx:
						literal1 = -1 * atoms2num[("Value", reg, valx, i)] 
						literal2 = -1 * atoms2num[("Value", reg, valy, i)] 
						cnfs.append([literal1, literal2])

	#positive effects of actions
	for i in range(k):
		for rA in start.keys():
			for rB in start.keys():
				if rA != rB:
					for v in start.values():
						literal1 = -1 * atoms2num[("Assign", rA, rB, i)] 
						literal2 = -1 * atoms2num[("Value", rB, v, i)] 
						literal3 = atoms2num[("Value", rA, v, i+1)] 
						cnfs.append([literal1, literal2, literal3])
						
	#Frame axiom
	for i in range(k):
		for reg in start.keys():
			for v in start.values():
				literals = []
				literals.append(-1 * atoms2num[("Value", reg, v, i)])
				for regn in start.keys():
					if reg != regn:
						literals.append(atoms2num[("Assign", reg, regn, i)])
				literals.append(atoms2num[("Value", reg, v, i+1)])
				cnfs.append(literals)

	#Incompatible assignments
	for i in range(k):
		for rA in start.keys():
			for rB in start.keys():
				for rC in start.keys():
					if rA != rB and rB!= rC and rA != rC:
						literal1 = -1 * atoms2num[("Assign", rA, rB, i)]
						literal2 = -1 * atoms2num[("Assign", rB, rA, i)]
						literal3 = -1 * atoms2num[("Assign", rA, rC, i)]
						literal4 = -1 * atoms2num[("Assign", rB, rC, i)]
						cnfs.append([literal1, literal2])
						cnfs.append([literal1, literal3])
						cnfs.append([literal1, literal4])

	#starting state
	for reg, v in start.items():
		literal = atoms2num[("Value", reg, v, 0)]
		cnfs.append([literal])
	


	#goal state
	for reg, v in goal.items():
		literal = atoms2num[("Value", reg, v, k)]
		cnfs.append([literal])


	return cnfs


#Back_End Generate Answers
def solution(output, k, atoms):

	if not output:
		return print("No Solution")

	assign_res = []

	
	for key,v in output.items():
			if v and atoms[key][0] == "Assign":
				i = atoms[key][3]
				assign_res.append([atoms[key][1], atoms[key][2], i])


	solution = ''
	assign_res.sort(key = lambda x : x[2])	
	print(assign_res)

	for t in range(k):
		print("Cycle %d :" % (t+1))
		for i in range(len(assign_res)):		
			if assign_res[i][2] == t:
				solution += "R%d = R%d; " % (assign_res[i][0], assign_res[i][1])
				print(solution)
			solution = ''


def main():
	start = {}
	goal = {}
	str_start = stdin.readline().split()
	str_goal = stdin.readline().split()
	k = int(stdin.readline())

	len_start = len(str_start)
	len_goal = len(str_goal)

	for i in range(0, len_start, 2):
		start[int(str_start[i])] = str_start[i + 1]


	for j in range(0, len_goal, 2):
		goal[int(str_goal[j])] = str_goal[j + 1]

	atoms, atoms2num = create_atoms(start, goal, k)
	cnfs = create_CNF(atoms2num, start,goal,k)
	output = dp(cnfs)


	return solution(output, k, atoms)

if __name__ == "__main__":
	main()



						





