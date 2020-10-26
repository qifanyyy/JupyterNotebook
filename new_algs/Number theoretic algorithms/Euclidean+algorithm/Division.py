
'''
    This function divides two integers (positive or negative), then returns the quotient and the rest
    @:param a, b: the dividend and the divisor, in that order
    @:return q, r: the quotient and the rest, in that order
'''
def euclidian_division(a, b):
    q = 0
    r = 0
    #Division by zero impossible
    if b == 0:
        raise ValueError("Division by zero impossible")
    if a > 0 and b > 0:
        return __positive_euclidian_division(a, b)
    '''
        If b < 0, then b = -|b|
        If a = |b|q + r, then a = -|b| * -q + r, so a = b * -q + r (The quotient becomes -q)
    '''
    if a > 0 and b < 0:
        q, r = euclidian_division(a, -b)
        q = -q


    '''
        If a < 0,  then a = -|a|
        If |a| = |b|q + r, then a = -|a| = -|b|q - r, so a = -|b|q - |b| + |b| - r = -|b|(q + 1) + |b| - r,
        Thus, a = -|b|(q + 1) + |b| - r, and 0 <= |b| - r < |b| (as long as r != 0), so we have three cases:
            if r = 0, a = -|b|q, so the quotient is q if b < 0 and -q if b > 0
            if b > 0, b = |b|, so a = -b(q + 1) + b - r, so the quotient is -(q + 1) and the rest is b - r
            if b < 0, b = -|b|, so a = b(q + 1) - b - r, so the quotient is q + 1 and the rest is -b - r
    '''
    if a < 0 and b > 0:
        q, r = euclidian_division(-a, b)
        if r == 0:
            q = -q
        else:
            q = -q - 1
            r = b - r
    if a < 0 and b < 0:
        q, r = euclidian_division(-a, -b)
        if r != 0:
            q = q + 1
            r = -b - r
    return q, r

'''
    This method divides two positive integers, then returs their quotient and rest
    @:param a, b: the dividend and the divisor, in that order
    @:return q, r: the quotient and the rest, in that order
'''
def __positive_euclidian_division(a, b):
    if b == 0:
        raise ValueError("Division by zero impossible")
    q = 0
    r = 0
    while a >= b:
        a = a - b
        q = q + 1
    r = a
    return q, r


'''
    This method returns true if the given dividend is divisible by the divisor, and false otherwise
'''
def isDivisible(dividend, divisor):
    return euclidian_division(dividend, divisor)[1] == 0
