"""
Algorithms CSC 421 
Programming Assignment Closest Pair
Due: 7 NOV 2017
Author: Drew Stroshine
"""

import math
from operator import itemgetter


def readfile(filepath):
    """Extracts coordinates from a text file

    Reads a text file in the format of the files given for this programming 
    assignment, and extracts the ordered pairs of the coordinates stored in the 
    file.
    
    Args:
        filepath: A string representing the file path of the text file to read.
        
    Returns:
        A list of integer tuples where each tuple is an ordered pair for an 
        (x, y) coordinate.
    """
    
    with open(filepath, 'r') as f:
        data = f.readlines()
        
        coordinates = []        
        
        for line in data:
            temp = line.split()
            temp = [int(val) for val in temp] 
            temp = tuple(temp)
            coordinates.append(temp)
        
        return coordinates
    
def writefile(filepath, solution, testData):
    """Writes data to a text file

    Writes the closest pair solution to a text file.
    
    Args:
        filepath: A string representing the file path of the text file to 
                  write to.
        
        solution: A list of two integer tuples that are the ordered pairs for 
                  the (x, y) coordinate of the the closest pair.
                  
        testData: A string representing the title of the test data being used
        
    Returns:
        Void output
    """
    
    with open(filepath, 'a+') as f:
        f.write(testData + ' test file:\n\n')
        
        minDist = computeDistance(solution[0], solution[1])
        f.write('The minimum distance is:\n')
        
        f.write(str(minDist) + ': ' 
                + str(solution[0]) + '<--->' + str(solution[1]) + '\n\n\n')
 

def computeDistance(point1, point2):
    """Computes distance between two points

    Computes distance between two points using the distance formula as defined,
    distance = sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    
    Args:
        point1: An integer tuple that is an ordered pair for an (x, y) 
        coordinate of the first point.
        
        point2: An integer tuple that is an ordered pair for an (x, y) 
        coordinate of the second point.
        
    Returns:
        A floating point number that is the distance between the two points.
    """
    
    return math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)

    
def bruteForceClosestPair(S):
    """Finds the closest pair by brute force
    
    Finds the closest pair by calculating the distance between each point, and
    saving the minimum distance.
    
    Args:
        S: A list of integer tuples where each tuple is an ordered pair for an 
        (x, y) coordinate.
        
    Returns:
        A list of two integer tuples that are the ordered pairs for the (x, y) 
        coordinate of the the closest pair.
    """
    minimumDistance = computeDistance(S[0], S[1])
    closestPair = []
    
    for i in range(0, len(S)-1):
        for j in range(i+1, len(S)):
            tempDistance = computeDistance(S[i], S[j])
            
            if tempDistance <= minimumDistance:
                minimumDistance = tempDistance
                closestPair = [S[i], S[j]]
    
    return closestPair


def computeLeftRightSubsetsOfD(S, D):
    """Compute subsets that are to the left and right of vertical line D
    
    Computes the subsets Sleft and Sright of S that are to the left and right
    of the vertical line D.
    
    Args:
        S: A list of integer tuples where each tuple is an ordered pair for an 
        (x, y) coordinate.
        
        D: An integer value that represents the vertical line D a.k.a the 
        median x-coordinate of X.
        
    Returns:
        A list comprised of two lists [[Sleft], [Sright]] each containing 
        integer tuples where each tuple is an ordered pair for an (x, y) 
        coordinate.
    """
    
    Sleft = []
    Sright = []
    
    for point in S:
        if point[0] <= D:
            Sleft.append(point)
        
        if point[0] >= D:
            Sright.append(point)  
    
    return [Sleft, Sright]
    
     
