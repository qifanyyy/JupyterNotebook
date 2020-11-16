
# Algorithm to find the target value using binarySerach for an unsorted array of values

def linearSearch(theValues,target):
	n=len(theValues)
	for i in range(n):
		if theValues[i]==target:
			return True
	return False

# Algorithm to find the target value using linear Serach for an sorted array of values

def sortedLinearSearch(theValues,target):
	n=len(theValues)
	for i in range(n):
		if theValues[i]==target:
			return True
		elif theValues[i]>target:
			return False
	return False