"""
@author: David Lei
@since: 22/08/2016
@modified: 

"""

class TreeNode:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.parent = None
        self.extra_data = None          # Can hold any info I forgot to add
        self.left = left
        self.right = right
        self.height = None              # Assume it's a leaf
        self.colour = None              # Can use for red/black implementation
        self.balance = None
        # Pointers for data structure mutation.
        self.next = None
        self.back = None
