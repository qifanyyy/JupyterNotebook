import math

#Save the list in a local variable
file = open("list.txt", "r")

l = []

tmp = 0
for x in file:
    l.append(x)
    l[tmp] = l[tmp][:-1]
    tmp+=1

file.close()

#Create the algorithm
Running = True

while Running == True:
    #Creates the left, middle, right variables
    firstNum = l[0]

    if len(l)%2==0:
        middle = len(l)/2
        middle -= 1
    else:
        middle = (len(l)-1)/2

    middle = math.floor(middle)
    middleNum = l[middle]

    lastNum = l[len(l)-1]

    #Start the algorithm
    print("Answer yes or no.")
    option = input(f"Is the number higher than {middleNum}: ").lower()

    if option == "yes":
        for x in range(middle+1):
            l.pop(0)
    elif option == "no":
        for x in range(middle+1, len(l)):
            l.pop()
    else:
        print(f"\n\nERROR: Answer not \"yes\" or \"no\". Please answer again.")

    print("\n\n")

    if len(l) == 1:
        break

print(f"Your number was {l[0]}.")