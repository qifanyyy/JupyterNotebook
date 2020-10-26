'''
    A Recursive Binary Search Implementation
    Binary search divides a problem down by
    half on each iteration of searching an
    ordered list of items. It's part of a
    divide and conquer family of algorithms

    :param aItem    mixed   An item to search for in the list
    :param aList    list    An ordered list of items to search
    :param low      int     The lowest index to search
    :param high     int     The highest index to search

    :return mixed
'''
def search (aItem, aList, low = 0, high = None):
    high = len(aList) if high is None else high
    mid = (high + low) // 2
    if low >= high :
        return False
    if aItem is aList[mid]:
        return mid
    elif aItem < aList[mid]:
        return search(aItem, aList, low, mid)
    elif aItem > aList[mid]:
        return search(aItem, aList, mid+1, high)
