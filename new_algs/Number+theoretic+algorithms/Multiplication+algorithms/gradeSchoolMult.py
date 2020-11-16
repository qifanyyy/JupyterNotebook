#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Grade School Multiplication algorithm #
#########################################
# 1234 x 5678      
# -----------
#        9872    *for each of partial mults we need n multiplications and at most n carry additions
#       8638o       so we have 2n operations
#      7404oo    *we have n partial multiplications, so number of operations is at most 2n**2
#     6170ooo       therefore, time complexity of Grade School Multiplication is O(n**2)


def gradeSchoolMult(x, y):
    """Multiply two integers using the grade-school algorithm."""
    #convert x and y to strings for easier manipulation
    x = str(x)
    y = str(y)
    
    #sum of partial multiplications to be returned
    sumPartial = 0
    
    #loop trough digits of x, LSB to MSB
    for i in range(len(x)-1, -1, -1):
        #keeping track of carry
        carry = 0
        #partial multiplications as str, with added zeros
        partial = '0' * (len(x)-1-i)
        #loop trought digits of y, LSB to MSB
        for j in range(len(y)-1, -1, -1):
            #mult digits of x and y, keeping track of carry
            z = int(x[i])*int(y[j])
            z += carry
            #convert to string for easier manipulation
            z = str(z)   
            #carry
            if(int(z)>9):
                carry = int(z[0])
            else:
                carry = 0
            #adding digit to partial mult
            partial = z[-1] + partial
        #taking care of leftover carry
        if carry > 0 :
            partial = str(carry) + partial
        #adding partial multiplication to final sum
        sumPartial += int(partial)
    return sumPartial


print(gradeSchoolMult(1234,5678))
