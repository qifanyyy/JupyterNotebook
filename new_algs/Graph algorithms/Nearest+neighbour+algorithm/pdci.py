import numpy as np
from heapq import heappush, heappop
import os
from sklearn.datasets.samples_generator import make_blobs
from datetime import datetime
from sets import Set
from timeit import Timer
from sklearn.neighbors import KDTree
from sklearn.neighbors import BallTree
from sklearn.datasets import fetch_mldata

class Node():
    def __init__(self, proj, point, parent = None):
        self.proj = proj
        self.points = []
        self.points.append(point)
        self.parent = parent
        self.left = None
        self.right = None
        self.balance = 0
        
    def has_left(self):
        return True if self.left != None else False
    
    def has_right(self):
        return True if self.right != None else False
    
    def is_left(self):
        return True if self == self.parent.left else False
    
    def is_right(self):
        return True if self == self.parent.right else False
    
    def is_root(self):
        return True if self.parent == None else False
    
    def is_leaf(self):
        return True if self.left == None and self.right == None else False
    
class AVLTree():
    def __init__(self):
        self.root = None
        
    def insert(self, proj, point, currentNode=None):
        '''
        Time Complexity: O(log(n))
        '''
        if self.root == None:
            self.root = Node(proj, point)
            return
            
        if proj < currentNode.proj:
            if currentNode.has_left():
                self.insert(proj, point, currentNode.left)
            else:
                currentNode.left = Node(proj, point, parent = currentNode)
                self.update_balance(currentNode.left)
        elif proj > currentNode.proj:
            if currentNode.has_right():
                self.insert(proj, point, currentNode.right)
            else:
                currentNode.right = Node(proj, point, parent = currentNode)
                self.update_balance(currentNode.right)
        else:
            currentNode.points.append(point)
                
    def update_balance(self, node):
        '''
        Time Complexity: O(log(n))
        ??? why <= we just need to update the inserted node's parent, grandparent, ..., root
        How many node needs to be updated = how many parents the node has = how many level the tree has = log2n
        '''
        if node.balance < -1 or node.balance > 1:
            self.rebalance(node)
            return
        if node.parent != None:
            if node.is_left():
                node.parent.balance += 1
            elif node.is_right():
                node.parent.balance -= 1
            if node.parent.balance != 0:
                self.update_balance(node.parent)
    
    def rebalance(self, node):
        '''
        Time Complexity: O(C)
        '''
        if node.balance < 0:
            if node.right.balance > 0:
                self.right_rotate(node.right)
                self.left_rotate(node)
            else:
                self.left_rotate(node)
        elif node.balance > 0:
            if node.left.balance < 0:
                self.left_rotate(node.left)
                self.right_rotate(node)
            else:
                self.right_rotate(node)
    
    def left_rotate(self, old_root):
        '''
        Time Complexity: O(C)
        '''
        new_root = old_root.right
        
        old_root.right = new_root.left
        if new_root.left != None:
            new_root.left.parent = old_root
        
        new_root.parent = old_root.parent
        
        if old_root.is_root():
            self.root = new_root
        else:
            if old_root.is_left():
                old_root.parent.left = new_root
            else:
                old_root.parent.right = new_root
        
        new_root.left = old_root
        old_root.parent = new_root
        
        old_root.balance = old_root.balance + 1 - min(new_root.balance, 0)
        new_root.balance = new_root.balance + 1 + max(old_root.balance, 0)
        
    def right_rotate(self, old_root):
        '''
        Time Complexity: O(C)
        '''
        new_root = old_root.left
        
        old_root.left = new_root.right
        if new_root.right != None:
            new_root.right.parent = old_root

        new_root.parent = old_root.parent
        
        if old_root.is_root():
            self.root = new_root
        else:
            if old_root.is_left():
                old_root.parent.left = new_root
            else:
                old_root.parent.right = new_root
                
        new_root.right = old_root
        old_root.parent = new_root
        
        old_root.balance = old_root.balance - 1 - max(new_root.balance, 0)
        new_root.balance = new_root.balance - 1 - min(old_root.balance, 0)
        
    def display(self, level=0, pref="Root"):
        if(self.root != None): 
            print '-' * level * 10, pref, "[", self.root.proj, str(self.root.points), "b=" + str(self.root.balance) + "]", 'L' if self.root.is_leaf() else 'N', "]"   
            if self.root.left != None: 
                left_subtree = AVLTree()
                left_subtree.root = self.root.left
                left_subtree.display(level + 1, 'L')
            if self.root.right != None:
                right_subtree = AVLTree()
                right_subtree.root = self.root.right
                right_subtree.display(level + 1, 'R')
        else:
            print "Empty Tree"
            
    def predecessor(self, root, pred, proj):
        '''
        Time Complexity: O(log(n))
        '''
        if root is None:
            return None
        if proj < root.proj:
            if root.has_left():
                return self.predecessor(root.left, pred, proj)
            else:
                return pred
        elif proj == root.proj:
            if root.has_left():
                pred = self.maximum(root.left)
            return pred
        else:
            if root.has_right():
                pred = root
                return self.predecessor(root.right, pred, proj)
            else:
                return root
                
    def maximum(self, root):
        '''
        Time Complexity: O(log(n))
        '''
        while root.has_right():
            root = root.right
        return root
    
    def successor(self, root, succ, proj):
        '''
        Time Complexity: O(log(n))
        '''
        if root is None:
            return None
        if proj < root.proj:
            if root.has_left():
                succ = root
                return self.successor(root.left, succ, proj)
            else:
                return root
        elif proj == root.proj:
            if root.has_right():
                succ = self.minimum(root.right)
            return succ
        else:
            if root.has_right():
                return self.successor(root.right, succ, proj)
            else:
                return succ
            
    def minimum(self, root):
        '''
        Time Complexity: O(log(n))
        '''
        while root.has_left():
            root = root.left
        return root
    
    def closer(self, pred, succ, proj):
        '''
        Time Complexity: O(C)
        '''
        if abs(pred.proj-proj) < abs(succ.proj-proj):
            return [pred, succ]
        elif abs(pred.proj-proj) > abs(succ.proj-proj):
            return [succ, pred]
        else:
            return [pred, succ]
        
    def search(self, current_node, proj):
        '''
        Time Complexity: O(log(n))
        '''
        if self.root is None:
            return None
        if proj < current_node.proj:
            if current_node.has_left():
                return self.search(current_node.left, proj)
            else:
                return None
        elif proj > current_node.proj:
            if current_node.has_right():
                return self.search(current_node.right, proj)
            else:
                return None
        else:
            return current_node
    
    def query(self, proj, k):
        
        #Time Complexity: O(log(n))
        
        if self.root is None:
            return None
        closest = []
        node = self.search(self.root, proj)
        pred = self.predecessor(self.root, None, proj)
        succ = self.successor(self.root, None, proj)
        if node is not None:
            closest += [node]
        while len(closest) < k+1:
            if pred is not None and succ is not None:
                closest += self.closer(pred, succ, proj)
            elif pred is not None and succ is None:
                closest += [pred]
            elif pred is None and succ is not None:
                closest += [succ]
            else:
                pass
            if pred is not None:
                pred = self.predecessor(self.root, None, pred.proj)
            if succ is not None:
                succ = self.successor(self.root, None, succ.proj)
        return closest[k].proj, closest[k].points[0]
    
    def sort_tree(self, proj, n):
        '''
        Given a projection of a point, sort avl tree, return a list of nodes.
        closest = [node1, node2, ..., node3]
        '''
        #t_start = datetime.now()
        if self.root is None:
            return None
        closest = []
        node = self.search(self.root, proj)
        pred = self.predecessor(self.root, None, proj)
        succ = self.successor(self.root, None, proj)
        if node is not None:
            closest += [node]
        while len(closest) < n:
            if pred is not None and succ is not None:
                closest += self.closer(pred, succ, proj)
            elif pred is not None and succ is None:
                closest += [pred]
            elif pred is None and succ is not None:
                closest += [succ]
            else:
                pass
            if pred is not None:
                pred = self.predecessor(self.root, None, pred.proj)
            if succ is not None:
                succ = self.successor(self.root, None, succ.proj)
        #t_end = datetime.now()
        #print "time:",t_end-t_start
        return closest

