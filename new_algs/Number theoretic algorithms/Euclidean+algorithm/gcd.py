#Owner: Overrideveloper
#Description: GCD Program 


from datetime import datetime
import os
import psutil

startTime = datetime.now()

#Creating a function that uses two parameters 
def GreatestCommonDivisor(x, y):

   while(y):
       x, y = y, x % y

   return x

#Taking user input 
FirstNumber = int(input("Enter the first number: /n"))

SecondNumber = int(input("Enter the second number: /n"))

ThirdNumber = int(input("Enter the third number: /n"))

FourthNumber = int(input("Enter the fourth number: /n"))

FifthNumber = int(input("Enter the fifth number: /n"))


output = GreatestCommonDivisor (GreatestCommonDivisor (GreatestCommonDivisor(GreatestCommonDivisor(FirstNumber,SecondNumber ),ThirdNumber),FourthNumber),FifthNumber)

print ("The Greatest Common Divisor of the five numbers is: ")

print (output)
process = psutil.Process(os.getpid())

print ("The execution time is ",(datetime.now()- startTime))
print("Memory consumption in Kilobytes is: ")
print(process.memory_info().rss / 1024)
