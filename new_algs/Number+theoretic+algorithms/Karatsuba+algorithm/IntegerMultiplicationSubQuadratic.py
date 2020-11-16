import math

def zeroPad(numberString, zeros, left = True):
    """Return the string with zeros added to the left or right."""

    for i in range(zeros):
        if left:
            numberString = '0' + numberString
        else:
            numberString = numberString + '0'
    return numberString

def RecursiveMultiplication(A, B):
    """ Function to compute multiplication using divide and conquer algorithm """

    A = str(A)
    B = str(B)
    
    if len(A) == 1 and len(B) == 1:
        return int(A) * int(B)
    if len(A) < len(B):
        A = zeroPad(A, len(B) - len(A))
    elif len(B) < len(A):
        B = zeroPad(B, len(A) - len(B))

    max_len = max(len(A), len(B))

    split_position = math.ceil(max_len/2)

    #Split numbers in high and low order of digits for both the numbers
    A1 = A[:-split_position] 
    A2 = A[-split_position:]
    B1 = B[:-split_position]
    B2 = B[-split_position:]
    
    f.write("\n--------------------------------")
    f.write("\nIntermediate Values of A1, B1 after partition:")
    f.write("\n--------------------------------")
    f.write("\nA : "+ A + "  A1 : "+ A1 + " A2 : " + A2)
    f.write("\nB : "+ B + "  B1 : "+ B1 + " B2 : " + B2)
    
    #Steps for sub quadratic calculation with 3 multiplications
    A1_B1 = RecursiveMultiplication(A1, B1)
    A2_B2 = RecursiveMultiplication(A2, B2)

    P = RecursiveMultiplication(int(A1) + int(A2), int(B1) + int(B2))

    return (A1_B1*10**(2*split_position)) + ((P - A1_B1 - A2_B2)*10**(split_position)) + A2_B2

if __name__ == '__main__':
    filename = 'inputPS2.txt'
    x, y = "", ""
    num_list = []
    outfile = 'outputPS2.txt'
    f = open(outfile, 'w')

    with open (filename, 'r') as infile:
        for line in infile:
            if line.strip():
                num = line.strip()
                if not num.isdigit():
                    f.write("\nNot a valid number")
                    num = ""
                else:
                    num_list.append(num)
    
    for i, number in enumerate(num_list):
        if i == 0:
            x = number
        if i == 1:
            y = number
            
    if len(x) > 1 and len(y) > 1:
        f.write("--------------------------------")
        f.write("\nFirst Number is: " + x)
        f.write("\nSecond Number is: " + y)
        f.write("\nResult: > " + x + "  x " + y + "  = " + str(RecursiveMultiplication(x, y)))
        f.write("\n--------------------------------")

    else:
        f.write("\nEither x or y is invalid")
    f.close()