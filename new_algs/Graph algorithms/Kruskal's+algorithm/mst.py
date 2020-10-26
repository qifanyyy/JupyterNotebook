# create graph symmetric matrix

import numpy, random, time

class Graph:
    ''' Graph stored in an adjacency matrix '''
    def __init__(self, n):
        ''' Create the graph '''
        #start = time.time()
        self.adjmatrix = numpy.zeros((n,n))
        #self.createEdges()
        self.generate()
        #print "graph generated in %s" % (time.time() - start)

    def generate(self):
        size = len(self.adjmatrix)
        for i in xrange(0,size):
            for n in xrange(0,size):
                if i != n:
                    self.join(i,n)
        #print self.adjmatrix
        #self.testConnected()

    def createEdges(self):
        ''' populates the graph with edges by iterating over every
            vertex and connecting it to one previously iterated vertex '''
        for n in xrange(1, len(self.adjmatrix)):
            randvert = random.randint(0,n-1)
            self.join(n, randvert)


    def testConnected(self):
        connected = True
        for n in xrange(len(self.adjmatrix)):
            edges = numpy.nonzero(self.adjmatrix[n])
            if len(edges[0]) == 0:
                connected = False
                break;
        assert connected == True

    def join(self, a, b):
        weight = random.uniform(0,1)
        self.adjmatrix[a][b] = weight
        self.adjmatrix[b][a] = weight

    def adjacentWeights(self, n):
        indices = numpy.nonzero(self.adjmatrix[n])
        return (self.adjmatrix[n][indices], indices[0])

    def weight(self, a, b):
        return self.adjmatrix[a][b]

    def __len__(self):
        return len(self.adjmatrix)

class DisjointSet:
    ''' Disjoint set implementation for kruskal's '''
    rank = {}
    parents = {}
    rep_members = {}

    def __init__(self, graph):
        ''' initialises the DisjointSet '''
        for n in xrange(len(graph)):
            self.makeSet(n)

    def makeSet(self, x):
        ''' Creates an new set '''
        self.rank[x] = 0
        self.parents[x] = x
        self.rep_members[x] = set([x])

    def find(self, x):
        ''' Finds the representative of the specified vertex '''
        if self.parents[x] == x:
            return x
        else:
            return self.find(self.parents[x])

    def isCycle(self, a, b):
        return self.find(a) == self.find(b)

    def union(self, x, y):
        ''' Merges two sets '''
        xroot = self.find(x)
        yroot = self.find(y)
        if self.rank[xroot] > self.rank[yroot]:
            self.parents[yroot] = xroot
            self.rank[xroot] += 1
            self.rep_members[xroot] = self.rep_members[xroot] | self.rep_members[yroot]
            self.rep_members[yroot].pop()
        else:
            self.parents[xroot] = yroot
            self.rank[yroot] += 1
            self.rep_members[yroot] = self.rep_members[yroot] | self.rep_members[xroot]
            self.rep_members[xroot].pop()

class BinaryHeap:
    ''' Min sorted binary heap of tuples '''
    def __init__(self):
        self.heap = []
        self.size = 0

    def heapify(self, array):
        ''' Converts array into heap. Runs in O(n) '''
        floor = len(array) // 2
        self.size = len(array)
        self.heap = [0] + array[:]
        while floor > 0:
            self.bubbleDown(floor)
            floor -= 1

    def push(self, priority, value):
        ''' Adds to the heap. To add n elements via this method costs O(n log n) '''
        self.size += 1
        self.heap.append((priority, value))
        self.bubbleUp(self.size)

    def pop(self):
        ''' Pop smallest and reorder heap '''
        smallest = self.heap[1]
        self.heap[1] = self.heap[self.size]
        self.size -= 1
        self.heap.pop()
        self.bubbleDown(1)
        return (smallest[0],smallest[1])

    def min(self, n):
        ''' Gets the index of the smallest node of n '''
        if n * 2 + 1 > self.size:
            return n * 2
        else:
            if self.heap[n*2][0] < self.heap[n*2+1][0]:
                return n * 2
            else:
                return n * 2 + 1

    def bubbleUp(self, n):
        ''' Orders upwards '''
        floor = n // 2
        while floor > 0:
            if self.heap[n][0] < self.heap[floor][0]:
                tomove = self.heap[floor]
                self.heap[floor] = self.heap[n]
                self.heap[n] = tomove
            n = floor
            floor = n // 2

    def bubbleDown(self, n):
        ''' Orders downwards '''
        while n * 2 <= self.size:
            smallest = self.min(n)
            if self.heap[n][0] > self.heap[smallest][0]:
                tomove = self.heap[n]
                self.heap[n] = self.heap[smallest]
                self.heap[smallest] = tomove
            n = smallest

    def __len__(self):
        return len(self.heap)

