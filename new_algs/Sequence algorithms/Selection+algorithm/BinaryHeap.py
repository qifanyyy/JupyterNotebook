class BinaryHeap:

    '''
        Initialise an empty heap and the current size
        We set the empty heap to have an initial zero value
        for integer division for our percolation method
    '''
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0

    '''
        Percolate an item up from the end of the list to it's correct position
        :param  int i    The index of the node to move up
    '''
    def percUp(self, i):
        # while the node index is greater than 0
        # i//2 is used to move up or down as disctated by complete binary trees definition
        # (all parents at all levels - except the last - will have 2 children)
        while i//2 > 0:
            # if our current node is less than the node above, swap them
            if self.heapList[i] < self.heapList[i//2]:
                self.heapList[i], self.heapList[i//2] = self.heapList[i//2], self.heapList[i]
        # select the next node
        i = i//2

    '''
        Percolate an item from the top of the list down to it's correct position
        :param  int     i   The index of the node to move down
    '''
    def percDown(self, i):
        # while the index at the next level is less than the currentSize
        while (i * 2) <= self.currentSize:
            # get the minimum child from the node given at i
            mc = self.minChild(i)
            # if our node is greater than the minimum child node
            if self.heapList[i] > self.heapList[mc]:
                # swap it
                self.heapList[i], self.heapList[mc] = self.heapList[mc], self.heapList[i]
            # select our next node
            i = mc

    '''
        Return the index of the node with the minimum value from the parent
        :param int      i   The index of the current node
    '''
    def minChild(self, i):
        # if there is 1 child node return this
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            # else return the left or the right node
            if self.heapList[i*2] < self.heapList[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1

    '''
        Insert an item into the binary heap
        :param mixed    k   The item to add to the heap
    '''
    def insert(self, k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    '''
        Removes the root node from the heap and rebuilds it

        :return object
    '''
    def delMin(self):
        # our heap items start at 1, so grab this
        retval = self.heapList[1]
        # place the last element in the heap as the root node
        self.heapList[1] = self.heapList[self.currentSize]
        # decrement the size by 1
        self.currentSize = self.currentSize - 1
        # pop the last element off, as we've copied the value to root
        self.heapList.pop()
        # percolate the root node down
        self.percDown(1)
        # return the original root node
        return retval

    '''
        Builds a heap from a List of keys in O(n) complexity.
        - we start at the middle of the list
        - we create a base heapList from our list (as is)
        - we then move up through the list, moving each item down as required
        - when we reach root, the BinaryHeap should be valid

        :param  List    aList   A list of keys to construct our binary heap 
    '''
    def buildHeap(self, aList):
        # let's start half way through the tree
        i = len(aList) // 2
        # set the size to the amount of nodes we have
        self.currentSize = len(aList)
        # build our initial heapList
        self.heapList = [0] + aList[:]
        # while we haven't reached root
        while (i > 0):
            # move the node at poisition i down
            self.percDown(i)
            # move back an item
            i = i - 1
