import random
myrandomnumber = random.sample(range(1000000),100000)
mysortedrandomnumber = sorted(myrandomnumber)
randomnumberfromthelist = random.choice(mysortedrandomnumber)
elapsed_unsorted=[]
elapsed_sorted=[]
elapsed_smallest=[]
elapsed_binary=[]
from time import time
j=0

def linearSearch(theValues,target):
	n=len(theValues)
	for i in range(n):
		if theValues[i]==target:
			return True
	return False

def sortedLinearSearch(theValues,target):
	n=len(theValues)
	for i in range(n):
		if theValues[i]==target:
			return True
		elif theValues[i]>target:
			return False
	return False

def findSmallest(theValues):
	n=len(theValues)
	smallest=theValues[0]
	for i in range(1,n):
		if theValues[i]<smallest:
			smallest=theValues[i]
	return smallest


def binarySearch(theValues,target):
	low=0
	high=len(theValues)-1
	while low<=high:
		mid=(high+low)/2
		mid=int(mid)
		if theValues[mid]==target:
			return true
		elif target<theValues[mid]:
			high=mid-1
		else:
			low=mid+1
	return False
	

for i in range(10000,100001,10000):
	start_time = time( ) # record the starting time

	#run algorithm
	linearSearch(myrandomnumber[0:i],randomnumberfromthelist)
	end_time = time( ) # record the ending time
	elapsed_unsorted.insert(j,end_time-start_time) # compute the elapsed time
	j+=1
print ("\nUnsorted Linear Search times")
for i in range(10):
	print (elapsed_unsorted[i])
print

for i in range(10000,100001,10000):
	start_time = time( ) # record the starting time
	sortedLinearSearch(mysortedrandomnumber[0:i],randomnumberfromthelist)	
	end_time = time( ) # record the ending time
	elapsed_sorted.insert(j,end_time-start_time) # compute the elapsed time
	j+=1
print ("\nSorted Linear Search times")
for i in range(10):
	print (elapsed_sorted[i])
print

for i in range(10000,100001,10000):
	start_time = time( ) # record the starting time
	findSmallest(myrandomnumber[0:i])	
	end_time = time( ) # record the ending time
	elapsed_smallest.insert(j,end_time-start_time) # compute the elapsed time
	j+=1
print ("\nFinding Smallest element times")
for i in range(10):
	print (elapsed_smallest[i])
print

for i in range(10000,100001,10000):
	start_time = time( ) # record the starting time

	#run algorithm
	binarySearch(myrandomnumber[0:i],randomnumberfromthelist)
	end_time = time( ) # record the ending time
	elapsed_binary.insert(j,end_time-start_time) # compute the elapsed time
	j+=1
print ("\nBinary Search times")
for i in range(10):
	print (elapsed_binary[i])
	



