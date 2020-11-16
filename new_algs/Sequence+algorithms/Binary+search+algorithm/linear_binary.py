# Linear Search and Binary Search Algorithms:
# Algorithm prints the Boolean value of the required element

#Linear Search Algorithm
def linear_search(l,key):
	for value in l:
		if value==key:
			return True
	else:
		return False
		print("This will never get Executed")

#l is the list here
l=[10,20,30,40,50]
key=30
print(linear_search(l,key))

# output: True

#Binary Search Alogrithm

def binary(l,key):
	if len(l)==0:
		return False
	else:
		mid = len(l)//2
		if l[mid]==key:
			return True
		elif key < l[mid]:
			return binary(l[:mid],key)
		else:
			return binary(l[mid+1:],key)

#l is the list here
l=[10,20,30,50,60,70,80]
key=50
print(binary(l,key))

# output: True
#Note: Your list should be sorted for Binary Search


