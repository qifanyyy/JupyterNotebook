"""
@author: David Lei
@since: 21/08/2016
@modified: 

Non comparison sorting algorithm

How it works:
    Least significant digit radix sort:
        - shorter keys before longer
        - keys of same len sorted lexicographically
        eg: sorted result = 1, 2, 3, 9, 10, 11 (so normal order of integer representations)

    Most significant digit radix sort:
        - uses lexicographical order suitable for strings
        eg: sorted result = "b, ba, c, d, e, f, g, ga, gaa, i"
        if used on integers with variable length, 1 - 10 will be
            sorted result = 1, 10, 2, 3, 4,.., 8, 9
            will need to left justify values and pad them to make same length as longest

Time Complexity: O(d(n + k)) where O(n + k) is time for inner stable sort --> O(n)

    - given n d digit numbers in which each digit can take up to k possible values (alphabet restriction)
        takes O(d(n+k)) if the stable sort takes O(n+k) time

            - k is the range from 0..k-1 that each digit can take (alphabet restriction)
                in counting sort k is the range, but as we look at 1 digit at a time, that 1 digit has to be in a
                specific range i.e. 0-9 for integers a-z for alphabet so k is that range
            - d is the number of digits in the number (100 will have d = 3)

            when d is a constant (i.e. sorting only 8 digit numbers) and k = O(n) or less (i.e. is the alphabet of
            integers 1-9) we can make radix sort run in linear time

            when digit d is in the range 0..k-1 and k is not too large, counting sort is a good choice
            each pass over n number of d digits takes O(n+k) time
            there will be d passes (to sort from least sig digit to most sig digit)
            so O(d(n+k)) or O(d(inner_stable_sort_time))

            so  O(n * d + n * k) for n keys of size d digits (number of characters i.e. 11 = 2 digits) with k
            the range of the alphabet for each digit, in application i.e. sorting 10 digit IDs
                - k will be a constant, 0-9
                - d will be a constant, 10
                so we can achieve O(n) time

            can also think about it as
            The running time is O (p(N + b))
            where p is the number of passes, N is the number of elements to sort, and b is the number of buckets.
            - passes depend on digits in that number (d)
            - 1 bucket for each element in the alphabet (or range) of each digit (k)

            note: http://www.geeksforgeeks.org/radix-sort/
             Radix Sort takes O(d*(n+b)) time where b is the base for representing numbers
             for example, for decimal system, b is 10
             - so if base = 10 and d is set as well we can make them out to be constants

Space Complexity: O(n + k)
    - count array of size k (10), k is the number of subdivisions or alphabet or range which for decimals is [0-9]
    - output and copy array of size n
    O(2n + k)

Stability: yes as iterating backwards when you put back into output array (like in counting sort)

Notes:

lexicographical order = dictionary order

consider the numbers: 15, 20, 33, 12, 21, 11, 31, 13
to sort these
    a) most sig value first:        15, 12, 11, 13, 20, 21, 33, 31
        then least sig:             20, 11, 21, 32, 12, 33, 13, 15
    b) least sig value first:       20, 11, 21, 31, 12, 13, 33, 15
        then most sig:              11, 12, 13, 15, 20, 21, 31, 33  # lexicographically sorted

so sort LBD then move towards MSD (Least sig dig first leads to stable correct sort)

This helps: https://www.cs.usfca.edu/~galles/visualization/RadixSort.html (implementation based off)

Binary radix sort is good:
    -  use 2 buckets [0,1]
    -  convert things to binary --> do things with them
"""

def radix_sort_decimal_integers(arr):
    """Radix sort implementation for integers
        d = len(str(max_value))
        k = 10 as decimals (base 10)"""

    max_value = max(arr)                                        # use to know number of digits
    digits = len(str(max_value))                                # found d

    arr_copy = [p for p in arr]                                 # copy arr so we can update this at each pass
    counting_sort_num = 0
    for i in range(1, digits+1):                                # loop for the number of digits in max_value, start at first digit (largest)
                                                                # using str(num)[-1] for last digit
        counting_sort_num += 1
        # run a counting sort to sort least sig digit to most sig digit (value of i)
        # need for each pass of counting sort

        counts = [0 for _ in range(10)]
        output = [0 for _ in range(len(arr_copy))]               # array of same size as input

        for j in range(len(arr_copy)):

            current_number = arr_copy[j]                         # find current digit we are looking at
            if len(str(current_number)) >= i:                    # get digit in number we care about
                digit_to_consider = int(str(current_number)[-i]) # this is an integer in range 0-9
            else:
                digit_to_consider = 0
            index = digit_to_consider                            # use this as index to count

            counts[index] += 1

        for l in range(1, len(counts)):                          # get cumulative sum of counts
            counts[l] += counts[l-1]

        for x in range(len(arr_copy)-1, -1, -1):                 # move items into output array stably (iterate backwards) based on counts
            current_number = arr_copy[x]
            if len(str(current_number)) >= i:                    # get digit we care about, use this to look up counts
                                                                 # array
                digit_to_consider = int(str(current_number)[-i])
            else:
                digit_to_consider = 0
            output_idx = counts[digit_to_consider] -1

            output[output_idx] = arr_copy[x]
            counts[digit_to_consider] -= 1

        arr_copy = output
        # completed once pass of O(n + k) counting sort, k is range or in this case size of alphabet (possible values)
        # which is [0-9] so 10
    return arr_copy

