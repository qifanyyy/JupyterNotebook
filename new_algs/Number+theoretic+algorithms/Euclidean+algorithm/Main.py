__author__ = 'louciampanelli'
#
# this is a program that displays the steps of the euclidean algorithm

# make euclidean a function so it can be imported into other programs
def euclidean(num1, num2):

    # initial numbers from user
    n = num1
    m = num2

    # if n is less than m, flip n and m
    if n < m:
        temp = n
        n = m
        m = temp

    # store original n and m values
    first_n = n
    first_m = m

    # create empty list to store the steps
    my_list = []

    # set remainder to 1, when it hits 0 the loop breaks
    remainder = 1

    # loop that divides, then keeps on dividing by the remainder
    # until the remainder == 0
    while remainder != 0:

        q = n // m
        remainder = n % m

        # display each step
        print ("{0} = {1} * {2} + {3}".format(n, m, q, remainder))

        # reorganize for next loop
        n = m
        m = remainder

        # add each q to the list
        my_list.append(q)

    # set gcd to n, a and b are used while stepping through the list
    gcd = n
    a = 0
    b = 1

    # go through list to calculate the linear combo
    for i in reversed(my_list):
        z = b - (i * a)
        b = a
        a = z

    # set up string for linear combo
    combo = "{0} = {1} * {2} + {3} * {4}".format(gcd, a, first_m, b, first_n)

    # calculate lcm
    lcm = first_n * first_m / gcd

    # display lcm, gcd, linear combo
    print ("\nLMC: {0}".format(lcm))
    print ("GCD: {0}".format(gcd))
    print ("Linear Combination: " + combo)

# ----------------------- END OF FUNCTION --------------------------------------

# run program only if it is main.py otherwise this doesn't happen
if __name__ == '__main__':

    # ask user for n number, make sure it is an int
    nVal = None
    while nVal is None:
        try:
            nVal = int(raw_input("Please enter your first number\n"))
        except ValueError:
            print("You must enter an integer.")

    # ask user for m number, make sure it is an int
    mVal = None
    while mVal is None:
        try:
            mVal = int(raw_input("Please enter your second number\n"))
        except ValueError:
            print("You must enter an integer.")

    euclidean(nVal, mVal)