
#/bin/python
'''
Shell sort is an efficient sorting algorithm based on insertion sort.
This algorithm avoids large shifts, that hamper insertion sort.

This algorithm uses insertion sort on sublists, defined by a given interval.
The final insertion sort sweep across the entire list then has to do minimal swaps
to ensure the list is sorted.


Pseudocode:

Given a list
Set an initial gap
Iterate across each index item in aList
    If the index is greater than the gap, and the item at index-gap is greater than the current item
        Then place the item at index-gap at the current index position of the list
        Then move the index back to the position index-gap
    Place the current item, at the current index position of the list
Calulate the next gap

Given [10, 9, 6, 5, 11, 8, 1, 2, 19, 15, 4, 88]
First it will skip over the first half of the items  (6)
It will then compare the second half with the first half, swapping out high with low
Next it will set the gap to a new value (2)
Skip the first two, and compare them with the next 2, repeat through the list
Sompare the first 2, with the next 2, and swap out the high and low
The final gap will be 1, so do a single insertion sort sweep through the list
    -  making minimal changes

:param list     aList   The list to sort
'''
def sort(aList):
    # initial gap for the sublist
    gap = len(aList) // 2
    while gap:
        # loop over each item in n time
        for i, item in enumerate(aList):
            # for the sublist from gap -> end
            while i>= gap and aList[i - gap] > item:
                # if i = 11 and  gap = 5, aList[6] > aList[11], aList[11] = aList[6]
                aList[i] = aList[i-gap]
                # move to one less in the gap (4)
                i = i - gap
            # place the current item at 4
            aList[i] = item
        # calculate next gap
        gap = 1 if gap == 2 else int((gap * 5.0) // 11)
    return aList
