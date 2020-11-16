
# coding: utf-8

# In[22]:


# Calculate x^pox in O(logn): n is the power of x (pox)
def power(x, pox):
    
    # Base case
    if pox == 0:
        return 1
    
    temp = power(x, pox//2)
    # Power is even
    if pox % 2 == 0:
        
        # x^4 = x^2 * x^2
        return temp * temp 
    
    # Power is odd
    else:
        
        # x^5 = x * x^2 * x^2
        return x * temp * temp
    
     


# In[23]:


# Get the length of val in O(n): n is input size
# ex. val = 1243 would return 4
# ex. val = 124 would return 3
def length(val):

    count = 0;
    while val != 0:  

        val = val//10
        count += 1

    return count
    


# In[24]:


# Calculate x*y in O(n^1.585)
def multiplyks(x,y):
    
    xLen = length(x)
    yLen = length(y)
    # base case
    if xLen < 2 or yLen < 2:
        return x*y 
    
    else:
       
        n = xLen if xLen > yLen else yLen
        
        nHalfToPower = power(10, n//2)
        
        # Extract upper digits of x, ex. x = 100, 100/10^2 = 1
        xH = x // nHalfToPower
        # Extract lower digits of x, ex. x = 100, 100%10 = 0
        xL = x % nHalfToPower
        yH = y // nHalfToPower
        yL = y % nHalfToPower
        
        # Recursions
        a = multiplyks( xH, yH )
        d = multiplyks( xL, yL )
        e = multiplyks( xH + xL, yH + yL ) - a - d
        return a * nHalfToPower * nHalfToPower + e * nHalfToPower + d

    


# In[25]:


# Test different length and size against python implementation for correctness
import unittest
class TestMultiplyKsMethod(unittest.TestCase):  
    def test_multiplyks(self):
        self.assertTrue(multiplyks(10,10) == 10*10,"Not equal")
        self.assertTrue(multiplyks(1000,100000) == 1000*100000,"Not equal")
        self.assertTrue(multiplyks(99999,9999999) == 99999*9999999,"Not equal")
        self.assertTrue(multiplyks(234567894567,234692192456) 
                        == 234567894567*234692192456,"Not equal")
    


# In[26]:


# Run tests
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

