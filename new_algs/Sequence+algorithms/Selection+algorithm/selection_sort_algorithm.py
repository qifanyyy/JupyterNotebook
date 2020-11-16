import random
import time

def random_numbers_generator():
    l = []
    for i in range(999):
        l.append(random.randint(0,999))
    return l

random_list = random_numbers_generator()

unsorted_l = random_list

start = time.time()

def selection_sort(unsorted_list):
    for index in range(len(unsorted_l)):
        min_index = index
        for i in range(min_index+1, len(unsorted_l)):
            if unsorted_l[min_index] > unsorted_l[i]: # if the index element is higher than the next one, we will switch them around
                min_index = i
        cache = unsorted_l[index] # have to save the actual element to override it in the next step
        unsorted_l[index] = unsorted_l[min_index] # the actual element on position 0 will be overwrited with the element on index
        unsorted_l[min_index] = cache # after the switch on position 0 is the smallest number and on position index the element which was before on postion o

    return unsorted_l

print(selection_sort(unsorted_l))

end = time.time()
print(end - start) # checks the amount of time the algorithm needs to sort the list


    