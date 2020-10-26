import math
def insertionsort(A):
    global comp
    for i in range(1, len(A)): 
        key = A[i] 
        j = i-1
        while j >=0 and key < A[j] :
                
                A[j+1] = A[j] 
                j -= 1
        A[j+1] = key 
    return A

def findMedian(arr, l, n): 
    lis = [] 
    for i in range(l, l + n): 
        lis.append(arr[i]) 
          
    # Sort the array  
    lis.sort() 
  
    # Return the middle element 
    return lis[n // 2] 
    
def fourth(A):
    n = len(A)
    mod = n % 5
    div = math.floor(n / 5)

    fr = 0
    to = 5
    i = 0
    medians = []
    while div > 0:
        #print("fr:to:",A[fr:to])
        res = insertionsort(A[fr:to])
        #print(res)
        medians.append(res[2])
        fr +=5
        to += 5
        i += 1
        div -= 1
    if mod > 0:
        res = insertionsort(A[len(A)-mod:])
        #print(res)
        medians.append(res[math.floor(len(A[len(A)-mod:])/2)])
    return medians

def partitionOG(A,p,r,x):
    #print("Pivot:",x,"A:",A)
    for i in range(p, r): 
        if A[i] == x: 
            A[r],A[i] = A[i],A[r]
            break
    #print("New A:",A)
    i = p - 1
    j = p
    while j < r:
        #print("j=",j,"p=",p,"i=",i)
        if A[j] <= x:
            i=i+1
            A[i],A[j] = A[j],A[i]
            #print(A)
        j +=1
    A[i+1],A[r] = A[r],A[i+1]
    #print(A)
    #print("Partition done: ", i+1, "array:",A)
    return i+1

def idk(A):
    #print("idk(A) called, A= ",A)
    medians = fourth(A)
    medianmedian = fourth(medians)
    #print("Medians are:",medians, "Median of the medians is:", medianmedian)
    
    k = partitionOG(A,0,len(A)-1,medianmedian[0])
    #print("Partition result(number of low side median partition):",k)
    
    if k == 0 or k == 3:
        return medianmedian[0]
    elif k > 3:
        return idk(A[0:k])
    else:
        return idk(A[k+1:])
   
    return fourth(A[0:k])


    
A=[1,59,30,12,40,50,10,28,40,100,13,16,35,88,90,15] #4th smallest is 13
A2=[6,32,14,2,9,1,5,20]
A3=[5,1,35,6,6,62,3,34346,34,423,4,46,5,457,2,354,356,745,745,34,354,534,234,453,465,765,78,9,8,7,22,5,4,423,65,7,45,8,8,6,56,456,6,6,65,34,1,0]
print("4th smallest element is: ", idk(A))