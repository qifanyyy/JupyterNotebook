import time
# Search the list from beginning to end for target element, checking if it is in the list
def algorithmA(S,x):
    """Linear Search algorithm (algorithm A) that sequentially iterates over the entire list, checking if it matches the target value.
    Parameters
    ---------------
        S : list
            The input list of integers
        x : int
            The target value"""
    # store input list in new list
    list1 = []
    for i in S:
        list1.append(i)
    # iterate through new list, checking if target element is contained in it
    for i in list1:
        if i == x:
            return True
    return False


# Standard merge sort algorithm
def mergeSort(S):
    """Standard merge sort algorithm using divide and conquer approach.
    Parameters
    ---------------
        S : List
            The list of integers being sorted"""
    if len(S) > 1:
        # divide list into 2 sublists
        subList1 = S[:len(S)//2]
        subList2 = S[len(S)//2:]
        # recursive calls
        mergeSort(subList1)
        mergeSort(subList2)
        a = 0
        b = 0
        c = 0
        # merge sublists to produce sorted sublists
        while a < len(subList1) and b<len(subList2):
            if subList1[a] < subList2[b]:
                S[c] = subList1[a]
                a+=1
            else:
                S[c] = subList2[b]
                b+=1
            c+=1
        while a < len(subList1):
            S[c]=subList1[a]
            a+=1
            c+=1
        while b < len(subList2):
            S[c]=subList2[b]
            b+=1
            c+=1


def binarySearch(S, x):
    """Binary search algorithm to find a value in a sorted list.
    It starts by checking the middle of the list, eliminating half the list by checking if the target value is greater or less than the middle, and repeats.
    Parameters
    ---------------
        S : List
            The sorted list of integers in which to search for the target value
        x : int
            The target value being searched for"""
    first = 0
    last = len(S)-1
    done = False
    while first<=last and not done:
        mid = (first+last)//2
        if S[mid] == x:
            done = True
        else:
            if x<S[mid]:
                last = mid-1
            else:
                first = mid+1
    return done

def generateRandomList(n):
    """Create a list of n randomly generated even integers
    Parameters
    ---------------
        n :
            The name of the animal"""
    import random
    list1 = []
    c = 0
    while c < n:
        rand = random.randint(0,n)
        if ((rand % 2) == 0):
            list1.append(rand)
            c+=1
    return list1


def createSearchValues(S, k):
    """Generates list of k search values, half of which are in S, and half of which are odd (not in S).
    Parameters
    ---------------
    S : list
        Half of this list will be a search value (in the output list)
    k : int
        The quantity of search values (size of output list)"""
    import random
    elementsInS = []
    randomOddIntegers = []
    c = 0
    while c < (k//2):
        elementsInS.append(random.choice(S)) #generate random element in S and append to new list
        c+=1
    c = 0
    while c < (k//2):
        rand = random.randint(0,len(S))
        if not((rand % 2) == 0):
            randomOddIntegers.append(rand) #append random odd integer to new list
            c+=1
    return elementsInS + randomOddIntegers #return finished search value list


def compareAlgorithms(n):
    """Iterate through values of k starting at 10.
    For each k, generate a list of search values and compare the runtime performace for algorithm A and algorithm B.
    Parameters
    ---------------
    n : int
        The size of the list being searched over by each algorithm
    """
    S = generateRandomList(n) # generate a random list of n even integers
    for k in range(10,10000):
        # Create a list of k target values to be searched for in each algorithm (half in the list, half not)
        searchList = createSearchValues(S,k)

        preAlgA = time.time() # check the time prior to finding the search values with algorithm A
        # Iterate through the search list, trying to find each value in S using algorithm A
        for i in searchList:
            algorithmA(S,i)
        algA_time = (time.time() - preAlgA) # record the running time of algorithm A finding those search values

        preAlgB = time.time() # check the time prior to finding the search values with algorithm B
        mergeSort(S) # sort list S using merge sort
        # Iterate through the search list, trying to find each value in sorted list S with binary search
        for i in searchList:
            binarySearch(S,i)
        algB_time = (time.time() - preAlgB) # record the running time of algorithm B finding those search values

        # return the current k value if it is the first k value at which algorithm B was faster than algorithm A by more than 0.01 second
        if (algA_time - algB_time) > 0.01:
            return k
            break
    return

#set all averages to 0 initially, to have k values added to them
avg1000 = 0
avg2000 = 0
avg5000 = 0
avg10000 = 0

#execute each algorithm 500 times with a data set of size 1000,
#adding k values when algorithm B becomes faster than algorithm A by > 0.01 second
for i in range(500):
    minK = compareAlgorithms(1000)
    if minK > 0:
        avg1000 += minK
avg1000 = avg1000/500

#execute each algorithm 500 times with a data set of size 2000,
#adding k values when algorithm B becomes faster than algorithm A by > 0.01 second
for i in range(500):
    minK = compareAlgorithms(2000)
    if minK > 0:
        avg2000 += minK
avg2000 = avg2000/500

#execute each algorithm 500 times with a data set of size 2000,
#adding k values when algorithm B becomes faster than algorithm A by > 0.01 second
for i in range(500):
    minK = compareAlgorithms(5000)
    if minK > 0:
        avg5000 += minK
avg5000 = avg5000/500

#execute each algorithm 500 times with a data set of size 2000,
#adding k values when algorithm B becomes faster than algorithm A by > 0.01 second
for i in range(500):
    minK = compareAlgorithms(10000)
    if minK > 0:
        avg10000 += minK
avg10000 = avg10000/500

#print each average for their respective data set size
print("Algorithm B becomes faster than algorithm A at approximately k = " + str(avg1000) + " for n = 1000")
print("Algorithm B becomes faster than algorithm A at approximately k = " + str(avg2000) + " for n = 2000")
print("Algorithm B becomes faster than algorithm A at approximately k = " + str(avg5000) + " for n = 5000")
print("Algorithm B becomes faster than algorithm A at approximately k = " + str(avg10000) + " for n = 10000")
