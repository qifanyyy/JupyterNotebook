#Program to implement Booth's Algorithm for Multiplication
#Author - Navendra Jha

# Function to Convert integer values (decimal number) to their binary representation
# Parameter : n = A decimal number in integer format
def convert_to_binary(n, l=8):
    return ("{0:0%db}" %l).format(n)

# Function to Convert binary number to their decimal format or integer representation
# Param : b = A binary number in string format
def convert_to_integer(b):
    return int(b,2)

z = 8

#Function to Bitflip the binary number
#Paramete : a = A decimal number which is first converted to binary number and then bit flipped.
def bit_flip(a):
    a = convert_to_binary(a)
    b = ""
    for w in a:
        if w == '1':
            w = '0'
        else:
            w = '1'
        b += w
    return b


# Function to get Twos Complement of a given binary number
# Parameter : b = A binary number in string format
def get_twos_complement(b):
    w = bit_flip(b)
    one = convert_to_binary(1)
    a = add_binary(w, one)
    a = a[-8:]
    return a

# Function to Add two binary numbers
# Parameter : Two binary numbers as string
def add_binary(a, b, l=8):
    return convert_to_binary(int(a, 2) + int(b, 2))


#Function to get RightMost Bit of a number
#Parameter : A binary number as string
def getRMB(a):
    return a[len(a)-1:]

#Function to implement right shift
def right_shift(A):
    A = convert_to_integer(A)
    b = convert_to_binary(A >> 1, 16)
    return b


#Fucntion for multiplication using Booth's Algorithm
#Parameters : Two Decimal number in integer format
def multiply(a,b):
    A = convert_to_binary(0)
    B = ""
    q=""
    B_Comp = ""

    if(a < 0):  #For Negative Number
        a *= -1
        B = get_twos_complement(a)
        B_Comp = convert_to_binary(a)
    else:
        B = convert_to_binary(a)
        B_Comp = get_twos_complement(a)

    if(b<0):  #For Negative Number
        b *= -1
        q = get_twos_complement(b)
    else:
        q = convert_to_binary(b)


    q1 = '0'

    print("A = ", A)
    print("B = ", B)
    print("B_Comp = ", B_Comp )
    print("q = ", q)

    count = z
    step = 1

    while(count>0):
        q0 = getRMB(q)
        print("\nStep %d :" %step)

        #For the cases where q0 and q-1 are both 0 or 1
        if ((q0 == '0') and (q1 == '0')) or ((q0 == '1') and (q1 == '1')):
            print("Opcode = " , q0+q1, " So, The operation followed is RSA")
            c = A + q + q1
            c = right_shift(c)
            c = A[0] + c
            A = c[:z]
            q = c[z:2*z]
            q1 = c[len(c)-1]
            print("A = ", A, "q = ", q, "New q1 = ",q1)

        #For the cases where q0 is 0 and q-1 is 1
        elif (q0 == '0') and (q1 == '1'):
            print("Opcode = " , q0+q1, " So, The operation followed is Add + RSA")
            A = add_binary(A, B, 8)
            A = A[-8:]
            c = A + q + q1
            c = right_shift(c)
            c = A[0] + c
            A = c[:z]
            q = c[z:2*z]
            q1 = c[len(c)-1]
            print("A = ", A, "q = ", q, "New q1 = ",q1)

        #For the cases where q0 is 1 and q-1 is 0
        elif (q0 == '1') and (q1 == '0'):
            print("Opcode = " , q0+q1, "So, The operation followed is Subtract + RSA")
            A = add_binary(A, B_Comp, 8)
            A = A[-8:]
            c = A + q + q1
            c = right_shift(c)
            c = A[0] + c
            A = c[:z]
            q = c[z:2*z]
            q1 = c[len(c)-1]
            print("A = ", A, "q = ", q, "New q1 = ",q1)

        count-=1
        step+=1

    return A+q

#A utility function to display result
#Parameter : A Binary number as string
def printResult(a):
    res = ""
    if a[0] == '1':
        i = convert_to_integer(a)
        b = bit_flip(i)
        one = convert_to_binary(1)
        res = add_binary(b, one)
    else:
        res = a

    value = convert_to_integer(res)
    if a[0] == '1':
        value*=-1

    print("The result in decimal form is " , value)


#The booth multiplication fucntion
def boothMultiplication(a,b):
    c = (multiply(a,b))
    print("The Result in binary form is ", c)
    printResult(c)

#The main driver function
def main():
    print("************** Binary Multiplication using Booth's Algorithm")
    is_binary = False
    print("Is input a binary number? Y/N")
    s =str(input())
    if(s == "Y"):
        is_binary = True
    elif s != "N":
        print("Bad Input.. Re-Enter the choice")
        exit()
    print("Enter the number for the first variable = ")


    a = ""
    b = ""
    if (is_binary):
        s = str(input())
        inp = ""
        if s[0] == '1':
            i = convert_to_integer(s)
            q = bit_flip(i)
            one = convert_to_binary(1)
            inp = add_binary(q, one)
        else:
            inp = s

        a = convert_to_integer(inp)
    else:
        s = int(input())
        a = s

    print("Enter the number for the second variable = ")
    if (is_binary):
        t = str(input())
        inp = ""
        if t[0] == '1':
            i = convert_to_integer(s)
            q = bit_flip(i)
            one = convert_to_binary(1)
            inp = add_binary(q, one)
        else:
            inp = s
        b = convert_to_integer(inp)
    else:
        t = int(input())
        b = t


    print("The Result with calculation is as follows : ")
    boothMultiplication(a,b)


if __name__ == "__main__":
   main()



















