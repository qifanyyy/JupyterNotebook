'''
1) Ben Mackenzie
2) 3/26/2018
'''

from Queue import Empty

class HeapPriorityQueue(object):
    '''
    This class is a heap-based implementation of a Queue,
    containing public methods for inserting items, retrieving
    the queue minimum, deleting the queue minimum, and private methods 
    supporting these public methods.
    '''

    def __init__(self, root = None):
        '''
        Constructor
        '''
        self._root = root
        self._data = []    
        
    def __str__(self):
        return (' ').join([str(e) for e in self._data])  
    
    def _parent(self, i):
        return (i - 1) // 2
    
    def _left(self, i):
        return i * 2 + 1
    
    def _right(self, i):
        return i * 2 + 2
    
    def _hasLeft(self, i):
        return self._left(i) < len(self._data)
    
    def _hasRight(self, i):
        return self._right(i) < len(self._data)
    
    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]
    
    def _bubbleUp(self, i):
        if i > 0 and self._data[i]._element < self._data[self._parent(i)]._element:
            self._swap(i, self._parent(i))
            self._bubbleUp(self._parent(i))
    
    def _bubbleDown(self, i):
        if self._hasLeft(i):
            root = self._data[i]
            left = self._left(i)
            smallChild = left
            if self._hasRight(i):
                right = self._right(i)
                if self._data[left]._element > self._data[right]._element:
                    smallChild = right
            if self._data[smallChild]._element < root._element:
                self._swap(i, smallChild)
                self._bubbleDown(smallChild)
                
    def is_empty(self):
        if len(self._data) == 0:
            return True
        else:
            return False            
        
    def insert(self, item):
        self._data.append(item)
        self._bubbleUp(len(self._data) - 1)
    
    def deleteMin(self):
        if len(self._data) == 0:
            raise Empty('The Priority Queue is empty.')
        last = len(self._data) - 1
        self._swap(0, last)
        item = self._data.pop()
        self._bubbleDown(0)
        return item
    
    def min(self):
        if len(self._data) == 0:
            raise Empty('The Priority Queue is empty.')
        else:
            return self._data[0]
    
        
        