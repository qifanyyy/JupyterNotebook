"""
This runs the Grover simulation, implementing the input functions to determine how to run
"""

import numpy as np
import math as m
import time as t
import sys
import InOut as IO
import GroverGateWise as G

def main():
    '''
    Main to run Grover's Simulation
    '''
    check = 'run'   #is altered for testing purposes

    #runs grover
    if check == 'run':
        args = IO.start()
        noise = IO.gnoise()
        G.run(args, noise)

    #runs test for varying qubit reg size but constant fock target
    elif check == 'test1':
        # --- Time for n qubits ---
        args = np.zeros(2)
        nlist = [i for i in range(2,14)]   #varying reg size array
        time1 = np.zeros(len(nlist))
        target = 1   #constant target
        for i in range(len(nlist)):
            print('Running Grovers for ' + str(nlist[i]) + ' qubits for Fock value |1>')
            args[0] = nlist[i]
            args[1] = target
            time1[i] = G.run(args, 0)
        IO.timeplotn(nlist, time1)

    #runs test for varying fock target but constant qubit reg size
    elif check == 'test2':
        # --- Time for different Fock value targets ---
        args = [0,0]
        n = 10   #constant reg size
        tarlist = [i for i in range(0,200)]   #varying target
        time2 = np.zeros(len(tarlist))
        for i in range(len(tarlist)):
            print('Running Grovers for 10 qubits for Fock value |' + str(tarlist[i]) + '>')
            args[0] = n
            args[1] = tarlist[i]
            time2[i] = G.run(args, 0)
        IO.timeplottar(tarlist, time2)

    #invalid entry quits programme
    else:
        print('\nThis is not a valid option.')
        sys.exit()

main()
