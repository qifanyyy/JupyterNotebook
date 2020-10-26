from math import sqrt

'''
    This method checks wether or not a given input is prime
'''
def isPrime(n):
    # 0 and 1 are not prime
    if n <= 1:
        return False
    # 2 is the only prime even number
    if n == 2:
        return True
    # other even numbers are not prime
    if n % 2 == 0:
        return False
    # check for the remaining numbers (odd numbers greater than 2)
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

'''
    This method finds the highest power n such that a ^ n divides b
'''
def __highest_power(a, b):
    n = 0
    x = a
    while(b % x == 0):
        x = x * a
        n = n + 1
    return n

'''
    This method returns the smallest prime that divides n
'''
def __smallest_prime_divisor(n):
    if n <= 1:
        raise ValueError(n, "has no prime divisors")
    if isPrime(n):
        return n
    for i in range (2, n // 2 + 1):
        if n % i == 0 and isPrime(i):
            return i

'''
    This method returns the prime factorization of the given input, 
        displayed as [[1st_prime, 1st_power], [2nd_prime, 2nd_power], ...]
    Ex: prime_factorization(1944) = [[2, 3], [3, 5]]
'''
def prime_factorization(n):
    factorization = []
    # For n = 0, 1, 2, n = n ^ 1 = [[n, 1]]
    if n <= 2:
        return [[n, 1]]
    # find the primes that divide into n, then divides n by those primes until n becomes 1
    while n > 1:
        # find the smallest prime x that divides n
        currentPrimeFactor = __smallest_prime_divisor(n)

        # find the highest power k such that x ^ k divides n
        currentPower = __highest_power(currentPrimeFactor, n)

        # add x and k to the factorization, then divide n by x ^ k
        currentPrimeAndFactor = [currentPrimeFactor, currentPower]
        factorization.append(currentPrimeAndFactor)
        n = n // (currentPrimeFactor ** currentPower)

    return factorization

'''
    This method returns a list of prime numbers between start (inclusive) and end (exclusive)
'''
def list_of_primes(start, end):
    primes = []
    # if start <= 2, advance to 3 and add two to the list of primes
    if start <= 2:
        start = 3
        primes.append(2)
    #if start is even, advance to the next integer
    if start % 2 == 0:
        start = start + 1
    #increment by two, since the even integers are not prime at this point
    for i in range(start, end, 2):
        if isPrime(i):
            primes.append(i)
    return primes

'''
    This method returns a list of primes between start (inclusive) and end (exclusive), 
        that can be written in the form ax + b, where x is an integer (positive or negative)
'''
def dirichlet_primes(a, b, start, end):
    # if a and b are even, 2 is the only prime number that can be written as ax + b
    if a % 2 == 0 and b % 2 == 0:
        return [2]

    primes = []
    # if start <= 2, advance to 3 and add 2 to the list of primes if 2 has the form ax + b
    if start <= 2:
        start = 3
        if(__has_the_form_ax_plus_b(a, b, 2)):
            primes.append(2)

    # if start is even, advance to the next integer
    if start % 2 == 0:
        start = start + 1

    # increment by two, since the even integers are not prime at this point
    for i in range(start, end, 2):
        if __has_the_form_ax_plus_b(a, b, i) and isPrime(i):
            primes.append(i)
    return primes

'''
    Returns true if the given number n can be written as n = ax + b
'''
def __has_the_form_ax_plus_b(a, b ,n):
    # if n = ax + b, then n - b = ax, so a divides n - b, meaning (n - b) % a = 0
    return ((n - b) % a) == 0
