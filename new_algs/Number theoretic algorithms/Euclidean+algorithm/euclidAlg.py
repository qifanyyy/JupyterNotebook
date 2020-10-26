def findGCD(a, b, verbose=False):
    '''Implementation of Euclid's Algorithm for finding gcd(a, b)

    Args:
        a, b (int): the integers whoose gcd is to be found

    Returns:
        int: the number of algorithm iterations performed until the gcd was found
    '''
    r = [a, b] # Initlialize list of remainders

    # Generate succesive remainders
    while r[-1] != 0:
        #print(r[-2] % r[-1])
        r.append(r[-2] % r[-1])

    # Return results
    if verbose:
        print('gcd({}, {}) = {}'.format(a, b, r[-2]))
    return len(r) - 2 # Number of iterations of the algorithm performed
