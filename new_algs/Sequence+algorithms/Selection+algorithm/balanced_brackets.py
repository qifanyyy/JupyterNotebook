"""
@author: David Lei
@since: 7/11/2017

https://www.hackerrank.com/challenges/balanced-brackets/problem

Passed :)
"""

def isBalanced(s):
    opening = {
        "{": "}",
        "(": ")",
        "[": "]"
    }
    closing = {
        opening[key]: key for key in opening.keys()
    } # Not needed but yay I can do dict comprehension.
    stack = []

    for char in s:
        if char in opening:
            stack.append(char)
        else:
            if not stack:  # I forgot this, can't pop from an empty stack, need to check has stuff before popping.
                return "NO"
            first_opening = stack.pop()
            if not opening[first_opening] == char:
                return "NO"
            # Else the closing successfully closes and opening.
    if stack:
        return "NO"
    return "YES"


