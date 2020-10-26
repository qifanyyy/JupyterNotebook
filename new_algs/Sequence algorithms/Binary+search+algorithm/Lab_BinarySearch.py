
# Algorithm to find the target value using linear Serach for an unsorted array of values
def binarySearch(theValues,target):
	low=0
	high=len(theValues)-1
	while low<=high:
		mid=(high+low)/2
		mid=int(mid)
		if theValues[mid]==target:
			return True
		elif target<theValues[mid]:
			high=mid-1
		else:
			low=mid+1
	return False

# Algorithm to find the target value using linear Search for an sorted array of values

def sortedbinarySearch(theValues,target):
	low=0
	high=len(theValues)-1
	while low<=high:
		mid=(high+low)/2
		mid=int(mid)
		if theValues[mid]==target:
			return True
		elif target<theValues[mid]:
			high=mid-1
		elif target >theValues[mid]:
			low=mid+1
		else:
			return False
	return False




	