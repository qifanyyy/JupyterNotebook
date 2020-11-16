#ohamilton0079
#Binary search algorithm
#09/07/2020

def difference(num1, num2):
    #Return the difference between the two numbers, accounting for if one is larger than the other
    return num1 - num2 if num1 >= num2 else num2 - num1

def closest_index(leftPointer, rightPointer, targetItem, inputList):
    #Calculate the difference between the values at the pointer indexes and the target item
    leftDifference = difference(inputList[leftPointer], targetItem)
    rightDifference = difference(inputList[rightPointer], targetItem)

    #Return the pointer of the smallest value
    return leftPointer if leftDifference < rightDifference else rightPointer
    
def get_first_index(itemIndex, inputList):

    #Pointer for duplicate items
    duplicatePointer = itemIndex

    #Whilst the duplicate pointer points to the same item as the item index
    while inputList[duplicatePointer] == inputList[itemIndex]:
        #Decrement the duplicate pointer
        duplicatePointer -= 1

    #The smallest index where the item is found is the duplicate pointer + 1
    return duplicatePointer + 1

def binary_search(inputList, targetItem):
    
    #Set the pointers to the start and end indexes of the list
    leftPointer = 0
    rightPointer = len(inputList) - 1

    #While the left is less than or equal to the right pointer
    while leftPointer <= rightPointer:
        #Get the midpoint within the range of the pointers (cast to int)
        midPointer = (leftPointer + rightPointer) // 2
        
        #If the item at the mid point is less than the target item
        if inputList[midPointer] < targetItem:
            #Set the left pointer to the mid point + 1
            leftPointer = midPointer + 1

        #Otherwise, if the item at the mid point is more than the target item
        elif inputList[midPointer] > targetItem:
            #Set the right pointer to the mid point - 1
            rightPointer = midPointer - 1

        #Otherwise, the item has been found
        else:
            #Return the index where the item occurs first
            return get_first_index(midPointer, inputList)      

    #If the item doesn't exist in the list, return the index with a value closest to the target item
    return closest_index(leftPointer, rightPointer, targetItem, inputList)
