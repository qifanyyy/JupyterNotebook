"""
@author: David Lei
@since: 21/08/2016
@modified: 

How it works: compares 2 items (bubble), moves larger towards the end
Invariants: at end of each iteration, the very last element is sorted

Time complexity
- best O(n), when list is already sorted
- worst O(n^2), when list is sorted in reverse
- avg O(n^2)

Space complexity
- O(1), doesn't need any more space

Stablity: yes as > and not >=
"""

def bubble_sort(arr):
    count = 0
    for j in range(len(arr)-1):
        swapped = False
        for i in range(len(arr)-1): # inner comparison loop
            count += 1
            # compare 2 elements
            if arr[i] > arr[i+1]:
                temp = arr[i]
                arr[i] = arr[i+1]
                arr[i+1] = temp
                swapped = True
        if not swapped:             # means this is already sorted
            break
    print(count)
    return arr
if __name__ == "__main___":
    arr = [1,2,3,4]
    print(bubble_sort(arr[::-1]))
