"""
@author: David Lei
@since: 21/08/2016
@modified:

How it works: using a minheap (priority queue) we can just repeatedly graph the min element and when we are done
                it will be in sorted order!

                1. Put everything in a heap
                    - O(n log n) in standard heapify
                    - O(n) when done in a smart way
                2. While element in heap
                    3. get it and put in output
                        4. maintain heap structure

Invariants: min always at root

Time complexity: O(n log n)
- best O(n log n) = worst = avg
    1. O(n) or O(n log n) heapify
    2. take out n elements and each time need to maintain heap property O(n log n)
         so either O(n + n log n) or O(n log n + n log n) = O(n log n)

Space complexity: best O(1) inplace in array, just swap around pointers where the sorted portion starts
- O(1) if array implementation can do it inplace of the array or use an output array O(n) of same len - 1
- O(n) if use out array of same len to return
explanation http://stackoverflow.com/questions/22233532/why-does-heap-sort-have-a-space-complexity-of-o1

Stability: yes as only swap if > and not >=
"""

def heapify_standard(arr):
    """Uses standard implementation on a min heap as a priority queue
    need to insert n items from array, each insertion needs to maintain heap property
        - inserted at end
        - call rise method (filter up)

    If we start with an initially empty heap, n successive calls to the add operation will run in O(n log n) time in the worst case
    """
    minPQ = minHeap()
    # create heap is O(n log n)
    for element in arr:             # O(n)
        minPQ.add(element)          # inserting into a heap is O(log n)
    return minPQ

# TODO: Bug in get_min() or percolate_down().

def get_min(array, n):
    """To get min we need to first swap the root with the last item so we can remove the min at the root
    then we need ot filter down the new root to maintain heap property O(log n)

    root is at index 1
    n is the size of th heap
    index n is the last element in the heap"""
    array[1], array[n] = array[n], array[1]
    percolate_down(array, 1, n-1)
    return array[n]

def percolate_down(array, i, n):
    """example min heap
            2
        4       5
     5   7   10   8

    in array: |7|2|4|5|7|6|10|8|
    idx        0 1 2 3 4 5 6 7
    store len in index 0

    array[i] is the new value

    note: this is a min heap, for max heap change < to >
    """
    while (True):
        if 2*i > n:     # out side of array
            break       # we are done
        child_idx = 2*i     # left child index
        if child_idx < n and array[child_idx+1] < array[child_idx]:     # right child < left child
            child_idx += 1                                              # we want to store the smaller child
        # as we are implementing a min heap, the child should be > than parent
        if array[child_idx] < array[i]:                                 # swap if child < parent
            array[i], array[child_idx] = array[child_idx], array[i]
            i = child_idx
        else:
            break

def heapify_smart(array, n):
    """Uses an array and manipulate it to enforce heap structure

    However, if all n key-value pairs to be stored in the heap are given in advance,
    such as during the first phase of the heap- sort algorithm, there is an alternative
    bottom-up construction method that runs in O(n) time.

    using an array
    where node is the index of the current "node"
    Child:
        - left = 2 * node
        - right = 2 * node + 1
    Parent: floor(node/2)
    Root: 1, we leave index 0 as blank
    Next free spot: len + 1

    Refer to O(n) heapify notes
    """
    #n = array[0]                # size of the heap
    i = len(array)//2           # only need to look a non leaves
    """
    there at len(array)//2 leaves always in a binary heap
    leaves are already heaps, don't worry about them, look at only parents and those above

                2
             4      5
           7   6

    in array: |5|2|4|5|7|6|
    idx        0 1 2 3 4 5

    5 is a leaf, so are 6 and 7 so we just need to percolaate down 4 and 2
    start at i = len(heap) = arr[0] // 2 = index 2
    """
    while i > 0:                # i = 1 will be root, we are done after that
        percolate_down(array, i, n)
        i -= 1                  # only looking at parents and those above

def heap_sort_better(arr):      # uses O(n) heapify
    n = arr[0]                  # size of heap

    heapify_smart(arr, n)
    output = []
    while n > 0:                # still elements in heap
        min_val = get_min(arr, n)
        n -= 1                  # we have removed something
        arr[0] = n              # update heap size

        output.append(min_val)
    return output

