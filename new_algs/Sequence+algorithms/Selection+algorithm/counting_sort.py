"""
@author: David Lei
@since: 21/08/2016
@modified:

Not a comparison sort, so comparison O(n log n) lower bound doesn't apply

Visualization: https://www.cs.usfca.edu/~galles/visualization/CountingSort.html

How it works: Integer sorting algorithm - it counts the number of objects
                Applies when elements to be sorted come from a finite set i.e. integers 0 to k
                create an array of buckets to count how many times each element has appeared --> then place back in right order

            example: arr = [7, 1, 5, 2, 2]
            1. create array of buckets (size of max value +1) or of size k+1 where k is the max value in our set to sort
                    buckets = [[], [], [], [], [], [], [], []] # k + 1 buckets, k = 7
            2. count each element, look at the element in the input arr and put it in corresponding bucket
                    buckets = [[0], [1], [1,1], [0], [0], [1], [0], [1]]    # visual rep
                    buckets = [ 0,   1,    2,    0,   0,   1,   0,   1]     # actual rep
                    index:     0    1     2     3    4    5    6    7
                    means that we have zero 0's, two 2's, one 7 etc
            3. add up number of elements in the bucket array left to right (cumulative sum)
                    buckets = [0, 1, 3, 3, 3, 4, 4, 5]  # buckets[-1] == len(input_arr)
            4. put them back to output
                a) loop over input_arr
                b) find index of element in input arr in bucket (or count arr)
                c) put that element of input_arr into output arr in the index specified in bucket (after adding counts)
                    output = [?, ?, ?, ?, ?]           # same len as input
                    input = [7, 1, 5, 2, 2]
                    buckets = [0, 1, 3, 3, 3, 4, 4, 5] # after counting
                        idx    0  1  2  3  4  5  6  7
                    put 7 in index 5-1 (look at idx 7 of buckets) of output, decrement buckets[7] by 1
                    output = [?, ?, ?, ?, 7]
                              0  1  2  3  4
                    then do the same for 1 (idx 1 of input arr)

                    output = [1, ?, ?, ?, 7]
                    -->     [1, ?, ?, 5, 7]
                    -->     [1, ?, 2, 5, 7] # first 2 in input goes in idx 2 (then decrement value at idx 2 in bucket)
                    -->     [1, 2, 2, 5, 7] # second 2 in input goes in idx 1
                                            # so not stable if iterating over the unsorted array forwards
            ! iterating backwards over the sorted array will be stable
                above example iterating backwards
                    output = [?, ?, ?, ?, ?]
                    input = [7, 1, 5, 2!, 2*]
                    buckets = [0, 1, 3, 3, 3, 4, 4, 5]
                     idx       0  1  2  3  4  5  6  7

                    look at input[-1], it is 2, look at index 2 of buckets, it is 3, put 2 in index 3-1 of output
                    output = [?, ?, 2*, ?, ?]    now decrement buckets[2] by 1 so buckets = [0, 1, 2, 3, 3, 4, 4, 5]
                    -->      [?, 2!, 2*, ?, ?]   repeat, it has now it is stable
                    -->      [?, 2, 2, 5, ?]
                    -->      [1, 2, 2, 5, ?]
                    -->      [1, 2, 2, 5, 7]     done!

    Note:
            - doesnt't work for negative numbers
            - assumes each element is a small integer
            - O(max v - min v) which is O(n) if difference between min and max not too large

k is the range of the input

Time complexity: O(2n + k)
- efficient when range(k) not significantly greater than number of elements to sort

- dependent on number of buckets
    fast when data being sorted can be distributed between buckets evenly, if values sparse allocated then bigger buckets
    if values are dense, smaller buckets i.e.
        [2034, 33, 1001] --> bucket size around 1000
        [100,90,80,70,110] --> smaller bucket size ideal
Good when:
    - additional O(n+k) memory not an issue, n to copy array, k for the number of buckets(?)
    - elements expected to be fairly evenly distributed
    - as k is a constant for a set number of buckets, when small it gives O(n) performance
Bad when:
    - all elements are put into the same bucket
    - individual buckets are sorted, if everything put into 1 bucket, complexity dominated by inner
    sorting algo(?)

- first loop to count occurrences is always O(n)
- second loop to cumulative sum occurrences is always O(k+1) where k is the number such that all values lay in 0..k
- third loop to put elements in input in the right position of output is always O(n)
so overall O(2n + k + 1) = O(n+k) which is linear (best = worst = avg)

Space complexity: O(n + k)
- with just input arr it is O(1)
- we make a solution array (or output) which is the same size as input O(n)
- we also have an array for the buckets or counts which is the range of smallest to biggest which is of size k+1
so overall O(n + k) space complexity

When the max value difference is significantly smaller than number of items, counting sort is really efficient

Stability: yes when you put elements from input to output backwards
"""

