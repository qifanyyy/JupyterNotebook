"""
@author: David Lei
@since: 26/08/2016
@modified: 22/4/2017

Note: Didn't bother handling recursion depth reached.

The nth root of a number

For example the 3rd root or cube root of 27 is 3 as 3 * 3 * 3 = 27.
So looking for the nth root we can check if we have found it by taking the current estimate and
raising it to the power of n.

approx: 1.25e+23
approx: 1.5625e+22
approx: 1.953125e+21
...
approx: 211.8
approx: 26.5
approx: 3.3
approx: 11.2
approx: 17.7
approx: 14.2
approx: 15.9
approx: 16.8
approx: 17.3
approx: 17.0
"""

def binary_search_nth_root(number, nth_root, min_val, max_val, accuracy):
    hi = max_val
    lo = min_val
    while lo < hi:
        mid_val = (hi + lo) / 2  # Current estimate of the nth root.
        approx = round(mid_val ** nth_root, accuracy)
        print("approx: %s, mid_val: %s, hi: %s, lo: %s" % (approx, mid_val, hi, lo))
        if approx == number:  # Note: Round can round floats to accuracy decimal points.
            return mid_val
        elif approx > number:
            hi = mid_val
        else:
            lo = mid_val
    return -1


def binary_search_find_root(number, min_v, max_v, accuracy, n):
    """
    Use to find nth dimension root of number using binary search.

    Precondition: max > min.
    Precondition: number < max

    :param number: Number to find square root of.
    :param min_v: lower bound, start at 0.
    :param max_v: upper bound, max value of number.
    :param accuracy: accuracy to round to for decimal points.
    :param n: nth dimension root to find (square = 2, cube = 3, 4, 5 .. n)
    :return:
    """
    if max_v <= min_v:  # Can't find
        return -1
    mid_val = (max_v + min_v) / 2  # Returns a float.
    if round(mid_val ** n, accuracy) == number:
        return mid_val
    elif mid_val ** n > number:  # Need to make mid_val**2 less so it matches number.
        return binary_search_find_root(number, min_v, mid_val, accuracy, n)  # Look at values between min and mid, discard > mid point.
    elif mid_val ** n < number:
        return binary_search_find_root(number, mid_val, max_v, accuracy, n)  # Discard values lower than mid to make number bigger.

number = 17
min_v = 0
max_v = 100000000  # Max number range, number needs to be < max.
accuracy = 6
nth_dimension_root = 3

nth_root_1 = binary_search_find_root(number, min_v, max_v, accuracy, nth_dimension_root)
nth_root_2 = binary_search_nth_root(number, nth_dimension_root, min_v, max_v, accuracy)
# 2.57*2.57*2.57 = 16.9.
print(nth_root_1)
print(nth_root_2)
"""
root_to_find_number = 3
accuracy = 1
1.7229467630386353

accuracy = 2
1.7316779121756554

accuracy = 10
1.73205080757511

accuracy = 25
1.7320508075688772

Gets slightly closer every time, ~ 20 reaches recursion depth.
"""