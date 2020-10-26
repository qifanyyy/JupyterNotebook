"""
@author: David Lei
@since: 2/04/2017
@modified: 

ASCII representations.

https://www.hackerrank.com/challenges/the-love-letter-mystery?h_r=internal-search
"""
import math

def order_pair(char_a, char_b):  # Returns ascii values of char_a and char_b in order of size.
    ascii_value_a = ord(char_a)
    ascii_value_b = ord(char_b)
    if ascii_value_a < ascii_value_b:
        return ascii_value_a, ascii_value_b
    elif ascii_value_b < ascii_value_a:
        return ascii_value_b, ascii_value_a
    else:
        raise ValueError("Precondition characters are different violated.")

T = int(input())


for _ in range(T):
    s = input()
    mid_point = math.ceil(len(s)/2)
    lhs = s[:mid_point]  # if len 3, will include the 1st index, middle char is always part of palindrome for odd len.
    rhs = s[mid_point:][::-1]  # reverse this
    cost = 0

    for i in range(len(rhs)):
        if rhs[i] == lhs[i]:  # characters are the same.
            pass
        # comparing characters is based off ascii values i.e. 'a' = 97
        else:
            # make larger character the same as the smaller character.
            # 'd' to 'a' = 'd' -> 'c' -> 'b' -> 'a' = 3 = ord('d') - ord('a')
            smaller_ascii_value, larger_ascii_value = order_pair(rhs[i], lhs[i])
            cost += larger_ascii_value - smaller_ascii_value  # calculate cost

    print(cost)
