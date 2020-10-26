# to become master file for Numerical Methods : numeth

def sigma(func, frm, to):
    """
    Given f(x), frm: starting value for range, to: ending value
    returns sum
    """
    result = 0
    for i in range(frm, to + 1):
        result += func(i)
    return result

def deriv():
    """
    On the fly, allows user input of symblic expression
    prints derivative, returns derivative as string expression
    """
    expression = raw_input('Enter an expression involving x: ')

    from scitools.StringFunction import StringFunction

    from sympy import diff, Symbol

    x = Symbol('x')
    f = StringFunction(expression)
    df = diff(f, x)
    print 'The derivative of %s with respect to x is %s' % (expression, df)
    return df

from math import sqrt

def primeFactors(n):
    """
    Returns a vector of prime vacorization
    """
    limit = int(sqrt(n))
    a = list()

    while (n%2 == 0):
        a.append(2)
        n = n/2

    for i in range(3, (limit + 1), 2):
        while (n%i == 0):
            a.append(i)
            n = n/i

    if (n > 2):
        a.append(n)

    return a


from numpy import dot, array
from numpy.linalg import solve

def gaussElimin(a,b):
    n = len(b)
    # Elimination phase
    for k in range(0, n-1):
        for i in range(k+1, n):
            if a[i,k] != 0.0:
                lam = a[i,k]/a[k,k]
                a[i,k+1:n] = a[i,k+1:n] - lam * a[k, k+1:n]
                b[i] = b[i] - lam * b[k]
    # Back substitution
    for k in range(n-1, -1, -1):
        b[k] = (b[k] - dot(a[k,k+1:n], b[k+1:n]))/a[k,k]
    return b


from numpy import dot

def LUdecomp(a):
    n = len(a)
    for k in range(0,n-1):
        for i in range(k+1,n):
            if a[i,k] != 0.0:
                lam = a [i,k]/a[k,k]
                a[i,k+1:n] = a[i,k+1:n] - lam*a[k,k+1:n]
                a[i,k] = lam
    return a

def LUsolve(a,b):
    n = len(a)
    for k in range(1,n):
        b[k] = b[k] - dot(a[k,0:k],b[0:k])
    for k in range(n-1,-1,-1):
        b[k] = (b[k] - dot(a[k,k+1:n],b[k+1:n]))/a[k,k]
    return b


def euclid(a, b):
    """Euclid's algorithm for GCD

    Given input a, b the function returns d such that gcd(a,b) = d"""

    if a < b:
        a,b = b,a
    else:
        pass

    while b:
        a, b = b, a % b
    return a

