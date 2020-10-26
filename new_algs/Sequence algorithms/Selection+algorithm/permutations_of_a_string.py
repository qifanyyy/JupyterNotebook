"""
@author: David Lei
@since: 19/10/2017

"""
import functools

def permuate(string, permutation_holder, call_num):
    """Order is important in permutations.
    For a string of length n there are n! permutations.

    Args:
        call_num: used to help understand the complexity of the algorithm for each call print out the times the nested loop executes.
        string: the string to find permutations for.
        permutation_holder: list to append to holding permutations of string.
    """
    if len(string) <= 1:  # Base case, only 1 way to permute a string of length 1.
        permutation_holder.append(string)
        return
    first_char = string[0]
    sub_permutations = []
    permuate(string[1:], sub_permutations, call_num + 1)  # Recursive step to find all permutations of a substring of string (removing the first character).
    count = 0
    for sub_permutation in sub_permutations:
        # Put first_char in sub_permutation all ways possible.
        for i in range(len(sub_permutation) + 1):  # Careful for off by 1.
            permutation = sub_permutation[0:i] + first_char + sub_permutation[i:]
            permutation_holder.append(permutation)
            count += 1
    print("call_num: %s did nested loop %s times" % (call_num, count))

if __name__ == "__main__":
    permutations = []
    string = "apples"
    permuate(string, permutations, 1)
    expected_num_permutations = functools.reduce(lambda a, b: a * b, [i for i in range(1, len(string) + 1)])  # Don't multiply by 0.
    print(expected_num_permutations)
    print("%s permutations is correct: %s" % (len(permutations), len(permutations) == expected_num_permutations))
    print(permutations)
