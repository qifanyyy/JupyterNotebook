import random, math, time

#find the "k"th smallest element in array "a" with "n" elements by using Randomized-select in CLRS
def randomized_select(a, n, k):

    # CLRS textbook partition pseudocode
    # page: 147
    def Partition(A, p, r):
        x = A[r]    # select pivot as the last element in list
        i = p - 1   # get starting position
        for j in range(p, r):
            if A[j] <= x:    # check current value is smaller than pivot
                i = i + 1
                A[i], A[j] =  A[j], A[i]    # switch location
        A[i + 1], A[r] = A[r], A[i + 1]     # move pivot to correct location
        return i + 1

    # CLRS textbook randomized partition pseudocode
    # page: 154
    def RandomPartition(A, p, r):
        # select a random position as pivot
        try:
            i = random.randint(p, r)
        except ValueError:
            i = random.randint(r, p)
        A[i], A[r] = A[r], A[i]  # send pivot to last location in array

        # sort by pivot
        return Partition(A, p, r)

    # CLRS textbook randomized select pseudocode
    # page: 186
    def RandomSelect(A, p, r, i):

        # if only one in the array return it
        if p == r:
            return A[r]

        # get a random index
        q = RandomPartition(A, p, r)

        # check if we have found item
        # i = k what we have found is equal to search then return
        # i < k what we have found is larger then search between p to q
        # i > k what we have found is larger then search between q to r
        k = q - p + 1
        if i == k:
            return A[q]
        elif i < k:
            return RandomSelect(A, p, q-1, i)
        else:
            return RandomSelect(A, q + 1, r, i - k)

    return RandomSelect(a.copy(), 0, (n-1), k + 1)

#find the "k"th smallest element in array "a" with "n" elements by using the worst-case linear-time algorithm in CLRS
def  deterministic_select(a, n, k):

    # sepcial array grouping function
    divide = lambda A, s: [ A[i*s : (i+1)*s]   for i in range(math.ceil(len(A)/s)) ]

    # CLRS textbook insertion sort pseudocode
    # page: 17
    def InsertionSort(A):
        for j in range(1, len(A)):
            key = A[j]
            i = j - 1
            while i > -1 and A[i] > key:
                A[i + 1] = A[i]
                i = i - 1
            A[i + 1] = key
        return A

    # find the middle element in the given lst
    def findMedian(lst):

        # sort list using insertion sort
        sorted_list = InsertionSort(lst)

        # find the middle element by dividing list by 2
        middle = math.floor(len(sorted_list) / 2)

        # if list is even, get the lower element
        if len(lst) % 2 == 0:
            middle = middle - 1

        # return the middle element of the sorted list
        return sorted_list[middle]

    # A customized version of CLRS textbook partition pseudocode
    # page: 147
    # instead of select last element, send my current element to the last location
    def Partition(A, p, r, x):
        i = 0
        # find index of my searching element
        for j in range(p, r):
            if A[j] == x: break
            i = i + 1
        A[i], A[r] = A[r], A[i]    # send my current element to the back

        i = p - 1    # get starting position
        for j in range(p, r):
            if A[j] <= x: # check current value is smaller than pivot
                i = i + 1
                A[i], A[j] = A[j], A[i] # switch location
        A[i + 1], A[r] = A[r], A[i + 1] # move pivot to correct location
        return i + 1

    # CLRS textbook SELECT pseudocode
    # page: 189-190
    def Select(lst, p, r, i, group_size = 5):

        n = len(lst)

        # step 1 : Divide the n elements of the input array into floor(n/5) groups of 5 elements each and at most one group made ...
        if n <= group_size:
            newlst = InsertionSort(lst)
            return newlst[i-1] # <- array start's at 0 index

        # step 2 : Find the median of each of the ceil(4/5) group sby first insertion sorting the elements of each group (of ...
        group_list = divide(lst, group_size)

        # step 3 : Use SELECT recursively to find the median x of the ceil(n/5) medians found in step 2.
        median_list = [findMedian(group) for group in group_list]

        # step 4 : Partition the input array around the median-of-medians x using the modified version of PARTITION. Left k be one more...
        next_i = math.ceil(len(median_list)/2)  # middle guy
        median_of_median = Select(median_list, 0, len(median_list) - 1, next_i)

        # step 5 : i  = k return x, Otherwise, use SELECT recursively to find the ith smallest on the low side if i < k, or the (i-k) th....
        q = Partition(lst, p, r, median_of_median)
        k = q - p + 1

        if i < k:
            return Select(lst[p:q], p, len(lst[p:q]) - 1, i)
        elif i == k:
            return lst[q]
        else:
            return Select(lst[q + 1:(r + 1)], 0, len(lst[q + 1:(r + 1)]) - 1 , i - k)

    return Select(a.copy(), 0, (n-1), (k + 1))

