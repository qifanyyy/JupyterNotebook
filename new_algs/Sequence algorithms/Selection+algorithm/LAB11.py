#LAB 11
#Due Date: 11/22/2019, 11:59PM
########################################
#                                      
# Name:
# Collaboration Statement:             
#
########################################


def selectionSort(numList):
    '''
        Takes a list and returns 2 values
        1st returned value: a dictionary with the state of the list after each complete pass of selection sort
        2nd returned value: the sorted list

        >>> selectionSort([9,3,5,4,1,78,67])
        ({1: [9, 3, 5, 4, 1, 78, 67], 2: [1, 3, 5, 4, 9, 78, 67], 3: [1, 3, 5, 4, 9, 78, 67], 4: [1, 3, 4, 5, 9, 78, 67], 5: [1, 3, 4, 5, 9, 78, 67], 6: [1, 3, 4, 5, 9, 78, 67], 7: [1, 3, 4, 5, 9, 67, 78]}, [1, 3, 4, 5, 9, 67, 78])
    '''
    # YOUR CODE STARTS HERE
    # Traverse through all array elements 
    state = {}
    for i in range(len(numList)): 
        # save a dictionary with the state of the list after each complete pass        
        state[i + 1] = numList.copy()
                
        # Find the minimum element in remaining  
        # unsorted array 
        min_idx = i 
        for j in range(i+1, len(numList)): 
            if numList[min_idx] > numList[j]: 
                min_idx = j 
        
        # Swap the found minimum element with  
        # the first element         
        numList[i], numList[min_idx] = numList[min_idx], numList[i] 
    
    # Driver code to test above 
    return state, numList