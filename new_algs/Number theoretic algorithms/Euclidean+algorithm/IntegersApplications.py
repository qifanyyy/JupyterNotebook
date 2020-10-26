def hcf(x,y):  # Using the Euclidean Algorithm to compute the highest common factor
    if x < y:
        y,x = x,y
    if x % y == 0:
        return y  # The result will return only the hcf of x and y
    else:
        x , y= y ,x % y
        return hcf(x,y)


def lcm(x,y):  # By the lemma(The multiplication of lcm(x,y) and hcf(x,y) is equal to x times y
    return x * y / hcf(x,y)

def is_prime(x: int):  # Check if the value x have a factor excluding 1 and x itself
    for i in range(2, x-1):
        if x % i == 0:
            return True
    return False


def factors(x: int):  # Find all the factors of a number x, return all the values as a list
    if is_prime(x):
        for i in range(1, x):
            if x % i == 0:
                yield i
    else:
        yield 1
        yield x


def list_of_prime(x: int):  # In a range of 2 to its own value, return as a list of prime number in that range
    for i in range(2, x):
        if not is_prime(i):
            yield i


def prime_factorization(x: int):  # Find all the factors that will sum multiply to the input value
    for i in list(list_of_prime(x)):
        if not is_prime(x):
            return x
        else:
            if x % i == 0:
                return '{}*{}'.format(i, prime_factorization(x // i))  # return as a string
