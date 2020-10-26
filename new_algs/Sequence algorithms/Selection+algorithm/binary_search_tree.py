"""
@author: David Lei
@since: 21/08/2016
@modified: 

A BST implementation supporting
- insert = O(h)
- remove = O(h)
- look up = O(h)
- get min = O(h)
- get max = O(h)

assuming left < key =< right

Time Complexity:
    - best case, avg case = O(log n) as in inserting, removing, looking up, finding min/max we needed to traverse the tree
    down until (except if remove root but then will need to find min of right subtree and change pointers)
    - worst case = O(n) when each item inserted is > than last, leads to a long chain

Height = O(h)
    - worst = O(n), just a big chain on one side
    - best, avg = O(log n)
    expected depth of any individual node is O(log n)

Space Complexity: O(n), where n is the number of nodes

Traversals:
    - pre-order = root, Left, Right
    - in-order = Left, root, Right
    - post-order = Left, Right, root

    level first = BFS

    traversal example:
                        F
                      /  \
                    B     G
                  / \      \
                A   D       I
                   / \     /
                  C   E   H

    pre-order (r,L,R)  = F, B, A, D, C, E, G, I, H
    in-order (L,r,R)   = A, B, C, D, E, F, G, H, I
    post-order (L,R,r) = A, C, E, D, B, H, I, G, F

Note: Better than linear time, worse than hashtables
    - we use BST to get better performance than O(n) (linked lists etc can also do O(n)
    - but in the worst case they are also O(n) --> then comes AVL trees =]
"""