def query(sorted_tree, k):
    '''
    Return kth closest node
    '''
    return sorted_tree[k].proj, sorted_tree[k].points[0]

    
def CONSTRUCT(D, m, L, q):
    '''
    Time complexity: O(mL(nd+nlogn))
    Construct uvecs, projs and trees: mLd + mLnd + mLnlogn = m*L*(nd+nlogn)
    '''
    dims = D.shape[1]
    uvecs = np.zeros((m,L),object)
    trees = np.zeros((m,L),object)
    
    for j in range(m):
        for l in range(L):
            v = np.random.normal(0,1,dims)
            mag = np.dot(v,v)**0.5
            uvec = v / mag
            uvecs[j,l] = uvec
            projs = np.dot(D, uvec)
            trees[j,l] = AVLTree()
            for i in range(len(projs)):
                trees[j,l].insert(projs[i],i,trees[j,l].root)

    sorted_trees = np.zeros((m,L),object)
    q_projs = np.zeros((m,L))
    for j in range(m): # m * L * d
        for l in range(L):
            q_projs[j,l] = np.dot(uvecs[j,l], q)
            sorted_trees[j,l] = trees[j,l].sort_tree(q_projs[j,l], n)

    return uvecs, trees, sorted_trees, q_projs

def euclidean_dist(p, q):
    '''
    Time Complexity: O(d)
    '''
    return np.dot(p-q,p-q)**0.5

