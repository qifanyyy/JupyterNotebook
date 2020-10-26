''' ===================== HYBRID SELECTION STRATEGY (HSS) ======================
        Universidade Federal de Sao Carlos - UFSCar, Sorocaba - SP - Brazil

        Master of Science Project       Artificial Intelligence

        Prof. Tiemi Christine Sakata    (tiemi@ufscar.br)
        Author: Vanessa Antunes         (tunes.vanessa@gmail.com)
   
    ============================================================================ '''

import numpy as np

import validationIndexes

def objectives(partitions, dataset):
    f1 = []
    f2 = []

    con = getattr(validationIndexes, 'connectivity')
    var = getattr(validationIndexes, 'variance')

    for _ in range(0, len(partitions)):
        f1.append(var(partitions[_], dataset))
        f2.append(con(partitions[_], dataset))

    return f1, f2

def pareto_frontier(Xs, Ys, name, maxX = True, maxY = True):

    # Sort the list in either ascending or descending order of X
    # sort method average complexity is O(n(log n))
    myList = sorted([[Xs[i], Ys[i], name[i]] for i in range(len(Xs))], reverse=maxX)
    
    # Start the Pareto frontier with the first value in the sorted list
    p_front = [myList[0]]  
    p_frontUname = [myList[0][2]]
    lenP = 1

    # Loop through the sorted list
    for pair in myList[1:]:
        if  set(p_front[-1][:2]) == set(pair[:2]):
            #continue
            p_front.append(pair)

        elif maxY: 
            if pair[1] >= p_front[-1][1]: # Look for higher values of Y
                p_front.append(pair) # and add them to the Pareto frontier
                p_frontUname.append(pair[2])
                lenP +=1
        else:
            if pair[1] <= p_front[-1][1]: # Look for lower values of Y
                p_front.append(pair) # and add them to the Pareto frontier
                p_frontUname.append(pair[2])
                lenP +=1

    # Turn resulting pairs back into a list of Xs and Ys
    p_frontX = []
    p_frontY = []
    p_frontName = []
    for pair in p_front:
        p_frontX.append(pair[0])
        p_frontY.append(pair[1])
        p_frontName.append(pair[2])
    
    return p_frontX, p_frontY, p_frontName