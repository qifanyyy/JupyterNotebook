'''
    Russian (Ethipoian) Multiplication
    This process involves divide and conquer for quickly calulating
    the product of two numbers.

    :param  int     a       First number
    :param  int     b       Second number

    :return int
'''
def multiply(a, b):
    result = 0
    while a > 0:
        if a % 2 != 0:
            result += b
        b *= 2
        a //= 2
    return result
