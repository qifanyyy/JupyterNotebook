"""
@author: David Lei
@since: 21/08/2016
@modified: 

"""
from Bubble_Sort import bubble_sort
from Insertion_Sort import insertion_sort
from Merge_Sort import merge_sort
from Selection_Sort import selection_sort
from Quick_Sort import quick_sort



arr = [1,2,3,4]
bar = [8, 100 ,1,-3,11,1,0]
car = [0,-3,1,-2]
foo = [123,91,-19, 1,1,2,1,-54,1909,-51293,192,3,-4]
goo = ['a','m','c','d', 'z', 'f','g', 'e']

tests = [arr, bar, car, foo, goo, foo+car+arr+bar]

for l in tests:
    bub = bubble_sort(l)
    ins = insertion_sort(l)
    mer = merge_sort(l)
    sel = selection_sort(l)
    qui = quick_sort(l)

    if bub == ins and bub == mer and bub == sel and bub == qui:
        print("\nAll same for: " + str(l) )
    else:
        print("\nError..Input: " + str(l) +
              "\nBubble sort: " + str(bub) +
              "\nInsertion sort: " + str(ins) +
              "\nMerge sort: " + str(mer) +
              "\nSelection sort: " + str(sel) +
              "\nQuick sort: " + str(qui))
    print("bub " + str(bub))