######################################################################
# Shawn Wonder                                                       #
# 09/07/2017                                                         #
# This implementation of a min heap uses the values (not the keys)   #
# for minimum values because duplicate keys (distances) may exist    # 
######################################################################
import math
from node import *

class binaryHeap:
    def __init__(self):
        self.nodes = []
        #Indexing is used to keep runtime of decreaseKey at O(log(n))
        self.index = {}

    def makeHeap(self, nodesList):
        for n in nodesList:
            self.insertNode(n)

    def getIndex(self, v):
        for i in range(1, len(self.nodes)):
            if v == self.nodes[i].value:
                return i
        return -1

    def insertKeyValue(self, k, v):
        n = node(k, v)
        self.insertNode(n)

    def insertNode(self, n):
        #Add a dummy element to the list becuase list index must start at 1
        #for heap operations to work
        if len(self.nodes) == 0:
            self.nodes.append(node(-1, -1))
        self.nodes.append(n)
        self.index[n.value] = len(self.nodes)-1
        self.bubbleUp(n)

    def decreaseKey(self, k, v):
        idx = self.index[v]
        self.nodes[idx].key = k
        self.bubbleUp(self.nodes[idx])
    
    def bubbleUp(self, n):
        while True:
            keyPos = self.getIndex(n.value)
            parentKeyPos = int(keyPos/2)
            #If key values are equal, heap is then ordered by value
            if self.nodes[keyPos].key <= self.nodes[parentKeyPos].key:
                if self.nodes[keyPos].key == self.nodes[parentKeyPos].key:
                    if self.nodes[keyPos].value < self.nodes[parentKeyPos].value:
                        self.swapNodes(keyPos, parentKeyPos)
                else:
                    self.swapNodes(keyPos, parentKeyPos)
            else:
                break
            n = self.nodes[parentKeyPos]

    def getMin(self):
        return self.nodes[1]

    #Deletes the minimum node off the heap and returns the minimum node    
    def popMin(self):
        minNode = self.getMin()
        self.deleteMin()
        return minNode

    #Only deletes the minimum node off the heap 
    def deleteMin(self):
        self.swapNodes(1, len(self.nodes)-1)
        del self.index[self.nodes[len(self.nodes)-1].value]
        self.nodes = self.nodes[:-1]
        if len(self.nodes) > 1:
            minNode = self.getMin()
            self.siftDown(minNode)

    def siftDown(self, n):
        node = n
        while True:
            keyPos = self.getIndex(node.value)
            minChildPos = self.minChild(node.value)
            if minChildPos != -1:
                if self.nodes[minChildPos].key <= self.nodes[keyPos].key:
                    self.swapNodes(keyPos, minChildPos)
                node = self.nodes[minChildPos]
            else:
                break
        keyPos = minChildPos

    def minChild(self, v):
        pos = self.getIndex(v)
        if 2*pos >= len(self.nodes):
            return -1
        leftChild = self.nodes[2*pos].key

        rightChild = -1
        if 2*pos+1 < len(self.nodes):
            rightChild = self.nodes[(2*pos)+1].key
            
        if leftChild <= rightChild and rightChild > -1:
            return self.getIndex(self.nodes[2*pos].value)
        elif leftChild > rightChild and rightChild > -1:
            return self.getIndex(self.nodes[2*pos+1].value)
        else:
            return self.getIndex(self.nodes[2*pos].value)

    def swapNodes(self, i, j):
        self.index[self.nodes[i].value] = j
        self.index[self.nodes[j].value] = i
        self.nodes[i], self.nodes[j] = self.nodes[j], self.nodes[i]
        
    def isEmpty(self):
        return True if len(self.nodes) <= 1 else False

    def exists(self, k, v):
        for node in self.nodes:
            if node.key == k and node.value == v:
                return True
        return False

    def keyList(self):
        keys = []
        for i in range(1, len(self.nodes)):
            keys.append(self.nodes[i].key)
        return keys

    def valueList(self):
        values = []
        for i in range(1, len(self.nodes)):
            values.append(self.nodes[i].value)
        return values

    #Display a flat list of the heap
    def display(self):
        print("--List for min heap--")
        for i in range(1, len(self.nodes)):
            print(str(self.nodes[i].key) + ":" + str(self.nodes[i].value))

    #Display a text tree representation of key:value pairs
    def displayTree(self):
        level = 1
        depth = math.floor(math.log(len(self.nodes), 2.0))
        print("Tree depth " + str(depth))
        s = True
        for i in range(1, len(self.nodes)):
            if s: 
                print(' ' * depth*5, end='')
                s = False
            print(str(self.nodes[i].key)+':'+str(self.nodes[i].value)+'   ', end='') 
            if i == 2**level-1:
                print(' ' * depth*5)
                level+=1
                depth-=1
                s=True
        print()
        
            

