

w, h = 8, 5;
Matrix = [[0 for x in range(w)] for y in range(h)] 

def NWDistance(comparisonString, originalString, returnMax=False):
    
    if(len(comparisonString) > 20 or len(originalString) > 20):
        raise ValueError('Words must be 20 characters or less')

    match = 1
    orthoMismatch = 0.5
    phonoMismatch = 0
    mismatch = -3
    indel= -1
    foreignMismatch = -2
    

    #s = max(len(comparisonString), len(originalString))
    #w = s+2
    #h = s+2
    w, h = len(comparisonString)+2, len(originalString)+2
    Matrix = [[0 for x in range(w)] for y in range(h)]

    #Add Letters to matrix
    for i, c in enumerate(comparisonString):
        Matrix[0][i+2]=c
    for i, c in enumerate(originalString):
        Matrix[i+2][0]=c

    #Add intial values to matrix
    index = 1
    for i in range(h-1):
        Matrix[i+1][1]=(index-1)
        index = index-1

    index = 1
    for i in range(w-1):
        Matrix[1][i+1]=(index-1)
        index = index-1

    latestVal = 0
    #Iterating through each cell
    for i in range(h-2):
        for y in range(w-2):
            TopChar = Matrix[0][y+2]
            LeftChar = Matrix[i+2][0]
            AboveCell =  Matrix[i+1][y+2]
            LeftCell =  Matrix[i+2][y+1]
            DiagonalCell = Matrix[i+1][y+1]




            #if match
            if(TopChar == LeftChar):
                DiagonalScore = DiagonalCell+match
            #if mismatch
            if(TopChar != LeftChar):
                DiagonalScore = DiagonalCell+mismatch
            #if indel
            LeftScore = LeftCell+indel
            AboveScore = AboveCell+indel

            Matrix[i+2][y+2] = max(DiagonalScore, LeftScore, AboveScore)
            latestVal =  Matrix[i+2][y+2]


    if(returnMax==False):
        maxScore = NWDistance(originalString, originalString, True)
        minScore = NWDistance("QQQQQQQQQQQQQQQQQQQQ", originalString, True)
        

        try:
            percentScore = (latestVal - (minScore))/(maxScore - (minScore))
        except ZeroDivisionError:
            percentScore = 0
        #Print the matrix to the cmd line
        for row in Matrix:
            print(row)
        print("Distance =", percentScore*100,"%")
        print("Max score:",maxScore)
        print("Min score:",minScore)

    if(returnMax==True):
        return latestVal

NWDistance("cluann","cluann")


