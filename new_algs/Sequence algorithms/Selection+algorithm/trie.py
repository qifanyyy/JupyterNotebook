"""
@author: David Lei
@since: 28/08/2016
@modified: 

ReTRIEval tree = Trie

Tree data structure (reTRIEval tree)
- used to store collections of strings
- if 2 strings have a common prefix, will have a same ancestor in this tree
- idea for dictionaries, less space compared to hashtable

a.k.a digital tree, radix tree, prefix tree (as they can be searched by prefixes)
is a search tree (ordered tree data structure) that is used to store a dynamic set or
associative array where the keys are usually strings.

note: associative array, map, symbol table, or dictionary is an abstract data type composed
of a collection of (key, value) pairs, such that each possible key appears at most once in the collection.

based on: https://www.youtube.com/watch?v=AXjmTQ8LEoI

Time Complexity:
There can not be more than n * l nodes in the tree, where n is the number of strings and l is the length of search string
so at worst the below operations are O(n * l)
- look up (search):
- delete (remove):
- insert (add):

Space Complexity: O(n * l) where l is the avg length of the strings

A standard trie storing a collection S of s strings of total length n from an alphabet Σ has the following properties:
• The height of T is equal to the length of the longest string in S. • Every internal node of T has at most |Σ| children.
• T has s leaves
• The number of nodes of T is at most n+1
"""

class Trie_Node:
    def __init__(self):
        self.children = {}              # dictionary, can also be done with array of 26 for alphabet
        self.end_of_word = False        # dictionary provides a mapping of 'char': next_tree_node_object

class Trie:
    def __init__(self):
        self.root = Trie_Node()

    def insert_iterative(self, string):
        node = self.root

        for character in string:
            if character in node.children:          # O(1) best=avg case look up for a dictionary
                node = node.children[character]
            else:
                # finished searching prior to string ending
                # add this character to the trie
                new_node = Trie_Node()
                node.children[character] = new_node     # add the char:obj mapping to node.children
                node = new_node                         # update the node to be the new node we just created
        node.end_of_word = True

    def insert_recursive(self, string):
        self._insert_recursive_aux(self.root, string, 0)

    def _insert_recursive_aux(self, node, string, char_index):
        if char_index == len(string):                   # done looping through string
            node.end_of_word = True
        elif string[char_index] in node.children:
            self._insert_recursive_aux(node.children[string[char_index]], string, char_index + 1)
        else:
            new_node = Trie_Node()
            node.children[string[char_index]] = new_node
            self._insert_recursive_aux(node.children[string[char_index]], string, char_index + 1)

    def search_iterative(self, string):
        node = self.root

        for i in range(len(string)):
            if string[i] in node.children:
                node = node.children[string[i]]
            else:
                return False
        if node.end_of_word:
            return True
        return False

    def search_recursive(self, string):
        start = self.root
        return  self._search_recursive_aux(start, string, 0)

    def _search_recursive_aux(self, node, string, char_index):
        if char_index == len(string):       # search loop through string
            return node.end_of_word
        elif string[char_index] in node.children:
            return self._search_recursive_aux(node.children[string[char_index]], string, char_index + 1)
        else:
            return False


    def remove(self, string):
        """
        needs a recessive implementation as you might delete all the way up one side of the tree
        doing this iteratively is a lot of work and might take a lot of space
        """
        start = self.root
        self._remove_aux(start, string, 0)

    def _remove_aux(self, node, string, char_index):
        """
        note: we can remove a node from the trie if that node no children
        """
        if char_index == len(string):
            if node.end_of_word:            # the string is in the tree, can delete
                node.end_of_word = False    # no string ends here anymore
                print("string " + str(string) +" in trie, trying to delete up")
                return len(node.children) == 0   # return whether this node has any children
                                            # if not, we can delete, else we can't
            else:
                # raise KeyError("Not in trie")
                print("Can't delete, it's not in the trie")
                return False                # can't delete, return false
        elif string[char_index] in node.children:
            # just keep searching
            node_next = node.children[string[char_index]]
            can_remove_child = self._remove_aux(node_next, string, char_index + 1)
            if can_remove_child:            # nothing in my child's .children
                # can delete
                print("Can delete, prev: " + str(node.children.items()))
                node.children.pop(string[char_index])         # can remove the child referencing returning node
                print("Can delete, after: " + str(node.children.items()))
                return len(node.children) == 0                # no more children
            else:
                # can't delete
                print("Can't delete, it's has other children")
                return False
        else:                               # character is not in the children dict of current node
            # raise KeyError("Not in trie")
            print("Can't delete, it's not in the trie")
            return False

if __name__ == "__main__":
    T = Trie()
    T.insert_iterative('abcd')
    T.insert_recursive('egg')
    T.insert_recursive('abg')

    print(T.search_iterative('gp'))
    print(T.search_iterative('egg'))
    print(T.search_iterative('eg'))
    print(T.search_recursive('abc'))
    print(T.search_recursive('abcd'))

    print("\nTrie structure works fine!\n")

    print(T.remove('xg'))
    print(T.remove('eg'))
    print(T.remove('abcd'))

    print("Removed things, for the case where we could delete, the path from b --> c --> d got truncated, b --> g stil here ")
    print()

    # note: check tree strcuture via debugging because didn't have time to implement a print fn