from Linkedlist import Linkedlist
from random import randrange
Linked_list = Linkedlist()
def Selection_Sort_Array(arr):
    for i in range(0, len(arr) - 1):
        mn = arr[0]
        pos = 0
        for j in range(0, len(arr) - i ):
            if (arr[j] > mn):
                mn = arr[j]
                pos = j
        arr[pos], arr[len(arr) - i - 1] = arr[len(arr) - i - 1], arr[pos]
    return arr
def selectionsort_linked(list):
      I= list.head
      while I != None:
        J = I.getNext()
        min = I
        while J != None:
            if J.getData() > min.getData():
                min = J
            J = J.getNext()
        TEMP = min.getData()
        min.setData(I.getData())
        I.setData(TEMP)
        I = I.getNext()
def Selection_Sort_Linked_List(linked_list):
    flag = True
    cur = linked_list.head
    precur = None
    while flag:
        min_node = cur
        min_prev = None
        nxt = min_node.getNext()
        prev = cur
        flag = False
        while nxt != None:
            if nxt.getData() < min_node.getData():
                min_prev = prev
                min_node = nxt
                flag = True
            if nxt.getNext() != None and nxt.getData() > nxt.getNext().getData():
                flag = True
            prev = nxt
            nxt = nxt.getNext()
        cur_nxt = cur.getNext()
        min_nxt = min_node.getNext()
        if (precur == None) and cur.getNext() == min_node:
            linked_list.head = min_node
            min_node.setNext(cur)
            cur.setNext(min_nxt)
            precur = linked_list.head
            cur = min_node
        if (precur == None) and cur != min_node:
            linked_list.head = min_node
            linked_list.head.setNext(cur_nxt)
            min_prev.setNext(cur)
            cur.setNext(min_nxt)
            precur = linked_list.head
            cur = min_node
        elif cur.getNext() == min_node:
            precur.setNext(min_node)
            min_node.setNext(cur)
            cur.setNext(min_nxt)
            cur = min_node
        elif cur != min_node:
            precur.setNext(min_node)
            min_node.setNext(cur_nxt)
            min_prev.setNext(cur)
            cur.setNext(min_nxt)
            cur = min_node
        precur = cur
        cur = cur.getNext()





"""Linked_list = Linkedlist()

Linked_list.add(2)
Linked_list.add(4)
Linked_list.add(1)
Linked_list.add(5)
Linked_list.add(3)
Selection_Sort_Linked_List(Linked_list)
current = Linked_list.head
while (current != None):
    print(current.getData())
    current = current.getNext()"""


"""Selection_Sort_Linked_List(Linked_list)"""


