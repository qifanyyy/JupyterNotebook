'''
Quick sort is a divide and conquer algorithm that selects an element
as a pivot point (the first in this case). It then selects two variables to point
left and right of the list (omitting the pivot). Left points to the low index (0+1)
right points to the high index (len-1). While the value at left is less than pivot
iterate right, and the opposing rule for the value at right.
If the rule above isn't met, then swap left and right.
if left is greater than right the that becomes the new pivot

:param  aList   list    The list to sort

:return list
'''
def sort(aList):
    if len(aList) <= 1:
        return aList
    else:
        pivot = aList[0]
        less = []
        more = []
        pivots = []
        for item in aList:
            less.append(item) if item < pivot else more.append(item) if item > pivot else pivots.append(item)
    return sort(less) + pivots + sort(more)