def QUERY(q, uvecs, trees, sorted_trees, q_projs, D, k0, k1, k):
    '''
    Time Complexity:
    heapq.push() and heapq.pop(): O(log(m))
    k1 refers how many points popped from a heap
    k0 refers how many candidates a composite index can have
    
    in fact:
    
    '''
    n = D.shape[0]
    m = uvecs.shape[0]
    L = uvecs.shape[1]
    Cls = np.zeros((L, n))
    Sls = np.zeros(L, dtype=object)
    for l in range(L): # L
        Sls[l] = Set()
    Pls = np.zeros(L, dtype=object)  
    for l in range(L): # L
        Pls[l] = []


    for l in range(L): # L * m * (log(n) + log(m))
        for j in range(m):
            #p_proj, pt = trees[j,l].query(q_projs[j,l], 0)
            p_proj, pt = query(sorted_trees[j,l], 0)
            priority = abs(p_proj - q_projs[j,l])
            heappush(Pls[l], (priority, pt, j, l, 0))
    
    count = 0
    for i in range(k1): # k1 * L * k0 * ((m+3)log(m) + log(n))
        for l in range(L):
            if len(Sls[l]) < k0:
                cp_Pl = Pls[l][:] # m
                while(cp_Pl[0][4] == n-1): # m * log(m)
                    heappop(cp_Pl)
                popped_pt = None
                if len(cp_Pl) == 0:
                    popped_pt = heappop(Pls[l])[1] # log(m)
                else:
                    popped_pt = heappop(Pls[l])[1] # log(m)
                    point, origin_j, origin_l, ith = cp_Pl[0][1:5]
                    #p_proj, pt = trees[origin_j, origin_l].query(q_projs[origin_j, origin_l], ith+1) # log(n)
                    p_proj, pt = query(sorted_trees[origin_j, origin_l], ith+1)
                    priority = abs(p_proj - q_projs[origin_j, origin_l])
                    heappush(Pls[l], (priority, pt, origin_j, origin_l, ith+1)) # log(m)
                Cls[l, popped_pt] += 1
                if Cls[l, popped_pt] == 70 * m / 100:
                #if Cls[l, popped_pt] == m:
                    Sls[l].add(popped_pt)
                count += 1

    
    print "The number of points visisted:",count
    for l in range(L):
        print "The number of points in "+ str(l) +"th candidate set:",len(Sls[l])
    candidates = Set()
    for l in range(L):
        candidates = candidates.union(Sls[l])
    print "The number of candidates:",len(candidates)   
    candi_pt = []
    candi_eudist = []
    for pt in candidates:
        candi_pt.append(pt)
        candi_eudist.append(euclidean_dist(D[pt], q))
    
    k_neighbours = []
    sorted_eudist = np.argsort(candi_eudist)
    i = 0
    while i < k:
        k_neighbours.append(candi_pt[sorted_eudist[i]])
        i += 1
    
    return np.array(k_neighbours)

