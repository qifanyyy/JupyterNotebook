# /bin/python3
import itertools # we'll need the unique combinations of multiples

'''
    Calculate the sum of all multiples in a given total
    Using arithmetic progression, the sum of the members of a finite
    arithmetic progression is done by taking the number of n terms being added,
    adding the first and last number, and dividing it by two

    :param int  multiple    The multiples to search for
    :param int  total       The total to derive the multiples from

    :return int
'''
def calculateSumOfMultiples(multiple, total):
    multiples = (total // multiple)
    # we multiply multiples by multiple as we've done integer division - so we
    # we need the result that that has derived.
    return (multiples * ((multiples * multiple) + multiple) // 2)

'''
    Derive the greatest common devisor from two numbers

    :param int a    The first number
    :param int b    The second number

    :return int
'''
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

'''
    Derive the lowest common multiplier from two numbers

    :param int a    The first number
    :param int b    The second number

    :return int
'''
def lcm(a, b):
    return a * b // gcd(a, b)

'''
    Find the sum of all multiples up to a limit

    :param int  limit       The limit to derive our multiples from
    :param list multiples   The multiples to sum

    :return int
'''
def sum(limit, multiples):
    # for each multiple in multiples calculate the sum of the multiples from the total
    # and remove all combinations of the lowest common divisor of 2 values from the total
    return reduce(
        lambda x, y: x + y,
        [calculateSumOfMultiples(multiple, limit) for multiple in multiples]
    ) - (reduce(
        lambda x, y: x + y,
        [calculateSumOfMultiples(lcm(m, om), limit) for m, om in itertools.combinations(multiples, 2)]
    ) if len(multiples) > 1 else 0) # only call this if we have more than 1 multiplier in the sum
