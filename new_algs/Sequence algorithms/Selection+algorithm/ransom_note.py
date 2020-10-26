"""
@author: David Lei
@since: 13/08/2017

Note: is case sensitive.

The words in his note are case-sensitive and he must use whole words available in the magazine,
meaning he cannot use substrings or concatenation to create the words he needs.
"""
from collections import defaultdict


def ransom_note_characters(magazine, ransom): # O(5m + 5n) = O(m + n)
    """Solution to the same problem where you can use substrings/concatenate chars any way needed."""
    alphabet = [0 for _ in range(26 * 2)]  # Only the 26 chars of the alphabet are relevant.
    for word in magazine:  # O(m), read all words in mag
        for char in word:  # O(5).
            ascii_value = ord(char)
            alphabet[ascii_value - 97] += 1

    for word in ransom:  # O(n).
        for char in word:  # O(5)
            ascii_value = ord(char)
            if alphabet[ascii_value - 97] <= 0:
                # No more count for this char in mag.
                return False
            alphabet[ascii_value - 97] -= 1
    return True  # Looked at all chars in all words of ransom.


def ransom_note(magazine, ransom):  # O(m + n)
    """Solution where only whole words can be used."""
    words = defaultdict(int)
    # Note: to start with a default value of not 0 (int is callable, makes default value 0) use lambda.
    # defaultdict(lambda: start_val)

    for word in magazine:  # O(m), read all words in mag.
        words[word] += 1

    for word in ransom:  # O(n), read all words in ransom.
        if words[word] == 0:
            return False
        words[word] -= 1

    return True  # Looked at all chars in all words of ransom.

m, n = map(int, input().strip().split(' '))
magazine = input().strip().split(' ')
ransom = input().strip().split(' ')
answer = ransom_note(magazine, ransom)
if(answer):
    print("Yes")
else:
    print("No")

