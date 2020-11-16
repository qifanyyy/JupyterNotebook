from gcd_lcm import diophantine_equation as diophantine
from gcd_lcm import arePrime
from PrimeNumbers import prime_factorization
from Division import euclidian_division as divide
'''
    This method returns true if a = b[n], and false otherwise
    a = b[n], read as "a is congruent to b modulo n", means
        that n divides a - b
'''
def are_congruent(a, b, n):
    return (a - b) % n == 0

'''
    This method solves the congruence equation ax = b[n]
    Ex: congruence_equation(5, 1, 6) solves 5x = 1[6] and outputs (-6, -1),
        meaning x = -6k - 1, k being an integer
'''
def congruence_equation(a, b, n):
    # ax = b[n] => ax = b + ny (y being an integer)
    # Thus, ax - ny = b, so solving the congruence equation
    #   is equivalent to solving the resulting diophantine equation
    return diophantine(a, -n, b)[0]

'''
    This method returns the order of a given number x modulo n, which is
        the smallest non negative integer m such that x ^ m = 1[n]
'''
def order(x, n):
    if not arePrime(x, n):
        raise ValueError(str(x) + " and " + str(n) + " are not prime")
    current = x
    i = 1
    while True:
       if are_congruent(current, 1, n):
           return i
       current = current * x
       i = i + 1

'''
    This method calculates Euler's phi function for a given integer n, which is
        the number of positive integers smaller than n and relatively prime with n.
        It uses the formulas: phi(p^a) = p^a - p^(a-1) when p is prime, and
        phi(mn) = phi(m) * phi(n) when m and n are relatively prime
'''
def euler_phi(n):
    factorization = prime_factorization(n)
    result = 1
    # If the prime factorization of n is n = p^a * q^b, then
    #   phi(n) = phi(p^a) * phi(q^b) = (p^a - p^(a - 1)) * (q^b - q^(b - 1))
    for p in factorization:
        result = result * (p[0] ** (p[1] - 1)) * (p[0] - 1)
    return result

'''
    This method solves the chinese remainder equations x = a[m], x = b[n]
    Ex: chinese_remainder_equation(1, 6, 2, 5) solves the system x = 1[6], x = 2[5]
        and the solution is (30, 7), meaning that x = 30k + 7, k being an integer
'''
def chinese_remainder_equation(a, m, b, n):
    # Since x = a[m] and x = b[n], then x = a + mp = b + nq, implying the diophantine
    #   equation mp - nq = b - a. Solving for p or q gives us x
    p = diophantine(m, n, b - a)
    #p[0] is p in this case
    return (p[0][0] * m, a + m * p[0][1])

'''
    This method computes a ^ m modulo n
    Ex: power_modulo(7, 91, 100) = 43, since 7^91 = 43[100]
'''
def power_modulo(a, m, n):
    # Let o the order of a modulo n, and let m = oq + r. Then a^m = (a^o)^g * a^r,
    #   So a^m = 1^q * a^r[n] => a^m = a^r[n].
    o = order(a, n)
    r = divide(m, o)[1]
    # All we have to do then is to computer a^r modulo n
    current = 1
    for i in range(1, r + 1):
        current = (current * a) % n
    return current