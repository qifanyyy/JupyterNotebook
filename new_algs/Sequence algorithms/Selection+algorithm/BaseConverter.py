'''
    BaseConverter converts a decimal number to a different base
    The algorithm has an O(logn) order of magnitude, because the problem is
    divided down on each iteration - this is based on the divide by 2 principal
    of converting decimal to binary

    :param  int     decimal     Our number to convert
    :param  int     base        The base to use (from 2 to 16)

    :return string
'''
def convertTo(decimal, base):
    digits = "0123456789ABCDEF"
    data = list()
    while decimal > 0:
        data.append(digits[decimal % base])
        decimal //= base
    data.reverse()
    return ''.join(data)


def convertFrom(aString, base):
    digits = "0123456789ABCDEF"
    total = 0
    aList = list(aString)
    aList.reverse()
    while len(aList) > 0:
        total += digits.index(aList.pop()) * len(aList) * base
    return total
