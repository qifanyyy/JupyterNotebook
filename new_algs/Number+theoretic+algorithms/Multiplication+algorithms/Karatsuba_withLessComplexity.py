from math import ceil

# This approach is Divide and Conquer, we can multiply two integers in less time complexity
# We divide the given numbers in two halves. Let the given numbers be A and B.
# This method is for multiply two number
# First number is provided as A and second number is provided as B
def numberMultiplication(A, B):
    A = str(A)
    B = str(B)

    # checking the length of both the numbers
    if len(A) == 1 and len(B) == 1:     # if length of both the number is 1,then multiply them
        return int(A) * int(B)
    if len(A) < len(B):                 # if length of the first number is less than the length of the second ,  zero's are padded to A to make its length equal to B
        A = A.zfill(len(B))
    elif len(B) < len(A):               # if length of the second number is less than the length of the first , zero's are padded to B to make its length equal to A
        B = B.zfill(len(A))

    max_len=len(A)                      # length is stored in max_length

    split_position = int(ceil(max_len / 2))     # split_position is half of the max_len(ceil is for odd length number)

    # splitting number to two parts on the basis of split position
    A1 = A[:-split_position]
    A2 = A[-split_position:]
    B1 = B[:-split_position]
    B2 = B[-split_position:]

    #printing intermediate values after splitting of A and B
    file.write("\n--------------------------------")
    file.write("\nIntermediate Values of A1, B1 after partition:")
    file.write("\n--------------------------------")
    file.write("\nA : " + A + "  A1 : " + A1 + " A2 : " + A2)
    file.write("\nB : " + B + "  B1 : " + B1 + " B2 : " + B2)

    A1_B1 = numberMultiplication(A1, B1)        # recursive call to multiply A1 and B1 part
    A2_B2 = numberMultiplication(A2, B2)        # recursive call to multiply A2 and B2 part

    P = numberMultiplication(int(A1) + int(A2), int(B1) + int(B2))   # recursive call to multiply A1+A2 and B1+B2 part

    result = (A1_B1 * 10 ** (2 * split_position)) + ((P - A1_B1 - A2_B2) * 10 ** (split_position)) + A2_B2
    return result


# Path of file is provided as inputfile
# x and y for storing two digit
# numbers is a list to save data of input file
def readInputAndMultiply(filename):

    x = None
    y = None
    numbers = []

    # Reading file line by line
    with open(filename, 'r') as infile:
        for line in infile:
            if line.strip():
                temp = line.strip()                                         # extra leading and trailing spaces are removed
                if temp.isdigit():                                          # checking whether user is providong valid number or not
                    numbers.append(temp)                                    # if valid, then adding to numbers list
                else:
                    file.write("\nNot a valid number.")                     # in case of number is not valid,writing error message to output file.
                    temp = None

    for i, number in enumerate(numbers):
        if i == 0:
            x = number
        if i == 1:
            y = number

    if len(x) > 1 and len(y) > 1:                                           # length check whether it is a valid number
        file.write("1st number, A: " + x)
        file.write("\n2nd number, B: " + y)
        file.write("\n--------------------------------\nResult: > " + x + "  x " + y + "  = " + str(numberMultiplication(x, y)))  #Calling the multiplication function
        file.write("\n--------------------------------")

    else:
        file.write("\nEither x or y is invalid.")                            # in case of number is not valid,writing error message to output file.


if __name__ == '__main__':
    file = open('outputPS3.txt', 'w')
    readInputAndMultiply('inputPS2.txt')
    file.close()