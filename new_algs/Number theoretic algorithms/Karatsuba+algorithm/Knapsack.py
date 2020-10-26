def knapSack(S,size,values):

	n = len(values)
	K = [[0 for i in range(S+1)]for j in range(n+1)]

	for i in xrange(1,n+1):
		for j in xrange(1,S+1):
			if size[i-1] <= j:
				K[i][j] = max(values[i-1]+K[i-1][j-size[i-1]],  K[i-1][j])
			else:
				K[i][j] = K[i-1][j]

	return K[-1][-1]

values = [60, 100, 120]
size = [10, 20, 30]
S = 50
print knapSack(S, size, values)
