#ohamilton0079
#Linear Search Algorithm
#08/07/2020

def linear_search(inputList, targetItem):
    found = False
    for index, item in enumerate(inputList, 1):
        #If the item has been found
        if item == targetItem:
            #Output the position where it was found
            #print("The item", item, "was found at position", index, "in the list")
            #Update the found flag
            found = True
            break

    #If the found flag still hasn't been set to true
    #if not found:
        #Output a message saying the item isn't in the list
        #print("The item", targetItem, "couldn't be found in the list provided")


#Function for working with sorted lists
def linear_search_sorted(sortedList, targetItem):
    #A flag to monitor whether the existence of an element of the list has been ascertained
    finished = False
    for index, item in enumerate(sortedList, 1):
        
        #If the item is greater than the target item, it doesn't exist
        if item > targetItem:
            #Output a message saying the item isn't in the list
            #print("The item", targetItem, "couldn't be found in the list provided")
            #Update the finished flag
            finished = True
            break
        
        #If the item has been found
        if item == targetItem:
            #Output the position where it was found
            #print("The item", item, "was found at position", index, "in the list")
            #Update the finished flag
            finished = True
            break
        
    #If the finished flag still hasn't been set to true
    #if not finished:
        #Output a message saying the item isn't in the list
        #print("The item", targetItem, "couldn't be found in the list provided")
