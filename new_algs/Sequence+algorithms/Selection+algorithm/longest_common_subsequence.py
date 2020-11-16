"""
@author: David Lei
@since: 26/08/2016
@modified: 

Similarity between strings

a subsequence of a string is defined as a sequence of characters of that string that are not necessarily contiguous but
are taken in order.

AGGA is a substring of TAGGCTA

Approach:
    1. Naive: enumerate over all subsequences of the string X and take larges also a subsequence of string Y
        - potentially 2^n different subsequences of X each needing O(m) time to determine if it is also a subsequence of Y
        so brute for runs in O(2^n * m) time which is bad
    2. DP
        - X & Y are strings --> natural set of indices with which to define subproblems
        - subproblem: computing the value of Lj,k
            which prefixes X[0:j] and Y[0:k]
    we have 2 cases:
        1. match between the last character of X[0:j] and Y[0:k]
        eg: Caps = match
            X = GTTccTAatA
            Y = cGaTaaTTgAgA
            LCS = GTTTAA

    eg:             X
              a  b  c  d  a  f  # 2! is asking if we have the string 'abcd' and 'ac' what is LCS = 2
           0  0  0  0  0  0  0  # 1* is asking if we have a string 'abcd' and 'a' what is the LCS = 1
    Y   a| 0 .1. 1  1  1* 1  1  # 1. is asking, if we have a string 'a' and 'a' what is LCS = 1
        c| 0 .1& 1  2! 2  2  2  # 1& is asking, if we have string 'a' and 'ac' what is LSC = 1
        b| 0  1 .2  2  2  2  2
        c| 0  1  2 .3 .3 .3  3
        f| 0  1  2' 3  3  3 .4

        path denoted with prefix '.'
        f c b a --> rev = a b c f

        look at 2' b is not the same as f, so we look at the max of top and left
        - top = comparing the string 'ab' with 'acbcf', LCS = ab = 2
        - left = comparing the string 'a' with 'acbcf', LCS = a = 1
        so take max = 2

        if not same, LCS wil be either max(top or left)

Time Complexity: O(a*b) = best = worst = avg
    - string_a has len a
    - string_b has len b
    nested for loops run for each in string_b for each in string_a so O(a*b)
    a lot better than exponential, it is (almost linear), if a is near b O(2b) = O(b)

    with putting the solution togeter = O(a * b + a + b) = dominated by O(a*b)
Space Complexity: O(a*b) due to table
"""

def lowest_common_subsequence(string_a, string_b):
    len_a = len(string_a)   # rows
    len_b = len(string_b)   # columns
    table = [[0 for _ in range(len_b + 1)] for _ in range(len_a + 1)]   # create a len_b x len_a table, with initial col and row of 0s
    for i in range(len_a):                          # loop for each char in a
        for j in range(len_b):                      # compare to each char in b
            if string_a[i] == string_b[j]:          # match
                # if match, extend len common subseq by 1
                # when they are the same, we know they will contribute 1 to the LCS
                # go top left diagonal (top left corner) to get prev LCS and add 1 to that string
                table[i+1][j+1] = table[i][j]+ 1    # current is j+1, i+1 as we have init row, col of 0s, prev is j,i --> extend that
            else:
                # no match, current longest = best prev longest (didn't add anything on to it)
                # check value to the right and value above
                table[i+1][j+1] = max(table[i+1][j], table[i][j+1])

    solution = reconstruct_lcs_solution(table, string_a, string_b)
    return table, solution

def reconstruct_lcs_solution(table, string_a, string_b):
    """
    to reconstruct the solution (actual string)
        1. start at table[-1][-1] for max length
        2. if string_a[i] == string_b[j], chars match, then the current position we are at is
           associated with table[i-1][j-1] (as to make the table we extend the max sub seq by 1 when they machted)
           so update our current position and add the common character we were at to output
           string_a[i] is added to output
        3. if not match, then the number would have come from max(left, top) so move there and update our position
           nothing has been added to LCS
        continue until reaching 0 (where table[i][j] = 0 or i or j, boundary case) and we are done

    Time Complexity to make solution: O(a+b) where a is len(string_a) and b is len(string_b)
        this is because we loop until i or j = 0 and each pass decrements one of i or j or both
        so at worst bound is when only one of i or j decrements each pass which is O(i + j)

    :return: longest common subsequence
    """
    solution = []
    i = len(string_a)
    j = len(string_b)
    # remember table has i columns indexed from 0 to i
    while table[i][j] > 0:
        if string_a[i-1] == string_b[j-1]:      # remember need to index-1 for strings, only the table has + 1 row, col
            solution.append(string_a[i-1])      # add common element to solution
            i -= 1                              # decrement i and j (go to top left diagonal)
            j -= 1
        else:                                   # no match
            top = table[i-1][j]
            left = table[i][j-1]
            if top >= left:
                i -= 1                          # decrement j to update our position
            else:                               # top < left
                j -= 1                          # decrement i to update our position
    return solution[::-1]

if __name__ == "__main__":
    a = 'abcaf'
    b = 'acbcf'
    x = 'gttcctaata'
    y = 'cgataattgaga'
    t1, sol1 = lowest_common_subsequence(a, b)
    print("Strings: " + str(a) + ", " + str(b))
    for r in t1:
        print(r)
    print("Longest common subsequence: " + str(sol1) + ", len: " + str(t1[-1][-1]))
    t2, sol2 = lowest_common_subsequence(x, y)
    print("\nStrings: " + str(x) + ", " + str(y))
    for r in t2:
        print(r)
    print("Longest common subsequence: " + str(sol2) + ", len: " + str(t2[-1][-1]))
