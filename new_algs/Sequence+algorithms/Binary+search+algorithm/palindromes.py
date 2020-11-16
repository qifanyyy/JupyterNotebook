#!python
"""STARTER CODE FROM NEPTUNIUS"""
import string
import re
# Hint: Use these string constants to ignore capitalization and/or punctuation
# string.ascii_lowercase is 'abcdefghijklmnopqrstuvwxyz'
# string.ascii_uppercase is 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# string.ascii_letters is ascii_lowercase + ascii_uppercase


def is_palindrome(text):
    """A string of characters is a palindrome if it reads the same forwards and
    backwards, ignoring punctuation, whitespace, and letter casing."""
    # implement is_palindrome_iterative and is_palindrome_recursive below, then
    # change this to call your implementation to verify it passes all tests
    assert isinstance(text, str), 'input is not a string: {}'.format(text)
    return is_palindrome_recursive(text)
    # return is_palindrome_recursive(text)


def is_palindrome_iterative(text):
    #implements the is_palindrome function iteratively here
    regex = re.compile('[^a-zA-Z]')
    text = regex.sub('', text)
    text = text.upper()
    thing_1 = 0
    thing_2 = len(text)-1
    while thing_1 < thing_2:
        if text[thing_1] != text[thing_2]:
            return False
        thing_1+=1
        thing_2-=1
    return True
    # once implemented, change is_palindrome to call is_palindrome_iterative
    # to verify that your iterative implementation passes all tests


def is_palindrome_recursive(text, left=None, right=None):
    #implements the is_palindrome function recursively here
    if left is None:
        regex = re.compile('[^a-zA-Z]')
        text = regex.sub('', text)
        text = text.upper()
        left = 0
        right = len(text)-1
    if text == '':
        return True
    if text[left] != text[right]:
        return False
    if left < right:
        return is_palindrome_recursive(text, left=left+1, right=right-1)
    else:
        return True
    # once implemented, change is_palindrome to call is_palindrome_recursive
    # to verify that your iterative implementation passes all tests


def main():
    import sys
    args = sys.argv[1:]  # Ignore script file name
    if len(args) > 0:
        for arg in args:
            is_pal = is_palindrome(arg)
            result = 'PASS' if is_pal else 'FAIL'
            is_str = 'is' if is_pal else 'is not'
            print('{}: {} {} a palindrome'.format(result, repr(arg), is_str))
    else:
        print('Usage: {} string1 string2 ... stringN'.format(sys.argv[0]))
        print('  checks if each argument given is a palindrome')


if __name__ == '__main__':
    #print(is_palindrome_iterative("talcat"))
    print(is_palindrome_recursive("TAC!!!Oc      at", left=None, right=None))
    print(is_palindrome_iterative("no, on!"))
