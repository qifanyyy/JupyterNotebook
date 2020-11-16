import numpy as np
import random as rnd

"""
Following program consist of functions for:
    - Euclid's Algorithm and                                                    https://en.wikipedia.org/wiki/Euclidean_algorithm
    - Bézout's Identity.                                                        https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity
Euclid's Algorithm is a nice and straight forward way
to find greatest common divider for two given numbers.
This is useful knowledge example in modular arithmetics,
algebra and number theory.
If greatest common divider of two given numbers is 1,
the numbers are called to be relative primes for eachother.
    Say, if "gdc( a, b ) = 1" for some numbers 'a' and 'b',
    then "ax + bx = 1" for some values of 'x' and 'y'.
    Now we know couple of things. First of all
    number 'ax' is said to be congruent with 1 mod 'b' and
    similiarily number 'bx' is congruent with 1 mod 'a'
    in terms of modular arithmetic.                                             https://en.wikipedia.org/wiki/Modular_arithmetic
    This also means that if number 'a' belongs to a
    algebraic structure called ring Z_b,                                        https://en.wikipedia.org/wiki/Ring_(mathematics)
    then 'a' has an inverse 'x' that also belongs to the
    same ring, such that "ax = 1".
    This is equivalent for number 'b' an 'y' in a ring Z_a.

OBS!    Bézout's Identity is defined first because it is called
        inside the Euclid's Algorithm.
"""

    #########################
    #   Bézout's identity   #
    #########################

def bezoutID( list ):                                                           #   FUNCTION: Bézout's identity uses values of Euclid's Algorithm to
    print("Bézout's Identity:")                                                 #             find a proper presentation for greatest common divisor
                                                                                #             as a equation called Bézout's Identity:
                                                                                #                                           "ax + bx = c".

    vector = list[ len( list ) - 1]                                             #   Pick the last vector from the list for initial values.
    a = vector[ 0 ]                                                             #   Initialize the starting values for variables 'a',
    x = 1                                                                       #   'x',
    b = vector[ 2 ]                                                             #   'b',
    y = vector[ 1 ]                                                             #   'y' and
    gcd = vector[ 3 ]                                                           #   initialize the already known value of greatest common divisor.

    print( "\n"                                                                 #   Print the first equation:
            + str( a ) + " * "                                                  #                   "ax + bx = c",
            + str( x ) + " - "                                                  #                    where 'c' = greatest common divisor.
            + str( b ) + " * "
            + str( y ) + " = "
            + str( gcd ) )

    aStd = str( a )                                                             #   Initialize a string version of a and
    bStd = str( b )                                                             #   'b' that will come handy later.

    for i in range( len( list ) - 1, 0, -1):                                    #   Iterate the list from one step from the end to beginning
                                                                                #   (or alternavely from bottom to top).
        vector = list[ i - 1 ]                                                  #   Pick a vector from next step to compare current values of equation.

        if( b == vector[ 3 ] ):                                                 #   Test if the value of 'b' is equal to remainder value
                                                                                #   from the vector = list[ i - 1 ].
            bStd = str( vector[ 0 ] )

            print( aStd + " * "                                                 #   Print the next step where value of 'b' is replaced with '(a - bx)'
                    + str( x ) + " - "                                          #   from the vector = list[ i - 1 ].
                    + "( " + str( vector[ 0 ] ) + " - "
                    + str( vector[ 2 ] )  + " * "
                    + str( vector[ 1 ] ) + " )" + " * "
                    + str( y ) + " = "
                    + str( gcd ) )

            x += y * vector[ 1 ]                                                #   Correct the value of 'x'.
            b = vector[ 0 ]                                                     #   Set 'b' equal to 'a' from vector = list[ i - 1 ].

            print( aStd + " * "                                                 #   Print the step where all the values are corrected
                    + str( x ) + " - "                                          #   and nicely presedented.
                    + bStd + " * "
                    + str( y ) + " = "
                    + str( gcd ) )

        if( a == vector[ 3 ] ):                                                 #   Test if the value of 'a' is equal to remainder value
                                                                                #   from the vector = list[ i - 1 ].
            aStd = str( vector[ 0 ] )

            print( "( " + str( vector[ 0 ] ) + " - "                            #   Print the next step where value of 'a' is replaced with '(a - bx)'
                    + str( vector[ 2 ] ) + " * "                                #   from the vector = list[ i - 1 ].
                    + str( vector[ 1 ] ) + " )" + " * "
                    + str( x ) + " - "
                    + bStd + " * "
                    + str( y ) + " = "
                    + str( gcd ) )

            y += x * vector[ 1 ]                                                #   Correct the value of 'y'.
            a = vector[ 0 ]                                                     #   Set 'a' equal to 'a' from vector = list[ i - 1 ].

            print( aStd + " * "                                                 #   Print the step where all the values are corrected
                    + str( x ) + " - "                                          #   and nicely presedented.
                    + bStd + " * "
                    + str( y ) + " = "
                    + str( gcd ) )


    print( "\n"                                                                 #   Print the final form of the Bézout's Identity.
            + "Final form: "
            + aStd + " * "
            + str( x ) + " - "
            + bStd + " * "
            + str( y ) + " = "
            + str( gcd ))

    return                                                                      #   Bézout's Identity -function will end here.

    #########################
    #   Euclid's Algorithm   #
    #########################