def divideandconquer(array, start, end):
    ''' helper function for quicksort, does the actual sorting '''
    pivot = start
    for n in xrange(start+1, end+1):
        if array[n] <= array[start]:
            pivot += 1
            array[n], array[pivot] = array[pivot], array[n]
    array[pivot], array[start] = array[start], array[pivot]
    return pivot

def quicksort(array, start, end):
    ''' recursive in place quicksort '''
    if start >= end:
        return
    pivot = divideandconquer(array, start, end)
    quicksort(array, start, pivot-1)
    quicksort(array, pivot+1, end)

def prim(graph):
    weightsum = 0
    mstset = set()
    edgeheap = BinaryHeap() # min priority heap
    heapvals = {} # heap lowest calculated weights
    # add the vertices to the heap (weight, vertex id)
    heapvals[0] = 0
    start = time.time()
    toheapify = [(0,0)]
    for n in xrange(1, len(graph)): # O(n)
        toheapify.append((float('inf'),n))
        heapvals[n] = float('inf')
    edgeheap.heapify(toheapify)
    # build the mst
    while len(mstset) < len(graph):
        smallest = edgeheap.pop()
        if smallest[1] in mstset:
            continue
        if smallest[0] == float('inf'):
            break
        # add this to the mst
        mstset.add(smallest[1])
        # add to sum
        weightsum += smallest[0]
        # store the weights of the connected vertices
        weights, indices = graph.adjacentWeights(smallest[1])
        for i in xrange(len(weights)):
            # if the weight of an edge from this vertex is lower than our stored value
            if weights[i] < heapvals[indices[i]]:
                # replace it
                heapvals[indices[i]] = weights[i]
                edgeheap.push(weights[i],indices[i])
    #print "prim's done in %s)" % (time.time() - start)
    return weightsum

def kruskal(graph):
    mst = set() # the output mst
    edgeheap = BinaryHeap() # min ordered heap
    disjointset = DisjointSet(graph)
    heapededges = set()
    weightsum = 0.0

    toheap = []
    # step 1: sort the edges
    start = time.time()
    for n in xrange(len(graph)): # O(n)
        weights, indices = graph.adjacentWeights(n)
        for i in xrange(len(weights)):
            if (indices[i],n) not in heapededges:
                # store values in array rather than pushing one at a time
                toheap.append((weights[i],(n,indices[i])))
                heapededges.add((n,indices[i]))
    # heapify the values all at once O(n) instead of O(n log n)
    edgeheap.heapify(toheap)

    #print "step 1: %f" % (time.time() - start)
    # step 2: build the mst by joining the smallest non-cycle edges
    start = time.time()
    while len(mst) < len(graph)-1:
        weight,edges = edgeheap.pop()
        if not disjointset.isCycle(edges[0], edges[1]):
            mst.add((edges[0],edges[1]))
            weightsum += weight
            disjointset.union(edges[0], edges[1])
    #print "step 2: %f" % (time.time() - start)
    return weightsum

'''
a = [(4,40),(6,60),(9,90),(2,20),(3,30),(5,50)]
binheap = BinaryHeap()
binheap.heapify(a)
for n in xrange(binheap.size):
    print binheap.pop()
'''
def run(n):
    iterations = 20
    weightsum = 0
    # create the graphs ahead of time
    graphs = []
    for i in xrange(iterations):
        graphs.append(Graph(n))
    #print "%d Graphs of size: |V|=%d, |E|=%d generated in %f" % (iterations,n,n-1,(time.time() - start))
    start = time.time()
    # prim's
    for i in xrange(iterations):
        weightsum += prim(graphs[i])/iterations
        #print n
    ptime = time.time() - start
    #print "Prim's (average over %d iterations) is: %f. Running time: %s" % (iterations, weightsum, ptime)
    # kruskal's
    ksum = 0
    start = time.time()
    for i in xrange(iterations):
        ksum += kruskal(graphs[i])/iterations
    ktime = time.time() - start
    print "L(%d) (average over %d iterations ): Prim's: %f Running time: %f -- Kruskal's: %f Running time: %f" % (n, iterations,weightsum, ptime, ksum, ktime)
    #print "Time diff [Prim's - Kruskal's]: %f. Prim's time/n: %f, Kruskal's time/n %f" % ((ptime - ktime)*1000000, (ptime/n), (ktime/n))

torun = [10,100,500,1000]
for i in torun:
    run(i)