# ---- Another implementation for practice -----


def get_character(string, position):
    """Returns the character in the string at the position if it exists, else a.
    If the position is out of bounds of the string then we return a placing it in the first bucket.

    This works as the order we encounter strings in the array is sorted if the position is > len(string) -1 meaning we have sorted
    all characters in that string, so we can place it in the 0th bucket in the order it is encountered."""
    if len(string) - 1 < position:
        return 'a'
    return string[position]


def radix_sort_alphabet_strings(array, verbose):  # Should be stable.
    max_chars = len(max(array, key=len)) # Get make string by key length of string.
    buckets = [[] for _ in range(26)]  # Make buckets, 26 possible characters.

    for position in range(max_chars - 1, -1, -1):  # Loop from max_chars - 1 to 0 (most significant to least to get lexicographical order).
        for string in array:
            # If the position we are looking at is outside of the bounds of the string then will return 'a' or the 0th bucket.
            significant_char = get_character(string, position)
            buckets[ord(significant_char) - ord('a')].append(string)

        # Copy strings back into array in order of buckets.
        index = 0
        for bucket in buckets:
            for string in bucket:
                array[index] = string
                index += 1

        if verbose:
            print("array:        " + str(array))
            print("buckets:      " + str(buckets))
        # Clear buckets.
        buckets = [[] for _ in range(26)]

    # Since we have looped for max_chars, each string will be in sorted order now from the last copying of buckets to array.
    return array

def get_digit(number, position, base=10):
    """Return the digit we are looking at based on the position and the base.
    For example:
        number = 1234, position = 3, looking at the 1.
        position_digit = 10 ** 3 = 1000.
        divide 1234 by 1000 floored = 1.
        modulo the result by 10 as we are doing it base 10 = 1.
    If number = 1234, position = 2, looking at the 2.
        position_digit = 10 ** 2 = 100.
        divide 1234 by 1000 floored = 12
        modulo the result by 12 = 2.
    If the number is 1234, position = 0, looking at the 4.
        position_digit = 10 ** 0 = 1
        divide 1234 by 1 floored = 1234
        modulo the result by 10 = 4.
    Handles the base in which len(number) < position, will result in 0.
    """
    position_digit = base ** position  # The 1 in the resulting digit is the position of the digt we are looking at.
    floored = number // position_digit
    return floored % base

def radix_sort_decimal_integers_2(array):
    max_digits = len(str(max(array)))
    buckets = [[] for _ in range(10)]  # Make buckets, 10 possible digits.

    for position in range(max_digits):

        for number in array:  # Put numbers in buckets based on sig digit.
            significant_digit = get_digit(number, position)
            buckets[significant_digit].append(number)

        # Put items in bucket (sorted to an extend) back into array.
        # Should be stable as when we first encounter it will append, then will copy back in same order.
        index = 0
        for bucket in buckets:
            for number in bucket:
                array[index] = number
                index += 1

        # Clear buckets.
        buckets = [[] for _ in range(10)]

    # Since we have looped for max_digits, each integer will be in sorted order now from the last copying of buckets to array.
    return array


if __name__ == "__main__":
    from utils.random_array_generator import random_lowercase_strings_generator
    from utils.random_array_generator import random_integer_array_generator

    print("\n~~ Testing radix sort with integers\n")
    integer_arrays = random_integer_array_generator(lower_bound_inclusive=0, upper_bound_inclusive=1000,
                                                    integers_per_array=10000, number_of_arrays=100)
    correct = 0
    for num_array in integer_arrays:
        sorted_array = num_array[::]
        sorted_array.sort()
        result1 = radix_sort_decimal_integers(num_array)
        result2 = radix_sort_decimal_integers_2(num_array)

        if sorted_array == result1 == result2:
            if correct % 10 == 0:  # Print every 10th as generating stuff takes time.
                print("Results match: " + str(result2))
            correct += 1
        else:
            print("Oh No! Results don\'t match")
            print("radix sort decimal integers:   " + str(result1))
            print("radix sort decimal integers 2: " + str(result2))
    print("Radix sort with integers correct: {0}/{1}".format(correct, 100))

    print("\n~~ Testing radix sort with strings\n")
    string_arrays = []
    for _ in range(100):
        string_array_gen = random_lowercase_strings_generator(number_of_strings=50, max_length=100)
        string_arrays.append(list(string_array_gen))

    correct = 0
    for strings in string_arrays:
        sorted_strings = strings[::]
        sorted_strings.sort()
        result1 = radix_sort_alphabet_strings(strings, verbose=False)
        if sorted_strings == result1:
            if correct % 10 == 0:  # Print every 10th as generating stuff takes time.
                print("Results match: " + str(result1))
            correct += 1
        else:
            print("Oh No! Results don\'t match")
            print("radix sort alphabet:   " + str(result1))
            print("should be:             " + str(sorted_strings))
    print("Radix sort with strings correct: {0}/{1}".format(correct, len(string_arrays)))