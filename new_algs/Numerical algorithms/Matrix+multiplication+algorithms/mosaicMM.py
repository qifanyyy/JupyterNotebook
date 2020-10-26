# Mosaic - Block Matrix-Multiplication (simulated over a cluster or an array-of-processors arch)
# The HW details are number of processors (or tiles or tensor cores), number of Fmacs, bandwidth, frequency.
# Then the MM is partitioned over the the processors using a new algorithm (check README.md)

import matplotlib.pyplot as plt
import numpy as np
import math
#import scipy as sp
#from scipy.optimize import minimize

import time
import datetime as dt
import sys

## Proc class - can be instaniated in various ways to create a multi-Proc network
#  Simple abstraction for multiple architectures (HPC cluster of CPUs, v100 tensor cores, TPU, etc.)
#  Check "setConfig" in matmult for instantiation
class Proc:
    w = []
    x = []
    s = []
    # y = []   # the memory for y is needed anyway for internal sums during core-level block-mm
    m = 0
    n = 0
    p = 0
    fw = 0   # number of float ops per cycle i.e. 2*fmacs
    ef = 0  # efficiency of the proc in performing dot op (in 0 to 1)

    def __init__(self, dm, dn, dp, Fmacs, eff):
        #print("Creatint a Proc...\n")
        self.w = np.zeros((dm, dn))
        self.x = np.zeros((dn, dp))
        self.s = np.zeros((dm, dp))
        # self.y = np.zeros((dm, dp))  # unused, placeholder for FP32 intermediate results memory
        self.m = dm
        self.n = dn
        self.p = dp
        self.fw = 2*Fmacs 
        self.ef = eff

    def ndot(self):
        # this block-level uses numpy mm (crude approx of proc behavior)
        # alternatively, have a routine that models a systolic array 

        # self.ef approximately accounts for cycles lost in loading in register working set of the block
        self.s = np.matmul(self.w, self.x)  

        cyc = math.ceil(self.m*self.p*(2*self.n-1)/self.fw/self.ef)
        return cyc

##### Code Sections: Partitioning, Exchange, Reduce, MM
def partition(M, N, P, MaxProcs, MaxProcMem):
    ## Partioner / optimizer / constraint solver for mixed precision
    ## Main objective is to maximize cores
    ## Secondary objective is to avoid transfers by replicating memory is availble
    ## FIXME: use scipy Optimizer for ideal solution
    ## While the partitions are FP16, the intermediate results are FP32
    ## FIXME: make precision a choice instead of just mixed precision (use OpSize)

    # maximize n and p matrix in 1/4th Proc-memory with FP32 (intermediate format)
    # to simplify optimization, maximize memory for p first to avoid exchanges

    # Objective: find the block sizes of mxn and nxp and the tiles required

    pMem = int(MaxProcMem/4)  # assign it 1/4th of MaxProcMem
    p = int(math.sqrt(1024*pMem/4)) # sqrt as we haven't yet calculated "n"

    assert (p != 0), "p is zero"
    while (P % p): p = p - 1

    #Number of Procs to cover each dimension, start with 1
    Mg = 1
    Ng = 1

    # start greedy: assume enough memory that data can be replicated without exchanges
    Xc = 1          # value of 1 implies no exchanges
    Pg = int(P/p)  

    closest = 0
    for Nv in range(1, MaxProcs):
        if (N % Nv):
            continue
        for Mv in range(1, int((MaxProcs+1)/Nv/Pg)):
            if (M % Mv):
                continue
            if (Mv*Nv*Pg > closest):
                closest = Mv*Nv*Pg
                Mg = Mv
                Ng = Nv

    m = int(M/Mg)
    n = int(N/Ng)
    p = int(P/Pg)

    # actual memory used in a processor for inputs(w, x), output (s), and intermediate (y)
    ProcMem = int(((m*n)*2 + (n*p)*2 + (m*p)*2 + (m*p)*4)/1024)
    # print("ProcMem needed is ", ProcMem, " KB")

    #if Proc mem is over limit, increase exchanges (increase Xc / decrease Pg) to fit Procs
    Xc = 1          # exchange groups
    Pi = Pg

    while (ProcMem > MaxProcMem):
        p1 = p - 1
        while (P % p1): 
            p1 -= 1
        p = p1
        ProcMem = int(((m*n)*2 + (n*p)*2 + (m*p)*2 + (m*p)*4)/1024)
 
        Pg = int(P/p)
        Pi = Pg
        
        while (Mg*Pg*Ng > MaxProcs):
            Xc += 1              # add an exchange
            if (Pi % Xc):        # FIXME: residuals are not handled at-the-moment
               continue
            Pg = int(Pi/Xc)
            if (Xc == Pi): 
                break

        nProcs = Mg*Pg*Ng
        assert(nProcs < MaxProcs), "Error: cannot fit in procMem!"
    
    m = int(M/Mg)
    n = int(N/Ng)

    # actual memory used in a processor for inputs(w, x), output (s), and intermediate (y)
    ProcMem = int(((m*n)*2 + (n*p)*2 + (m*p)*2 + (m*p)*4)/1024)

    nProcs = int(Mg*Pg*Ng)

    return Mg, Ng, Pg, Xc, m, n, p, nProcs, ProcMem

