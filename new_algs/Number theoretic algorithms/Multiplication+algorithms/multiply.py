# Karatsuba Multiplication algorithm

# Arjun Krishna Babu
# 10 May 2020
# Python 3.8.2

from termcolor import colored

def getColoredOutput(x, y, product):
    color = 'red' if ((product - (x*y)) != 0) else 'green'
    return colored("Product of {} * {} = {}; Act={}, Error={}".format(x, y, product, x * y, product - (x*y)), color)

def recursiveMultiply(x, y):
    xs, ys = str(x), str(y)

    # padding... because this works iff length of both numbers are the same
    # So, if we store the length as max of the available two lengths
    # then further down the line when we split the numbers
    # the math automatically works out.
    n = max(len(xs), len(ys)) # max of number of digits between either numbers

    # base case (digit length is 1):
    if n == 1:
        return int(x) * int(y)

    # recursive case:
    p = int(n//2) # the power of 10 to which the digit-group must be separated by

    # compute A, B, C, D
    a = x//(10**p)
    b = x % (10**p)
    c = y//(10**p)
    d = y % (10**p)

    ac = recursiveMultiply(a, c)
    bd = recursiveMultiply(b, d)
    a_b__c_d = recursiveMultiply(a + b, c + d)
    ad_plus_bc = a_b__c_d - ac - bd     # Gauss' Trick

    # useful for debugging
    # print("a={}, b={}, c={}, d={}".format(a, b, c, d))
    # print("ac\t\t= {}\nbd\t\t= {}\n(a+b)*(c+d)\t= {}\n(ad+bc)\t\t= {}".format(ac, bd, a_b__c_d, ad_plus_bc))

    product = (10**(p*2))*ac + (10**p)*(ad_plus_bc) + bd
    # print(getColoredOutput(x, y, product))
    return product

def main():
    num1 = input().strip()
    num2 = input().strip()
    # print("{} {}".format(num1, num2))
    print(recursiveMultiply(int(num1), int(num2)))

if __name__ == "__main__":
    main()
