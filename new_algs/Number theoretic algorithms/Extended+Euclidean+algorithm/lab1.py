#udl computational tools for problem solving lab1
#humakal
#'19
import math 

def trial_div(m):
    divisors = []
    sqrt_m = math.sqrt(m)
    while (m % 2 == 0): 
        divisors.append(2) 
        m = m / 2
    for n in range(3,int(sqrt_m)+1): 
        while (m % n == 0): 
            divisors.append(n)
            m = m / n 
        n = n+1
    if (m > 2): 
        divisors.append(int(m))
    return divisors

def division_alg(m,n):
    # n = q.m + r
    if(m>0): 
        if(m>n):
            q=0
            r=m
        q=1
        while(n-(q*m)>=m):
            q = q + 1 
        r= n- (q*m)
        return(q,r)
    return(-1,-1) #error
    
def gcd(m,n):
    if(n != 0):
        return gcd(n, m%n)
    return m
    
def extended_gcd(n,d):
    s, old_s = 0, 1
    t, old_t = 1, 0
    while n != 0:
        q, r = d//n, d%n
        t = old_t - q * t
        s = old_s - q * s
        d,n, s,t, old_s, old_t = n,r, old_s, old_t, s,t
    gcd = d
    return old_s, old_t,gcd, t, s

def main():
    #print("TRIAL DIVISION")
    print(trial_div(18))
    
    #print("DIVISION ALGORITHM - (103,11)")
    print(division_alg(103, 11))

    #print("EUCLIDEAN GCD - (891555, 191415)")
    print(gcd(891555, 191415))

    #print("EXTENDED EUCLIDEAN GCD - (23,18)")
    old_s, old_t, old_r, t, s = extended_gcd(7,11)
    print("Bezout coefficients:", old_s, old_t)
    print("GCD:", old_r)
    print("Quotients:", t, s)

if __name__== "__main__":
  main()