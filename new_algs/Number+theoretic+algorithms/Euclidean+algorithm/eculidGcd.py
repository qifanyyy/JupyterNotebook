def eGcd(firstNum, secondNum):
    if firstNum > secondNum:    # check which one is greater
        while(secondNum):       # loop will work till secondNum > 0
            firstNum, secondNum = secondNum, firstNum % secondNum
        return firstNum
    else:
        while(firstNum):
            secondNum , firstNum = firstNum , secondNum % firstNum
        return secondNum

# Take input from user.
num1 = int(input("Enter 1st number: "))
num2 = int(input("Enter 2nd number: "))

# function call.
print(eGcd(num1, num2))
