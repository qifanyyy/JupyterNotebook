#!/usr/bin/env python3
# AUTHOR:       April Castaneda
# DATE:         10.21.2019
# DESCRIPTION:  Implements Activity Selection Last-to-Start Algorithm using 
#               insert sort. The program reads input from a file named 
#               "act.txt". The file contains a list of activity sets with
#               number of activities in the set in the first line followed by
#               lines containing the activity number, start time, and finish
#               time. The results including the number of activities selected
#               and their order are outputted to the terminal.

# First, open file to read.
read_file = open('act.txt', 'r')

# Read each line in file and store in lines.
lines = []
for line in read_file:
    lines.append(line)
read_file.close()

# Start empty list for sets
Sets = {}

# Start a counter on how many sets there are and store starting index for activities
if int(lines[0]) > 0:
    num_sets = 1
    lines_ind = 0
    acts_ind = 0
else:   # Error message if there is nothing in input file.
    raise ValueError("No lines in file.")

# Start empty list storing how many acts are in each set.
num_acts = []

# Go through lines and store activities 
while lines_ind < len(lines):

    # Empty dictionary for each Set
    Sets[str(num_sets)] = {}                      

    # Get the number of activities and store in num_acts list    
    num_acts.append(int(lines[lines_ind]))
    lines_ind += 1                          # increment lines index

    # Start empty lists for start times and finish times
    start = [0] * num_acts[acts_ind]
    finish = [0] * num_acts[acts_ind]

    # Go through lines and store start and finish lists    
    for i in range(0, num_acts[acts_ind]):
        idx, start[idx-1], finish[idx-1] = [int(x) for x in lines[lines_ind].split()]
        lines_ind += 1

    # Store start and finish lists in Sets dictionary under appropriate #num_sets    
    Sets[str(num_sets)]['S'] = start
    Sets[str(num_sets)]['F'] = finish 

    # If not at end of list, increment acts_ind index and num_sets
    if lines_ind < len(lines):
        acts_ind += 1
        num_sets += 1

# Print test if input is in correctly
#for i in range(1, num_sets+1):
#    print("Set:", i)
#    print("S:", Sets[str(i)]['S'])
#    print("F:", Sets[str(i)]['F'])
#print("Num_sets:", num_sets)
#print("Lines_ind:", lines_ind)

# Function
def sort_two(a_list, b_list):
    """
    Implements insert-sort algorithm to sort a_list. Then uses the way a_list
    was sorted to sort b_list.
    """

    # Create empty lists indices list and make copies of a_list and b_list
    indices = [-1] * len(a_list) 
    copy_list_a = list(a_list)
    copy_list_b = list(b_list)

    # Start Insert-sort algorithm
    # Go through list starting with 2nd value
    for j in range(1,len(a_list)): 
        
        # Store value as key.
        key = a_list[j]

        # Store index to one less than key.             
        i = j - 1

        # Sort numbers more than key.
        while i >= 0 and a_list[i] < key:
            a_list[i+1] = a_list[i]
            i = i - 1
        
        # Put key number to number's position that it replaced.
        a_list[i+1] = key
    # End Insert-sort algorithm

    # Turn sorted a_list into dictionary with values as key, and indices as values
    sorted_dict = {v: k for v, k in enumerate(a_list)}

    # Create list of indices based on where the numbers were originally
    for i in range(0, len(a_list)):
        sort_val = copy_list_a[i]
        idx = [key for (key, value) in sorted_dict.items() if value == sort_val]
        indices[i] = idx[0]
        del sorted_dict[idx[0]]

    #print(indices)    

    # Sort b_list per how a_list was sorted using indices list
    for i in range(0, len(indices)):
        idx = indices[i]
        value = copy_list_b[i]
        b_list[idx] = value

    # Change indices to dictionary with its values as keys and indices as values.
    indices = {k: v for v, k in enumerate(indices)}
    return indices

# Function
def insert_sort(a_list, num_ints):
    """
    Implements insert-sort algorithm.
    """

    # Go through list starting with 2nd value
    for j in range(1,num_ints): 
        
        # Store value as key.
        key = a_list[j]

        # Store index to one less than key.             
        i = j - 1

        # Sort numbers less than key.
        while i >= 0 and a_list[i] > key:
            a_list[i+1] = a_list[i]
            i = i - 1
        
        # Put key number to number's position that it replaced.
        a_list[i+1] = key

# Function 
def activity_selector(sets_dict, set_num):
    """
    Function that implements greedy algorithm for activity selection. It
    selects the last activity to start that is complatible with all 
    previously selected activities.
    Input:  Dictionary of sets
            Number of sets in dictionary
    Output: List of selected activities
    """

    Out_sets = {}                       # Empty dictionary sets to be outputted.
    
    Out_sets['num_sets'] = set_num            # Store how many sets there are.

    # Go through all sets to store their data
    for a in range(1, num_sets+1):        

        Out_sets[str(a)] = {}            # Empty dictionary for each set #a

        S = sets_dict[str(a)]['S']      # Store S = list of start times
        F = sets_dict[str(a)]['F']      # Store F = list of finish times

        A = []                          # Empty list for activities selected

        acts = sort_two(S, F)           # Get dictionary of indices from sorted S and F

        #print(S)
        #print(F)

        # Activity Selection Algorithm
        A.append(acts[0]+1)             # Add first act to Activity list
        n = len(S)                      # Set n value to length of S
        k = 0                           # Set index k

        for m in range(1, n):
            if F[m] <= S[k]:            # If finish time is less than start time of previous act
                A.append(acts[m]+1)     # Add activity to list A
                k = m                   # Update k index
        # End Activity Selection Algorithm

        insert_sort(A, len(A))          # Sort the picked activities A

        Out_sets[str(a)]['A'] = A       # Add A to Out_sets dictionary
    
    return Out_sets

# Store the resulting Sets from Activity Selector
Sets = activity_selector(Sets, num_sets)

# Print sets
print("\n")
for i in range(1, Sets['num_sets']+1):
    print("Set", i)
    act_list = Sets[str(i)]['A']
    print("Number of activities selected = " + str(len(act_list)))
    act_string = " ".join(map(str, act_list))
    print("Activities: " + act_string)
    print("\n")