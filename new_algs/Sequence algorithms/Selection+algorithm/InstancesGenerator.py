import random
import LinearSelection
import BubbleSort
import time

# generate number instances for both algorithms
def generate_instances(size): 
    values = []
    for _ in range(size):
        value = random.randint(1,100000)
        values.append(value)
    
    return values

# uses linear selection to find kth element and measure its execution time
def get_linear_execution_time_for(values):
    instance_size = len(values)

    kLinear_start = time.time()
    k = instance_size // 2
    _ = LinearSelection.linear_selection(values, k)
    kLinear_end = time.time()

    return kLinear_end - kLinear_start

# uses sort selection with bubble sort to find kth element and measure its execution time
def get_bubble_execution_time_for(values):
    instance_size = len(values)

    kBubble_start = time.time()
    k = instance_size // 2
    _ = BubbleSort.sort_selection(values, k)
    kBubble_end = time.time()

    return kBubble_end - kBubble_start

def prepare_file():
    file = open('ComparisonResults.csv', 'w')
    file.write('Linear Selection, Bubble Sort Selection\n')
    file.close()


# write the results to a CSV file
def save_to_file(linear_time, bubble_time):
    file = open('ComparisonResults.csv', 'a+')
    file.write('{},{}\n'.format(linear_time,bubble_time))
    file.close()

STEP_SIZE = 1000
# runs both 
def comparison():
    prepare_file()
    counter = 0
    for i in range(1,11):
        for _ in range(10):
            values = generate_instances(STEP_SIZE*i)
            linear_time = get_linear_execution_time_for(values)
            bubble_time = get_bubble_execution_time_for(values)
            counter += 1
            print('{}. Linear Selection time: {}s | BubbleSort Selection time: {}s'.format(counter, linear_time, bubble_time))
            save_to_file(linear_time, bubble_time)

comparison()