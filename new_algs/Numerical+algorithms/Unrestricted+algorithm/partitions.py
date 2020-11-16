##############################################
# Unrestricted Partitions: Efficient solution
##############################################

pos = lambda k: (k*(3*k-1))/2 #Positive Pentagonal numbers

neg = lambda k:(k*(3*k + 1))/2 #Negative Pentagonal numbers

def nP(n, memo = [1,1]): 	#Reverse summation of alternating Pentagonal numbers.
							#Tested in under 10 seconds for n up to 6*10^4 and 100 Queries.  
	if n < 0:
		return 0
	elif memo[n] != 0:
		return memo[n]
	else:
		memo[n] = sum([(-1)**(i-1)*(nP(n-pos(i), memo) + nP(n-neg(i), memo)) for i in range(int((n/2)**0.5)+50,0,-1)]) #%(10**9 + 7)
		return memo[n]

#This could be cleaned up with a dictionary, I was just hoping to save memory
L = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, 792, 1002, 1255, 1575, 1958, 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977, 21637, 26015, 31185, 37338, 44583, 53174, 63261, 75175, 89134, 105558, 124754, 147273, 173525]
A = [0]*(6*10**4 - 49)
L+=A

# for _ in range(input()):
#     print nP(input(), L)#%(10**9 + 7)

###################################################################################################################
#Restricted Partitions: Efficient solution

#Solves coin change problem when C = [1,2,5,10,20,50,100,200] (Europe) or C = [1,5,10,25,100,200] (North America)
##################################################################################################################


# N,M = map(int, raw_input().split(' ')) # N - number to be partitioned, M - is useless data that represents the length of C below
# C = map(int, raw_input().split(' ')) #C is parts to which N can be partitioned. 

C.sort()

A = [[0 for j in range(M)] for i in range(N+1)]

A[0] = [1 for _ in range(M)]
for i in range(1,N+1):
	if i%C[0]==0:
		A[i][0] = 1
	else:
		A[i][0] = 0
	for j in range(1,M):
		if i>=C[j]:
			A[i][j]+=A[i][j-1]
			A[i][j]+=A[i-C[j]][j]
		else:
			A[i][j] = A[i][j-1]

print (A[N][-1])

######################################################################################################
#Original Solution (closed formula) for Restricted partitions with parts C = [1,2,5,10,20,50,100,200]
######################################################################################################
def f(n,b):
	#sum of the Floor of (5k+b)/2
	m = int(n/2)
	if n % 2 == 0:
		return 5*(m**2) + (b+2)*m + b/2
	else:
		return (5*m+b+2)*(m+1)

def inside(c,i):
	Ni = 100*i+c
	ri = Ni % 10
	xi = (Ni - ri)/10		
	mid_total = 0
	for j in range(xi+1):
		yij = xi-j
		lij = yij % 5
		aij = (yij - lij)/5
		left_total = (f(aij,lij) + aij+1) #% (10**9 + 7)
		
		zij = 10*j+ri
		lij = zij % 5
		aij = (zij - lij)/5
		right_total = (f(aij,lij) + aij+1) #% (10**9 + 7)
		
		mid_total += left_total*right_total #% (10**9 + 7)

	return mid_total

def waysToMakeChange(N):
	#Computes specifically the number of restricted partitions with parts [1,2,5,10,20,50,100,200]
	c = N % 100
	d = (N - c)/100
	grand_total = 0
	for i in range(d+1):		
		grand_total += (int((d-i)/2)+1)*inside(c,i) #% (10**9 + 7)
	return grand_total

#########################################################
#Related Functions; e.g. generator for actual partitions
#########################################################

#No good past n = 50.
def generatePartitions(n):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2*x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]


################################
#Less efficient implementations
################################

## Naive Solution to restricted partitions

def nRPNaive(n,L):
	if L == [1]:
		return 1
	elif n < L[-1]:
		return nRPNaive(n,L[:-1])
	else:
		tot = 0
		for k in range(int(n/L[-1])+1):
			tot += nRPNaive(n - k*L[-1], L[:-1])
		return tot

## Partitions of n with exactly k parts.
def part(n,k, memo = {(5,2):2}):	 
	if k>n:
		return 0
	elif k in {1,n-1,n}:
		return 1
	elif k == 2:
		return int(n/2)
	elif (n,k) in memo:
		return memo[(n,k)]
	else:		
		memo[(n-k,k)] = part(n-k,k)
		memo[(n-1,k-1)] = part(n-1,k-1)
		return memo[(n-1,k-1)] + memo[(n-k,k)]

## nP(n) = \frac{1}{n} \sum_k \sigma(n-k)*nP(k) with \sigma(k) = the sum of proper divisors of k

def primesTo(n):
	if n == 1:
		return []
	if n in {2,3}:
		if n == 3:
			return [2,3]
		else:
			return [2]
	z = [1]*(n+2)
	k = 2
	while k<= n:
		for i in range(k, int(n/k)+1):
			z[k*i] =  0
		j=k
		while True:
			j+=1
			if z[j]==1:
				k = j
				break
	l = []
	for i in range(2,len(z)-1):
		if z[i] == 1:
			l.append(i)
	return l

def largestPrimeFactor(n):
	P = primesTo(int(n**0.5)+1)
	for i in range(len(P)):
		if n%P[i] == 0:
			return P[i]
	return n

def factors(n):
	if n == 1:
		return []
	if n in P:
		return [int(n)]
	p = largestPrimeFactor(n)
	return [p] + factors(n/p)

def sumDivisors(k):
	f = factors(k)
	df = {x:f.count(x) for x in set(f)}
	sum = 1
	for p in set(f):
		sum = sum * int((p**(df[p]+1)-1)/(p-1)) 
	return sum

# A dynamic recursive algorithm to count partitions, 
# but it already takes forever when n = 500 and 
# exceeds recursion depth at n = 997.
def numPartitions(n, memo = {0:1,1:1,2:2,3:3}):
	if n in memo:
		return memo[n]
	else:
		count = numPartitions(n-1, memo) + sumDivisors(n)
		for k in range(2,n):
			count += sumDivisors(n-k)*numPartitions(k, memo)
		memo[n] = count/n
		return memo[n]
