#RSA defacto' – Proof-of-concept 
#RSA public key (semi prime) factoring algorithm

#Copyright 2016 Goldcove a.k.a. 2f426c5f72137f8ba47eb4db48c475c98ee5ba82de1f555b7902d2c5975fa2a7 (sha256). 
#This work is licensed under a GPLv3 or later license. 

#
# Python proof-of-concept
#

from math import sqrt

#Semiprime (RSA public key/modulus). This is what we're factoring
num=6037*9803 #2213*911 #2213*227 


def getnewnr(x, y, carry, num):
    """Calcualtes the next numbers"""
    y-=2 #Only odd numbers can be prime, subtract 2.
    x+=(x*2+carry)/y #(2 rows + carry) over y
    carry=num-(x*y)
    return x, y, carry

def initnumber(num):
    """Get initial value of x, y and carry"""
    x = int(sqrt(num))
    #We can also check for last digit 1, 3, 7 or 9 as prime number must end with one of these.
    if not x & 1: #not odd number
        x+=1
    y=num/x
    if not y & 1: #not odd number
        y-=1
    carry=num-x*y
    return x,y,carry

#MAIN
iter=1
x,y,carry = initnumber(num)
print "Semiprime: %d" % num
print "Start ratio x/y: %0.3f. x=%d y=%d carry=%d" % (float(x)/float(y),x,y,carry)

while carry <> 0:
    iter+=1
    x, y, carry = getnewnr(x,y,carry,num)

print "End ratio x/y: %0.3f" % (float(x)/float(y))
print "SUCCESS! Prime 1: %d Prime 2: %d" % (x, y)
print "Iterations: %d" % iter
