import threading, random, math, sys, time, Queue
from a2_functions import *
from a2_adts import *
from a2_peers import *
        
def main():
        random.seed(time.time());

        N = input("Enter the size of the matrix (N): ")
        print
        #Create NxN matrix
        print"Generating matrix... ",
        A = randomMatrix(N);
        print"Done."
        #N=5;A=[[0,1,0,0,1],[1,1,1,0,1],[0,0,1,0,0],[1,0,0,1,0],[0,1,1,0,1]]
        numOfThreads=int(math.ceil(math.log(N, 2)));
        #Initialize list of M powers
        mList,cList,mPeers,cPeers,kPeers=([] for i in range(5));
        print"Generating kPeers... ",     
        for i in range(1, N-1):
                p = kPeer(i, A);
                kPeers.append(p);
        print"Done."
        print"Starting kPeers... ",
        # Start peer list
        start= time.time();
        for i in range(0, N-2):
                kPeers[i].start();
        for i in range(0, N-2):
                kPeers[i].join();
        print"Done.",
        end = time.time();
        print "Time: %f"%(end-start)
        print "Generating C Product Matrix... ",
        C_N   = [[1],[A[N-1][N-1]]]
        C_Nm1 = [[1,0],[A[N-2][N-2],1],[A[N-1][N-2]&A[N-2][N-1],A[N-2][N-2]]]
        cList = []
        cList.append(0);
        for i in range(0, N-2):
                cList.append(aElement(kPeers[i].C))
        cList.append(aElement(C_Nm1));
        cList.append(aElement(C_N));
        
        B = [[0 for x in xrange(N+1)] for x in xrange(N+1)]
        for i in range(1, N+1):
                B[i-1][i]=cList[i].A
        print "Done."
        
        print "Calculating Product of C matrices... ",
        start=time.time()
        aList = []
        aList.append(aElement(1));
        aList.append(aElement(B));
        aList[1].done.set()
        for i in range(0, N):
                aList.append(aElement(0))
        cPeers=[]
        for i in range(0, numOfThreads):
                c = cPeer(aList)
                cPeers.append(c)
        
        for i in range(0, numOfThreads):
                cPeers[i].start()
        for i in range(0, numOfThreads):
                cPeers[i].join()
        END = aList[N].A[0][N]
        end=time.time()
        print "Done. %f"%(end-start)
        print "Testing... ",
        testRes(N, A, END)
        

main()





