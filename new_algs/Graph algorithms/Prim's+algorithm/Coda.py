from collections import deque

class CodaArrayList():
    """ Implementation of a FIFO queue using a Python's list built-in type, i.e., lists based on array implementation.
    """
    
    def __init__(self):
        self.q = []
        
    def enqueue(self, elem):
        self.q.append(elem)
    
    def dequeue(self):
        if len(self.q) == 0:
            return None
        return self.q.pop(0)
    
    def getFirst(self):
        if len(self.q) == 0:
            return None
        else:
            return self.q[0]
    
    def isEmpty(self):
        return len(self.q) == 0
    
    def stampa(self):
        print "Elements in the collection (ordered):"
        print self.q
        
class CodaArrayList_deque(CodaArrayList):
    """ Faster implementation of a FIFO using the type deque, optimized also for removing elements at the beginning of the collection.
    """
    def __init__(self):
        self.q = deque()
    
    #Override
    def dequeue(self):
        if len(self.q) == 0:
            return None
        return self.q.popleft()