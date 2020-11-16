#!/usr/bin/python

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
#  file:   spigot.c
#  goal:   allows user to enter an output file name, then calculates pi
#          using the spigot algorithm and outputs the result to the file.
#  *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

# **************************************************************
# function: spigot
# output:   string containing pi result
# goal:     calculate pi result and write to result string
# **************************************************************
def spigot():
    # declare and initialize variables
    i = 0
    j = 0
    k = 0
    q = 0
    x = 0
    nines = 0
    predigit = 0
    precision = 1002
    temp = ''
    result = ''

    # create empty array a
    a = []

    # calculate array length and create array
    size = (10 * precision / 3) + 1

    # initialize array to (2,2,2,2,2,...,2)
    for i in range (0, size):
        a.append(2)

    # repeat this loop 'precis' times,depending on the desired precision
    for j in range (1, precision):
        q = 0
        
        # calculate q value by division
        for i in range (size, 0, -1):
           x = 10 * a[i-1] + q * i
           a[i-1] = x % (2 * i - 1)
           q = x / (2 * i - 1)

        a[0] = q % 10
        q = q / 10

        # append different digits based on q value
        if q == 9:
            # if q is 9, increment nines counter
            nines = nines + 1
        elif q == 10:
            # if q is 10 (overflow case), write 9 then predigit + 1
            result += str(predigit + 1)

            for k in range (0, nines):
                result += '0'

            predigit = 0
            nines = 0
        else:
            # if q is not 9 or 10, print predigit
            result += str(predigit)
            predigit = q
            if nines != 0:
                for k in range (0, nines):
                    result += '9'

                nines = 0
    result += str(predigit)
    result += '9'
    return result
    
# display intro message
print('')
print(' ------------------------------------')
print('    WELCOME TO MY SPIGOT ALGORITHM!')
print('           (python edition)')
print('    Built with love for CIS*3190')
print('    By: Maddie Gabriel (0927580)')
print(' ------------------------------------')
print('')

# get custom file name from user
fname = raw_input(' Enter output filename (with extension): ')

print('')
print(' ** Please wait while your result is calculating **');
print('')

# call function to calculate pi result
result = spigot()

# write result to file and tell user where to find it
file = open(fname, 'w')
file.write(result)
file.close()

print(' Done! Please see your result in the file: ' + fname);
print('')
