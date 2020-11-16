"""
@author: David Lei
@since: 11/08/2017

Functional-ish things in Python3:

Other cool functional programming things in Python3: https://docs.python.org/3/howto/functional.html

Note: Differences in Python2 and Python3:
- Python3 map(), filter() return iterators instead of lists
- reduce moved to functools.reduce() but usually for loops are more readable
"""

from functools import reduce
import math
import time

"""
Filter: filter(fn_that_evals_true_or_false, iterable)
    - iterable can be a sequence (list), container that supports iteration, an iterator
    - returns an iterable over elements that evaluate to true in the original iterable.
    - if function is None, identify function used which removes all False elements
    - equivalent to generator expression: (item for item in iterable if function(item)) assuming function is not None
"""
print("\n~~~~~~ Filter ~~~~~~~\n")

numbers = [x for x in range(100)]


def is_even(n):
    return n % 2 == 0


is_multiple_of_3 = lambda x: x % 3 == 0

even_numbers = filter(is_even, numbers)  # Need to case to list to print as it is an iterator.
print(even_numbers)  # <filter object at 0x10a74eac8>
print(list(even_numbers))

even_numbers = filter(is_even, numbers)  # returns iterator <filter object at 0x10a74eac8>
even_multiple_of_3 = filter(is_multiple_of_3, even_numbers)  # Pass an iterator instead of a list.
print(list(even_multiple_of_3))  # [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96]

# Note: a = 0 is evaluated as a None type, a == False is True.
# Empty structures such as [], {} etc aren't False or None but are evaluated as falsey.
has_some_nones = [None, [], {}, set(), 'apple', False, 0, 1, "0"]
removed_nones = filter(None, has_some_nones)
print(list(removed_nones))  # ['apple', 1, '0']


"""
Reduce: reduce(function, iterable)
    - moved to functools.reduce() in Python3
    - reduce applies the function (expects two args) to continuously to the iterable from left to right
        to return a single accumulated value
"""
print("\n~~~~~~ Reduce ~~~~~~\n")
numbers = [x for x in range(5)]


def add(x, y):
    """Adds x and y. The left arg x is the accumulated value, the right argument y is the value form the sequence
    x: -3, y: 0
    x: -3, y: 1
    x: -2, y: 2
    x: 0, y: 3
    x: 3, y: 4

    Applied 5 times to list numbers, first time takes in the initial value and the first number, adds them and stores
    the sum in x then repeats this for rest of sequence.

    If the initial value is not provided then the first item in the iterable is taken as the initial value.
    """
    print("x: {0}, y: {1}".format(x, y))
    return x + y

initial_value = -3
total = reduce(add, numbers, initial_value)
print("Sum of {0} + initial value of {2} is {1}".format(numbers, total, initial_value))


"""
- Map: map(function, iterable)
    - returns an iterator after applying a function to every element in the original iterable yielding the results
    - can be applied to multiple iterables but function must take that many arguments and is applied to each item in
        all iterables at the same time.
        i.e. def f (x, y): pass two iterables, for each index in iterables apply
        function(iterable1[i], iterable2[i])
        If iterables are different lengths, stops at shortest.
    - use to convert a list

Note: Look at itertools.starmap() when args are already grouped in a tuple in a single iterable.
"""
print("\n~~~~~~ Map ~~~~~~~\n")


def combine(magnitude, unit):
    return "{0} {1}".format(magnitude, unit)


magnitudes = [1, 3, 10, 0, 4]
units = ["kg", "mm", "L"]
formatted = map(combine, magnitudes, units)
print(list(formatted)) # ['1 kg', '3 mm', '10 L']


"""
Lambda: my_lambda_fn = lambda args: operations_on_args
    - Create an anon function at runtime, not bound to a name
    - Can be assigned to a variable
    - No return statement, has an expression that is returned
    - Used with Map, Reduce, Filter

Note: PEP8 says you shouldn't assign a lambda function, use def instead.
"""
print("\n~~~~~~ Lambda ~~~~~~~\n")


def normal_squared(n):
    return n ** 2
print("normal squared: {}".format(normal_squared(6)))

lambda_squared = lambda param: param ** 2
print("lambda squared: {}".format(lambda_squared(6)))


# Lambda with nested scopes, allows you to pass a variable down from function scope to lambda scope.
# I think this is closure?


def make_increment(n):
    """Creates and returns an anon function.

    :param n: value to increment by, passed in my caller.
    :return: an anon function that looks something like
    def anon(x):
        return x + n
    Where n exists in the scope of make_increment
    """
    return lambda x: x + n

# Create different increment functions and assign to a variable.
increment_by_2 = make_increment(2)
increment_by_10 = make_increment(10)
print("lambda scope, increment 10 by 2: {}".format(increment_by_2(10)))
print("lambda scope, increment 10 by 10: {}".format(increment_by_10(10)))
print(increment_by_2)

print("lambda scope, increment 10 by 7: {} ".format(make_increment(7)(10)))
"""
Explanation:
make_increment(n) returns a new function that takes in x
when assigning to a variable i.e. increment_by_2 = make_increment(2)
increment_by_2 is a function <function make_increment.<locals>.<lambda> at 0x1037fda60>
that takes 1 argument x which is the base value to increment by.

Can also call by make_increment(7)(10)
make_increment(7) returns a function that accepts 1 param like increment_by_2.
The (10) calls that function passing 10 as the arg.
"""

# Prime numbers
n = 60000

# Via filter and lambda, not the most efficient but nice and concise.

filter_lambda_start_time = time.time()

nums = range(2, n)
for i in range(2, math.floor(math.sqrt(n))):
    nums = list(filter(lambda x: x == i or x % i != 0, nums))
print(list(nums))

filter_lambda_end_time = time.time()

# Via a loop, faster than above, start at 3 and only increment by two as even numbers all divisible by 2.

loop_start_time = time.time()

primes = [2]
for number in range(3, n, 2):
    is_prime = True
    for divisor in range(2, math.floor(math.sqrt(n))):
        if number % divisor == 0 and number != divisor:
            is_prime = False
            break
    if is_prime:
        primes.append(number)
print(primes)

loop_end_time = time.time()

print("Prime numbers: time via filter & lambda: {}".format(filter_lambda_end_time - filter_lambda_start_time))
print("Prime numbers: time via loop:            {}".format(loop_end_time - loop_start_time))