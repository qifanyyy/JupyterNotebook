'''
Purpose:
Design an OrderedTreeSet class which can be used to insert items, delete items,
and lookup items in O(log n) time. Implement the "in" operator on this class for
set containment. Also, implement an iterator that returns the items of the set
in ascending order. The design of this set should allow items of any type to be
added to the set as long as they implement the __lt__ operator. This OrderedTreeSet
class should be written in a file called orderedtreeset.py.

Reference: Data Structures and Algorithms with Python by Kent D. Lee and Steve Hubbard
'''

import random

class Stack:
    def __init__(self):
        self._items = []

    def push(self, new_item):
        self._items.append(new_item)

    def peek(self):
        if len(self._items) > 0:
            return self._items[-1]
        else:
            raise IndexError('The stack is empty')


    def __len__(self):
        return len(self._items)

    def size(self):
        return len(self._items)

    def pop(self):
        return self._items.pop()

    def is_empty(self):
        return len(self._items) == 0

    def clear(self):
        self._items = []
        return self._items

    def __str__(self):
        return str(self._items)

class OrderedTreeSet:
    class BinarySearchTree:
        # This is a Node class that is internal to the BinarySearchTree class.
        class Node:
            def __init__(self, val, left=None, right=None):
                self.val = val
                self.left = left
                self.right = right

            def getVal(self):
                return self.val

            def setVal(self, newval):
                self.val = newval

            def getLeft(self):
                return self.left

            def getRight(self):
                return self.right

            def setLeft(self, newleft):
                self.left = newleft

            def setRight(self, newright):
                self.right = newright

            # This method deserves a little explanation. It does an inorder traversal
            # of the nodes of the tree yielding all the values. In this way, we get
            # the values in ascending order.

            # @deprecated
            # def __iter__(self):
            #     if self.left != None:
            #         for elem in self.left:
            #             yield elem
            #
            #     yield self.val
            #
            #     if self.right != None:
            #         for elem in self.right:
            #             yield elem
            #

            def __repr__(self):
                return "BinarySearchTree.Node(" + repr(self.val) + "," + repr(self.left) + "," + repr(self.right) + ")"

        def __init__(self, root=None):
            self.root = root

        def insert(self, val):
            self.root = OrderedTreeSet.BinarySearchTree.__insert(self.root, val)

        def __insert(root, val):
            if root == None:
                return OrderedTreeSet.BinarySearchTree.Node(val)

            if val < root.getVal():
                root.setLeft(OrderedTreeSet.BinarySearchTree.__insert(root.getLeft(), val))
            else:
                root.setRight(OrderedTreeSet.BinarySearchTree.__insert(root.getRight(), val))

            return root

        def remove(self, val):
            self.root = OrderedTreeSet.BinarySearchTree._remove(self.root, val)

        def _remove(currentNode, val):
            if currentNode == None:
                return None

            if val < currentNode.getVal():
                currentNode.setLeft(OrderedTreeSet.BinarySearchTree._remove(currentNode.getLeft(), val))
            elif val > currentNode.getVal():
                currentNode.setRight(OrderedTreeSet.BinarySearchTree._remove(currentNode.getRight(), val))
            else:
                # case 1: no children
                if currentNode.getLeft() == None and currentNode.getRight() == None:
                   return None
                # case 2: has left child
                elif currentNode.getRight() == None:
                    return currentNode.getLeft()
                # case 3: has right child
                elif currentNode.getLeft() == None:
                    return currentNode.getRight()
                # case 4: has both children
                else:
                    successorNodeVal = OrderedTreeSet.BinarySearchTree.getRightMost(currentNode.getLeft())
                    currentNode.setVal(successorNodeVal)
                    currentNode.setLeft(OrderedTreeSet.BinarySearchTree._remove(currentNode.getLeft(), successorNodeVal))

            return currentNode
            
        def getRightMost(currentNode):
            # base case
            if currentNode == None:
                return None
            # we found the max value
            elif currentNode.getRight() == None:
                return currentNode.getVal()
            # keep looking
            else:
                return OrderedTreeSet.BinarySearchTree.getRightMost(currentNode.getRight())

        def __iter__(self):
            s = Stack()
            currentNode = self.root
            done = False
            while not done:
                if currentNode != None:
                    s.push(currentNode)
                    currentNode = currentNode.getLeft()
                elif currentNode == None and s.is_empty() == False:
                    currentNode = s.pop()
                    yield currentNode.getVal()
                    currentNode = currentNode.getRight()
                else:
                    done = True

        def _find(node, val):
            if node == None:
                return False

            if node.getVal() == val:
                return True

            if val > node.getVal():
                return OrderedTreeSet.BinarySearchTree._find(node.getRight(), val)

            return OrderedTreeSet.BinarySearchTree._find(node.getLeft(), val)

        def _getLen(node):
            if node == None:
                return 0
            else:
                return (OrderedTreeSet.BinarySearchTree._getLen(node.getLeft()) + 1 + OrderedTreeSet.BinarySearchTree._getLen(node.getRight()))

        # @deprecated
        # def __iter__(self):
        #     if self.root != None:
        #         return iter(self.root)
        #     else:
        #         return iter([])

        def __str__(self):
            return "BinarySearchTree(" + repr(self.root) + ")"

    def __init__(self, contents=None):
        self.tree = OrderedTreeSet.BinarySearchTree()
        if contents != None:
            # randomize the list
            indices = list(range(len(contents)))
            random.shuffle(indices)

            for i in range(len(contents)):
                self.tree.insert(contents[indices[i]])

            self.numItems = len(contents)
        else:
            self.numItems = 0

    def __str__(self):
        pass

    def __iter__(self):
        return iter(self.tree)

    # Following are the mutator set methods
    def add(self, item):
        OrderedTreeSet.BinarySearchTree.insert(self.tree, item)

    def remove(self, item):
        return OrderedTreeSet.BinarySearchTree.remove(self.tree, item)

    # Following are the accessor methods for the HashSet
    def __len__(self):
        return OrderedTreeSet.BinarySearchTree._getLen(self.tree.root)

    def intersection_update(self, otherTree):
        for item in self.tree:
            if item != None and item not in otherTree:
                OrderedTreeSet.BinarySearchTree.remove(self.tree, item)

    def update(self, otherTree):
        for item in otherTree:
            if item not in self.tree:
                self.tree.insert(item)

    def clear(self):
        self.tree.root = None

    def difference_update(self, otherTree):
        for item in otherTree:
            OrderedTreeSet.BinarySearchTree.remove(self.tree, item)

    def difference(self, otherTree):
        diffSet = OrderedTreeSet()
        for item in self.tree:
            if item != None and item not in otherTree:
                diffSet.add(item)
        return diffSet

    def issubset(self, otherTree):
        subTotal = 0
        for item in self.tree:
            if item in otherTree:
                subTotal += 1
        if self.__len__() == subTotal:
            return True
        return False

    def issuperset(self, otherTree):
        subTotal = 0
        for item in self.tree:
            if item in otherTree:
                subTotal += 1
        if self.__len__() > subTotal:
            return True
        return False

    def copy(self):
        newOrderTreeSet = OrderedTreeSet()
        for item in self.tree:
            newOrderTreeSet.add(item)
        return newOrderTreeSet

    def discard(self, item):
        try:
            OrderedTreeSet.BinarySearchTree.remove(self.tree, item)
        except Exception:
            pass

    def __contains__(self, val):
        return OrderedTreeSet.BinarySearchTree._find(self.tree.root, val)

    def __eq__(self, otherTree):
        if self.__len__() != otherTree.__len__():
            return False
        numSame = 0
        for item in self.tree:
            if item in otherTree:
                numSame += 1
        if self.__len__() == numSame:
            return True
        return False


def main():
    s = input("Enter a list of numbers: ")
    lst = s.split()

    tree = OrderedTreeSet()

    for x in lst:
        tree.add(float(x))

    print(tree)


if __name__ == "__main__":
    main()