def closestPairAlgo(S, X, Y):
    """Executes closest pair algorithm
        
    Computes the closest pair in a set of (x, y) coordinates by using a 
    divide-and-conquer technique.
    
    Args:
        S: A list of integer tuples where each tuple is an ordered pair for an 
        (x, y) coordinate.
        
        X: S sorted in non-descending order by x-coordinate.
        
        Y: S sorted in non-descending order by y-coordinate.
        
    Returns:
        A list of two integer tuples that are the ordered pairs for the (x, y) 
        coordinate of the the closest pair.
    """
    
    """ STEP 1 Base case that returns closest pair of S <= 3"""
    if len(S) <= 3:
        return bruteForceClosestPair(S)
    
    
    """ STEP 2 Compute D as median x-coordinate of X"""
    if len(X) % 2 == 0:
        middlePoint1 = X[int((len(X)/2)-1)]
        middlePoint2 = X[int(len(X)/2)]
        
        D = (middlePoint1[0] + middlePoint2[0]) / 2
    
    else:
        middlePoint = X[int(len(X)/2)+1]
        
        D = middlePoint[0]
    
    Ssplit = computeLeftRightSubsetsOfD(S, D)
    Sleft = Ssplit[0]
    Sright = Ssplit[1]
    
    
    """ STEP 3 Compute Xleft, Xright and Yleft, Yright from X and Y using D"""
    Xsplit = computeLeftRightSubsetsOfD(X, D)
    Xleft = Xsplit[0]
    Xright = Xsplit[1]
    
    Ysplit = computeLeftRightSubsetsOfD(Y, D)
    Yleft = Ysplit[0]
    Yright = Ysplit[1]
    
    
    """ STEP 4 Recursively compute closest pair of Sleft and Sright """
    PlQl = closestPairAlgo(Sleft, Xleft, Yleft)
    PrQr = closestPairAlgo(Sright, Xright, Yright)
    
    
    """ STEP 5 Set delta as min distance of closest pair in Sleft or Sright """
    Sleft = computeDistance(PlQl[0], PlQl[1])
    Sright = computeDistance(PrQr[0], PrQr[1])
    
    if Sleft < Sright:
        delta = Sleft
        
    else:
        delta = Sright
    
    
    """ STEP 6 Compute Ymid as pairs of Y where D - delta <= x <= D + delta"""
    Ymid = []
    
    for i in Y:
        if (D - delta) <= i[0] and i[0] <= (D + delta):
            Ymid.append(i)
    
        
    """ STEP 7 Compute closest pair of Ymid """
    if len(Ymid) >= 2:
        minDist = computeDistance(Ymid[0], Ymid[1])
        minPair = [Ymid[0], Ymid[1]]
        
        for i in range(0, len(Ymid)-1):
            if (i+7) >= len(Ymid):
                pair = bruteForceClosestPair(Ymid[i:(i+8)])
                tempDist = computeDistance(pair[0], pair[1])
                
                if  tempDist < minDist:
                    minDist = tempDist
                    minPair = pair
                           
            else:
                pair = bruteForceClosestPair(Ymid[i: len(Ymid)])
                tempDist = computeDistance(pair[0], pair[1])
                
                if  tempDist < minDist:
                    minDist = tempDist
                    minPair = pair            
        
        PmidQmid = minPair
        minimumPairs = minimumPairs = [PlQl, PrQr, PmidQmid]
        
    else: 
        minimumPairs = [PlQl, PrQr]
    
    """ STEP 8 Compare closest pair from left, right, and middle""" 
    minDist = computeDistance(PlQl[0], PlQl[1])
    minPair = PlQl
    
    for pair in minimumPairs[1:len(minimumPairs)]:
        tempDist = computeDistance(pair[0], pair[1])
        
        if tempDist < minDist:
            minDist = tempDist
            minPair = pair
        
    
    return minPair


"""/***************************** MAIN DRIVER *****************************/"""
 
""" 10 POINTS EXECUTION """      
""" Create a list of coordinates sorted by X and sorted by Y """
S = readfile('10points.txt')

X = sorted(S, key=itemgetter(0))
Y = sorted(S, key=itemgetter(1))

""" Call closestPairAlgo """
solution = closestPairAlgo(S, X, Y)

""" Write out file """
writefile('solutions_stroshine.txt', solution, '10 points')

""" Console Output """
print('10 points test file:\n')

minDist = computeDistance(solution[0], solution[1])
print('The minimum distance is:')

print(str(minDist) + ': ' + str(solution[0]) 
      + '<--->' + str(solution[1]) + '\n\n')



""" 100 POINTS EXECUTION """
""" Create a list of coordinates sorted by X and sorted by Y """
S = readfile('100points.txt')

X = sorted(S, key=itemgetter(0))
Y = sorted(S, key=itemgetter(1))

""" Call closestPairAlgo """
solution = closestPairAlgo(S, X, Y)

""" Write out file """
writefile('solutions_stroshine.txt', solution, '100 points')

""" Console Output """
print('100 points test file:\n')

minDist = computeDistance(solution[0], solution[1])
print('The minimum distance is:')

print(str(minDist) + ': ' + str(solution[0]) 
      + '<--->' + str(solution[1]) + '\n\n')



""" 1000 POINTS EXECUTION """
""" Create a list of coordinates sorted by X and sorted by Y """
S = readfile('1000points.txt')

X = sorted(S, key=itemgetter(0))
Y = sorted(S, key=itemgetter(1))

""" Call closestPairAlgo """
solution = closestPairAlgo(S, X, Y)

""" Write out file """
writefile('solutions_stroshine.txt', solution, '1000 points')

""" Console Output """
print('1000 points test file:\n')

minDist = computeDistance(solution[0], solution[1])
print('The minimum distance is:')

print(str(minDist) + ': ' + str(solution[0]) 
      + '<--->' + str(solution[1]) + '\n\n')

  



































