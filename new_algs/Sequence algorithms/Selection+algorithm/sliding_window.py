"""
@author: David Lei
@since: 19/10/2017

"""
import heapq

# Note: Not entirely convinced this is O(n log k) but I can see how you can get there.

class Heap:
    def __init__(self, max_heap=False):
        self.max = max_heap
        self.heap = []

    def add(self, i):
        if self.max:
            i *= -1
        heapq.heappush(self.heap, i)

    def pop(self):
        # Will remove item from the heap.
        value = heapq.heappop(self.heap)
        if self.max:
            value *= -1
        return value

    # def delete(self, index):
    # # Magic heapify.
    # self.heap[index] = self.heap[-1]  # Move root to index i.
    # self.heap.pop()  # pop() last element in array O(1).
    # if index < len(self.heap):  # Need to sift things.
    # # Magical internal heapify functions that does stuff in log n.
    #     heapq._siftup(self.heap, index)
    #     heapq._siftdown(self.heap, 0, index)

    def peak_max_value(self):
        return self.heap[0] if not self.max else self.heap[0] * -1 # Root has max value.

def sliding_window_brute_force(array, k):
    # O((n - k) * 2k) = O(nk - k^2) = O(nk).
    soln = []
    for i in range(len(array) - k + 1): # O(n - k)
        window = array[i: i + k] # O(k)
        max_val = max(window) # O(k)
        soln.append(max_val)
    return soln

def sliding_window(array, k):  # Faster by changing k to log k.
    # O(k * log k) + O(n - k * (2 log k)) = O(n log k + 2(k log k)) = O(n log k).
    soln = []
    heap = Heap(max_heap=True)
    value_to_index = {}  # Stores the index for each value, if values are duplicated will take the one encountered last.
    for i in range(0, k): # O(k)
        heap.add(array[i]) # O(log k)
        value_to_index[array[i]] = i
    soln.append(heap.peak_max_value())
    j = 1
    for i in range(k, len(array)): # O(n - k)
        print("index: %s, value: %s" % (i, array[i]) )
        print(heap.heap)
        value_to_index[array[i]] = i
        heap.add(array[i])
        heap_max = heap.peak_max_value() # O(1)
        occurrence_index = value_to_index[heap_max] # O(1)
        if occurrence_index >= j and occurrence_index <= i:
            soln.append(heap_max) # O(1)
        else:
            heap.pop() # O(log k).
            print("popped")
            while True:
                heap_max = heap.peak_max_value() # O(1)
                occurrence_index = value_to_index[heap_max] # O(1)
                if occurrence_index >= j and occurrence_index <= i:
                    soln.append(heap_max) # O(1)
                    break
                else:
                    heap.pop()
                    print("popped")
        j += 1
        # Reasoning for log k heap pop().
        # If extra elements are so small they don't effect heap structure much then they are at leaves and not much happens to them.
        # if they are maximal they will be popped off.
    return soln

array = [2, 3, 4, 2, 6, 2, 5, 1]
k = 3
print("\nBrute force solution")
print(sliding_window_brute_force(array, k))
print("\nOptimized solution")
print(sliding_window(array, k))

# A brilliant O(n) solution.
# https://leetcode.com/problems/sliding-window-maximum/discuss/

def sliding_window_max(array, k):
    soln = []

    left_max_so_far = [x for x in array]
    left_max = left_max_so_far[0]
    for i in range(1, len(left_max_so_far)):
        if i % k == 0:  # New window
            left_max = left_max_so_far[i]
            continue
        left_max = max(left_max, left_max_so_far[i])
        left_max_so_far[i] = left_max

    right_max_so_far = [x for x in array]
    right_max = right_max_so_far[-1]
    for i in range(len(right_max_so_far) - 2, -1, -1):
        if i % k == 0:
            right_max = right_max_so_far[i]
            continue
        right_max = max(right_max, right_max_so_far[i])
        right_max_so_far[i] = right_max
    # print(left_max_so_far)
    # print(right_max_so_far)

    for i in range(0, len(array) - k + 1):
        value = max(left_max_so_far[i + k - 1], right_max_so_far[i])
        soln.append(value)
    return soln

print("\nLeet code magic")
print(sliding_window_max(array, k))