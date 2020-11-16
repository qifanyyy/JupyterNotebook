#!/usr/bin/python
from constraint import *
import random
import sys
from time import time

MINLEN = 3

def main(puzzle, lines):
    puzzle = puzzle.rstrip().splitlines()
    while puzzle and not puzzle[0]:
        del puzzle[0]

    # Extract horizontal words
    horizontal = []
    word = []
    predefined = {}
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            char = puzzle[row][col]
            if not char.isspace():
                word.append((row, col))
                if char != "#":
                    predefined[row, col] = char
            elif word:
                if len(word) > MINLEN:
                    horizontal.append(word[:])
                del word[:]
        if word:
            if len(word) > MINLEN:
                horizontal.append(word[:])
            del word[:]

    # Extract vertical words
    vertical = []
    validcol = True
    col = 0
    while validcol:
        validcol = False
        for row in range(len(puzzle)):
            if col >= len(puzzle[row]):
                if word:
                    if len(word) > MINLEN:
                        vertical.append(word[:])
                    del word[:]
            else:
                validcol = True
                char = puzzle[row][col]
                if not char.isspace():
                    word.append((row, col))
                    if char != "#":
                        predefined[row, col] = char
                elif word:
                    if len(word) > MINLEN:
                        vertical.append(word[:])
                    del word[:]
        if word:
            if len(word) > MINLEN:
                vertical.append(word[:])
            del word[:]
        col += 1

    hnames = ["h%d" % i for i in range(len(horizontal))]
    vnames = ["v%d" % i for i in range(len(vertical))]
    #domain of letters variables
    alphabet= ["A", "B", "C" "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    
    #######################################define problem solver to use#############################################
    #problem = Problem(MinConflictsSolver())
    problem = Problem()
    
    ################################"#####"store words from dico by length##########################################
    wordsbylen = {}
    for hword in horizontal:
        wordsbylen[len(hword)] = []
    for vword in vertical:
        wordsbylen[len(vword)] = []
        
    for line in lines:
        line = line.strip()
        l = len(line)
        if l in wordsbylen:
            wordsbylen[l].append(line.upper())
    
    #######################define variables: letters and their domain: alphabet#########################################
    for hl,hword in enumerate(horizontal):
        for hi,hc in enumerate(hword):
            problem.addVariable("h%d%d" %(hl,hi), alphabet)
    for vl,vword in enumerate(vertical):
        for vi,vc in enumerate(vword):
            problem.addVariable("v%d%d" % (vl,vi), alphabet)        
    for hi, hword in enumerate(horizontal):
        words = wordsbylen[len(hword)]
        random.shuffle(words)
        problem.addVariable("h%d" % hi, words)
    for vi, vword in enumerate(vertical):
        words = wordsbylen[len(vword)]
        random.shuffle(words)
        problem.addVariable("v%d" % vi, words)

    
    ###########################constraint that words variables have to begin with initial letter variable placed of each word##################################
        
    for hl,hword in enumerate(horizontal):
        length= len(hword)
        for hi,hc in enumerate(hword):
            hci = hword.index(hc)
            if (hci == 0) :
                problem.addConstraint(lambda hw, h, hci=hci: hw[hci] == h,("h%d" % hl,"h%d%d" % (hl,hci),))
    
    for vl,vword in enumerate(vertical):
        length= len(vword)
        for vi,vc in enumerate(vword):
            vci = vword.index(vc)
            if (vci == 0) :
                #problem.addConstraint(lambda h, length=length,wordsbylen=wordsbylen: len((w for w in wordsbylen[len(length)] if w[0] in h))!=0 ,("h%d%d" % (hl,hci)))
                problem.addConstraint(lambda vw, v, vci=vci: vw[vci] == v,("v%d" % vl,"v%d%d" % (vl,vci),))   
                

    #################################constraint that in every intersection letter variables should be the same#########################################################
    
    for hi, hword in enumerate(horizontal):
        for vi, vword in enumerate(vertical):
            for hchar in hword:
                if hchar in vword:
                    hci = hword.index(hchar)
                    vci = vword.index(hchar)
                    #hchar donne la position dans la grille d'une lettre"
                    problem.addConstraint(lambda hw, vw, h,v, hci=hci, vci=vci: hw[hci] == vw[vci] == h == v ,("h%d" % hi, "v%d" % vi,"h%d%d" % (hi,hci), "v%d%d" % (vi,vci),))

    for char, letter in predefined.items():
        for hi, hword in enumerate(horizontal):
            if char in hword:
                hci = hword.index(char)
                problem.addConstraint(lambda hw, h, hci=hci, letter=letter: hw[hci] == h == letter, ("h%d" % hi,"h%d%d" % (hi,hci),))
        for vi, vword in enumerate(vertical):
            if char in vword:
                vci = vword.index(char)
                problem.addConstraint(lambda vw, v, vci=vci, letter=letter: vw[vci] == v == letter, ("v%d" % vi,"v%d%d" % (vi,vci),))

    
    ##########################getsolution########################################## 
    solution = problem.getSolution()
    if not solution:
        print ("No solution found!")
        
    ##########################affichage de la grille solution#######################  
 
    maxcol = 0
    maxrow = 0
    for hword in horizontal:
        for row, col in hword:
            if row > maxrow:
                maxrow = row
            if col > maxcol:
                maxcol = col
    for vword in vertical:
        for row, col in vword:
            if row > maxrow:
                maxrow = row
            if col > maxcol:
                maxcol = col

    matrix = []
    for row in range(maxrow+1):
        matrix.append([" "]*(maxcol+1))

    for variable in solution:
        if (len(solution[variable])>3): 
            if variable[0] == "v":
                word = vertical[int(variable[1:])]
                i=0
                w=solution[variable]
                for x in word:
                    (row,col)=x
                    matrix[row][col] = w[i] 
                    i=i+1
                        
            if variable[0] == "h":
                word = horizontal[int(variable[1:])]
                i=0
                w=solution[variable]
                for x in word:
                    (row,col)=x
                    matrix[row][col] = w[i]
                    i=i+1
    print ("\n\n *********** A possible solution is: ******************\n")
    for row in range(maxrow+1):
        for col in range(maxcol+1):
            sys.stdout.write(matrix[row][col])
        sys.stdout.write("\n")
    print ("\n\n ******************************************************\n")
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: crosswords_hybrid.py <maskfile> <wordsfile>")
    main(open(sys.argv[1]).read(), open(sys.argv[2]))

