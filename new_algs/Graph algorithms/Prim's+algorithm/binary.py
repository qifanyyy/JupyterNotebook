from LinkedList import ListaCollegata
from Coda import CodaArrayList_deque as queue

class BinaryHeapNode:
    def __init__(self, e, k, i):
        self.elem = e
        self.key = k
        self.index = i

class PQbinaryHeap:
    def __init__(self):
        self.heap = [] 
        self.length = 0

    def minSon(self, node):
        if node.index * 2 + 1 > self.length - 1:
            return None
        if node.index * 2 + 2 > self.length - 1:
            return self.heap[node.index * 2 + 1]    
        return self.heap[node.index * 2 + 1] if  self.heap[node.index * 2 + 1].key < self.heap[node.index * 2 + 2].key else self.heap[node.index * 2 + 2]

    def swap(self, node1, node2):
        self.heap[node1.index] = node2
        self.heap[node2.index] = node1
        node1.index, node2.index = node2.index, node1.index

    def moveUp(self, son):
        if son.index <= 0:
            return
        father = self.heap[(son.index - 1) / 2]
        while son.index > 0 and son.key < father.key:
            self.swap(son, father)
            father = self.heap[(son.index - 1) / 2]
    
    def moveDown(self, father):
        son = self.minSon(father)
        while son != None and son.key < father.key:
            self.swap(father, son)
            son = self.minSon(father)
    
    def isEmpty(self):
        if self.length == 0:
            return True
        return False

    def findMin(self):
        if self.isEmpty():
            return None
        return self.heap[0].elem
    
    def insert(self, k, e):
        n = BinaryHeapNode(e, k, self.length)
        if self.length<len(self.heap):
            self.heap[self.length]=n
        else:
            self.heap.append(n)
        self.length += 1
        self.moveUp(n)     
        return n        

    def deleteMin(self):
        if self.length == 0:
            return
        first = self.heap[0]
        last = self.heap[self.length - 1]
        self.swap(first, last)
        self.length -= 1
        self.moveDown(last)
      
        
    def decreaseKey(self, node, nKey):
        node.key = nKey
        self.moveUp(node)
    
    def stampa(self):
        s = ""
        for i in xrange(self.length):
            n=self.heap[i]
            s += "[{},{}] ".format(n.elem, n.key)
        print s
