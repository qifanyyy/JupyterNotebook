# -*- coding: utf-8 -*-
import random  
import matplotlib.pyplot as plt



def jacobi(a,n):  
    j = 1                                #j is jacobi symbol
    while (a != 0):  
        while (a%2==0):                  # loop till a is even number     
            j = j * pow(-1,(n*n-1)/8)    # if n=3(mod 8) or n=5(mod 8) or simply (-1)^((n^2-1)/2)==-1 then j = -j
            a = a/2  
        if not ( (a-3)%4 or (n-3)%4 ):   # if a=3(mod 4) and n=3(mod 4) [So, (a-3)%4 and (n-3)%4 = 0] or simply (-1)^((n 1)/2)==-1 then j = -j
            j = -j
        a,n = n,a                        # interchange(a,n)  
        a = a % n                                  
    return j  
   
def solovay_strassen(n, k=10): 
    if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
        return False
    if n==2 or n==3 or n==5 or n==7:
        return True
    if not n & 1:  
        return False  
    for i in xrange(k):  
        a = random.randrange(2, n - 1)       # choose any random number from 1 to (n-1)  
        x = jacobi(a, n)                     # find n's jacobi number  
        y = pow(a, (n - 1) / 2, n)           # calculate legendre symbol from euler criterion formula  
        if y != 1 and y != 0:                          
            y = -1  
        if (x == 0) or (y != x):             # if jecobi and eular criterion formula are not same (y != x) then the number is not prime  
            return False         
    return True  



def is_prime_miller_rabin(n, k):
    if n!=int(n):
        return False
    n=int(n)
    #Miller-Rabin test for prime
    if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
        return False
    if n==2 or n==3 or n==5 or n==7:
        return True
    s = 0
    d = n-1
    while d%2==0:
        d>>=1
        s+=1
    assert(2**s * d == n-1)
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  
    for i in range(k):#number of trials 
        a = random.randrange(2, n)
    if trial_composite(a):
        return False
    return True 


def solovay_test():
    solovay_results = list()
    solovay_counter = 0
    for i in range(1,1000001):    
        if solovay_strassen(i, 10):
            solovay_counter += 1
        if i == 10 or i == 100 or i == 1000 or i == 10000 or i == 100000 or i == 1000000:
            print(solovay_counter)
            solovay_results.append(solovay_counter)
    return solovay_results


def miller_rabin_test():
    miller_results = list()
    miller_counter = 0
    for i in range(1,1000001):    
        if is_prime_miller_rabin(i, 1):
            miller_counter += 1
        if i == 10 or i == 100 or i == 1000 or i == 10000 or i == 100000 or i == 1000000:
            miller_results.append(miller_counter)
    return miller_results


def plot():  
    solovay_results = solovay_test()
    true_results = [4, 25, 168, 1229, 9592, 78498]
    difference_solovay = list()
    for i in range(len(true_results)):
        difference_solovay.append(solovay_results[i] - true_results[i])
    x_labels = [1,2,3,4,5,6]
    plt.bar(x_labels, difference_solovay, width = 0.5, color = "blue")
    for i_x, i_y in zip(x_labels, difference_solovay):
        plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))
    plt.title("False Alarms Using 10 Iterations")
    plt.xlabel("Primes Up to 10^")
    plt.ylabel("Number of False Positives")
    plt.show()

plot()