def xlgcd(a, b):
    """Displays the steps of Extended Euclid's algorithm for GCD
    This version displays a summary before returning value.
    It stores these values in lists throughout the loop.


    Given input a, b the function returns d such that gcd(a,b) = d
    and x, y such that ax + by = d, as well as u,v such that
    xv + yu = d"""

    d = euclid(a, b)
    step = 0
    
    if a < b:
        a,b = b,a
    else:
        pass
    u, v, x, y = 0, 1, 1, 0

    La=[]
    Lb=[]
    Lx=[]
    Ly=[]
    Lu=[]
    Lv=[]

    A, B = a, b

    print "Displaying the steps of Extended Euclid's algorithm for GCD\n"
    print "The intitial values are:"
    print "a = ", a, "\nb = ", b
    print "x = ", x, "\ny = ", y, "\nu = ", u, "\nv = ", v
    print "----------------------------------\n"
    print "We write the equation in this form: a = q*b + r"
    print "\n", a, "=", a//b,"*", b, "+", a%b
    print "\nwhere q is the integer part of a/b, and r is a%b\n"
    print "----------------------------------\n"
    print "During the recursive loop, values will change.\n"
    print "a <---| b"
    print "b <---| a%b"
    print "x <---| u"
    print "y <---| v"
    print "u <---| x - (a/b)*u"
    print "v <---| y - (a/b)*v"
    print "----------------------------------\n"

    La.append(a)
    Lb.append(b)
    Lx.append(x)
    Ly.append(y)
    Lu.append(u)
    Lv.append(v)
    
    while b != 0:
        a, b, x, y, u, v = b, a%b, u, v, x - (a // b) * u, y - ( a // b) * v
#        a = b
#        b = a%b
#        x = u
#        y = v
#        u = x - (a//b) * u
#        v = y - (a//b) * v
        step += 1
        La.append(a)
        Lb.append(b)
        Lx.append(x)
        Ly.append(y)
        Lu.append(u)
        Lv.append(v)
        print "\nSTEP#: ", step
        print "a = ", a, "\nb = ", b
        print "x = ", x, "\ny = ", y, "\nu = ", u, "\nv = ", v
        print "\nNow,", b, "=", u,"*", A,"+", v,"*", B
        if (b != 0):
            print "Meanwhile,", a, "=", a//b,"*", b, "+", a%b
   
    print "\nx = ", x, "\ny = ", y, "\nu = ", u, "\nv = ", v
    print "\n", A,"*", x," + ", B,"*", y," = ", (A*x + B*y)
    print "\nDoes", A,"*", x," + ", B,"*", y," = ", d," ?"
    print (A*x + B*y) == d
    print "--------------------\n"

    if ((A*x + B*y) == d):
        print "\nSUMMARY of:"
        print "a = ((a/b) * b) + a%b"
        print "------------------------------------"
        for i in range(step):
            print La[i], "= (", La[i]//Lb[i],"*", Lb[i], ") +", La[i]%Lb[i]
        print "\nSUMMARY of:"
        print "r = (u * a0)  +  (v * b0)"
        print "------------------------------------"
        for i in range(step):
            print Lb[i], "= (", Lu[i],"*", A,") + (", Lv[i],"*", B, ")"
        print "\na, x, y, u, v: "
        return a, x, y, u, v
    else:
        print "There's been some kind of error."
    raw_input("Press enter")

def isolve(a,b,d):
    """
    Usage:  Given ax + by = d, returns x, y
    """
    q, r = divmod(a, b)
    if r == 0:
        return ([0, d/b])
    else:
        sol = isolve(b,r,d)
        u = sol[0]
        v = sol[1]
        return ([v, u - q*v])
    
# Iterative Algorithm (xgcd)
def iterative_egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q,r = b//a,b%a; m,n = x-u*q,y-v*q # use x//y for floor "floor division"
        b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y

def modinv(a, m):
    g, x, y = iterative_egcd(a, m) 
    if g != 1:
        raise ZeroDivisionError, "Inverse does not exist."
    else:
        return x % m

# The MotherLoad for Number Theory: see Brian Gladman
# 173.254.28.24/~brgladma/number_theory.py

def gcd(a, *r):
  '''
  Greatest Common Divisor of a sequence of values

  >>> gcd(1701, 13979)
  7

  >>> gcd(117, -17883411)
  39

  >>> gcd(3549, 70161,  336882, 702702)
  273
  '''
  for b in r:
    while b:
      a, b = b, a % b
  return abs(a)


def lcm(a, *r):
  '''
  Least Common Multiple Divisor of a sequence of values

  >>> lcm(1701, 13979)
  3396897

  >>> lcm(117, -17883411)
  53650233

  >>> lcm(3549, 70161,  336882, 702702)
  111426753438
  '''
  for b in r:
    a *= b // gcd(a, b)
  return abs(a)

def xgcd(a, b):
  '''
  Euclid's Extended GCD Algorithm

  >>> xgcd(314159265, 271828186)
  (-18013273, 20818432, 7)
  '''
  u, u1 = 1, 0
  v, v1 = 0, 1
  while b:
    q, r = divmod(a,  b)
    a, b = b, r
    u, u1 = u1, u - q * u1
    v, v1 = v1, v - q * v1
  return (a, u, v) if a > 0 else (-a, -u, -v)

def cong(a, p, n):
  '''
  Solve the congruence a * x == p (mod n)

  >>> cong(13, 17, 19)
  13

  >>> cong(17, 19, 23)
  16

  >>> cong(14, 6, 91) is None
  True
  '''
  g = gcd(a, n)
  if p % g > 0:
    return None
  return (xgcd(a, n)[1] * (p // g)) % (n // g)

def inv(a, n):
  '''
  Find the modular inverse of a (mod n)

  >>> inv(271828, 314159)
  898

  >>> inv(314159, 271828)
  271051
  '''
  return None if gcd(a, n) > 1 else xgcd(a, n)[1] % n


def crt(a, m):
  '''
  The Chinese Remainder Theorem (CRT)

  Solve the equations x = a[i] mod m[i] for x

  >>> crt((2, 3, 5, 7), (97, 101, 103, 107))
  96747802
  '''
  def _crt(a, b, m, n):
    d = gcd(m, n)
    if (a - b) % d:
      return None
    x, y, z = m // d, n // d, (m * n) // d
    r, p, q = xgcd(x, y)
    return (b * p * x + a * q * y) % z

  if len(a) == len(m):
    x, mm = a[0], m[0]
    for i in range(1, len(a)):
      x = _crt(a[i], x, m[i], mm)
      if x is None:
        break
      mm = lcm(m[i], mm)
  else:
    raise IndexError
  return x


