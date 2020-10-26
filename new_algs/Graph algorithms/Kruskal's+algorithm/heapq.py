'''
Emmanuel John (emmanuj)
Implementation for edge priority queue
'''

from edge import Edge
import math

class Heapq:
    def __init__(self, d):
        self.data = []
        self.d = d

    def make_heap(self, lst):
        self.data = lst
        k = self.size() -1
        while k >=0:
            self.siftdown(k)
            k = k-1

    def find_min(self):
        return self.data[0]

    def delete(self, k):
        if(k == self.size() - 1):
            del self.data[self.size() -1]
            return

        last = self.data[self.size() - 1]
        del self.data[self.size() -1]
        item = self.data[k]
        self.data[k] = last

        if(last.weight < item.weight):
            self.siftup(k)
        else:
            self.siftdown(k)


    def delete_min(self):
        if self.size() == 0: return
        self.delete(0)

    def size(self):
        return len(self.data)

    def siftup(self, k):
        if k > self.size() - 1:
            return #throw error
        p = int((k-1)/self.d)
        while(k > 0 and self.data[p].weight > self.data[k].weight):
            #swap
            temp = self.data[k]
            parent = self.data[p]
            self.data[k] = parent
            self.data[p] = temp
            k = p #go up one
            p = int((k-1)/self.d)

    def siftdown(self, k):
        j = self.minchild(k)
        while(j != None and self.data[j].weight < self.data[k].weight):
            #swap
            temp = self.data[k]
            child = self.data[j]
            self.data[k] = child
            self.data[j] = temp
            k = j
            j = self.minchild(k)

    def minchild(self, k):
        i = (self.d * k) + 1
        end = (self.d * k) + self.d
        if(i>=self.size()):
            return None
        min_idx = i
        minValue = self.data[i].weight
        while(i<=end and i < self.size()):
            if(self.data[i].weight <= minValue  ):
                minValue = self.data[i].weight
                min_idx = i
            i = i+1
        return min_idx


    def __repr__(self):
        return str(self.data)
