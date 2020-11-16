#/bin/python3

'''
    An example of interpolation search (advanced binary search)
    Interpolation search is a variant of binary search.
    This algorithm works on probing the position of the required value

    To probe the position interpolation needs to be able to understand the key, and the equation
    that calculates the mid position must be able to interpret this.
    You have to do computations on the keys to estimate a likely distance.

    Initially, the probe position is the position of the middle most item of the collection.

    Preconditions of the list:
        - It must be sorted, like most searching algorithms
        - The data in the list should be evenly (to a degree) distributed.
        - The mid test should be able to understand the key - in this case integers/float

    Below we use this algorithm to calculate the mid point:
    mid = (Lo + ((N - A[Lo]) * (Hi - Lo)) // (A[Hi] - A[Lo]))

    where
       A    = list
       Lo   = Lowest index of the list
       Hi   = Highest index of the list
       N    = Search item
       A[n] = Value stored at index n in the list

    Because we are dividing down the mid point, we have a complexity of O(log log n)

    :param aItem    mixed   An item to search for in the list
    :param aList    list    An ordered list of number items to search

    :return mixed
'''
def search (aItem, aList):
    low = 0
    high = len(aList) - 1
    while aList[low] <= aItem and aList[high] >= aItem:
        if low == high or aList[low] == aList[high]:
            return False
        mid = (
            low + (
                (aItem - aList[low]) * (high - low)
            ) // (aList[high] - aList[low])
        )
        if aList[mid] == aItem:
            return mid
        if aList[mid] < aItem:
            low = mid + 1
        elif aList[mid] > aItem:
            high = mid - 1
