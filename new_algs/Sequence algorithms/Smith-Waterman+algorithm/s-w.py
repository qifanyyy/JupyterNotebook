def PrintMatrix(M):
	print "  ",
	for i in range(len(M[0])):
		print str(i) + ".",
	print
	for i in range(len(M)):
		print str(i), M[i]
	print

def GenerateMatrix(M, column, row):
	for i in range(row + 1):
		aux = []
		for j in range(column + 1):
			aux.append(0)
		M.append(aux)
# a = "ATAGACGACATACAGACAGCATACAGACAGCATACAGA"
# b = "TTTAGCATGCGCATATCAGCAATACAGACAGATACG"

a = "ACACACTAC"
b = "AGCACACA"

row = len(b)
column = len(a)

M = []
gap = column - row
match = 0
err = -1

# count match #
m_ = column
if row < m_:
	m_ = row
for i in range(m_):
	if a[i] == b[i]:
		match += 1
# generate matrix solution #
GenerateMatrix(M, column, row)
PrintMatrix(M)
# algorithm smith-water #
for i in range(1, row + 1):
	for j in range(1, column + 1):
		if a[j - 1] == b[i - 1]:
			w = match
		else:
			w = err
		m1 = M[i - 1][j - 1] + w
		m2 = M[i - 1][j] + err
		m3 = M[i][j - 1] + err
		M[i][j] = max(m1, m2, m3)
PrintMatrix(M)
# get path solution #
# 1: diagonal, 2: top, 3: left #
i = row
j = column
path = []
while i > 0 and j > 0:
	max_ = -1
	if M[i-1][j-1] > max_:
		max_ = M[i-1][j-1]
		dir_ = 1
	if M[i][j-1] > max_:
		max_ = M[i][j-1]
		dir_ = 2
	if M[i-1][j] > max_:
		max_ = M[i-1][j]
		dir_ = 3
	if dir_ == 1:
		i -= 1
		j -= 1
	elif dir_ == 2:
		j -= 1
	else:
		i -= 1
	path.append(dir_)
	# print i, j, max_
print path
# generate new string #
a_ = ""
b_ = ""
i = column
j = row
for k in range(len(path)):
	if path[k] == 1:
		i -= 1
		j -= 1
		a_ = a[i] + a_
		b_ = b[j] + b_
	elif path[k] == 2:
		i -= 1
		a_ = a[i] + a_
		b_ = "-" + b_
	else:
		j -= 1
		a_ = "-" + a_
		b_ = b[j] + b_
# print solution #
print a_
print b_