def heap_sort_worse(arr):       # uses O(n log n) heapify
    minPQ = minHeap()
    for e in arr:               # build heap
        minPQ.add(e)
    output = []
    while not minPQ.is_empty():
        min_value = minPQ.get_min()
        output.append(min_value)
    return output

# supporting data structures

class minHeap:
    """
    Uses array implementation to create a min Heap ADT which acts as a priority queue
    Heap order: each  child <= parent
    Heap: Complete --> each level full, bottom L-R
    Heap: Heap-ordered, child <= parent, siblings dont matter
    root: min
    """
    def __init__(self):
        self.count = 0
        self.array = [None]

    def is_empty(self):
        return self.count == 0

    def __len__(self):
        return self.count


    def swap(self, a, b):
        self.array[a],self.array[b] = self.array[b], self.array[a]

    def add(self, item):
        """Add item to the end of the array, then need to raise to the correct position
        due to heap property which has ~ log n levels, only around ~ log n raises needed"""

        if self.count + 1 < len(self.array):
            self.array[self.count+1] = item
        else:
            self.array.append(item)
        self.count += 1
        self.rise(self.count)

    def rise(self, k):
        '''
        rise item at index k to correct position
        note: parent of k at k//2
        @precondition: 1 <= k <= self.count
        @return:
        '''
        while k > 1 and self.array[k]< self.array[k//2]:
            self.swap(k, k//2)
            k = k//2

    def get_min(self):
        '''
        # swap items at root and min
        #return self.array[1]
        '''
        try:
            self.swap(1, self.count)
            self.minItem = self.array[self.count]
            self.count -= 1 # delete item
            self.array.pop()
            self.sink(1)
            return self.minItem
        except IndexError:
            print("Nothing in the heap! ")

    def sink(self, k):
        """
        sink item k to correct position
        """
        while 2*k <= self.count:
            child = self.smallest_child(k)
            if self.array[k] <= self.array[child]:
                break
            self.swap(child, k)
            k = child

    def smallest_child(self,k):
        '''
        return the index of smallest child of K
        @precondition: 2*k <= self.count (has at least 1 child)
        '''
        if 2*k == self.count or self.array[2*k] < self.array[2*k+1]:
           return 2*k
        else:
            return 2*k+1

    def __str__(self):
        return str(self.array[1:])

    def return_array(self):
        self.mirrage_array = []
        for item in self.array[1:]:
            self.mirrage_array.append(str(item))
        #print(self.mirrage_array)
        return self.mirrage_array

    def delete(self, k):
        if k > 0 and k < self.count:
            self.swap(k, self.count)
            self.count-=1
            self.array.pop()
            self.sink(k)
        else:
            raise IndexError ("Invalid index")

def test_pq():
    heap = minHeap()
    heap.add(42)
    heap.add(23)
    heap.add(8)
    heap.add(-15)
    heap.add(16)
    heap.add(4)
    print(heap.get_min())
    print(str(heap))
    print(heap.get_min())
    print(str(heap))

if __name__ == '__main__':
    arr = [1,2,3,4,2]
    b = [10, 9, 8, 7, 4, 1, 0, -1, -40]
    bar = [8, 100 ,1,-3,11,1,0]
    car = [0,-3,1,-2]
    foo = [123,91,-19, 1,1,2,1,-54,1909,-51293,192,3,-4]
    dada = [-100301203, 1231, 90, 0, 123199, 123818, 14124, 12, 4, -41, -51, 9]
    boo = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 0, 0.131, 19]
    arrays = [arr, bar, car, foo, dada, boo, b]

    from algorithms_datastructures.heaps.min_heap import MinHeap

    heap = MinHeap()  # Another implementation for practice.
    for array in arrays:
        sorted_array = array[::]
        sorted_array.sort()


        heap.heapify(array)
        hs_2 = []
        for _ in range(heap.count):
            hs_2.append(heap.get_min())

        #hs_better = heap_sort_better(array)
        hs_worse = heap_sort_worse(array)

        if hs_2 == hs_worse == sorted_array:
            print("Results match: " + str(hs_2))
        else:
            print("Oh No! Results don\'t match")
            #print("heap sort better: " + str(hs_better))
            print("heap sort worse: " + str(hs_worse))
            print("heap sort 2: " + str(hs_2))