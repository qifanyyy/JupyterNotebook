#! /usr/bin/env/python3

import sys
import subprocess

def ctr(base):
    c = base
    while True:
        yield c
        c = c + 1

def get_diff(x, y):
    den = 1 if float(y) == 0 else abs(float(y))
    return abs(abs(float(x)) - abs(float(y)))/den
        
TOLERANCE = .50;

if len(sys.argv) < 6 or len(sys.argv) > 8:
    print("Usage: python3 tester.py [your executable (ie. ./spmv)] [matrix file] [vector file] [blocksize] [blocknum] [alg=atomic] [tester=spmv_test]")
    print("Note that the tester only runs the atomic implementation. Hence times may mismatch.")
    print("All errors will be reported.")
    print("The algorithm defaults to atomic and the tester ./spmv_test.")
    sys.exit(1)

alg = sys.argv[6] if len(sys.argv) >= 7 and sys.argv[6] in ['atomic', 'segment', 'own'] else 'atomic'
tester = sys.argv[-1] if len(sys.argv) >= 7 and sys.argv[-1] not in ['atomic', 'segment', 'own'] else './spmv_test'
their_exe_args = [sys.argv[1], "-mat", sys.argv[2], "-ivec", sys.argv[3], "-alg", alg, "-blockSize", sys.argv[4], "-blockNum", sys.argv[5]]
our_exe_args = [tester, "-mat", sys.argv[2], "-ivec", sys.argv[3], "-alg", "atomic", "-blockSize", sys.argv[4], "-blockNum", sys.argv[5]]
try:
    compl_their = subprocess.check_output(their_exe_args, stderr = subprocess.STDOUT).decode('utf-8')
    compl_our = subprocess.check_output(our_exe_args, stderr = subprocess.STDOUT).decode('utf-8')

    their_time = float(compl_their[:compl_their.find("micro-seconds")].split(' ')[-2])
    our_time = float(compl_our[:compl_our.find("micro-seconds")].split(' ')[-2])
    print("We took " + str(our_time) + " micro-seconds and you took " + str(their_time) + " microseconds.")
    print(["Congratulations, you beat us!", str(their_time - our_time) + " microseconds to reduce!"][their_time > our_time])
    
    print("Everything has run! Comparing the files...")

    with open("output.txt") as their:
        with open("output_test.txt") as our:
            r = ctr(1)
            #goes through each line and gets the difference.
            #r is used to track line numbers.
            diff = list(filter(lambda things: get_diff(things[0], things[1]) >= TOLERANCE, zip(their, our, r)))
            if len(diff) == 0: 
                print("Everything agreed within " + str(TOLERANCE * 100) + "%, so good on you!")
            else:
                print("Disagreements!")
                print("\n".join("You got {0}, we got {1}, on line {2}".format(i) for i in diff))
    #their and our are implicitly closed here...
                
except subprocess.CalledProcessError as e:
    print("Command '" + e.cmd + "' failed!")
    print("Output:")
    print(e.output)
