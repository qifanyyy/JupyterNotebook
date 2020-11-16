import math
import time

def zeroPad(numberString, zeros, left = True):
    """Return the string with zeros added to the left or right."""
    for i in range(zeros):
        if left:
            numberString = '0' + numberString
        else:
            numberString = numberString + '0'
    return numberString
 
def gradeSchoolMultiplication(x, y):
    start = time.time()
    """Multiply two integers using the grade-school algorithm."""
    #convert to strings for easy access to digits
    x = str(x)
    y = str(y)
    #keep track of number of zeros required to pad partial multiplications
    zeroPadding = 0
    #sum the partial multiplications as we go
    partialSum = 0
    #loop over each digit in the second number
    for i in range(len(y) -1, -1, -1):
        #keep track of carry for multiplications resulting in answers > 9        
        carry = 0
        #partial multiplication answer as a string for easier manipulation
        partial = ''
        #pad with zeros on the right
        partial = zeroPad(partial, zeroPadding, False)
        #loop over each digit in the first number
        for j in range(len(x) -1, -1, -1):
            z = int(y[i])*int(x[j])
            z += carry
            #convert to string for easier manipulation
            z = str(z)
            #keep track of carry when answer > 9
            if len(z) > 1:
                carry = int(z[0])
            else:
                carry = 0
            #concatenate final answer to the left of partial string    
            partial = z[len(z) -1] + partial
        #if there's any carry left at the end concatenate to partial string
        if carry > 0:
            partial = str(carry) + partial
        #sum the partials as you go        
        partialSum += int(partial)
        #for the next digit of the second number we need another zero to the right
        zeroPadding += 1
    
    end = time.time()
    print(end - start)

    return partialSum

print(gradeSchoolMultiplication(111,101))
