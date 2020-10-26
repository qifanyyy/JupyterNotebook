import random

def min_conflicts(n):
	individual=list(range(n))
	while True:
		conflicts = find_conflicts(individual, n)
		if sum(conflicts) == 0:
			print(individual)
			return
		col = random_position(conflicts, lambda elt: elt > 0,n)
		vconflicts = [hits(individual, n, col, row) for row in range(n)]
		individual[col] = random_position(vconflicts, lambda elt: elt == min(vconflicts),n)
	
def random_position(li, filt,n):
	return random.choice([i for i in range(n) if filt(li[i])])

def find_conflicts(individual, n):
	return [hits(individual, n, col, individual[col]) for col in range(n)]

def hits(individual, n, col, row):
	total = 0
	for i in range(n):
		if i == col:
			continue
		if individual[i] == row or abs(i - col) == abs(individual[i] - row):
			total += 1
	return total

welcome_text="""
************ N-Queen Problem With Min-Conflict Algorithm **************
"""
print(welcome_text)
n=(int)(input('Enter the value of N \n -'))

min_conflicts(n) 