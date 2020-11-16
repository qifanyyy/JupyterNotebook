print("Python started")

def euclideanAlgorithmToSimplifyFractions(numer, denom): 
    intialNumer = numer
    intialDenom = denom 

    if numer == 0 or denom == 0:
        print("one of the values entered is zero!")
        exit()
    
    numer = abs(numer)
    denom = abs(denom)
    
    listOfRemainders = []

    r = int(max(numer, denom) / min(numer, denom))
    remainder = int( (max(numer, denom)) - (min(numer, denom) * r) )
    GCD = int(0)

    listOfRemainders.append(remainder)

    while remainder != 0:
        numer = denom
        denom = remainder
        r = int(max(numer, denom) / min(numer, denom))
        remainder = int( (max(numer, denom)) - (min(numer, denom) * r) )
        listOfRemainders.append(remainder)
    
    if len(listOfRemainders) > 2:
        GCD = int( listOfRemainders[len(listOfRemainders) - 2] )
        
    else:
        GCD = int((min(numer, denom)))
    
    print("Greatest Common Divisor: " + str(GCD))
    print("Intial Fraction: " + str(intialNumer) + "/" + str(intialDenom) + "  ->  " + "Simplified Fraction: " + str(int(intialNumer/GCD)) + "/" + str(int(intialDenom/GCD)))


euclideanAlgorithmToSimplifyFractions(7777, -4949)

print("")
print("Python Ended")