#check whether the "k"th smallest element in array "a" with "n" elements is the "ans"
def checker(a, n, k, ans):

    # CLRS textbook counting sort pseudocode
    # page: 168
    def RadixSort(A, n):
        largest = max(A)
        digitPlace = 1

        a = len(str(largest)) + 1

        while largest/digitPlace > 0 and len(str(digitPlace)) <= a:

            B = [0] * n
            C = [0] * 10

            for j in range(0, n):
                index = int( (A[j]/digitPlace)%10 ) # use module to find  current digit place
                C[index] = C[index] + 1

            # Count the cummulative values
            for i in range(1, 10):
                C[i] = C[i] + C[i-1]

            for j in range( n-1, -1, -1 ):
                index = int((A[j] / digitPlace) % 10) # use module to find  current digit place
                B[ C[ index ] - 1 ] = A[j]
                C[index] = C[index] - 1

            for i in range(0, n):
                A[i] = B[i]

            # increase digitplace by one 0
            digitPlace = digitPlace * 10

        return A

    lst = a.copy()
    sorted_lst = RadixSort(lst, n)
    if sorted_lst[k] == ans:
        return True
    return False


if __name__ == "__main__":

    '''
        This is code for checkingmy custom data time set
    '''
    for i in range(1, 3):
        with open("custom_{0}.txt".format(i)) as file:
            lines = [line for line in file]
            head = lines.pop(0).split()

            n = int(head[0])
            k = int(head[1])
            a = list(map(lambda x: int(x), lines))

            start = time.time()
            ans1 = randomized_select(a, n, k)
            end = time.time() - start
            c = checker(a, n, k, ans1)
            print("n: {0}, k: {1}, randomzed_select_result: {2}, checker result:{3}, run time: {4}".format(n, k, ans1, c, end))

            start = time.time()
            ans2 = deterministic_select(a, n, k)
            end = time.time() - start
            c = checker(a, n, k, ans2)
            print("n: {0}, k: {1}, deterministic_select_result: {2}, checker result:{3}, run time: {4}".format(n, k, ans2, c, end))

    '''
        This code is for checking the time complexity using TA's test data
    '''

    time_complexity_dataset = {};

    for i in range(5):
        with open("{0}.txt".format(i)) as file:
            lines = [line for line in file]
            head = lines.pop(0).split()
            time_complexity_dataset[i] = { "n" : int(head[0]), "k" : int(head[1]), "data" : list(map(lambda x : int(x), lines)) }

    for key in time_complexity_dataset:
        dataset             = time_complexity_dataset[key]
        run_time_random     = 0
        run_time_linear     = 0
        test_count          = 5

        time_complexity_dataset[key]["time_complexity_random"] = []
        time_complexity_dataset[key]["time_complexity_linear"] = []

        for i in range(test_count):

            start_time = time.time()
            a = randomized_select(dataset["data"], dataset["n"], dataset["k"])
            time_complexity_dataset[key]["time_complexity_random"].append(time.time() - start_time)

            start_time = time.time()
            b = deterministic_select(dataset["data"], dataset["n"], dataset["k"])
            time_complexity_dataset[key]["time_complexity_linear"].append(time.time() - start_time)

            status = "correct" if a == b else "incorrect"
            print(i, dataset["n"], a, b, status)

    print("number of iteration:", test_count)
    for key in time_complexity_dataset:
        item = time_complexity_dataset[key]
        print(item["n"], item["k"])

        time_complexity_random = 0
        time_complexity_linear = 0
        for i in range(5):
            time_complexity_random = time_complexity_random + item["time_complexity_random"][i]
            time_complexity_linear = time_complexity_linear + item["time_complexity_linear"][i]
            print(item["time_complexity_random"][i], item["time_complexity_linear"][i])
        print("============={0} | {1}".format(time_complexity_random/5, time_complexity_linear/5))



