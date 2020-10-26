# Example: [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2]

def rotated_array_search(input_list, number):
    if number < 0:
        return -1

    start = 0
    end = len(input_list) - 1
    
    while start <= end:
        middle = start + (end - start) // 2
        
        if input_list[middle] == number:
            return middle
        
        if input_list[start] < input_list[middle]:
            if number >= input_list[start] and number < input_list[middle]:
                end = middle - 1
            else:
                start = middle + 1
        else:
            if number <= input_list[end] and number > input_list[middle]:
                start = middle + 1
            else:
                end = middle - 1
    return -1

def linear_search(input_list, number):
    for index, element in enumerate(input_list):
        if element == number:
            return index
    return -1

def test_function(test_case):
    input_list = test_case[0]
    number = test_case[1]
    if linear_search(input_list, number) == rotated_array_search(input_list, number):
        print("Pass")
    else:
        print("Fail")

test_function([[6, 7, 8, 9, 10, 1, 2, 3, 4], 6])    # index = 0 Pass
test_function([[6, 7, 8, 9, 10, 1, 2, 3, 4], 1])    # index = 1 Pass
test_function([[6, 7, 8, 1, 2, 3, 4], 8])           # index = 2 Pass
test_function([[6, 7, 8, 1, 2, 3, 4], 1])           # index = 3 Pass
test_function([[6, 7, 8, 1, 2, 3, 4], 10])          # -1 Pass
test_function([[6, 7, 8, 1, 2, 3, 4], -7])          # -1 Pass
test_function([[1], 1])                             # index 0 Pass
test_function([[1], 0])                             # -1 Pass
test_function([[], 0])                              # -1 Pass

# NOTE: algorithm does not work with negative numbers