def euclidsAlg( a, b ):                                                         #   FUNCTION: Euclid's Algorithm finds the greatest common divisor
    print("Euclid's Algorithm: \n")                                              #             of given whole numbers 'a' and 'b'.

    times = int( np.floor( a / b ) )                                            #   How many times number 'b' goes in number 'a'.
    remainder = a % b                                                           #   Remainder of division of 'a' with 'b'.
    gdc = str( str( a ) + ", " + str( b ) )                                     #   Makes a string for the print function in the end of
                                                                                #   the Euclid's Algorithm -function.
    list = []                                                                   #   Create a list to keep record of the algorithm. This list
                                                                                #   will be given for Bézout's Identity -function as a parameter.

    while( remainder >= 1 ):                                                    #   Makes sure that current remainder is larger or equal than 1.
        remainder = a % b                                                       #   Revalues the remainder with every while loop.
        times = int( np.floor( a / b ) )                                        #   Revalues the times coefficient with every while loop.

        print( str( a ) + " = "                                                 #   Prints the state of the equation:
                + str( times ) + " * "                                          #                           "a = times * b + remainder".
                + str( b ) + " + "
                + str( remainder ) )

        if( remainder >= 1):                                                    #   Makes sure that current value of remainder is
                                                                                #   larger than 1 to revalue some varibles.
            list.append([a, times, b, remainder])                               #   Add a vector of current values to the list.
            a = b                                                               #   Revalues 'a' with value of 'b' for the next while loop.
            b = remainder                                                       #   Revalues 'b' with value of remainder for the next while loop.

    print( "=> gdc( " + gdc + " ) = " + str( b ) + "\n" )                       #   Print the greatest common divisor of given values.

    if( len(list) > 1 ):
        bezoutID( list )                                                        #   Function call for Bézout's Identity.

    return                                                                      #   Euclid's Algorithm -function will end here.

    #####################################
    #   Initialization & Function call  #
    #####################################

a = rnd.randint( 1, 1000 )                                                      #   Gives a random value 1 <= 'a' <= 1000.
print( "Value of a is " + str( a ) )
b = rnd.randint( 1, a )                                                         #   Gives a random value 1 <= 'b' <= 'a'.
print( "Value of b is " + str( b ) + "\n" )
print( "Find the greatest common divisor for numbers "
        + str( a ) + " and " + str( b )
        + " by using Euclid's Algorithm. \n" )
euclidsAlg( a, b )                                                              #   Function call for Euclid's Algorithm.
