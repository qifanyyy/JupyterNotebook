# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 13:31:31 2017

@author:Ravindra Kompella
"""
import sys
sys.version

fN = int(input("Input the first number: "))
sN = int(input("Input the second number: "))

def doMultiply(fN,sN):
    
    if fN < 10 or sN < 10:
        return fN*sN
    n = max(len(str(fN)), len(str(sN)))
    
    nby2= int(n/2)
    
    a, b = divmod(fN, 10**nby2)
    c, d = divmod(sN, 10**nby2)
    
    
    ac = doMultiply(a,c)
    bd = doMultiply(b,d)
    ad_bc = doMultiply((a+b),(c+d)) - ac - bd
    product = (10**n)*ac+(10**nby2)*(ad_bc)+bd
              
    return product
        
s = str(doMultiply(fN,sN))
print(s)
    
