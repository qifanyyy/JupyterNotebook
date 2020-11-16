"""
    EDA Tools WS 2017-2018
    Equivalence checking for two netlists

    Submitted by: ICS Students WS2016 batch
        Yeshwanth Reddy Manasani 455949
        Hemanth kumar Maliga 456131

    Python 3.6.3

"""

import sys

def readNetlist(file,netporting):
    nets = int(file.readline())
    inputs  = file.readline().split()
    inputs.sort()
    outputs = file.readline().split()
    outputs.sort()

    # read mapping
    mapping = {}
    while True:
        line = file.readline().strip()
        if not line:
            break

        net,name = line.split()
        mapping[name] = int(net)+netporting

    # read gates
    gates = []
    for line in file.readlines():
        bits = line.split()
        gate = bits.pop(0)
        ports=list(map(int,bits))
        _ports=[]
        for port in ports:
            port=port+netporting
            _ports.append(port)
        gates.append((gate,_ports))

    return nets,inputs,outputs,mapping,gates

# read netlists
nets1,inputs1,outputs1,mapping1,gates1 = readNetlist(open(sys.argv[1],"r"),0)
nets2,inputs2,outputs2,mapping2,gates2 = readNetlist(open(sys.argv[2],"r"),nets1)

#add your code here!

#Create an appropriate miter Circuit
def mitercircuit(inputs1, inputs2, outputs1, outputs2, gates1, gates2,mapping1,mapping2,nets1,nets2):


    miter=[] # stores total gates and their ports used in the mitercirvuit
    miter.extend(gates1) # added gates list of circuit 1
    miter.extend(gates2) # added gates list of circuit 2

    nets=nets1+nets2
    XorOutputs=[]
    for op1,op2 in zip(outputs1, outputs2):# to connect equivalent outputs
        nets+=1
        miter.append(("xor",[mapping1[op1], mapping2[op2],nets]))
        XorOutputs.append(nets)

    if len(XorOutputs)==1:
        miter.append(("unit", XorOutputs))

    elif len(XorOutputs)==2:
        nets+=1
        XorOutputs.append(nets)
        miter.append(("or", XorOutputs))

    #if len(XorOutputs)1:
    else:
        nets+=1
        XorOutputs.append(nets)
        miter.append(("multiInputOr",XorOutputs))

    for ip1, ip2 in zip(inputs1,inputs2): # to connect equivalent inputs
        miter.append(("equivalent",[mapping1[ip1],mapping2[ip2]]))

    #print()
    #print("nets", nets)
    #print()
    #print("XorOutputs", XorOutputs)
    #print()
    #print("miter is ", miter)
    #print()
    return miter,nets


#write the formula in CNF using the characteristic functions of logic-gates used in the mitercircuit
def formulaInCNFFromMiterCircuit(miter):

    miterlength = len(miter)
    cnf = []
    while (miterlength > 0):
        x = miter.pop(0)
        if ( x[0] == "and" ):
            cnf.extend( [[x[1][0], -x[1][2]]] )
            cnf.extend( [[x[1][1], -x[1][2]]] )
            cnf.extend( [[-x[1][0], -x[1][1], x[1][2]]] )
        elif ( x[0] == "or" ):
            cnf.extend( [[x[1][0], x[1][1], -x[1][2]]] )
            cnf.extend( [[-x[1][0], x[1][2]]] )
            cnf.extend( [[-x[1][1], x[1][2]]] )
        elif ( x[0] == "xor" ):
            cnf.extend( [[-x[1][0], x[1][1], x[1][2]]] )
            cnf.extend( [[x[1][0], -x[1][1], x[1][2]]] )
            cnf.extend( [[x[1][0], x[1][1], -x[1][2]]] )
            cnf.extend( [[-x[1][0], -x[1][1], -x[1][2]]] )
        elif (x[0]=="equivalent"):
            cnf.extend( [[x[1][0], -x[1][1]]] )
            cnf.extend( [[-x[1][0], x[1][1]]] )
        elif (x[0]=="inv"):
            cnf.extend( [[x[1][0], x[1][1]]] )
            cnf.extend( [[-x[1][0], -x[1][1]]] )
        elif (x[0]=="unit"):
            cnf.extend( [[x[1][0]]] )
        else:
            cnf.extend( [[x[1][0], x[1][1], x[1][2], x[1][3], x[1][4], -x[1][5]]] )
            cnf.extend( [[-x[1][0], x[1][5]]] )
            cnf.extend( [[-x[1][1], x[1][5]]] )
            cnf.extend( [[-x[1][2], x[1][5]]] )
            cnf.extend( [[-x[1][3], x[1][5]]] )
            cnf.extend( [[-x[1][4], x[1][5]]] )
        miterlength = miterlength - 1
    return cnf

