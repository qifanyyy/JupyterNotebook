"""
@author: David Lei
@since: 13/08/2017

https://www.hackerrank.com/challenges/ctci-contacts/problem

Implemented using a Trie, can get the words that have a prefix in the target for find and the number as well.
Note: Current approach is slow, TLE on 10/13 test cases, but it is right afaik :)

TODO: Optimize, can get rid of most of the Trie class code, https://www.youtube.com/watch?v=vlYZb68kAY0
"""


class Trie_Node:
    def __init__(self):
        self.children = {}              # dictionary, can also be done with array of 26 for alphabet
        self.end_of_word = False        # dictionary provides a mapping of 'char': next_tree_node_object


class Trie:
    def __init__(self):
        self.root = Trie_Node()

    def find_words_from_node(self, node, words, prefix):
        for child_char, next_node in node.children.items():
            next_prefix = prefix + child_char
            self.find_words_from_node(next_node, words, next_prefix)
        if node.end_of_word:
            words.append(prefix)

    def find_partial(self, target, want_words=False):
        """
        Nodes have children which string together to form a word.

        Loop for all characters in target string, until the least most node is found, return the number of children.
        If the least most node is not found then the target is not in our trie.
        """
        prefix = ""
        node = self.root
        for character in target:
            if character in node.children:
                if want_words:
                    prefix += character
                node = node.children[character]
            else:
                return 0  # Not found.
        # Exhausted target string, need to find end of words.
        # Recursively search through the node's children.
        words = []
        self.find_words_from_node(node, words, prefix)
        if want_words:
            return words
        return len(words)




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
        return self._search_recursive_aux(start, string, 0)

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
inputs = [
    'add hack',
    'add hackerrank',
    'find hac',
    'find hak'
]

trie = Trie()

# n = int(input().strip())
# for _ in range(n):
for cmd in inputs:
    operation, details = cmd.split(' ')
    if operation == "add":
        trie.insert_iterative(details)
    else:
        partial_search_result = trie.find_partial(details, want_words=True)
        print(partial_search_result)
