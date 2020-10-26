import math
import random
import time

# recursive function that implements mergsort
# for a list of numbers
def mergeSort(A):
    if len(A) > 1:
        mid = (int)(len(A)/2)
        left = A[:mid]
        right = A[mid:]
        
        mergeSort(left)
        mergeSort(right)

        i = 0
        j = 0
        k = 0
        
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                A[k] = left[i]
                i += 1
            else:
                A[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
           A[k] = left[i]
           i += 1
           k += 1
        while j < len(right):
           A[k] = right[j]
           j += 1
           k += 1
    return

# fucntion for partitioning in quicksort or quickselect
# returns the piviot position
def partition(A,low,high):
    pivot = A[low]
    j = low

    for i in range(low+1,high+1):
        if A[i] < pivot:
            j += 1
            A[j],A[i] = A[i],A[j]
    pivotPos = j
    A[low],A[pivotPos] = A[pivotPos],A[low]
    return pivotPos

# function for finding the kth smallest element
# using mergesort, returns the value of k
def select1(A,x):
    B = list(A)
    if x <= len(B) and x > 0:
        mergeSort(B)
        return B[x-1]
    return

# iterative function for finding the kth smallest element
# using partion from quicksort, returns the value of k
def select2(A,low,high,x):
    B = list(A)
    while low <= high:
        i = partition(B,low,high)
        if x == i+1:
            return B[i]
        elif x < i+1:
            high = i-1
        else:
            low = i+1
    return

# recursive function for finding the kth smallest element
# using partion from quicksort, returns the value of k
def select3(A,low,high,x):
    B = list(A)
    if low <= high:
        i = partition(B,low,high)
        if x == i+1:
            return B[i]
        elif x < i+1:
            return select3(B,low,i-1,x)
        else:
            return select3(B,i+1,high,x)
    return

# recursive function for finding the kth smallest element
# using partion from quicksort and MM as the pivot, 
# returns the value of k
def select4(A,n,k):
    B = list(A)
    r = 5
    sizeOfM = math.floor(n/r)
    M = list()

    if n <= r:
        B.sort()
        return B[k-1]

    for i in range(sizeOfM):
        low = i * r
        high = low + r
        M.append(select4(B[low:high],r,math.ceil(r/2)))

    V = select4(M,sizeOfM,math.ceil(sizeOfM/2))
    indexOfV = B.index(V)
    B[0],B[indexOfV] = B[indexOfV],B[0]
    pivotPosition = partition(B,0,n-1)

    if k-1 == pivotPosition:
        return (V)
    elif k-1 < pivotPosition: 
        return select4(B[0:pivotPosition],pivotPosition,k)
    else: 
        return select4(B[pivotPosition+1:n],n-pivotPosition-1,k-pivotPosition-1)

# test for algorithms
trails = 5
loops = 20

for i in range(5):
    print("***********")
    print("Trial",i)
    print("***********")
    const = 250
    for n in range(loops):
        n += 1
        if n > 4:
            size = const
            const = size*2
        elif n == 1:
            size = 10
        elif n == 2:
            size = 50
        elif n == 3:
            size = 100
            
        A = random.sample(range(size),size)

        for x in range(5):
            k = math.floor((x % 5) * (size/4))
            if k == 0:
                k = 1
            start1 = time.time()
            select1(A,k)
            end1 = time.time()
            print("select1 n =",size,"k =",k,":",end1-start1)

            start2 = time.time()
            select2(A,0,size-1,k)
            end2 = time.time()
            print("select2 n =",size,"k =",k,":",end2-start2)

            start3 = time.time()
            select3(A,0,size-1,k)
            end3 = time.time()
            print("select3 n =",size,"k =",k,":",end3-start3)

            start4 = time.time()
            select4(A,size,k)
            end4 = time.time()
            print("select4 n =",size,"k =",k,":",end4-start4)
            print()

        print()
        print()