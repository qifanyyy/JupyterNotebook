#LAB 12
#Due Date: 11/22/2019, 11:59PM
########################################
#                                      
# Name:
# Collaboration Statement:             
#
########################################

class MinHeap:
    '''
        >>> h = MinHeap()
        >>> h.insert(10)
        >>> h.insert(5)
        >>> h
        [5, 10]
        >>> h.insert(14)
        >>> h.heap
        [5, 10, 14]
        >>> h.insert(9)
        >>> h
        [5, 9, 14, 10]
        >>> h.insert(2)
        >>> h
        [2, 5, 14, 10, 9]
        >>> h.insert(11)
        >>> h
        [2, 5, 11, 10, 9, 14]
        >>> h.insert(14)
        >>> h
        [2, 5, 11, 10, 9, 14, 14]
        >>> h.insert(20)
        >>> h
        [2, 5, 11, 10, 9, 14, 14, 20]
        >>> h.insert(20)
        >>> h
        [2, 5, 11, 10, 9, 14, 14, 20, 20]
        >>> h.parent(2)
        2
        >>> h.leftChild(1)
        5
        >>> h.rightChild(1)
        11
        >>> h.parent(8)
        10
        >>> h.leftChild(6)
        >>> h.rightChild(9)
        >>> h.deleteMin
        2
        >>> h.heap
        [5, 9, 11, 10, 20, 14, 14, 20]
        >>> h.deleteMin
        5
        >>> h
        [9, 10, 11, 20, 20, 14, 14]
    '''

    # -- YOU ARE NOT ALLOWED TO MODIFY THE CONSTRUCTOR!
    def __init__(self):
        self.heap=[]        

    def __str__(self):
    	return f'{self.heap}'

    __repr__=__str__

    def parent(self,index):
        # -- YOUR CODE STARTS HERE
        if index < 1 or index > len(self) :
            return None

        parent_index, parent_value = self.__get_parent(index - 1)
        return parent_value


    def leftChild(self,index):
        # -- YOUR CODE STARTS HERE
        if index < 1 or index > len(self) :
            return None

        index_value = self.heap[index - 1]
        left_child_index, left_child_value = self.__get_left_child(index - 1, index_value)
        return left_child_value


    def rightChild(self,index):
        # -- YOUR CODE STARTS HERE        
        if index < 1 or index > len(self) :
            return None

        index_value = self.heap[index - 1]
        right_child_index, right_child_value = self.__get_right_child(index - 1, index_value)
        return right_child_value

    def __len__(self):
        # -- YOUR CODE STARTS HERE
        return self.__last_index + 1
       

    def insert(self,x):
        # -- YOUR CODE STARTS HERE
        self.push(x)

            
    @property
    def deleteMin(self):
        if len(self)==0:
            return None        
        elif len(self)==1:
            out=self.heap[0]
            self.heap=[]
            return out

        # -- YOUR CODE STARTS HERE
        return self.pop()

    __last_index = -1
    def push(self, value):
        self.__last_index += 1
        if self.__last_index < len(self.heap):
            self.heap[self.__last_index] = value
        else:
            self.heap.append(value)
        self.__siftup(self.__last_index)

    def pop(self):
        if self.__last_index == -1:
            raise IndexError('pop from empty heap')

        min_value = self.heap[0]

        self.heap[0] = self.heap[self.__last_index]
        self.__last_index -= 1
        self.__siftdown(0)

        return min_value

    def __siftup(self, index):
        while index > 0:
            parent_index, parent_value = self.__get_parent(index)

            if parent_value <= self.heap[index]:
                break

            self.heap[parent_index], self.heap[index] =\
                self.heap[index], self.heap[parent_index]

            index = parent_index

    def __siftdown(self, index):
        while True:
            index_value = self.heap[index]

            left_child_index, left_child_value = self.__get_left_child(index, index_value)
            right_child_index, right_child_value = self.__get_right_child(index, index_value)

            if index_value <= left_child_value and index_value <= right_child_value:
                break

            if left_child_value < right_child_value:
                new_index = left_child_index
            else:
                new_index = right_child_index

            self.heap[new_index], self.heap[index] =\
                self.heap[index], self.heap[new_index]

            index = new_index

    def __get_parent(self, index):
        if index == 0:
            return None, None

        parent_index = (index - 1) // 2

        return parent_index, self.heap[parent_index]

    def __get_left_child(self, index, default_value):
        left_child_index = 2 * index + 1

        if left_child_index > self.__last_index:
            return None, default_value

        return left_child_index, self.heap[left_child_index]

    def __get_right_child(self, index, default_value):
        right_child_index = 2 * index + 2

        if right_child_index > self.__last_index:
            return None, default_value

        return right_child_index, self.heap[right_child_index]    



def heapSort(numList):
    '''
       >>> heapSort([9,7,4,1,2,4,8,7,0,-1])
       [-1, 0, 1, 2, 4, 4, 7, 7, 8, 9]
    '''
    sort_heap = MinHeap()
    # -- YOUR CODE STARTS HERE

    # push number list to heap
    for i in range(len(numList)): 
        sort_heap.insert(numList[i])

    # pop list from heap
    sort_list = []
    while len(sort_heap) > 0 :
        val = sort_heap.pop()
        sort_list.append(val)

    return sort_list
        