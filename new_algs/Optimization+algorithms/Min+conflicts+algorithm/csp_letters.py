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
    alphabet= ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    
    #problem = Problem(MinConflictsSolver())
    problem = Problem()
    
    #store words from dico by length
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
        
    print ("c1") 
    wordListV = []
    #constraint that letters together in vertical columns should be a word from dico
    for vl,vword in enumerate(vertical):
        variablesV = []
        pairListV = []
        for vt, vwo in enumerate(vword):
            #print "v constraint variables"
            #print "v%d%d" % (vl, vt)
            variablesV.append("v%d%d" % (vl, vt))
            l = random.choice(alphabet)
            #print "choice is : " + l
            pairListV.append((vwo, l))
        #print "variablesV = " + str(variablesV)
        wordListV.append(pairListV)
        problem.addConstraint(lambda vw = pairListV, wordsbylen = wordsbylen: ("".join(x[1] for x in pairListV)) in wordsbylen[len(pairListV)], variablesV)

    #print "pairListH = " + str(pairListH)
    #print "pairListV = " + str(pairListV)
    print ("c2") 
    hw = []
    vw = []
    for hi, hword in enumerate(horizontal):
        for vi, vword in enumerate(vertical):
            for hchar in hword:
                if hchar in vword:
                    hci = hword.index(hchar)
                    vci = vword.index(hchar)
                    for x in wordListH[hi]:
                        hw.append(x[1])
                    print ("hw 1 = " + str(hw))
                    for x in wordListV[vi]:
                        vw.append(x[1])
                    print ("vw 1 = " + str(vw))
                    #print "hci = " + str(hci) + "   vci = " + str(vci)
                    problem.addConstraint(lambda hl, vl, hw=hw, vw=vw, hci = hci, vci = vci:
                                          hw[hci] == hl and vw[vci] == vl and hl == vl,
                                          ("h%d%d" % (hi,hci), "v%d%d" % (vi,vci)))

    for char, letter in predefined.items():
        for hi, hword in enumerate(horizontal):
            if char in hword:
                hci = hword.index(char)
                for x in wordListH[hi]:
                    hw.append(x[1])
                print ("hw 2 = " + str(hw))
                problem.addConstraint(lambda hl, hw = hw, hci=hci, letter=letter:
                                      hw[hci] == hl and hl == letter, ("h%d%d" % (hi,hci),))
        for vi, vword in enumerate(vertical):
            if char in vword:
                vci = vword.index(char)
                for x in wordListV[vi]:
                    vw.append(x[1])
                print ("vw 2 = " + str(vw))
                problem.addConstraint(lambda vl, vw = vw, vci=vci, letter=letter:
                                      vw[vci] == vl and vl == letter, ("v%d%d" % (vi,vci),))
                                      
    print ("c3")  
    
    #define varialbes: letters and their domain: alphabet
    for hl,hword in enumerate(horizontal):
        for hi,hc in enumerate(hword):
            problem.addVariable("h%d%d" %(hl,hi), alphabet)
    for vl,vword in enumerate(vertical):
        for vi,vc in enumerate(vword):
            problem.addVariable("v%d%d" % (vl,vi), alphabet)
    """for hi, hword in enumerate(horizontal):
        words = wordsbylen[len(hword)]
        random.shuffle(words)
        problem.addVariable("h%d" % hi, words)
    for vi, vword in enumerate(vertical):
        words = wordsbylen[len(vword)]
        random.shuffle(words)
        problem.addVariable("v%d" % vi, words)"""

    problem.addConstraint(AllDifferentConstraint())
    
    print ("c4" )
    
    solution = problem.getSolution()
    if not solution:
        print ("No solution found!")
        
    print ("c5")
    
    #print grid
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

    print ("solution")
    print (solution)
    """for variable in solution:
        print "variables solution"
        print variable
        print "numero mot"
        n=[]
        n= list(variable)
        number=n[1]
        print number
        if variable[0] == "v":
            #word = vertical[int(variable[1:])]
            word = vertical[int(number)]
        else:
            #word = horizontal[int(variable[1:])]
            word = horizontal[int(number)]
        for (row, col), char in zip(word, solution[variable]):
            print "word 2"
            print word
            print "solution[variable]"
            print solution[variable]
            matrix[row][col] = char
            print " char" 
            print char"""

    """for row in range(maxrow+1):
        for col in range(maxcol+1):
            sys.stdout.write(matrix[row][col])
        sys.stdout.write("\n")"""

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: crosswords_letter_approach.py <maskfile> <wordsfile>")
    main(open(sys.argv[1]).read(), open(sys.argv[2]))