def QUERY2(q, uvecs, trees, D, k):
    n = D.shape[0]
    m = uvecs.shape[0]
    L = uvecs.shape[1]
    Cls = np.zeros((L, n))
    Sls = np.zeros(L, dtype=object)
    for l in range(L): # L
        Sls[l] = Set()
    q_projs = np.zeros((m,L))
    for j in range(m): # m * L * d
        for l in range(L):
            q_projs[j,l] = np.dot(uvecs[j,l], q) ## slow, need to remove loops

    count = 0
    for i in range(n): 
        for l in range(L):
            for j in range(m):
                p_proj, pt = trees[j,l].query(q_projs[j,l], i)
                Cls[l, pt] += 1
            if Cls[l,pt] == 70 * m / 100: ## hack
                Sls[l].add(pt)
        count += 1
        print count
        ## FIXME: need stopping condition!!!
    
    print "The number of points visisted:",count
    for l in range(L):
        print "The number of points in "+ str(l) +"th candidate set:",len(Sls[l])

    candidates = Set()
    for l in range(L):
        candidates = candidates.union(Sls[l])

    candi_pt = []
    candi_eudist = []
    for pt in candidates:
        candi_pt.append(pt)
        candi_eudist.append(euclidean_dist(D[pt], q))
    
    k_neighbours = []
    sorted_eudist = np.argsort(candi_eudist)
    i = 0
    while i < k:
        k_neighbours.append(candi_pt[sorted_eudist[i]])
        i += 1
    
    return np.array(k_neighbours)

def bruteforce(q,dataset,k):
    '''
    Time complexity: O(dn + nlog(n))
    '''
    dataset_eu_dist = []
    for i in range(len(dataset)):
        dataset_eu_dist.append(euclidean_dist(q,dataset[i]))
    return np.argsort(dataset_eu_dist)[:k]

def accuracy(pre, gold):
    count = 0
    for pt in pre:
        if pt in gold:
            count += 1
    return float(count) / len(gold)