variableAssignmentMapping={} # a dict used to track down the variable assignment

#solving clauses that contain the variable
def heuristics(hCNF, variable, _variableAssignmentMapping):


    #updating cnf
    for clause in hCNF[:]:
        for literal in clause:
            #removing all satisfied clauses
            if variable==literal:
                hCNF.remove(clause)
            #remove all satisfied literals from the clauses
            elif variable==-literal:
                clause.remove(literal)

    # variable assignment
    if variable > 0:
        _variableAssignmentMapping[variable]=1
    else:
        _variableAssignmentMapping[abs(variable)]=0

    # Checking for unit clause
    for clause in list(reversed(hCNF)):
        if len(clause)==1:
            variable=clause[0]
            #repeating the heuristics if unit clause found
            hCNF, _variableAssignmentMapping = heuristics(hCNF, variable, _variableAssignmentMapping)
    #if no unit clause found return the updated cnf and variable assigment dict to devisPutnamAlgorithm
    return(hCNF, _variableAssignmentMapping)

#devis Putnam Algorithm
def devisPutnamAlgorithm(dCNF, variable, variableAssignmentMapping): #This algorithm is implemented recursively

    #tries to simplify the cnf using 3 steps
    #step1: heuristics
    #    """repeat
    #            apply unit clause rule to cnf until heuristics not applicable anymore"""
    sCNF, variableAssignmentMapping = heuristics(dCNF, variable, variableAssignmentMapping)

    #step2: Terminal conditions
    #    """if cnf is empty: # no more heuristics rules applicable
    #        terminate algorithm, solution found (not equivalent, counter example)"""
    if len(sCNF)==0:#
        return(True)

    #    """else if cnf has empty clause:
    #no solution possible/exits (circuits are equivalent)
    #        return"""
    else:
        for clause in sCNF:
            if len(clause)==0:
                return(False)

        #step3: backtracking  (if terminal conditions do not apply)
        #"""else:
        #Backtracking (choose a variable and guess its assignment)
        #variable=choose variable from CNF
        variable=sCNF[-1][-1]
        sCNF0=list(sCNF)

        #recurse on cnf with variable=-sCNF[-1][-1]
        #dp(cnf, -variable)
        satisfiable=devisPutnamAlgorithm(sCNF, -variable, variableAssignmentMapping)

        if not satisfiable:
            #recurse on cnf with variable=sCNF[-1][-1]
            #dp(duplicatecnf, variable, )
            satisfiable= devisPutnamAlgorithm(sCNF0, variable, variableAssignmentMapping)

        return(satisfiable)

#to create a mitercircuit using the netlists' data
miter,nets=mitercircuit(inputs1, inputs2, outputs1, outputs2,gates1, gates2,mapping1,mapping2,nets1,nets2)

#to transform the mitercircuit to a formula in CNF
cnf=formulaInCNFFromMiterCircuit(miter)

#calling ing devisputnam algorithm with initial/original cnf
satisfiable=devisPutnamAlgorithm(cnf, nets, variableAssignmentMapping)

#printing counter example
def counterExample(inputs1, inputs2, mapping1, mapping2, outputs1, outputs2, variableAssignmentMapping):

    print("Inputs of Netlists")
    for input in inputs1:
        for key, value in variableAssignmentMapping.items():
            if mapping1[input]==key:
                print(input, "=" , value)

    print("Outputs of Netlist 1")
    for output in outputs1:
        for key, value in variableAssignmentMapping.items():
            if mapping1[output]==key:
                print(output, "=" , value)

    print("Outputs of Netlist 2")
    for output in outputs2:
        for key, value in variableAssignmentMapping.items():
            if mapping2[output]==key:
                print(output, "=" , value)
    return()

#code
if satisfiable==True:
    print("Circuits are 'not equivalent' ")
    print("Counter example is")
    #to print counter example
    counterExample(inputs1, inputs2, mapping1, mapping2, outputs1, outputs2, variableAssignmentMapping)
elif satisfiable==False:
    print("Circuits are 'equivalent' ")
