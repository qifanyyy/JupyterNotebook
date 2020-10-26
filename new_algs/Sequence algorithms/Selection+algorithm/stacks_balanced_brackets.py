"""
@author: David Lei
@since: 13/08/2017

"""

closing_brackets = {
    "}": "{",
    ")": "(",
    "]": "[",
}


def is_matched(expression):
    stack = []
    for char in expression:
        if char in closing_brackets:
            if stack:
                opening_bracket = stack.pop()
                if closing_brackets[char] == opening_bracket:
                    pass
                else:
                    return False
            else:
                return False
        else:
            stack.append(char)
    if len(stack) != 0:
        # Edge case, stuff still left on the stack, there is an opening with no closing.
        return False
    return True

expressions = [
    "{[()]}",
    "{[(])}",
    "{{[[(())]]}}"
]

for expression in expressions:
    if is_matched(expression):
        print("YES")
    else:
        print("NO")
