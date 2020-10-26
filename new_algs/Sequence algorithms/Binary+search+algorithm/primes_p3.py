import random as rd
import time
import primes_p1 as p1
import math as m
import itertools as it

def FermatsLT(p):
    """checks if given p is a prime number using Fermat's little theorem:
    --- if p is a prime number and a is a integer not divisible by p, then ---
    ---                         a^(p-1) mod p = 1                          ---"""
    
    assert isinstance(p, int), "Given argument has to be integer!"
      
    if p in {0, 1, 2}:
        return True if p == 2 else False
    if p % 2 == 0:                              # even numbers (except 2) are not primes
        return False
    
    for i in range(25):                         # twenty five repeats of the test
        a = rd.randint(2, p-1)                  # to increase its accuracy
        if m.gcd(a, p) != 1 or pow(a, p-1, p) != 1:
            return False
        
    return True


def MillerRabinPT(p):
    """checks if given p is a prime number using Miller-Rabin primality test:
    --- if p is an odd prime number of the form p = 1 + 2^s*d where d is odd,   ---
    --- then for any natural number a from <2, p-2> Miller-Rabin sequence:      ---
    ---             a^d, a^(2*d), a^(4*d), ..., a^(2^(s-1)*d)       (mod p)     ---
    --- ends with p-1 if a^d is not congruent modulo p to 1.                    ---"""
    
    assert isinstance(p, int), "Given argument has to be integer!"
    
    if p in {0, 1, 2, 3}:
        return True if p == 2 or p == 3 else False
    if p % 2 == 0:                                  # even numbers (except 2) are not primes
        return False
    
    d = p-1
    s = 0
    while d % 2 == 0:
        s += 1
        d >>= 1
    for i in range(10):                             # ten repeats of the test
        a = rd.randint(2, p-2)                      # to increase its accuracy
        x = pow(a, d, p)                            # a^d % p
        if x == 1 or x == p-1:
            continue
        j = 1
        while j <= s-1 and x != p-1:
            x = pow(x, 2, p)
            if x == 1:
                return False
            j = j+1
        if x != p-1:
            return False
        
    return True


def MersennePrimes(n):
    """generates all Mersenne primes (2^p-1 where p is also prime) up to n"""
    
    assert isinstance(n, int), "Given argument has to be integer!"
    primes = p1.SieveofEratosthenes(int(m.log2(n)))
    for p in primes:
        mp = pow(2,p)-1
        if MillerRabinPT(mp):
            yield mp


def SafePrimes(n):
    """generates all safe primes (p for which (p-1)/2 is also prime) up to n"""
    
    assert isinstance(n, int), "Given argument has to be integer!"
    primes = p1.SieveofEratosthenes(n)
    for p in primes:
        sp = (p-1)/2
        if sp in primes:
            yield p


def SexyPrimes(n):
    """generates all pairs, triplets, quadruplets and quintuplets of sexy primes
    (primes which differ from each other only by six) up to n"""
    
    assert isinstance(n, int), "Given argument has to be integer!"
    primes = p1.SieveofEratosthenes(n)
    for p in primes:
        if p+6 in primes:
            yield (p, p+6)
        else:
            continue
        if p+12 in primes:
            yield (p, p+6, p+12)
        else:
            continue
        if p+18 in primes:
            yield (p, p+6, p+12, p+18)
        else:
            continue
        if p+24 in primes:
            yield (p, p+6, p+12, p+18, p+24)


