# Merge Sort is a Divide and Conquer algorithm.
# It divides input array in two halves, calls itself for the two halves and then merges the two sorted halves.


def rearrange_digits(input_list):
    if len(input_list) <= 1:
        print(input_list)
        return input_list

    sorted_list = merge_sort(input_list)

    first_largest = 0
    second_largest = 0

    # build first number
    for number in range(len(sorted_list)):
        if(number % 2 == 0):
            first_largest = (first_largest * 10) + sorted_list[number]
        else:
            second_largest = (second_largest * 10) + sorted_list[number]
            
    print([first_largest, second_largest])
    return [first_largest, second_largest]

# implements merge sort to sort array
# 'Divide and Conquer Algorithm': O(n log n)
def merge_sort(input_list):
    if len(input_list) <= 1:
        return input_list

    middle = len(input_list) // 2
    left = merge_sort(input_list[:middle])
    right = merge_sort(input_list[middle:])

    return merge(left, right)


def merge(left, right):
    result = []
    left_index = 0
    right_index = 0

    # iterate and compare left to right
    while left_index < len(left) and right_index < len(right):
        if left[left_index] > right[right_index]:
            # print('left',left[left_index])
            result.append(left[left_index])
            left_index += 1
        else:
            # print('right',right[right_index])
            result.append(right[right_index])
            right_index += 1
    
    # add remaining items from left side
    while left_index < len(left):
        result.append(left[left_index])
        left_index += 1

    # add remaining items form right side
    while right_index < len(right):
        result.append(right[right_index])
        right_index += 1

    # return sorted array
    return result

def test_function(test_case):
    output = rearrange_digits(test_case[0])
    solution = test_case[1]
    if sum(output) == sum(solution):
        print("Pass")
    else:
        print("Fail")



# TEST

print('expected: [542, 31] or [531, 42]')
test_function([[1, 2, 3, 4, 5], [542, 31]])
print('-----')
print('expected: [964, 852]')
test_function([[4, 6, 2, 5, 9, 8], [964, 852]])
print('-----')
print('expected: [940, 720]')
test_function([[4, 0, 2, 0, 9, 7], [940, 720]])
print('-----')
print('expected: [320, 320]')
test_function([[2, 2, 0, 0, 3, 3], [320, 320]])
print('-----')
print('expected: [97531, 8642]')
test_function([[1, 9, 2, 8, 3, 7, 4, 6, 5], [97531, 8642]])
print('-----')
print('expected: []')
test_function([[], []])
print('-----')
print('expected: [5]')
test_function([[5], [5]])