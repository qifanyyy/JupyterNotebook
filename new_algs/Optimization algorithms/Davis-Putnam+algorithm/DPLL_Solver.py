import copy

def buildModel(model, P, value):
	modelcopy = copy.copy(model)
	if P[0] != '~':
		modelcopy[P] = value
	return modelcopy

def get_value(literal):
	if literal[0] == '~':
		return literal[1:], False
	else:
		return literal, True

def find_assignment(clause, model):
	P, value = None, None
	for literal in clause:
		l, v = get_value(literal)
		if l in model:
			if model[l] == v:
				return None, None # clause already True

		elif P:
			return None, None 
		else:
			P, value = l, v
	return P, value

def get_unitClause(cnf, model):
	for clause in cnf:
		P, value = find_assignment(clause, model)
		if P:
			return P, value
	return None, None

def removeAll(P, symbols):
	symbolscopy = copy.copy(symbols)
	del symbolscopy[symbolscopy.index(P)]
	return symbolscopy

# find if complement of the passed literal is present in the clauses
def find_complement(s, clauses):
	if s[0] == '~':
		compl = s[1:]
		flag = False
	else:
		compl = '~' + s
		flag = True

	for c in clauses:
		if compl in c:
			return True, flag
	return False, flag

# Find a pure if it exists
def get_pureSymbol(symbols, clauses):
	for s in symbols:
		for c in clauses:
			if s in c:
				 res, val = find_complement(s, clauses)
				 if res == False:
				 	return s, val
			if '~' + s in c:
				res, val = find_complement('~' + s, clauses)
				if res == False:
					return s, val
	return None, None



#This function finds if the passed clause is true, false or unknown
def is_true(clause, model = {}):
    if not model:
        return None

    flag = 0
    for literal in clause:
        if literal[0] == "~":
            compl = literal[1:]
        else:
            compl = "~" + literal
        if literal in model:
            if model[literal] == True:
                return True
            else:
                flag += 1
        elif literal not in model:
            if compl in model:
                if model[compl] == False:
                    return True
                else:
                    flag += 1
            else:
                continue

    if flag == len(clause):
        return False
    else:
        return None

'''
DPLL pseudo algorithm
function DPLL(Φ)
   if Φ is a consistent set of literals
       then return true;
   if Φ contains an empty clause
       then return false;
   for every unit clause {l} in Φ
      Φ ← unit-propagate(l, Φ);
   for every literal l that occurs pure in Φ
      Φ ← pure-literal-assign(l, Φ);
   l ← choose-literal(Φ);
   return DPLL(Φ ∧ {l}) or DPLL(Φ ∧ {not(l)});
'''
def DPLL(cnf, symbols, model):
	unknown_clauses = []
	for c in cnf:
		val = is_true(c, model)
		if val is False:
			return False
		if val is not True:
			unknown_clauses.append(c)
	if not unknown_clauses:
		return model

	# Calling Pure Symbols
	P, value = get_pureSymbol(symbols, unknown_clauses)
	if P:
		return DPLL(cnf, removeAll(P, symbols), buildModel(model, P, value))
	
	# Calling Unit Clause
	P, value = get_unitClause(cnf, model)
	if P:
		return DPLL(cnf, removeAll(P, symbols), buildModel(model, P, value))

	# Guessing a literal
	P, symbols = symbols[0], symbols[1:]
	return (DPLL(cnf, symbols, buildModel(model, P, True)) or DPLL(cnf, symbols, buildModel(model, P, False)))


def get_symbols(cnf):
	symbols = []
	for clause in cnf:
		for c in clause:
			if c[0] != '~':
				if c not in symbols:
					symbols.append(c)
	return symbols

# This function generates cnf statements
def generate_cnf(R):
    cnf = []

    for m in range(1, M + 1):
        clause = []
        for n in range(1, N+1):
            clause.append("X" + str([m, n]))
            for ni in range(n+1, N+1):
                clauseneg = []
                clauseneg.append("~X" + str([m, n]))
                clauseneg.append("~X" + str([m, ni]))
                cnf.append(clauseneg)
        cnf.append(clause)

    for x in range(1, M+1):
        for y in range(1, M+1):
            if R[x][y] == 1:
                for n in range(1, N+1):
                    clause = []
                    clause.append("X" + str([y, n]))
                    clause.append("~X" + str([x, n]))
                    cnf.append(clause)
                    clause = []
                    clause.append("X" + str([x, n]))
                    clause.append("~X" + str([y, n]))
                    cnf.append(clause)

    for x in range(1, M+1):
        for y in range(1, M+1):
            if R[x][y] == -1:
                for n in range(1, N+1):
                    clause = []
                    clause.append("~X" + str([x, n]))
                    clause.append("~X" + str([y, n]))
                    cnf.append(clause)

    symbols = get_symbols(cnf)
    return DPLL(cnf, symbols, {})

if __name__ == "__main__":
	try:
		f = open("input.txt", 'r')
	except Exception as err:
		print(err)

	inputList = f.readlines()

	params = []
	for word in inputList[0].split(' '): # first row indicates params
 		params.append(int(word))

	M = params[0] # Number of guests
	N = params[1] # Number of tables

	if M != 0 and N != 0:
		#R = [[0]*M]*M
		R = [[]]
		for x in range(0, M):
			inner = [[]]
			for y in range(0, M):
				inner.append(0)
			R.append(inner)

		for index in range(1, len(inputList)):
			b = inputList[index].split(' ')
			if b[2] == 'F' or b[2] == 'F\n':
				R[int(b[0])][int(b[1])] = 1
			else:
				R[int(b[0])][int(b[1])] = -1

		output = generate_cnf(R)

		with open('output.txt', 'w') as f:
			if output == False:
				f.write("no")
			else:
				f.write("Yes\n")
				Mylist = []
				for (k, v) in output.items():
					if v == True:
						Mylist.append(k)
				listnew = []
				for val in Mylist:
					listtmp = []
					tmp = val[2:-1].split(',')
					listtmp.append(int(tmp[0]))
					listtmp.append(int(tmp[1]))
					listnew.append(listtmp)
				for val in sorted(listnew):
					f.write(str(val[0]) + ' ' + str(val[1])+'\n')
		f.close()
	else:
		with open("output.txt", 'w') as f:
			f.write('no')
			f.close()



