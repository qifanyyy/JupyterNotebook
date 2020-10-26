from elements import Arc
import tkSimpleDialog
from Binomial import PQbinomialHeap
from Binary import PQbinaryHeap
from D_Heap import PQ_DHeap
Infinite = float("inf")

class comparableArc(Arc):
    def __init__(self, e):
        
        Arc.__init__(self, e[0], e[1], e[2])
        
    def __cmp__(self, other):
        if other == None:
            
            return 1
        if self.weight == None and other.weight == None:
            return 0

        if self.weight == None:
            
            return -1

        if other.weight == None:

            return 1

        if self.weight < other.weight:
            return -1

        if self.weight > other.weight:
            return 1
        return 0
    
    def __repr__(self):
        
        return "(" + str(self.tail) + ", " + str(self.head) + ", " + str(self.weight) + ")"
    
    def __str__(self):
        
        return self.__repr__()


class MST:
    
    
    @staticmethod
    def prim(g, root, l, d):

        
        n = len(g.nodes)
        nodes1 = n * [None]
        if root < 0 or root >= n:
            return
        nodes = n * [None]

        if l == 'PQ_DHeap':
            pq = PQ_DHeap(d)
        if l == 'PQbinaryHeap':
            pq = PQbinaryHeap()
        if l == 'PQbinomialHeap':
            pq = PQbinomialHeap()
            
        lui = g.nodes.keys()
        
        
        for i in xrange(len(g.nodes.keys())):
            
            if lui[i] == root:
                               
                nodes[i] = pq.insert(0.0, lui[i])

            else:
                
                nodes[i] = pq.insert(Infinite, lui[i])

                    
        mst_weight = 0
        n2e = n * [None]
        mst = []
        print ''
        print ''
        print 'prim'
        print ''
        print ''
        h = n
        c = 0
        h2 = 1
        while not pq.isEmpty():
            
            
           
            inode = pq.findMin()
            if inode == None:
                break
            
            
            
            if l == 'PQbinomialHeap':
                mst_weight += nodes[lui.index(inode)].ref.key if nodes[lui.index(inode)] != None else 0
            
            
            else:
                mst_weight += nodes[lui.index(inode)].key if nodes[lui.index(inode)] != None else 0
                
            
            

            if n2e[lui.index(inode)] != None:
                mst.append(n2e[lui.index(inode)])
            nodes[lui.index(inode)] = None  #nodes marked in mst
            
            pq.deleteMin()
            n = n-1
            

            curr = g.adj[inode].getFirstRecord()
            
            
            while curr != None:
                peso = curr.next
                el = curr.elem
                if l == 'PQbinomialHeap':
                        
                    if nodes[lui.index(el)] != None and (peso.elem == None or peso.elem < nodes[lui.index(el)].ref.key):
                        
                        nodes[lui.index(el)].decrease(peso.elem if peso.elem != None else 0)
                        n2e[lui.index(el)] = comparableArc((inode,el,peso.elem))
                        
                else:
                    
                    if nodes[lui.index(el)] != None and (peso.elem == None or peso.elem < nodes[lui.index(el)].key):    
                            
                        pq.decreaseKey(nodes[lui.index(el)], peso.elem if peso.elem != None else 0)
                        n2e[lui.index(el)] = comparableArc((inode,el,peso.elem))
                
                
                curr = curr.next
                curr = curr.next
            
            if c == 100*h2 or n == 0 :
                prog = 100*float(n)/float(h)
                print 100 - round(prog, 2), '%'
                h2 += 1
            c += 1
            
                
        return mst_weight, mst, d
        