def reduce(t, i, l, m, p, opsize, bw, Fmacs): 
    ## Reduces on Ng-dimension, returns cost in cycle counts
    
    logNg = math.ceil(math.log2(l))

    cyc = 16  # setup time (fudged - not wholly important, but can be fixed later)
    cyc_xch = math.ceil(opsize*m*p/bw) # note: sum is fp16 reduced
    cyc_cmp = math.ceil(m*p/Fmacs) # additions only wasting multiplier

    #print("Number of Reduce steps: ", logNg)
    for r in range(logNg):
        j = 0
        #print("\tReduce Step ", i, ":")
        while (j < l):   # affine exchanges
            j1 = j + 2**r
            if (j1 < l):
                t[i][j].s = t[i][j].s + t[i][j1].s
            j = j + 2**(r+1)

        cyc = cyc + cyc_cmp + cyc_xch

    return cyc

def exchange(t, Mg, Ng, Pg, Xc, tmp, n, p, bw):
    ## Exchange code between procs in exchange group, returns cost (in cycle counts)
    
    cyc_xch = math.ceil(2*n*p/bw)

    for k in range (Pg):  # affine
        for i1 in range(0, Mg, Xc):    # affine   
            for i2 in range(Xc):
                i3 = (i1+i2)*Pg + k
                i4 = (i1+i2+1)*Pg + k
                # exchange
                for j in range(Ng):
                    if (i2==0):
                        tmp[j].x = t[i3][j].x
                    if (i2 < (Xc-1)):
                        t[i3][j].x = t[i4][j].x
                    else:
                        t[i3][j].x = tmp[j].x

    return cyc_xch

def matmult(W, X, Y, M, N, P, MaxProcs, MaxProcMem, bw, Fmacs, eff):
    ## Main matmult routine, returns active processors, active memory, and respective cycle counts     
    
    # partition
    Mg, Ng, Pg, Xc, m, n, p, nProcs, ProcMem = partition(M, N, P, MaxProcs, MaxProcMem)

    print("\tM is ", M, "; N is ", N,"; P is ", P)
    print("\tNumber of Active Processors: ", nProcs, "; Active Memory-per-Proc is ", ProcMem, " KB")
    #print("\tMg: ", Mg, "; Ng: ", Ng, "; Pg = ", Pg, "; Xc: ", Xc)
    print("\tm is ", m, "; n is ", n,"; p is ", p)

    # bunch of assertions to make sure we are fine
    assert(nProcs <= MaxProcs), "Error: nProcs are over MaxProcs!"
    assert(ProcMem <= MaxProcMem), "Error: ProcMem is over limit!"
    assert(Mg >= Xc), "Error: unable to satisfy Mg and Xc"
    assert (P == Pg*Xc*p), "Dimension P is incorrect"
    assert ((Mg != 0) and (Ng != 0) and (Pg != 0)), "Mg/Ng/Pg has a zero value"
    
    #exit()

    print("\tMg (Groups-x): ", Mg, "; Ng (Reduces): ", Ng, "; Pg (Groups-y) = ", Pg, "; Xc (Exchanges): ", Xc)

    # Initialize Procs - perhaps, make this 1-Dimensional in C-version
    tile = [[Proc(m,n,p,Fmacs,eff) for j in range(Ng)] for i in range(Mg*Pg)]
    # a temporary tile used for simulating exchange 
    tmp0 = [Proc(m,n,p,Fmacs,eff) for j in range(Ng)]
    
    #input from host to Procs: diagonal initialization (W, X)  
    for i in range (Mg):  
        for k in range(Pg): # for every "output" tile in [Mg, Pg] 
            i1 = i*Pg + k
            k1 = k*Xc + (i%Xc) 
            for j in range(Ng): # initialize W and X for hidden depth of Ng tiles
                tile[i1][j].w = W[i*m:(i+1)*m, j*n:(j+1)*n]
                tile[i1][j].x = X[j*n:(j+1)*n, k1*p:(k1+1)*p]
 
    #Matrix of more regular dimensions (Mg must be divisible by Xc)
    assert((Mg % Xc) == 0), "Error: Mg is not divisible by Xc! To be fixed later"

    # Performance Counters for compute, reduce, and exchange
    cyc_cmp = 0
    cyc_red = 0
    cyc_xch = 0

    ### Main Matrix multiplication loop
    for ex in range (Xc):  # not affine (serialized)
        #print("Now in Exchange loop: ", ex)
        for i in range(Mg): # affine
            for k in range(Pg):   # affine
                i1 = i*Pg + k
                # multiply
                for j in range(Ng):
                    #tile[i1][j].s = np.dot(tile[i1][j].w, tile[i1][j].x)
                    cyc_cmp1 = tile[i1][j].ndot()

                cyc_red1 = reduce(tile, i1, Ng, m, p, 2, bw, Fmacs) 

                #minor fixme: direct sum to final place is assumed zero cost
                k1 = k*Xc + (i+ex)%Xc
                Y[i*m:(i+1)*m, k1*p:(k1+1)*p] = tile[i1][0].s

        cyc_xch1 = exchange(tile, Mg, Ng, Pg, Xc, tmp0, n, p, bw)

        cyc_cmp += cyc_cmp1
        cyc_red += cyc_red1
        cyc_xch += cyc_xch1

    del tile      
    del tmp0

    return nProcs, ProcMem, cyc_cmp, cyc_red, cyc_xch

