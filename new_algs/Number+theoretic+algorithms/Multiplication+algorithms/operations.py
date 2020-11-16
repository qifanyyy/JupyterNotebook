def add_with_overflow(n1, n2):  # Add two numbers and return result, overflow
    length = max(len(n1), len(n2))
    n1 = n1.zfill(length)
    n2 = n2.zfill(length)

    result = ""
    carray = 0
    while length != 0:
        # if n1[length - 1] == "1":
        #     if carray == "0":
        #         if n2[length - 1] == "0":
        #             result += "1"
        #             carray = "0"
        #         else:
        #             result += "0"
        #             carray = "1"
        #     else:
        #         if n2[length - 1] == "0":
        #             result += "0"
        #             carray = "1"
        #         else:
        #             result += "1"
        #             carray = "1"
        # else:
        #     if carray == "0":
        #         if n2[length - 1] == "0":
        #             result += "0"
        #             carray = "0"
        #         else:
        #             result += "1"
        #             carray = "0"
        #     else:
        #         if n2[length - 1] == "0":
        #             result += "1"
        #             carray = "0"
        #         else:
        #             result += "0"
        #             carray = "1"
        b1 = int(n1[length - 1])  # last bit
        b2 = int(n2[length - 1])
        s = b1 ^ b2 ^ carray
        carray = ((b1 ^ b2) & carray) | (b1 & b2)
        result = str(s) + result
        length -= 1

    return result, str(carray)


def comp(n):  # return Two's Complement
    s = [str(int(x) ^ 1) for x in n]
    s = ''.join(s)
    s = add_with_overflow(s, '1')
    return s[0]


def sub(n1, n2):
    n2 = comp(n2)
    n1 = add_with_overflow(n1, n2)
    return n1[0]


def arith_shift_right(a, b):  # Make Arith shift right to a, b and c then return the final value of a,b,c
    q = b[-1]
    b = a[-1] + b[:-1]
    a = a[0] + a[:-1]

    print(a, b, q)
    return a, b, q


def shift_left(r1, r2):  # return a, b after shift left
    r1 = r1[1:] + r2[0]
    r2 = r2[1:] + "0"
    return r1, r2


def is_less_than_zero(r):  # check of r is less than zero then return True or False
    return r[0] == "1"


def count(value, sign):  # sign=1: negative else: positive
    t = 1
    if sign == 1:
        while 2 ** (t-1) <= value:
            t += 1
    else:
        while (2 ** (t-1)) - 1 <= abs(value):
            t += 1
    return t


def to_binary(n, count):
    if n >= 0:
        return bin(n)[2:].zfill(count)
    n_filled = bin(abs(n))[2:].zfill(count)
    return comp(n_filled)