def counting_sort_alphabet_2(string):  # Not stable, can work with string or array.
    counts = [0] * 26  # Assumed lower case alphabet.
    output = []
    for char in string:
        index = ord(char) - ord('a')  # 'a' is index 0.
        counts[index] += 1
    for i in range(len(counts)):  # O(26) loop, inner loop will only execute O(n) times.
        # This will not preserve stability but is ok when just dealing with single chars.
        ascii_value = ord('a') + i
        for c in range(counts[i]):
            output.append(chr(ascii_value))
    return "".join(output)

def counting_sort_alphabet(arr):  # Assuming only lower case letters, is stable.
    count = [0] * 26
    output = [0] * len(arr)

    for char in arr:  # Count.
        count[ord(char) - ord('a')] += 1

    for i in range(1, len(count)):  # Accumulate indexes.
        count[i] += count[i-1]

    for j in range(len(arr)-1, -1, -1):     # Working backwards from input arr to keep stable.
        idx = count[ord(arr[j]) - ord('a')] -1  # Get position in output array, if value is count is 1 then put in index 0 of occurance of that character.
        output[idx] = arr[j]  # Copy over to output array.
        count[ord(arr[j]) - ord('a')] -= 1  # Decrement count.
    return output

def counting_sort_ints_2(array):
    max_val = max(array)
    min_val = min(array)
    counts = [0] * (max_val - min_val + 1)
    output = [0] * len(array)
    counts_offset = min_val
    for value in array:  # Count occurrences.
        index = value - counts_offset
        counts[index] += 1

    for i in range(1, len(counts)):  # Cumulative sum so can loop backwards.
        counts[i] += counts[i - 1]

    for i in range(len(array) - 1, -1, -1):  # Loop backwards over input array.
        index = counts[array[i] - counts_offset] - 1  # Find the index to copy the value to.
        output[index] = array[i]
        counts[array[i] - counts_offset] -= 1

    return output

def counting_sort_ints(arr):
    """
    for array [7,1,5,2,2] len = 5, range of values from 0 = 0 to 7
    the algorithm is
    O(len) to count (assuming that finding max and min is O(1))
    O(range) for cumulative sum
    O(len) to copy back

    so O(2n + k) = O(n) where k is the range of items and assumed to be less than the input size.

    if the range is big (like in big_arr), the complexity is dominated by k

    However in application, k usually small.
    """
    c1, c2, c3 = 0, 0, 0  # Use to look at the counts.

    # Set up
    max_number = max(arr)
    count = [0] * (max_number+1)            # is the array of "buckets" which starts at 0 and goes to max+1
    output = [0] * len(arr)

    # Count occurrences of each number in arr and put it in 'bucket' in count.
    for number in arr:                      # the item at index number of count += 1 to found occurrence of that number
        count[number] += 1
        c1 += 1

    # Cumulative sum of occurrences.
    for i in range(1, len(count)):          # cumulative sum
        count[i] += count[i-1]
        c2 += 1

    # Put into output stably.
    for j in range(len(arr)-1, -1, -1):     # work backwards to keep stable
        output_idx = count[arr[j]] - 1      # -1 as output len = arr len
        output[output_idx] = arr[j]         # put in right place in output
        count[arr[j]] -= 1                  # decrement value in count
        c3 += 1
    print("first loop counting: " + str(c1) + "\nsecond loop summing: " + str(c2) + "\nthird loop copying: " + str(c3))
    return output

if __name__ == "__main__":
    arr = [7,1,5,2,2,2,2,2,2,2,2,2,6,1,3,5,7,5,4,1,5,6,7]
    big_arr = [100,101,101,105,104,103, 1,1,1,1,2,3,3,4,5,6,7,8,9,10,11,100,150,160,170,200,300,650]
    test_arr = [1,2,3,4,5,6]
    negs = [-3, 0, 5, -10, 100, 4, -195, 13, -5, 100, 103, 14, 4, -123, -95]
    arrays = [arr, big_arr, test_arr]

    print("Counting sort 2 can handle negative numbers")
    print(counting_sort_ints_2(negs))

    print("\n~~ Testing integer counting sort")
    for array in arrays:
        sorted_array = array[::]
        sorted_array.sort()
        print("\nInput: " + str(array))
        result1 = counting_sort_ints(array)
        result2 = counting_sort_ints_2(array)
        if result1 == result2 == sorted_array:
            print("Success: " + str(result1))
        else:
            print("Error:")
            print("Result1: " + str(result1))
            print("Result2: " + str(result2))

    print("\n~~ Test alphabet counting sort")
    s = "zsquirtlebulbasaurcharmander"
    a = "applebeesfruittomato"
    strings = [s, a]
    for s in strings:
        sorted_string = s
        sorted_string = list(sorted_string)
        sorted_string.sort()
        sorted_string = "".join(sorted_string)

        print("\nInput: " + s)
        result1 = counting_sort_alphabet(s)
        result1 = "".join(result1)
        result2 = counting_sort_alphabet_2(s)
        if result1 == result2 == sorted_string:
            print("Success: " + result2)
        else:
            print("Error:")
            print("Result1: " + result1)
            print("Result2: " + result2)




