# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 14:17:33 2019

@author: DSU
"""

class MyBigIntegers:
    # can't create multiple constructors in python, so change input based
    # no input makes it be 0
    # a list of input turns every number in a list into part
    # a string input uses a string with x specified base
    def __init__(self, input=None, base=10):
        if input is None:
            self.integer = '0'
        elif isinstance(input, list):
            self.integer = ''.join(str(x) for x in input).lstrip('0')
            if self.integer is '': self.integer = '0'
        elif isinstance(input, str):
            self.integer = str(abs(int(input, base)))
    
    # returns the length of the string
    def __len__(self):
        return len(self.integer)
    
    # adds two bigints and returns their sum as a bigint
    def __add__(self, other):
        rst = ''
        if len(self.integer) > len(other.integer):
            num1, num2 = other.integer, self.integer
        else:
            num1, num2 = self.integer, other.integer
        
        diff = len(num2) - len(num1)
        num1 = '0' * diff + num1
        
        carry = 0
        rst= list()
        for i, j in zip(num1[::-1], num2[::-1]):
            cur = ord(i) + ord(j) - 2 * ord('0') + carry
            carry = cur // 10
            rst.append(str(cur % 10))
        return MyBigIntegers(['1'] + rst[::-1] if carry else rst[::-1])
    
    # multiplies two bigints and returns their product
    def __mul__(self, other):
        # turn digits into numbers
        num1 = [int(x) for x in self.integer[::-1]]
        num2 = [int(x) for x in other.integer[::-1]]
        
        # add up
        ans=[0] * (len(num1)+len(num2))
        for i in range(len(num1)):
            for j in range(len(num2)):
                ans[i+j] += num1[i] * num2[j]
        
        # convert
        carry = 0
        for i in range(len(ans)):
            ans[i] += carry
            carry = ans[i] // 10
            ans[i] %= 10
        
        # create
        return MyBigIntegers(ans[::-1])
            
    # returns a string, specifying if you want base 16
    def ToString(self, base16=False):
        if base16:
            # get hex number
            start = hex(int(self.integer))[2:]
            # finished product
            finish = list()
            # length for reference
            length = len(start) - 1
            # append each, adding colons as necessary
            for i, x in enumerate(start[::-1]):
                finish.append(x)
                if i != length and i%4 == 3:
                    finish.append(':')
            
            return ''.join(finish[::-1])
                
        else:
            return self.integer

"""
Driver code
verifies that we have working addition
"""
if __name__ == '__main__':
    
    A = ['523004898858735521', '220758617692186442', '460674828835159568',\
         '142038006856929955', '536121496772617388', '112137493324750603',\
         '690796069846053026', '814564078556167347', '180512479842461002',\
         '646588448516637981', '444556959154324505', '206725965987503988']
    B = ['810017810852848964', '69101654073787491', '235835651116434816',\
         '962022575760609851', '584994243195327903', '141893478896824908',\
         '278386261950154281', '413574972226298198', '437062588034587455',\
         '187818575705627797', '402813271607194236', '467620374047189121']
    C = ['1333022709711584485', '289860271765973933', '696510479951594384',\
         '1104060582617539806', '1121115739967945291', '254030972221575511',\
         '969182331796207307', '1228139050782465545', '617575067877048457',\
         '834407024222265778', '847370230761518741', '674346340034693109']
    
    for a, b, c in zip(A, B, C):
        assert (MyBigIntegers(a) + MyBigIntegers(b)).ToString() == c
    
    
    
    
    
def multiply(num1: str, num2: str) -> str:
    nums1 = [int(i) for i in num1][::-1]
    nums2 = [int(i) for i in num2][::-1]
    res = [0]*(len(nums1)+len(nums2))
        
    for i, a in enumerate(nums1):
        for j, b in enumerate(nums2):
            res[i+j] += a * b
    for i in range(len(res)-1):
        res[i+1] = res[i+1] + res[i] // 10
        res[i] = res[i] % 10
    for i in range(len(res)-1,-1,-1):
        if res[i]!=0:
            return ''.join([str(k) for k in reversed(res[0:i+1])])
    return '0'
                
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    