def AntiPrimes(n):
    """generates n antiprimes (highly composite natural numbers with more divisors than
    any smaller number has)"""
    
    assert isinstance(n, int), "Given argument has to be integer!"
    n_i = 1
    ap = 1
    record = 0
    while n_i <= n:
        div = []
        for i in range(1, m.ceil(ap**0.5)+1):
            if ap % i == 0:
                if i not in div:
                    div.append(i)
                if ap//i not in div:
                    div.append(ap//i)
        if len(div) > record:
            record = len(div)
            n_i += 1
            yield ap
        ap += (40 if ap >= 1680 else 20) if ap >= 60 else (2 if ap >= 2 else 1)
        # probabilistic assumption of a step because the larger numbers become, the more distance is between them
        # the last 3 digits of every antiprime greater than 1680 become ALWAYS divisible by 40
        

def EmirpPrimes(n):
    """generates n emirp primes (primes that when reversed are a different prime,
    except palindromic ones)"""
    
    # omits one-digit primes (they cannot be reversed) and 11
    # the least prime which can be reversed and give a different prime is 13
    assert isinstance(n, int), "Given argument has to be integer!"
    n_i = 0
    for p in it.accumulate(it.chain([13], it.cycle([4, 2]))):
        if n_i == n:
            break
        if MillerRabinPT(p):
            s = str(p)
            i, j = 0, len(s)-1
            while i <= j:
                if s[i] != s[j]:
                    break
                i, j = i+1, j-1
            else:
                continue
            rev_p = int(s[::-1])                            # reversed string
            if MillerRabinPT(rev_p):
                yield p
                n_i += 1


if __name__ == '__main__':
    print('************************************************************************************')
    print("{:^87}".format("1000 FIRST PRIME NUMBERS (FERMAT's LITTLE THEOREM)"))
    primes = []
    for n in range(7920): 
        if FermatsLT(n):
            primes.append(n)
    print(primes)
    print("LENGTH OF THE LIST: {}".format(len(primes)))
    print("(if the length is >1000, it's recommended to perform the test again because the algorithm is just probabilistic and determines if n is composite or probably prime)")
    print('************************************************************************************')
    print("{:^87}".format("10000 FIRST PRIME NUMBERS (MILLER-RABIN)"))
    primes2 = []
    time_start = time.time()
    for n in range(104730):
        if MillerRabinPT(n):
            primes2.append(n)
    time_end = time.time()
    total = time_end - time_start
    print(primes2)
    print("TEST PERFORMANCE TIME : {:0.3f} s".format(total))
    print("LENGTH OF THE LIST: {}".format(len(primes2)))
    print("(if the length is >10000, it's recommended to perform the test again because the algorithm is just probabilistic and determines if n is composite or probably prime)")
    print('************************************************************************************')
    print("SOME LARGE NUMBERS TESTED BY MILLER-RABIN:".format())
    n1 = 4547337172376300111955330758342147474062293202868155909489
    r1 = MillerRabinPT(4547337172376300111955330758342147474062293202868155909489)
    ans_tru = lambda r: 'yes' if r == True else 'no'
    ans_fal = lambda r: 'yes' if r == False else 'no'
    print("{}\n{}, is it a correct answer?: {}\n".format(n1, r1, ans_tru(r1)))
    n2 = 4547337172376300111955330758342147474062293202868155909393
    r2 = MillerRabinPT(4547337172376300111955330758342147474062293202868155909393)
    print("{}\n{}, is it a correct answer?: {}\n".format(n2, r2, ans_fal(r2)))
    n3 = 643808006803554439230129854961492699151386107534013432918073439524138264842370630061369715394739134090922937332590384720397133335969549256322620979036686633213903952966175107096769180017646161851573147596390153
    r3 = MillerRabinPT(643808006803554439230129854961492699151386107534013432918073439524138264842370630061369715394739134090922937332590384720397133335969549256322620979036686633213903952966175107096769180017646161851573147596390153)
    print("{}\n{}, is it a correct answer?: {}".format(n3, r3, ans_tru(r3)))
    print('************************************************************************************')
    print("{:^87}".format("MERSENNE PRIMES"))
    time_start = time.time()
    m_generator = MersennePrimes(170141183460469231731687303715884105728)
    m_list = [i for i in m_generator]
    time_end = time.time()
    print(m_list)
    total = time_end - time_start
    print("NUMBER GENERATING TIME : {:0.3f} s".format(total))
    print('************************************************************************************')
    print("{:^87}".format("SAFE PRIMES"))
    time_start = time.time()
    safep_generator = SafePrimes(10000)
    safep_list = [i for i in safep_generator]
    time_end = time.time()
    print(safep_list)
    total = time_end - time_start
    print("NUMBER GENERATING TIME {:0.3f} s".format(total))
    print('************************************************************************************')
    print("{:^87}".format("SEXY PRIMES"))
    time_start = time.time()
    sexyp_generator = SexyPrimes(10000)
    sexyp_list = sorted([i for i in sexyp_generator], key = len)
    time_end = time.time()
    print(sexyp_list)
    total = time_end - time_start
    print("NUMBER GENERATING TIME {:0.3f} s".format(total))
    print('************************************************************************************')
    print("{:^87}".format("ANTIPRIMES"))
    time_start = time.time()
    ap_generator = AntiPrimes(40)
    ap_list = [i for i in ap_generator]
    time_end = time.time()
    print(ap_list)
    total = time_end - time_start
    print("NUMBER GENERATING TIME {:0.3f} s".format(total))
    print('************************************************************************************')
    print("{:^87}".format("EMIRP PRIMES"))
    time_start = time.time()
    ep_generator = EmirpPrimes(120)
    ep_list = [i for i in ep_generator]
    time_end = time.time()
    print(ep_list)
    total = time_end - time_start
    print("NUMBER GENERATING TIME {:0.3f} s".format(total))
    print('************************************************************************************')
