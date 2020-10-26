"""
@author: David Lei
@since: 6/11/2017

https://www.hackerrank.com/challenges/tree-huffman-decoding/problem

Huffman coding assigns variable len codewords to fixed len input characters based on their frequencies.
- more frequent characters are assigned to shorter codewords
- less frequent characters are assigned to longer codewords

A huffman tree is made for the input string and characters are decoded based on their position in the tree.
- add a 0 to the code word if you move left
- add a 1 to the code word if you move right
- leaf nodes are assigned codes which represent the input characters

Given a tree:
        {ϕ,5}
     0 /     \ 1
    {ϕ,2}   {A,3}
   0/   \1
{B,1}  {C,1}

It means 'B' is encoded as '00' as you move down two lefts from the root to get to it.
The integer value at the nodes just represent idk.
'A' is encoded as '1'.

So '1001011' represents 'ABACA'

Given a pointer to the root of a Humman tree, use it to decode a binary coded string.
Print the decoded string.

Passes :)
"""

class Node:
    def __init__(self, freq,data):
        self.freq= freq
        self.data=data
        self.left = None
        self.right = None

def decodeHuff(root , s):
    cur = root
    decoded_string = []
    for char in s:
        if char == '1':
            cur = cur.right
        else:
            cur = cur.left
        if not cur.left and not cur.right: # At leaf.
            decoded_string.append(cur.data)
            cur = root
    print("".join(decoded_string))
