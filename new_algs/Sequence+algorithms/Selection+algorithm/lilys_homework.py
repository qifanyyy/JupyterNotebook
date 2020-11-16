"""
@author: David Lei
@since: 18/04/2017
@modified: 

- array of n distinct integers
- can swap any 2 elements any number of times
- distinct values

variation of selection sort --> need to do this on both input array and reverse input array, but this is O(n^2) and times out.

https://www.hackerrank.com/challenges/lilys-homework

Tripped up here: Does order matter --> YES.

say sorted ordering is [a, b, c, d] and the input array is [c, a, b, d]

number of swaps looping forwards:
1. swap c with a: [a, c, b, d]
2. swap c with b: [a, b, c, d]
- Done, 2 steps.

number of swaps looping backwards:
1. swap b with d: [c, a, b, d]
2. swap b with c: [b, a, c, d]
3. swap a with b: [a, b, c, d]
- Done, 3 steps.

Looping forwards here is smaller.

Likewise, there are cases in which looping backwards is better, eg: input array is [d, c, a, b]

number of swaps looping forwards:
1. swap d with a: [a, c, d, b]
2. swap c with b: [a, b, d, c]
3. swap d with c: [a, b, c, d]
- Done, 3 steps.

number of swaps looping backwards:
1. swap b with d: [b, c, a, d]
2. swap a with b: [a, b, c, d]
- Done, 2 steps.
"""

n = int(input())

data = [int(x) for x in input().split(' ')]


def solve(data):
    # Map input numbers to their indexes.
    index_map = {}  # Handles TLE.
    for number_index in range(len(data)):
        index_map[data[number_index]] = number_index

    sorted_data = data[:]  # Copy data.
    sorted_data.sort()

    swaps = 0
    for i in range(n):
        if data[i] == sorted_data[i]:
            continue
        # Need to do a swap.
        wanted_number = sorted_data[i]
        current_number = data[i]
        # Do swap
        data[i], data[index_map[wanted_number]] = data[index_map[wanted_number]], data[i]
        # Update mappings.
        index_map[current_number] = index_map[wanted_number]  # Current number is now at index of wanted number as they swapped.
        index_map[wanted_number] = i  # Wanted number is in correct position.
        # Increment swaps.
        swaps += 1
    return swaps

copy1 = data[:]
copy2 = data[:]
copy2.reverse()
# Reverse order of input array, print whichever has smallest number of swaps.
print(min(
    solve(copy1),
    solve(copy2)
))


