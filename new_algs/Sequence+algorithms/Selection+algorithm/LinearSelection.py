from math import ceil
BOLD = '\033[1m'
END = '\033[0m'

# finds and returns the k-th smallest element in the given array
def linear_selection(values, k):
    size = len(values)
    if k < 0 or k > size:
        raise Exception('Parameter k out of limits -> K: {}, SIZE: {}'.format(k, size))
    if size < 5:
        values.sort()
        return values[k-1]
    # slice
    parts = slice_in_groups_of_five(values)
    # find the median of each group
    medians_array = find_medians_array(parts, size)
    # find the median of medians
    all_median = len(medians_array) // 2
    median = linear_selection(medians_array, all_median)

    # partition original data around the median of medians
    lesser, greater = partition_set(values, median)

    lesser_size = len(lesser)
    # base case for the recursion
    if lesser_size == k-1:
        return median
    # recursive calls to find the element    
    if lesser_size > k-1:
        return linear_selection(lesser, k)
    if lesser_size < k-1:
        return linear_selection(greater, k-lesser_size-1)

# slice the given array into groups of five
def slice_in_groups_of_five(values):
    totalSize = len(values)

    arrays = []
    for i in range(0,totalSize, 5):
        leftMargin = i
        rightMargin = (i + 5)
        arrays.append(values[leftMargin:rightMargin])
    
    return arrays

# sort each array in an array
def sort_array_of_arrays(values):
    sorted_values = []
    for value in values:
        value.sort()
        sorted_values.append(value)

    return sorted_values

# find the medians in an array
def find_median(values):
    values.sort()
    half = len(values) // 2
    return values[half]

# find the medians in each array
def find_medians_array(values, size):
    # sorted_arrays = sort_array_of_arrays(values)
    medians_array = []
    floor = size // 5
    if floor == 0:
        median = find_median(values[0])
        return [median]
        
    for i in range(0, floor):
        median = find_median(values[i])
        medians_array.append(median)
        
    return medians_array

# partition data set, returning a set where all numbers are less then median and a set where all the numbers are greater than median
def partition_set(values, median):
    lesser = []
    greater = []

    for value in values:
        if value < median:
            lesser.append(value)
        elif value > median:
            greater.append(value)
    
    return list(set(lesser)), list(set(greater))

# read values from numbers file
def get_values_from_file(path):
    fileName = open(path, "r")
    values = []
    for val in fileName.read().split():
        values.append(int(val))
        fileName.close()

    return values

def main():
    print('If you want to customize the numbers in the list, please edit the {}numbers.txt{} file.'.format(BOLD,END))

    values = get_values_from_file("numbers.txt")
    
    k = int(input('Type the k for the k-th smallest element in the list: '))

    result = linear_selection(values,k)
    print(str(result))


if __name__ == '__main__':
    main()