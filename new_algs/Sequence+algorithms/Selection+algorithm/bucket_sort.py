"""
@author: David Lei
@since: 21/08/2016
@modified:

Visualization: https://www.cs.usfca.edu/~galles/visualization/BucketSort.html

a.k.a bin sort

Key idea: use keys ad indices to put them into a bucket, key k placed in bucket[k]

How it works: puts elements of array into buckets, each bucket sorted individually (by another sorting algo or
                recursively applying bucket sort)
            1. Set up array of empty "buckets"
            2. Scatter - go over input array putting each item in a bucket
            3. Sort each non empty bucket
            4. Gather - visit buckets in order and put elements back into original array

Ideal when the range of the data is small compared to n (keys to be sorted) and the data will be spread evenly

Time complexity:
        - O(n+k) when key distribution is event = best case = avg case
        - O(n+n) = O(n) when items to be sorted = buckets (and even distribution)
        - O(k*n) when a bucket is dense (lots of keys in one bucket)
        - O(n^2) when k is large like n = worst case
    O(k) to create buckets
    O(n) to iterate through input_arr
    O(k * d) to go through buckets and take stuff out
    where d is the distribution of the keys amongst buckets
    O(k + n + k * d) when distributed evenly O(n + k + k) d will be small = O(n + 2k) = O(n + k) = best
    when a bucket is very dense, d will approach n so O(n + k + n*k) = O(n + k + n*k) = O(n*k)
    when k (the range) is really big (approaching n, like in the big_arr) O(n*n) = O(n^2) = worst

    Assuming that the input is uniformly distributed, then we can expect that there won't be too many
    numbers that fall into each bucket

- dependent on number of buckets
    fast when data being sorted can be distributed between buckets evenly,

Good when:
    - additional O(n+k) memory not an issue, n to copy array, k for the number of buckets
    - elements expected to be fairly evenly distributed
    - as k is a constant for a set number of buckets, when small it gives O(n) performance
Bad when:
    - all elements are put into the same bucket
    - individual buckets are sorted, if everything put into 1 bucket, complexity dominated by inner
    sorting algo

Space complexity: O(n + k)

    Not too sure why wiki says O(n*k) but my reasoning is O(n + k) as outlined in
    http://kenics.net/algo/bucket_sort/

    - O(k) for buckets, we put n items into these buckets O(n)
        so O(k + n)

    - O(n) for output array of same size as input

    so O(k + n + n) = O(k + 2n) = O(k + n)

Stability: if buckets act as queues (FIFO) (append to end, graph first and put in output)

Note: number of buckets matters, i'll just use 10 as an example
- can be used with hash fn to distribute elements into buckets

"""

def bucket_sort(arr, k):
    """
    Based on Data Structures and Algorithms in Python
    This can't handle decimals

    :param arr: Sequence of integer keys
    :param k: an integer such that all keys are in the range [0, k-1]
    :return: arr in sorted order
    """
    output = []                         # n space O(n)
                                        # this operation dominated by k O(k), O(k) space and time
    buckets = [[] for _ in range(k)]    # let B be an array of k sequences (acting as queues)
    for key in arr:                     # O(n) time
        buckets[key].append(key)
    for bucket in buckets:              # O(k) time
        for element in bucket:          # if elements distributed well, then constant?
            output.append(element)      # else worst case everything is in one bucket O(n)
    print(buckets)
    return output

def insertion_sort(arr):
    for i in range(1, len(arr)):
        point = i - 1
        temp = arr[i]

        while point >= 0 and arr[point] > temp:
            arr[point + 1] = arr[point]
            point -= 1
        arr[point + 1] = temp
    #return arr



def bucket_sort_wi(arr, less_than_one=False):
    """Based on MIT Introduction to Algorithms - uses insertion sort to sort things in the buckets,
    can handle decimals"""
    n = len(arr)
    buckets = [[] for _ in range(n+1)]  # bucket array of same length as input
    # put elements in buckets
    for i in range(n):
        if less_than_one:
            idx = int((n * arr[i])//1)    # multiple arr[i] by n and floor the result
        else:
            idx = int(arr[i]//1)
        buckets[idx].append(arr[i])   # add item into bucket
    # sort each bucket with insertion sort
    # as we are assuming the data is uniformly distributed, insertion sort works well as it is quite fast with
    # a small number of elements
    # http://stackoverflow.com/questions/19617790/why-is-insertion-sort-quicker-when-the-input-size-is-small
    print("Before sorting buckets: " + str(buckets))
    output = []
    for b in buckets:
        if b:                        # avoid empty lists
            insertion_sort(b)
            for e in b:              # concatenate all elements in all buckets
                output.append(e)     # now that bucket is sorted add all into output, nested loop will be small
    print("After sorting buckets: " + str(buckets))
    return output                    # if data uniformly distributed


if __name__ == "__main__":
    arr_big_range = [9,1,0,4,5,6, 100, 50, 3, 1, 2, 1001,500, 10, 1]
    arr_small_range = [2,3,4,5,6,1,2,3,4,5,1,2,3,4,5,0,1,2,3,4,1,2,3,4,1,2,3,4,8,1,8,6,2,0]
    print("Big range: 1002")
    print(bucket_sort(arr_big_range, 1002))
    print("\nSmall range: 9")
    print(bucket_sort(arr_small_range, 9))

    # these won't work as you need to account for the massive range, so the distribution of data is too large
    # if we pass on the range as k like in the other implementation it will work
    #print(bucket_sort_wi(arr_big_range))
    #print(bucket_sort_wi(arr_small_range))
    print("\nMIT Version")
    # this data is fairly spread out and will work as they fit into n buckets
    arr_dec = [1.5, 1.1, 1.0, 2.7, 0.1, 3.4, 2.2]
    arr_mit = [.78, .17, .39, .26, .72, .94, .21, .12, .23, .68]
    print(bucket_sort_wi(arr_dec))
    print()
    print(bucket_sort_wi(arr_mit, less_than_one=True))
