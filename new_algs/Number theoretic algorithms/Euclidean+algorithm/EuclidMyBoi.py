#Sk Ayon Euclidean Division Algorithm
def GCD(a,b):
    if a < 0:
        a = -a                      #In my program, we only want the magnitude of
    if b < 0:                       #the GCD
        b = -b
    if a < b:
        temp = b                    #this is to make sure that b is always
        b = a                       #going to be less than or equal to a
        a = temp
    if a % b == 0:
       return b
    else:
        return GCD(b,a%b)
        
nums = input("Hello friend. Give me two numbers separated by spaces and I will give you their GCD\n")
split_nums = str.split(nums)
first_num = int(split_nums[0])
second_num = int(split_nums[1])
if first_num == 0 and second_num == 0:
    print("You cannot divide by 0")
else:
    the_GCD = GCD(first_num,second_num)
    print("A GCD of " + str(first_num) + " and " + str(second_num) + " is " + str(the_GCD))
