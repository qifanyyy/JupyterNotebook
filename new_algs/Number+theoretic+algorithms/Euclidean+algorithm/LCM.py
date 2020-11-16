#Owner: Overrideveloper
#Description: LCM Program 


from datetime import datetime
import os
import psutil 
startTime = datetime.now()

#Creating a function that uses two parameters 
def GCD(x, y):

   while(y):
       x, y = y, x % y

   return x
   
#Creating another function that uses two parameters 
def LCM(x, y):

    LCM = x*y//GCD(x, y)
    
    return LCM

#Taking user input 
FirstNumber = int(input("Enter the first number: /n"))

SecondNumber = int(input("Enter the second number: /n"))
ThirdNumber = int(input("Enter the third number: /n"))

FourthNumber = int(input("Enter the fourth number: /n"))

FifthNumber = int(input("Enter the fifth number: /n"))

output = LCM(FirstNumber, LCM(SecondNumber, LCM(ThirdNumber, LCM(FourthNumber,FifthNumber))))

print ("The Lowest Common Multiple of the five numbers is: ")

print (output)
process = psutil.Process(os.getpid())

print ("The execution time is ",(datetime.now()- startTime))
print("Memory consumption in Kilobytes is: ")
print(process.memory_info().rss / 1024)
