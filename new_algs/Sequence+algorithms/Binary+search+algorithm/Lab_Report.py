import random
from time import time
from Lab_LinearSearch import linearSearch, sortedLinearSearch
from Lab_BinarySearch import binarySearch, sortedbinarySearch


randomnum = random.sample(range(1000000),100000)
sortedrandomnum = sorted(randomnum)

target = random.choice(sortedrandomnum)

elapsed_unsorted=[]
elapsed_sorted=[]
elapsed_binary_unsorted=[]
elapsed_binary_sorted=[]

j=0
total_time=0


	
# Applying Algorithm for Unsorted Linear Search
for i in range(10000,100001,10000):
	start_time = time( ) 


	linearSearch(randomnum[0:i],target)

	end_time = time( ) 

	elapsed_unsorted.insert(j,end_time-start_time) 
	j+=1


print ("\nUnsorted Linear Search times")
for i in range(10):
	print (elapsed_unsorted[i])
	total_time=total_time+elapsed_unsorted[i]
print("Total Time Taken:",total_time)



# Applying Algorithm for Sorted Linear Search
for i in range(10000,100001,10000):
	start_time = time( ) 

	sortedLinearSearch(sortedrandomnum[0:i],target)	

	end_time = time( )

	elapsed_sorted.insert(j,end_time-start_time) 
	j+=1

print ("\nSorted Linear Search times")
for i in range(10):
	print (elapsed_sorted[i])
	total_time=total_time+elapsed_sorted[i]
print("Total Time Taken:",total_time)

# Applying Algorithm for Unsorted Binary Search

for i in range(10000,100001,10000):
	start_time = time( ) 

	binarySearch(randomnum[0:i],target)

	end_time = time( )

	elapsed_binary_unsorted.insert(j,end_time-start_time) 
	j+=1

print ("\nBinary Unsorted Search times")
for i in range(10):
	print (elapsed_binary_unsorted[i])
	total_time=total_time+elapsed_binary_unsorted[i]
print("Total Time Taken:",total_time)

# Applying Algorithm for Sorted Binary Search
for i in range(10000,100001,10000):
	start_time = time( ) 

	sortedbinarySearch(sortedrandomnum[0:i],target)

	end_time = time( )

	elapsed_binary_sorted.insert(j,end_time-start_time) 
	j+=1

print ("\nBinary Sorted Search times")
for i in range(10):
	print (elapsed_binary_sorted[i])
	total_time=total_time+elapsed_binary_sorted[i]
print("Total Time Taken:",total_time)