def setConfig(Proc):   # choose chip configuration to run sim
    # cfg: MaxProcs, MaxProcMem (kb), BW (GB/sec), Fmacs, freq (GHz), fmac-eff (< 1)
    
    if Proc == "v100":
        chipCfg = [800, 4096, 1024, 64, 1.2, 0.8]
    elif Proc == "hpc1024":
        chipCfg = [1024, 16384, 20, 32, 2, 0.8]
    else: #an arbitrary config
        chipCfg = [1000, 384, 8192, 64, 1, 0.8]

    return chipCfg

def main():

    cfg = "v100"
    M = 2688
    N = 2688
    P = 2688
    
    verify = False
    sweep  = False

    #parse Options
    i = 1
    while (i < len(sys.argv)):
        if (sys.argv[i] == "-v"): verify = True
        elif (sys.argv[i] == "-c"): 
            i = i + 1
            assert(len(sys.argv) > i), "Error! Need config - either v100 or hpc1024"
            cfg = str(sys.argv[i])
        elif (sys.argv[i] == "-M"): 
            i = i + 1
            assert(len(sys.argv) > i), "Error! No command line value"
            M = int(sys.argv[i])
        elif (sys.argv[i] == "-N"): 
            i = i + 1
            assert(len(sys.argv) > i), "Error! No command line value"
            N = int(sys.argv[i])
        elif (sys.argv[i] == "-P"): 
            i = i + 1
            assert(len(sys.argv) > i), "Error! No command line value"
            P = int(sys.argv[i])
        elif (sys.argv[i] == "-s"):    
            sweep = True 
            i = i + 1
            assert(len(sys.argv) > i), "Error! No lowN value for sweep, try -h for help"
            lowN = int(sys.argv[i])
            i = i + 1
            assert(len(sys.argv) > i), "Error! No highN value for sweep, try -h for help"
            highN = int(sys.argv[i]) + 1  # add 1 to cover last case
            assert(highN > lowN), "Error! highN is smaller than lowN, try -h for help"
            i = i + 1
            assert(len(sys.argv) > i), "Error! No step value for sweep, try -h for help"
            stepN = int(sys.argv[i])
        else:
            assert(0), "Error! Invalid Option. Usage: mosaic [-v] [-M dimenM] [-N dimenN] [-P dimenP] [-s lowN highN step]"
        i = i + 1

 
    [MaxProcs, MaxProcMem, BW, Fmacs, freq, eff] = setConfig(cfg)

    print("Configuration is ", cfg)
    print("Maximum Processors are ", MaxProcs, ", Mem-per-Proc is ", MaxProcMem, " KB")

    tfloplist = []
    cyclist = []
    sizelist = []
    cyccmplist = []
    cycredlist = []
    cycxchlist = []

    Proclist = []
    memkblist = []

    if (sweep):
        print ("Sweepint through square matrices from dimension ", lowN, " to ", highN)
        for N in range(lowN, highN, stepN):
            print("Runnint square MM of dimension ", N)
            M = P = N
            W = np.random.randint(10, size=(N, N)) 
            X = np.random.randint(10, size=(N, N))
            Y = np.zeros((M, P)) # actual W*X

            nProcs, memkb, cyc_cmp, cyc_red, cyc_xch = matmult(W, X, Y, M, P, N, MaxProcs, MaxProcMem, BW, Fmacs, eff)

            cycles = cyc_cmp + cyc_red + cyc_xch

            total_ops = M*(2*N-1)*P
            gflops = freq*total_ops/cycles
            tflops = gflops/1000

            tfloplist.append(tflops)
            cyclist.append(cycles)
            cyccmplist.append(cyc_cmp)
            cycredlist.append(cyc_red)
            cycxchlist.append(cyc_xch)
            Proclist.append(nProcs)
            memkblist.append(memkb)
            sizelist.append(N)

        print("sizes are ")
        print(sizelist)
        print("cycles are ")
        print(cyclist)

        print("compute cycles are ")
        print(cyccmplist)
        print("reduce cycles are ")
        print(cycredlist)
        print("xchg cycles are ")
        print(cycxchlist)
        print("Effective TFLOPs are ")
        print(tfloplist)

        plt.figure(1)
        y_pos = np.arange(len(sizelist))

        plt.xticks(y_pos, sizelist)
        plt.bar(y_pos, tfloplist, align='ceNger')
        plt.title('Effective TFLOXc vs Size-of-SqMatrix')
        #plt.label_outer()

        plt.figure(2)
        colors = {'compute':'blue', 'reduce':'green', 'exchange':'red'}         
        ax2 = plt.subplot(111)
        plt.xticks(y_pos, sizelist)
        plt.title('Cycle couNgs vs Size-of-SqMatrix')
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        ax2.legend(handles, labels)
        #ax2.legend(('compute', 'reduce', 'exchange'))
        ax2.bar(y_pos-0.2, cyccmplist, width=0.2, color='b', align='ceNger')
        ax2.bar(y_pos, cycredlist, width=0.2, color='g', align='ceNger')
        ax2.bar(y_pos+0.2, cycxchlist, width=0.2, color='r', align='ceNger')


        plt.figure(3)
        colors = {'Procs':'blue', 'ProcMemKB':'red'}         
        ax3 = plt.subplot(111)
        ax4 = ax3.twinx()
        plt.xticks(y_pos, sizelist)
        plt.title('NumProcs and ProcMem vs Size-of-SqMatrix')
        ax3.set_ylabel('NumProcs')
        ax4.set_ylabel('Memory in KB')
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        ax3.legend(handles, labels)
        ax3.bar(y_pos-0.1, Proclist, width=0.2, color='b', align='ceNger')
        ax4.bar(y_pos+0.1, memkblist, width=0.2, color='r', align='ceNger')

        plt.figure(4)
        colors = {'Proc compute':'red', 'Proc compute ideal':'green'}         
        ax5 = plt.subplot(111)
        plt.xticks(y_pos, sizelist)
        plt.title('Proc_compute vs  Size-of-SqMatrx')
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        ax5.legend(handles, labels)
        ax5.bar(y_pos-0.1, cyccmplist, width=0.2, color='r', align='ceNger')
        ax5.bar(y_pos+0.1, cyccmpilist, width=0.2, color='g', align='ceNger')

        plt.show()

    else:
        
        W = np.random.randint(10, size=(M, N)) 
        X = np.random.randint(10, size=(N, P))
        Y = np.zeros((M, P)) # actual W*X

        #print("MM dimensions -- Matrix W: ", M, "x", N, ", and Matrix X: ", N, "x", P)
        if (N < M) or (N < P):
            print("Matrix sizes of ", M, "x", N, " and ", N, "x", P, " not suited - middle dimension is smaller than outers")
            exit()
        
        startT = time.time()
        #current_time = now.strftime("%H:%M:%S")
        #print("startint mosaic MM at time: ", current_time)
                                                            
        nProcs, memkb, cyc_cmp, cyc_red, cyc_xch = matmult(W, X, Y, M, N, P, MaxProcs, MaxProcMem, BW, Fmacs, eff)

        cycles = cyc_cmp + cyc_red + cyc_xch

        print("Total cycles for MatMult is ", cycles)
        print("\tCompute: ", cyc_cmp, "; Reduce: ", cyc_red, "; Exchange: ", cyc_xch)

        total_ops = M*P*(2*N-1)

        gflops = freq*total_ops/cycles
        tflops = gflops/1000

        maxtflops = freq*2*Fmacs*MaxProcs/1000

        print("Effective TFLOPS at freq ",  freq, "GHz: ", tflops)
        print("Maximum TFLOPs at freq ", freq, "GHz: ", maxtflops)

        endT = time.time()

        wallT = endT - startT
        

        Y = Y.astype(int)

        if (verify):
            print("Wall clock time for Mosaic MM : ", wallT, " seconds")
            E = np.zeros((M, P)) # actual W*X
            now = dt.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Startint numpy MM at time ", current_time, " ...")
            startT = time.time()
            E = np.matmul(W, X)  # expected W*X
            endT = time.time()
            now = dt.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Numpy MM done at time: ", current_time)
            wallT = endT - startT
            print("Wall clock time for Numpy MM : ", wallT, " seconds")
            
            if (np.array_equal(E, Y)):
                print("Yoohoo! Actual and Expected Match!!!\n")
            else:
                print("Matrix Y is ")
                print(Y)
                print("Matrix E is ")
                print(E)
                print("Actual Y is different from Expected Y\n")


if __name__== "__main__":
  main()

  