if __name__ == "__main__":
    n = 1000
    d = 200
    d_prime = 20
    m = 20
    L = 20
    D, labels_true = make_blobs(n_samples=n, n_features=d,centers=10, cluster_std=5,random_state=0)    
    #mnist = fetch_mldata('MNIST original')
    #D = mnist.data
    #print len(D[1])
    
    k = 10
    pt = 50
    q = D[pt]
    k0 = int(k * max(np.log(n/k), (n/k)**(1-float(m)/d_prime)))
    k1 = int(m * k * max(np.log(n/k), (n/k)**(1-float(1)/d_prime)))

    print "*************** To find top",k,"nearest points from",n,"points ***************"
    print "Configuration:"
    print "Ambient dimensionality \t\t\t\t\t\td =",d
    print "Intrinsic dimensionality \t\t\t\t\td_prime =",d_prime
    print "The number of simple indices \t\t\t\t\tm =",m
    print "The number of composite indices \t\t\t\tL =",L
    print "The number of points to retrieve for one composite index \tk0 =",k0
    print "The number of points to visit for one composite index \t\tk1 =",k1
    print "the query point \t\t\t\t\t\tq = ",pt
    print "******************************************************************************\n"

    print "******************************************************************************"
    print "Construction\n"
    t_start = datetime.now()
    uvecs, trees, sorted_trees, q_projs= CONSTRUCT(D, m, L, q)
    t_end = datetime.now()
    print "Construction Time: ",t_end-t_start
    print "Done!"
    print "******************************************************************************\n"

    print "******************************************************************************"
    print "Algorithm 1 - Brute Force\n"
    t_start = datetime.now()
    bf_points = bruteforce(q, D, k)
    t_end = datetime.now()
    print "Output:",list(bf_points)
    print "Time:",t_end - t_start
    print "******************************************************************************\n"

    print "******************************************************************************"
    print "Algorithm 2 - Ball Tree\n"
    tree = BallTree(D, leaf_size=2)  
    t_start = datetime.now()            
    dist, neighbors = tree.query([q], k=10)
    t_end = datetime.now()
    print "Output:",list(neighbors[0])
    print "Time:",t_end - t_start
    print "Accuracy:",accuracy(list(neighbors[0]), bf_points)
    print "******************************************************************************\n"

    print "******************************************************************************"
    print "Algorithm 3 - KD Tree\n"
    tree = KDTree(D, leaf_size=2)
    t_start = datetime.now()            
    dist, neighbors = tree.query([q], k=10)
    t_end = datetime.now()
    print "Output:\n",list(neighbors[0])
    print "Time:",t_end - t_start
    print "Accuracy:",accuracy(list(neighbors[0]), bf_points)
    print "******************************************************************************\n"
    
    print "******************************************************************************"
    print "Algorithm 4 - PDCI (Lower bound)\n"
    l_k0 = 15 * k0 / 100
    l_k1 = 55 * k1 / 100
    print "k0=",l_k0
    print "k1=",l_k1
    t_start = datetime.now()            
    pdci_points = QUERY(q, uvecs, trees, sorted_trees, q_projs, D, l_k0, l_k1, k)
    t_end = datetime.now()
    print "Output:",list(pdci_points)
    print "Time:",t_end - t_start
    print "Accuracy:",accuracy(pdci_points, bf_points)
    print "******************************************************************************\n"

    print "******************************************************************************"
    print "Algorithm 4 - PDCI (Middle)\n"
    m_k0 = 55 * k0 / 100
    m_k1 = 80 * k1 / 100
    print "k0=",m_k0
    print "k1=",m_k1
    t_start = datetime.now()            
    pdci_points = QUERY(q, uvecs, trees, sorted_trees, q_projs, D, m_k0, m_k1, k)
    t_end = datetime.now()
    print "Output:\n",list(pdci_points)
    print "Time:",t_end - t_start
    print "Accuracy:",accuracy(pdci_points, bf_points)
    print "******************************************************************************\n"
    
    print "******************************************************************************"
    print "Algorithm 4 - PDCI (Upper bound)\n"
    print "k0=",k0
    print "k1=",k1
    t_start = datetime.now()
    pdci_points = QUERY(q, uvecs, trees, sorted_trees, q_projs, D, k0, k1, k)
    t_end = datetime.now()
    print "Output:\n",list(pdci_points)
    print "Time:",t_end - t_start
    print "Accuracy:",accuracy(pdci_points, bf_points)
    print "******************************************************************************\n"
    
    print "******************************************************************************"
    print "Algorithm 5 - DCI\n"
    t_start = datetime.now()            
    dci_points = QUERY2(q, uvecs, trees, D, k)
    t_end = datetime.now()
    print "Output:",list(dci_points)
    print "Time:",t_end - t_start
    print "Accuracy:",accuracy(dci_points, bf_points)
    print "******************************************************************************"
    
    