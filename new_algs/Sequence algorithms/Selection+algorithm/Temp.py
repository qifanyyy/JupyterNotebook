from Linkedlist import *
from random import *
def Selection_Sort_Linked_List(linked_list):
    flag = True
    cur = linked_list.head.getNext()
    precur = linked_list.head
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
        if cur.getNext() == min_node:
            precur.setNext(min_node)
            min_node.setNext(cur)
            cur.setNext(min_nxt)
        elif cur != min_node:
            precur.setNext(min_node)
            min_node.setNext(cur_nxt)
            min_prev.setNext(cur)
            cur.setNext(min_nxt)
        precur = min_node
        cur = min_node.getNext()
"""linked_list = LinkedList()
for i in range(30):
    linked_list.add(randrange(0, 100000))
Selection_Sort_Linked_List(linked_list)
current = linked_list.head.getNext()
while current != None:
    print(current.getData())
    current = current.getNext()"""