from algorithms_datastructures.trees.tree_node import TreeNode
class BinarySearchTree:

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root == None

    def insert(self, key):
        """specify the value of the key for the new node
        will create node for you and call auxiliary function to recursively find where the
        new node belongs"""
        new_node = TreeNode(key)
        if self.is_empty():                                     # make root point to the head of the tree (new node)
            self.root = new_node
        else:
            self._insert_aux(self.root, new_node)
    def _insert_aux(self, current_node, new_node):
        if new_node.key < current_node.key:                      # check if new node lies to the left
            if current_node.left is not None:                    # if None, we found where to put it
                self._insert_aux(current_node.left, new_node)    # else recursively find where to put
            else:
                current_node.left = new_node
        else:                                                    # new node lies to the right
            if current_node.right is not None:
                self._insert_aux(current_node.right, new_node)
            else:
                current_node.right = new_node

    def get_min(self, start_node=None):
        if not self.is_empty():
            if start_node:
                current_node = start_node       # can specify a start node to search on a particular part of the tree
            else:
                current_node = self.root
            while current_node.left is not None:
                current_node = current_node.left
            return current_node
        else:
            raise Exception

    def get_max(self, start_node=None):
        if not self.is_empty():
            if start_node:
                current_node = start_node
            else:
                current_node = self.root
            while current_node.right is not None:
                current_node = current_node.right
            return current_node
        else:
            raise Exception

    def look_up(self, key):
        """Recursively searches if key is in the tree, returns False if not"""
        if self.is_empty():
            raise Exception
        return self._look_up_aux_rec(self.root, key)

    def _look_up_aux_rec(self, current_node, key, parent=None): # returns parent as well now, less initiative as iterative
        if key < current_node.key:
            if current_node.left is not None:
                parent = current_node
                return self._look_up_aux_rec(current_node.left, key, parent)
            else:
                return False, parent
        elif key > current_node.key:
            if current_node.right is not None:
                parent = current_node
                return self._look_up_aux_rec(current_node.right, key, parent)
            else:
                return False, parent
        else:                                               # current_node.key = key
            return current_node, parent

    def _look_up_aux_itr(self, key):
        """Alternative look up that returns the parent of the
        node (if the node is in the tree) as well"""
        if self.is_empty():
            raise Exception
        current_node = self.root                            # start at root with parent = None
        parent = None
        while current_node is not None:
            if key < current_node.key:                      # search left
                if current_node.left is not None:           # iff left is not None
                    parent = current_node                   # update parent node to current node
                    current_node = current_node.left        # update current node to the left link
                else:
                    raise Exception ('Key not in tree, key: ' + str(key))
                    #return False, parent                    # left is None, item not found, return False, parent
            elif key > current_node.key:                    # search right
                if current_node.right is not None:          # iff right is not None
                    parent = current_node                   # update parent to current node
                    current_node = current_node.right       # update current node to right link
                else:
                    raise Exception ('Key not in tree, key: ' + str(key))
                    #return False, parent                    # right is None, item not found, return False, parent
            else:   # current_node.key == key
                return current_node, parent                 # found, return current node, parent

    def remove(self, key):
        """Remove a node with value key from the tree
        cases:
            1. node is a leaf, just get rid of it (easy)
            2. node has 1 child, make child go directly to parent of node, will maintain BST ordering (easy)
            3. node has 2 children, harder. Using the BST property, take the left child (grandchild) of the right child
        """
        remove_node, parent = self._look_up_aux_rec(self.root, key)
        if remove_node:                                                         # check for key in tree
            self._remove_aux(remove_node, parent)
        else:                                                                   # node to remove not in BST
            raise Exception ('node to remove (' + str(key) + ') not in BST')

    def _remove_aux(self, remove_node, parent):
        """
        removes remove_node
        :param remove_node: node to remove
        :param parent: parent of node to remove
        :return:
        """
        # if parent = None, we are trying to remove the root, can be done better but I forgot about boundary cases and
        # did this quick fix l0ls
        if parent == None:
            if self.root.left is None and self.root.right is None:
                self.root = None                                                   # set to None, we are done
            elif self.root.left is not None and self.root.right is None:           # 1 child, the left one
                self.root = self.root.left                                         # make it point to the left child
            elif self.root.left is None and self.root.right is not None:           # 1 child, the right one
                self.root = self.root.right                                        # make it point to the right child
            else:                                                                  # 2 children
                smallest_node_right_subtree = self.get_min(remove_node.right)
                remove_node.key = smallest_node_right_subtree.key   # copy the value over, then remove the smallest val
                parent = remove_node
                current = remove_node.right
                while current.left is not None:                     # find parent of smallest_node_right_subtree
                    parent = current
                    current = current.left
                self._remove_aux(current, parent)
        # else we are not looking to remove the root
        else:
            # case 1: leaf
            if remove_node.left is None and remove_node.right is None:             # case 1: leaf
                if parent.left == remove_node:                                     # to remove just reset parent link
                    parent.left = None
                elif parent.right == remove_node:
                    parent.right = None
                else:
                    raise Exception ('custom msg here')
            # case 2: 1 child                                                     # case 2: 1 child
            # skip over the node to be removed by assigning the parent pointer to the left/right pointer of removed node
            elif remove_node.left is not None and remove_node.right is None:      # only has a left child
                # need to see if we add it to parent.left or .right
                if parent.key > remove_node.key:            # parent > so add to .left
                    parent.left = remove_node.left          # parent.left -> (skipped removed) --> removed.left
                else:                                       # parent <= so add to .right
                    parent.right = remove_node.left         # parent.right -> (skipped removed) --> removed.right
            elif remove_node.left is None and remove_node.right is not None:     # only has a right child
                # need to see if we add it to parent.left or .right
                if parent.key > remove_node.key:        # parent > so add to .left
                    parent.left = remove_node.right
                else:                                   # parent <= so add to .right
                    parent.right = remove_node.right
            # case 3: 2 children
            elif remove_node.left is not None and remove_node.right is not None:  # case 3: 2 children
                # find the smallest element in the right subtree and swap that value with node to remove value
                # 2 children guarantees there is something in the right subtree so there will be a minimum
                # this min will either be the immediate right value or left most value in right subtree
                # to find the smallest element we can call get min on the node to remove to search that subtree
                smallest_node_right_subtree = self.get_min(remove_node.right)
                # swapping this node with remove_node will uphold BST property
                remove_node.key = smallest_node_right_subtree.key   # copy the value over, then remove the smallest val
                # get rid of the smallest_node_right_subtree from our tree
                # this will either be case 1 (leaf) or case 2 (one child)

                # remove small_node_right_subtree
                #
                parent = remove_node
                current = remove_node.right

                #"""Using a while loop like this can fk up, better to use recursive call to _remove_aux
                while current.left is not None:                     # find parent of smallest_node_right_subtree
                    parent = current
                    current = current.left
                #parent.left = None                                  # set parent.left to None removing this node
                self._remove_aux(current, parent)

            else:
                raise Exception ('custom msg here')

    """
    Traversal is O(n) as you need to visit the n nodes
    """
    def in_order(self):
        """
        in-order = left, root, right
        """
        a =[]
        self._in_order(self.root, a)
        #print()
        return a

    def _in_order(self, current_node, a):
        if current_node is not None:
            self._in_order(current_node.left, a)
            a.append(current_node.key)
            #print(current_node.key, end="b")
            self._in_order(current_node.right, a)

    def post_order(self):
        """
        post-order = left, right, root
        """
        a = []
        self._post_order(self.root, a)
        #print()
        return a

    def _post_order(self, current_node, a):
        if current_node is not None:
            self._post_order(current_node.left, a)
            self._post_order(current_node.right, a)
            a.append(current_node.key)
            #print(current_node.key, end="a")

    def pre_order(self):
        """
        pre-order = root, left, right
        """
        a = []
        self._pre_order(self.root, a)
        #print()
        return a

    def _pre_order(self, current_node, a):
        if current_node is not None:
            a.append(current_node.key)
            #print(current_node.key, end = "c")
            self._pre_order(current_node.left, a)
            self._pre_order(current_node.right, a)

