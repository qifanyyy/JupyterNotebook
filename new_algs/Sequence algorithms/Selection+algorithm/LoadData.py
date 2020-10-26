import math
def normalizeData(data):
	N = len(data)
	for col in range(1, len(data[0])):
		# calculate the sum
		s = 0
		for row in range(N):
			s += data[row][col]
		avg = s / N
		# calculate std deviation
		sum_squares = 0
		for row in range(N):
			sum_squares += (data[row][col] - avg)**2
		std_dev = math.sqrt(sum_squares / (N - 1))
		# replace data by normalized value
		for row in range(N):
			data[row][col] = (data[row][col] - avg) / std_dev
	
def loadData(path_to_txt):
	data = []
	with open(path_to_txt) as f:
		line = f.readline()
		while line:
			temp = line.split()
			for i in range(len(temp)):
				temp[i] = float(temp[i])
			data.append(temp)
			line = f.readline()
	return data


'''
data = loadData("../data/CS170_SMALLtestdata__96.txt")
for row in data:
	print(row)
print("\n\n\n")
normalizeData(data)
for row in data:
	print(row)
'''
