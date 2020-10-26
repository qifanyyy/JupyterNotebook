from LinkedList import ListaCollegata
from Coda import CodaArrayList_deque as queue


class DHeapNode:
    def __init__(self, e, k, i):
        self.elem = e
        self.key = k
        self.index = i

class PQ_DHeap:
    def __init__(self,d):
        self.d=d
        #representation by sons of node. Index=i is d*i + {1,...,d}
        self.heap = [] # DHeapNode
        self.length = 0

    def minSon(self, node):
        index=node.index
        minSon=None
        minKey=float('inf')
        for s in xrange(1,self.d+1):
            sindex=self.d*index+s
            if sindex>self.length-1:
                break
            son=self.heap[sindex]
            if son.key<minKey:
                minKey=son.key
                minSon=son
        return minSon

    def swap(self, node1, node2):
        self.heap[node1.index] = node2
        self.heap[node2.index] = node1
        node1.index, node2.index = node2.index, node1.index

    def moveUp(self, son):
        if son.index <= 0:
            return
        
        father = self.heap[(son.index - 1) / self.d]
        while son.index > 0 and son.key < father.key:
            self.swap(son, father)
            father = self.heap[(son.index - 1) / self.d]
    
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
        n = DHeapNode(e, k, self.length)
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
