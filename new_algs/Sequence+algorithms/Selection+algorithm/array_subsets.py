"""
@author: David Lei
@since: 7/11/2017

Given an array print out all subsets.

https://www.youtube.com/watch?v=bGC2fNALbNU&ab_channel=CSDojo

For example:
    array = [1, 2]

There will be no duplicates.

Expected output:
    {}
    {1, 2}
    {1}
    {2}

For an array of size n, there are 2^n subsets.

This is because we need to make the decision:
- should we include 1
- should we include 2

For each item we make a choice, do we include it: 2 outcomes either yes or no
Since there are n items we make this choice for n things.

2^n potential choices/outcomes/subsets.

Visually this looks like below starting with the empty set:

        ______ {}
       /n2
     {}
    /  \y2
   /n1  ------ {2}
{}
  \y1   ______ {1}
   \   /n2
    {1}
       \y2
        ------ {1, 2}

Where n_ means no don't pick _ and y means yes pick _

This looks like a recursion tree, so hints we can use recursion.
"""

arr = [1, 2, 3]

# CS Dojo's solutions, print out so dont need to use extra space and explores all the way down one as far as possible.
# This solution will find all possible variations from not taking item 0,
#   which requires trying to not take item 1
#       which requires trying to not take item 2
#           print this
#       now try take item 2
#           print this
#  now try take item 1
#       which requires trying to not take item 2
# ... and so on
# so the subset size is bounded by n, this is more space efficient as you try generate as much as possible from your
print("CS Dojo's soln")

def print_subset(subset):
    print("{", end="")
    printed = False
    for i in range(len(subset)):
        if subset[i] is not None:
            if i == len(subset) - 1:
                start = ", " if printed else ""
                print(start + str(subset[i]), end="")
            else:
                start = ", " if printed else ""
                print(start + str(subset[i]), end="")
                printed = True
    print("}")
def helper(array, subset, i):
    # We want to explore subset i as much as possible.
    if i == len(array):
        # Make our choices to choose things in this subset, just print it.
        print_subset(subset)
    else:
        # Make choices about the subset.
        subset[i] = None # Don't choose item i.
        helper(array, subset, i + 1)
        subset[i] = array[i] # Choose item i.
        helper(array, subset, i + 1)

def all_subsets_dojo(array):
    # A single subset has n items, for each item in array we choose
    # do i add into the subset or make it None.
    subset = [0] * len(array) # O(len(array)) extra space = O(n) space.
    helper(array, subset, 0)  # O(2^n) time.

all_subsets_dojo(arr)

# My solutions: all use extra space.
# I hold an extra 2^n space to each subset, each subset has at most n items.
# So 2^n * n extra space as an upper bound.

print("My soln: recursive")

def all_subsets_rec(arr, i, subsets):
    # subsets Grows to O(2^n) items each can have up to 2^n  subsets
    if i == len(arr):
        for subset in subsets:
            print(subset)
        return
    new = []
    for subset in subsets:
        look_at = arr[i]
        new.append(subset[::]) # Don't take item i.
        extended_subset = subset[::]
        extended_subset.append(look_at) # Take item i.
        new.append(extended_subset)
    i += 1
    all_subsets_rec(arr, i, new)

subsets = [[]]
all_subsets_rec(arr, 0, subsets)

print("My soln: iterative")
def all_subsets_itr(array):
    subsets = [[]] # Grows to O(2^n) items each can have up to 2^n  subsets.
    for i in range(0, len(array)): # Item we are looking at.
        new_subsets = []
        for subset in subsets:
            new_subsets.append(subset)
            extended_subset = subset[::]
            extended_subset.append(array[i])
            new_subsets.append(extended_subset)
        subsets = new_subsets
    print(subsets)
    space_count = 0
    for subset in subsets:
        for item in subset:
            space_count += 1
    print("space count - subsets held: %s, items in all subsets: %s" % (len(subsets), space_count))
    # 2^n space for subsets.
    # will have:
    # - 1 subset of None
    # - n subsets of 1
    # - n-1 subsets of 2
    # - ..
    # - 2 subsets of n-1
    # - 1 subset of n
    # there will be 2^n subsets and at most you can hold n items in 1 subset so
    # So 2^n * n extra space? This is bad :(
all_subsets_itr(arr)
