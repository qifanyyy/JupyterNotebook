'''
  File: btree.py
  Author: Kent D. Lee and Steve Hubbard
  Date: 06/30/2014
  Description: This module provides the BTree class, based on support from
    the BTreeNode class.  The BTreeNode class is also implemented in this
    module. This module is meant to support the recursive implementation of
    insert, lookup, and delete within a BTree.

    The module requires the Queue class in the queue module.

    This program has two main functions, the btreemain function and the main
    function. The btreemain function tests the BTree datatype. The expected
    output is provided in a comment after the function. Once the btreemain
    function runs and produces the proper output, the main function can be
    run to test the BTree with the join functionality.

    The main function either builds a new BTree or reads an existing BTree
    from the index files, Feed.idx and FeedAttribType.idx files. If the idx
    file does not exist, then a new BTree is built and written to the
    corresponding idx file.
'''
import datetime
import os
from copy import deepcopy
import statistics
import sys
import queue

class BTreeNode:
    '''
      This class will be used by the BTree class.  Much of the functionality of
      BTrees is provided by this class.
    '''
    def __init__(self, degree=1, numberOfKeys=0, items=None, child=None, \
        index = None):
        ''' Create an empty node with the indicated degree'''
        self.numberOfKeys = numberOfKeys
        if items != None:
            self.items = items
        else:
            self.items = [None]*2*degree
        if child != None:
            self.child = child
        else:
            self.child = [None]*(2*degree+1)
        self.index = index
        self.degree = degree

    def __repr__(self):
        ''' This provides a way of writing a BTreeNode that can be
            evaluated to reconstruct the node.
        '''
        return "BTreeNode("+str(len(self.items)//2)+","+str(self.numberOfKeys)+ \
            ","+repr(self.items)+","+repr(self.child)+","+str(self.index)+")\n"

    def __str__(self):
        st = 'The contents of the node with index '+ \
             str(self.index) + ':\n'
        for i in range(0, self.numberOfKeys):
            st += '   Index   ' + str(i) + '  >  child: '
            st += str(self.child[i])
            st += '   item: '
            st += str(self.items[i]) + '\n'
        st += '                 child: '
        st += str(self.child[self.numberOfKeys]) + '\n'
        return st

    def isLeafNode(self):
        if self.child[0] is None:
            return True
        return False

    def insert(self, bTree, item):
        '''
        Insert an item in the node. Return three values as a tuple,
        (left,item,right). If the item fits in the current node, then
        return self as left and None for item and right. Otherwise, return
        two new nodes and the item that will separate the two nodes in the parent.
        '''
        # 1. If this is a leaf node and there is room for it, store the item in the node
        # 2. Otherwise, if this is a leaf node, make a new node. Sort the new item and old
        # items. Choose the middle item to promote to the parent. Take the items after the
        # middle and put them into the new node. RETURN: tuple of the middle item  and new right node
        # 3. If this is a non-leaf node, call insert recursively on the appropriate subtree. Consult
        # the return value of the recursive call to see if there is a newly promoted key and right subtree.
        # If so, take the appropriate action to store the new item and subtree pointer in the node. If there
        # is no room to store the promoted value, split it again as described in step 2.

        # We found a leaf node
        if self.isLeafNode():
            # 1. This is a leaf node with room for insertion
            if not self.isFull():
                self.items[self.numberOfKeys] = item
                self.items = sorted(self.items, key=lambda x: (x is None, x)) # put all the Nones at the end of the list upon sorting
                self.numberOfKeys += 1
                return self, None, None
            # 2. No room for insertion, splitting required
            else:
                return BTreeNode.splitNode(self, bTree, item, None)

        # 3. This is NOT a leaf node. Call insert recursively on the appropriate subtree
        else:
            # a) Find the appropriate subtree
            done = False
            index = 0
            while not done and self.items[index] < item:
                if self.items[index] is None or index == self.numberOfKeys-1:
                    done = True
                index += 1
            leftNodeIdx, promotedItem, rightNodeIdx = BTreeNode.insert(bTree.nodes[self.getChild(index)], bTree, item)

            # b) If an item was promoted (i.e., promotedItem does not equal None) then repeat the above algorithm
            if promotedItem:
                # 1. There is room for insertion
                if not self.isFull():
                    self.items[self.numberOfKeys] = promotedItem
                    self.items = sorted(self.items, key=lambda x: (x is None, x))
                    promotedItemIdx = self.items.index(promotedItem)
                    self.child.insert(promotedItemIdx+1, rightNodeIdx)
                    self.child.pop()
                    self.numberOfKeys += 1
                    return self, None, None
                else:
                    return BTreeNode.splitNode(self, bTree, promotedItem, rightNodeIdx)
            return self, None, None


    def splitNode(self, bTree, item, right): #right is pointer
        '''
        This method is given the item to insert into this node and the node
        that is to be to the right of the new item once this node is split.

        Return the indices of the two nodes and a key with the item added to
        one of the new nodes. The item is inserted into one of these two
        nodes and not inserted into its children.
        '''

        # Copy items, append new item to copy list
        copyItems = sorted(self.items + [item])

        # Find item to be promoted
        promotedItem = copyItems[len(copyItems) // 2]

        # Figure out where children belong
        children = []
            # find index of item
        newItemIdx = copyItems.index(item)
        children.append(self.child[0])
        j = 1
        for i in range(bTree.degree*2 + 1):
            if i == newItemIdx:
                children.append(right)
            else:
                children.append(self.child[j])
                j += 1

        # Create right node
        rightNode = bTree.getFreeNode()

        # Find left and right node's children
        promotedItemIdx = len(copyItems) // 2
        leftNodeChildren = children[0:promotedItemIdx+1]
        rightNodeChildren = children[promotedItemIdx+1:]

        # If this is NOT a leaf node, we have to assign left and right children to their respective parents
        if not self.isLeafNode():
            # left
            for i in range(len(leftNodeChildren)):
                self.child[i] = leftNodeChildren[i]
            # right
            for i in range(len(rightNodeChildren)):
                rightNode.child[i] = rightNodeChildren[i]

        # Find appropriate items to place in each node
        leftNodeItems = copyItems[0:copyItems.index(promotedItem)]
        rightNodeItems = copyItems[copyItems.index(promotedItem) + 1:]

        # Add rightNodeItems to the actual right node, update number of keys
        for i in range(len(rightNodeItems)):
            rightNode.items[i] = rightNodeItems[i]
        rightNode.numberOfKeys = bTree.degree

        # Reset the current node's items and number of keys, replace old items with None
        self.numberOfKeys = bTree.degree
        for i in range(len(self.items)):
            if i < self.numberOfKeys:
                self.items[i] = leftNodeItems[i]
            else:
                self.items[i] = None

        # Replace extra children with None
        self.replaceWithNone()

        # Promoted item is the key (will be passed up to parent)
        return self.index, promotedItem, rightNode.index

    def replaceWithNone(self):
        for i in range(self.numberOfKeys+1, len(self.child)):
            self.child[i] = None

    def getLeftMost(self,bTree):
        ''' Return the left-most item in the
            subtree rooted at self.
        '''
        if self.child[0] == None:
            return self.items[0]

        return bTree.nodes[self.child[0]].getLeftMost(bTree)

    def delete(self,bTree,item):
        '''
           The delete method returns None if the item is not found
           and a deep copy of the item in the tree if it is found.
           As a side-effect, the tree is updated to delete the item.
        '''
        '''
        Rules:
        1. If the node containing the item is a leaf node and the node has more than degree
        items in it then the item may simply be deleted.
        2. If the node containing the item is a leaf node and has *degree* or fewer items in it
        before deleting the value, then rebalancing is required.
        3. If the node is a non-leaf node then the least value of the right subtree can replace
        the item in the node.
        '''
        '''
        1: k is a leaf node; num keys > degree
        2a: k is a leaf node; num keys <= degree; nearest sibling num keys > degree --> borrow
        2b: k is a leaf node; num keys <= degree; nearest sibling num keys <= degree --> borrow, merge
        3: k is not a leaf node; find leftmost of rightmost subtree
        '''

        # Return None if item to be deleted is not in the tree
        searchResult = BTreeNode.search(bTree.rootNode, bTree, item)
        if searchResult['found'] is False:
            return None

        # The node index containing the item we want to delete
        itemNodeIdx = searchResult['fileIndex']

        # Index of item we want to delete in items list
        itemItemsIdx = searchResult['nodeIndex']

        # Get the node of where we want to delete an item from
        itemNode = bTree.nodes[itemNodeIdx]

        # Item to delete is a child of self--the current node
        if itemNodeIdx in self.child:
            # Item to delete is in a leaf node
            if itemNode.isLeafNode():
                # itemNode's numberOfKeys is > degree, we can simply delete the item
                if itemNode.numberOfKeys > itemNode.degree:
                    itemNode.items.remove(item)
                    itemNode.numberOfKeys = itemNode.numberOfKeys - 1
                    return deepcopy(item)

                # itemNode's numberOfKeys is <= degree, we must redistribute
                itemNodeChildIdx = self.child.index(itemNodeIdx)
                BTreeNode.redistributeOrCoalesce(self, bTree, itemNodeChildIdx)

                # The node containing the item we want to delete may have been removed during the coalescing.
                    # We must find the node it coalesced into and remove it from there
                if itemNodeIdx in bTree.nodes:
                    itemNode.items.remove(item)
                else:
                    itemNodeIdx = self.child[itemNodeChildIdx-1]
                    itemNode = bTree.nodes[itemNodeIdx]
                    itemNode.items.remove(item)

                #todo: unsure how to merge parent node with its sibling if it has less then degree items after its child had to coalesce

            # Item to delete is in a non-leaf node. We must find the least value of the right subtree to replace the item in the node
            else:
                successor = BTreeNode.getLeftMost(itemNode, bTree)
                BTreeNode.delete(bTree.rootNode, bTree, successor)
                itemNode.items[itemItemsIdx] = successor

        # Item we want to delete is in the root
        elif itemNodeIdx == bTree.rootNode.index:
            if self.numberOfKeys > 1:
                self.items.remove(item)
                self.numberOfKeys = self.numberOfKeys-1
                return deepcopy(item)
            else:
                successor = BTreeNode.getLeftMost(self, bTree)
                BTreeNode.delete(bTree.rootNode, bTree, successor)
                itemNode.items[itemItemsIdx] = successor

        # Find appropriate subtree
        else:
            done = False
            index = 0
            while not done and self.items[index] < item:
                if self.items[index] is None or index == self.numberOfKeys - 1:
                    done = True
                index += 1
            return BTreeNode.delete(bTree.nodes[self.child[index]], bTree, item)

    def redistributeOrCoalesce(self,bTree,childIndex): # self is parent
        '''
          This method is given a node and a childIndex within
          that node that may need redistribution or coalescing.
          The child needs redistribution or coalescing if the
          number of keys in the child has fallen below the
          degree of the BTree. If so, then redistribution may
          be possible if the child is a leaf and a sibling has
          extra items. If redistribution does not work, then
          the child must be coalesced with either the left
          or right sibling.

          This method does not return anything, but has the
          side-effect of redistributing or coalescing
          the child node with a sibling if needed.
        '''
        # Note:  can call insert/delete in this method

        # Node we're deleting from
        delNode = bTree.nodes[self.child[childIndex]]

        # Find sibling to redistribute into
        sibling = 'left'
        if childIndex-1 < 0:
            sibling = 'right'

        # Find sibling index
        siblingIdx = childIndex - 1 if sibling == 'left' else childIndex + 1

        # Get sibling node
        siblingNode = bTree.nodes[self.child[siblingIdx]]

        # Check if we can redistribute
        if siblingNode.numberOfKeys > self.degree:
            # Retrieve item in sibling to be the new parent item
            if sibling == 'left':
                newParentItem = siblingNode.items[siblingNode.numberOfKeys - 1]
            else:
                newParentItem = siblingNode.items[0]
                siblingNode.items[0] = None
                siblingNode.items = sorted(siblingNode.items, key=lambda x: (x is None, x))

            # Update siblings' number of keys
            siblingNode.numberOfKeys = siblingNode.numberOfKeys-1

            # Grab parent item to be redistributed into childNode
            parentIdx = childIndex-1 if sibling == 'left' else childIndex
            parentItem = self.items[parentIdx]

            # Replace parent item with newParentItem
            self.items[parentIdx] = newParentItem

            # Add parentItem to the node we're deleting from
            delNode.items.append(parentItem)
            delNode.items = sorted(delNode.items, key=lambda x: (x is None, x))

        # Redistribution is not an option. We must coalesce.
        else:
            # Merge delNode items, sibling items, and selected parent item
            # if sibling == 'right', coalesce into delNode, else coalesce into 'left' node
            mergeNode = delNode if sibling == 'right' else siblingNode

            parentIdx = childIndex if sibling == 'right' else childIndex-1
            mergeItems = delNode.items + siblingNode.items + [self.items[parentIdx]]
            mergeItems = sorted(mergeItems, key=lambda x: (x is None, x))
            while len(mergeItems) > bTree.degree*2+1: #+1 because we haven't deleted item yet--we don't know where it is in the list
                mergeItems.pop()

            mergeNode.items = mergeItems

            # Replace the parent item that was moved down with None, sort
            self.items[parentIdx] = None
            self.items = sorted(self.items, key=lambda x: (x is None, x))

            # Replace the node that was not merged into None
            if sibling == 'right':
                self.child[siblingIdx] = None
            else:
                self.child[childIndex] = None

            # Put children in their appropriate places, parentIdx equals the child index of the node we merged into
            index = parentIdx + 1
            while index < len(self.child)-1:
                current = self.child[index]
                next = self.child[index+1]
                self.child[index] = next
                self.child[index+1] = current
                index += 1

            # Reset the number of keys for merged node
            mergeNode.numberOfKeys = 2*self.degree

            # Reset the number of keys for parent node
            self.numberOfKeys = self.numberOfKeys-1

            # Delete node from bTree that wasn't merged into
            unmergedNode = siblingNode if sibling == 'right' else delNode
            del bTree.nodes[unmergedNode.index]


    def getChild(self,i):
        # Answer the index of the ith child
        if (0 <= i <= self.numberOfKeys):
            return self.child[i]
        else:
            print( 'Error in getChild().' )

    def setChild(self, i, childIndex):
        # Set the ith child of the node to childIndex
        self.child[i] = childIndex

    def getIndex(self):
        return self.index

    def setIndex(self, anInteger):
        self.index = anInteger

    def isFull(self):
        ''' Answer True if the receiver is full.  If not, return
          False.
        '''
        return (self.numberOfKeys == len(self.items))

    def getNumberOfKeys(self):
        return self.numberOfKeys

    def setNumberOfKeys(self, anInt ):
        self.numberOfKeys = anInt

    def clear(self):
        self.numberOfKeys = 0
        self.items = [None]*len(self.items)
        self.child = [None]*len(self.child)

    def search(self, bTree, item):
        '''Answer a dictionary satisfying: at 'found'
          either True or False depending upon whether the receiver
          has a matching item;  at 'nodeIndex' the index of
          the matching item within the node; at 'fileIndex' the
          node's index. nodeIndex and fileIndex are only set if the
          item is found in the current node.
        '''
        # No items have been added to the tree yet:
        if self.numberOfKeys == 0:
            return {'found': False, 'nodeIndex': None, 'fileIndex': None}

        # There are items in tree. Call search recursively until item is found or a leaf node is reached
        for i in range(self.numberOfKeys):
            if item == self.items[i]:
                return {'found': True, 'nodeIndex': i, 'fileIndex': self.getIndex()}
            if item < self.items[i]:
                if self.getChild(i) is None:
                    return {'found': False, 'nodeIndex': None, 'fileIndex': None}
                return BTreeNode.search(bTree.nodes[self.getChild(i)], bTree, item)
            if i == self.numberOfKeys-1:
                if self.getChild(i) is None:
                    return {'found': False, 'nodeIndex': None, 'fileIndex': None}
                return BTreeNode.search(bTree.nodes[self.getChild(i+1)], bTree, item)


class BTree:
    def __init__(self, degree, nodes = {}, rootIndex = 1, freeIndex = 2):
        self.degree = degree

        if len(nodes) == 0:
            self.rootNode = BTreeNode(degree)
            self.nodes = {}
            self.rootNode.setIndex(rootIndex)
            self.writeAt(1, self.rootNode)
        else:
            self.nodes = deepcopy(nodes)
            self.rootNode = self.nodes[rootIndex]

        self.rootIndex = rootIndex
        self.freeIndex = freeIndex

    def __repr__(self):
        return "BTree("+str(self.degree)+",\n "+repr(self.nodes)+","+ \
            str(self.rootIndex)+","+str(self.freeIndex)+")"

    def __str__(self):
        st = '  The degree of the BTree is ' + str(self.degree)+\
             '.\n'
        st += '  The index of the root node is ' + \
              str(self.rootIndex) + '.\n'
        for x in range(1, self.freeIndex):
            node = self.readFrom(x)
            if node.getNumberOfKeys() > 0:
                st += str(node)
        return st


    def delete(self, anItem):
        ''' Answer None if a matching item is not found.  If found,
          answer the entire item.
        '''
        # allows you to return to the user the item that was deleted
        return BTreeNode.delete(self.rootNode, self, anItem)

    def getFreeIndex(self):
        # Answer a new index and update freeIndex.  Private
        self.freeIndex += 1
        return self.freeIndex - 1

    def getFreeNode(self):
        #Answer a new BTreeNode with its index set correctly.
        #Also, update freeIndex.  Private
        newNode = BTreeNode(self.degree)
        index = self.getFreeIndex()
        newNode.setIndex(index)
        self.writeAt(index,newNode)
        return newNode

    def inorderOn(self, aFile):
        '''
          Print the items of the BTree in inorder on the file
          aFile.  aFile is open for writing.
        '''
        aFile.write("An inorder traversal of the BTree:\n")
        self.inorderOnFrom( aFile, self.rootIndex)

    def inorderOnFrom(self, aFile, index):
        ''' Print the items of the subtree of the BTree, which is
          rooted at index, in inorder on aFile.
        '''
        pass

    def insert(self, anItem):
        ''' Answer None if the BTree already contains a matching
          item. If not, insert a deep copy of anItem and answer
          anItem.
        '''
        # Check if the new item is already in the tree
        searchResult = BTree.searchTree(self, anItem)
        if searchResult["found"] is False:
            # Item is not in the tree, call insert
            leftNodeIdx, promotedItem, rightNodeIdx = BTreeNode.insert(self.rootNode, self, anItem)
            # There has been a split at the root node, new root must be assigned with promotedItem
            if promotedItem:
                newRootNode = self.getFreeNode()
                newRootNode.items[0] = promotedItem
                newRootNode.child[0] = leftNodeIdx
                newRootNode.child[1] = rightNodeIdx
                newRootNode.numberOfKeys = 1
                self.rootNode = newRootNode
                self.rootIndex = newRootNode.index

    def levelByLevel(self, aFile):
        ''' Print the nodes of the BTree level-by-level on aFile. )
        '''
        pass

    def readFrom(self, index):
        ''' Answer the node at entry index of the btree structure.
          Later adapt to files
        '''
        if self.nodes.__contains__(index):
            return self.nodes[index]
        else:
            return None

    def recycle(self, aNode):
        # For now, do nothing
        aNode.clear()

    def retrieve(self, anItem):
        ''' If found, answer a deep copy of the matching item.
          If not found, answer None
        '''
        pass

    def searchTree(self, anItem):
        ''' Answer a dictionary.  If there is a matching item, at
          'found' is True, at 'fileIndex' is the index of the node
          in the BTree with the matching item, and at 'nodeIndex'
          is the index into the node of the matching item.  If not,
          at 'found' is False, but the entry for 'fileIndex' is the
          leaf node where the search terminated.
        '''
        return BTreeNode.search(self.rootNode, self, anItem)


    def update(self, anItem):
        ''' If found, update the item with a matching key to be a
          deep copy of anItem and answer anItem.  If not, answer None.
        '''
        pass

    def writeAt(self, index, aNode):
        ''' Set the element in the btree with the given index
          to aNode.  This method must be invoked to make any
          permanent changes to the btree.  We may later change
          this method to work with files.
          This method is complete at this time.
        '''
        self.nodes[index] = aNode


def btreemain():
    '''

    README:

    The delete method isn't fully operational yet. It is able to redistribute, coalesce, and find successor when
    deleting an item, however, it has issues merging the parent node with its sibling if it has less then degree
    items after its child had to coalesce, thus running this program will eventually throw an error when deleting an item.

    Thank you.

    '''

    print("My/Our name(s) is/are ")

    lst = [10, 8, 22, 14, 12, 18, 2, 50, 15]

    b = BTree(2)

    for x in lst:
        print(repr(b))
        print("***Inserting", x)
        b.insert(x)

    print(repr(b))

    lst = [14, 50, 8, 12, 18, 2, 10, 22, 15]

    for x in lst:
        print("***Deleting", x)
        b.delete(x)
        print(repr(b))

    # return
    lst = [54, 76]

    for x in lst:
        print("***Deleting", x)
        b.delete(x)
        print(repr(b))

    print("***Inserting 14")
    b.insert(14)

    print(repr(b))

    print("***Deleting 2")
    b.delete(2)

    print(repr(b))

    print("***Deleting 84")
    b.delete(84)

    print(repr(b))


'''
Here is the expected output from running this program. Depending on the order of 
redistributing or coalescing, your output may vary. However, the end result in 
every case should be the insertion or deletion of the item from the BTree. 

My/Our name(s) is/are 
BTree(2,
 {1: BTreeNode(2,0,[None, None, None, None],[None, None, None, None, None],1)
},1,2)
***Inserting 10
BTree(2,
 {1: BTreeNode(2,1,[10, None, None, None],[None, None, None, None, None],1)
},1,2)
***Inserting 8
BTree(2,
 {1: BTreeNode(2,2,[8, 10, None, None],[None, None, None, None, None],1)
},1,2)
***Inserting 22
BTree(2,
 {1: BTreeNode(2,3,[8, 10, 22, None],[None, None, None, None, None],1)
},1,2)
***Inserting 14
BTree(2,
 {1: BTreeNode(2,4,[8, 10, 14, 22],[None, None, None, None, None],1)
},1,2)
***Inserting 12
BTree(2,
 {1: BTreeNode(2,2,[8, 10, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[14, 22, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 18
BTree(2,
 {1: BTreeNode(2,2,[8, 10, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[14, 18, 22, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 2
BTree(2,
 {1: BTreeNode(2,3,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[14, 18, 22, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 50
BTree(2,
 {1: BTreeNode(2,3,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,4,[14, 18, 22, 50],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 15
BTree(2,
 {1: BTreeNode(2,3,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[14, 15, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[12, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 14
**Redistribute From Left**
BTree(2,
 {1: BTreeNode(2,2,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[12, 15, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[10, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 50
**Coalesce with Left Sibling in node with index 3
BTree(2,
 {1: BTreeNode(2,2,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,4,[12, 15, 18, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[10, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 8
**Redistribute From Right**
BTree(2,
 {1: BTreeNode(2,2,[2, 10, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[15, 18, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 12
BTree(2,
 {1: BTreeNode(2,2,[2, 10, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[18, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 18
**Coalesce with Left Sibling in node with index 3
BTree(2,
 {1: BTreeNode(2,4,[2, 10, 15, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 2
BTree(2,
 {1: BTreeNode(2,3,[10, 15, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 10
BTree(2,
 {1: BTreeNode(2,2,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 22
BTree(2,
 {1: BTreeNode(2,1,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 15
BTree(2,
 {1: BTreeNode(2,0,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 54
54 not found during delete.
BTree(2,
 {1: BTreeNode(2,0,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 76
76 not found during delete.
BTree(2,
 {1: BTreeNode(2,0,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Inserting 14
BTree(2,
 {1: BTreeNode(2,1,[14, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 2
2 not found during delete.
BTree(2,
 {1: BTreeNode(2,1,[14, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 84
84 not found during delete.
BTree(2,
 {1: BTreeNode(2,1,[14, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
'''


def readRecord(file, recNum, recSize):
    file.seek(recNum * recSize)
    record = file.read(recSize)
    return record


def readField(record, colTypes, fieldNum):
    # fieldNum is zero based
    # record is a string containing the record
    # colTypes is the types for each of the columns in the record

    offset = 0
    for i in range(fieldNum):
        colType = colTypes[i]

        if colType == "int":
            offset += 10
        elif colType[:4] == "char":
            size = int(colType[4:])
            offset += size
        elif colType == "float":
            offset += 20
        elif colType == "datetime":
            offset += 24

    colType = colTypes[fieldNum]

    if colType == "int":
        value = record[offset:offset + 10].strip()
        if value == "null":
            val = None
        else:
            val = int(value)
    elif colType == "float":
        value = record[offset:offset + 20].strip()
        if value == "null":
            val = None
        else:
            val = float(value)
    elif colType[:4] == "char":
        size = int(colType[4:])
        value = record[offset:offset + size].strip()
        if value == "null":
            val = None
        else:
            val = value[1:-1]  # remove the ' and ' from each end of the string
            if type(val) == bytes:
                val = val.decode("utf-8")
    elif colType == "datetime":
        value = record[offset:offset + 24].strip()
        if value == "null":
            val = None
        else:
            if type(val) == bytes:
                val = val.decode("utf-8")
            val = datetime.datetime.strptime(val, '%m/%d/%Y %I:%M:%S %p')
    else:
        print("Unrecognized Type")
        raise Exception("Unrecognized Type")

    return val


class Item:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return "Item(" + repr(self.key) + "," + repr(self.value) + ")"

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key

    def getValue(self):
        return self.value

    def getKey(self):
        return self.key


def main():
    # Select Feed.FeedNum, Feed.Name, FeedAttribType.Name, FeedAttribute.Value where
    # Feed.FeedID = FeedAttribute.FeedID and FeedAttribute.FeedAtribTypeID = FeedAttribType.ID
    attribTypeCols = ["int", "char20", "char60", "int", "int", "int", "int"]
    feedCols = ["int", "int", "int", "char50", "datetime", "float", "float", "int", "char50", "int"]
    feedAttributeCols = ["int", "int", "float"]

    feedAttributeTable = open("FeedAttribute.tbl", "r")

    if os.path.isfile("Feed.idx"):
        indexFile = open("Feed.idx", "r")
        feedTableRecLength = int(indexFile.readline())
        feedIndex = eval("".join(indexFile.readlines()))
    else:
        feedIndex = BTree(3)
        feedTable = open("Feed.tbl", "r")
        offset = 0
        for record in feedTable:
            feedID = readField(record, feedCols, 0)
            anItem = Item(feedID, offset)
            feedIndex.insert(anItem)
            offset += 1
            feedTableRecLength = len(record)

        print("Feed Table Index Created")
        indexFile = open("Feed.idx", "w")
        indexFile.write(str(feedTableRecLength) + "\n")
        indexFile.write(repr(feedIndex) + "\n")
        indexFile.close()

    if os.path.isfile("FeedAttribType.idx"):
        indexFile = open("FeedAttribType.idx", "r")
        attribTypeTableRecLength = int(indexFile.readline())
        attribTypeIndex = eval("".join(indexFile.readlines()))
    else:
        attribTypeIndex = BTree(3)
        attribTable = open("FeedAttribType.tbl", "r")
        offset = 0
        for record in attribTable:
            feedAttribTypeID = readField(record, attribTypeCols, 0)
            anItem = Item(feedAttribTypeID, offset)
            attribTypeIndex.insert(anItem)
            offset += 1
            attribTypeTableRecLength = len(record)

        print("Attrib Type Table Index Created")
        indexFile = open("FeedAttribType.idx", "w")
        indexFile.write(str(attribTypeTableRecLength) + "\n")
        indexFile.write(repr(attribTypeIndex) + "\n")
        indexFile.close()

    feedTable = open("Feed.tbl", "rb")
    feedAttribTypeTable = open("FeedAttribType.tbl", "rb")
    before = datetime.datetime.now()
    for record in feedAttributeTable:
        feedID = readField(record, feedAttributeCols, 0)
        feedAttribTypeID = readField(record, feedAttributeCols, 1)
        value = readField(record, feedAttributeCols, 2)

        lookupItem = Item(feedID, None)
        item = feedIndex.retrieve(lookupItem)
        offset = item.getValue()
        feedRecord = readRecord(feedTable, offset, feedTableRecLength)
        feedNum = readField(feedRecord, feedCols, 2)
        feedName = readField(feedRecord, feedCols, 3)

        lookupItem = Item(feedAttribTypeID, None)
        item = attribTypeIndex.retrieve(lookupItem)
        offset = item.getValue()
        feedAttribTypeRecord = readRecord(feedAttribTypeTable, offset, \
                                          attribTypeTableRecLength)
        feedAttribTypeName = readField(feedAttribTypeRecord, attribTypeCols, 1)

        print(feedNum, feedName, feedAttribTypeName, value)
    after = datetime.datetime.now()
    deltaT = after - before
    milliseconds = deltaT.total_seconds() * 1000
    print("Done. The total time for the query with indexing was", milliseconds, \
          "milliseconds.")


if __name__ == "__main__":
    btreemain()