def big_test():
    BST1 = BinarySearchTree()
    print('\nTest vs https://www.cs.usfca.edu/~galles/visualization/BST.html, cant do - ')
    a = [6, 2, 9, 1, 4, 8, 5]
    for n in a:
        BST1.insert(n)
    in_order = BST1.in_order()
    print("In order: ", end= "")
    print_ordering(in_order)
    print("Removed 4")
    BST1.remove(4)
    in_order = BST1.in_order()
    print("In order: ", end= "")
    print_ordering(in_order)

    BST2 = BinarySearchTree()
    print('\nTest traversals: https://en.wikipedia.org/wiki/Tree_traversal')
    a = ['F', 'B', 'G', 'A', 'D', 'I', 'C', 'E','H']
    for n in a:
        BST2.insert(n)
    pre_order = BST2.pre_order()
    in_order = BST2.in_order()
    post_order = BST2.post_order()
    print("Pre order: ", end= "")
    print_ordering(pre_order)
    print("In order: ", end= "")
    print_ordering(in_order)
    print("Post order: ", end= "")
    print_ordering(post_order)

    print("\nRemoved A")
    BST2.remove('A')
    in_order2 = BST2.in_order()
    print("Removed F")
    print("In order: ", end= "")
    print_ordering(in_order2)
    BST2.remove('F')
    in_order3 = BST2.in_order()
    print("In order: ", end= "")
    print_ordering(in_order3)
    print("Pre order: ", end= "")
    pre_order3 = BST2.pre_order()
    print_ordering(pre_order3)
    print("root: " + str(BST2.root.key))

    print('\nTest vs http://quiz.geeksforgeeks.org/binary-search-tree-set-2-delete/')
    BST3 = BinarySearchTree()
    a = [50, 40, 70, 60, 80]
    for n in a:
        BST3.insert(n)
    print("In order: ", end= "")
    print(BST3.in_order())
    print("Removed 50")
    BST3.remove(50)
    print("In order: ", end= "")
    print(BST3.in_order())

    print("root: " + str(BST3.root.key))


def print_ordering(a):
    for key in a:
        print(key, end=" ")
    print()

if __name__ == "__main__":
    BST = BinarySearchTree()
    print('Test binary search tree')
    a = [10, 5] #, 20, 4, 3, 6, 7, 0, 1, 11, 15, 25, 30, 40, 26, 7, 17, 22, 26, 10, -5, -2]
    for n in a:
        BST.insert(n)
    print(BST.in_order())
    print(BST.pre_order())
    print("root: " + str(BST.root.key))
    BST.remove(10)
    print(BST.in_order())           # works!
    BST.remove(5)
    print(BST.in_order())
    # test boundary
    #BST_tests = BinarySearchTree()
    #BST_tests.insert(1)
    #BST_tests.remove(1)

    big_test()
    """
    To maintain the BST property, when a node with 2 children is deleted we need to find a
    value that fits between node.left and node.right or
    a value such that node.left < value <= node.right

    Due to the BST property, the left path in the right subtree will give us the minmum value in that subtree
    this min value will be (denoted v)
    node.left < v <= node.right thus satisfying the requirement

    The same goes for the right most path in the left subtree

    So we should be able to do both ways.

    I chose the smallest element in the right subtree.
    https://en.wikipedia.org/wiki/Tree_traversal chooses the max in the left subtree
    """