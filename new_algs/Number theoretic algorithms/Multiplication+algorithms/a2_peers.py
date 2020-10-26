import threading, random, math, sys, time, Queue
from copy import deepcopy
from a2_functions import *
from a2_adts import *

# The peer that calculates M^x values for x = (2, N)
class mPeer(threading.Thread):
        def __init__(self, mList):
                # Initilize Object
                super(mPeer, self).__init__()
                self.list  = mList;
        # Run Thread
        def run(self):
                # Initilize running operation
                running=True;
                myName=self.getName();
                # mList[0] = -A[0][0], and mList[1] = M^1,
                # which are both already calculated.
                i=1
                while(running):
                        # Stop threads when they reach the end of mList

                        if (i == len(self.list)-1):
                                running = False;

                        # Get current object from list
                        obj = self.list[i];
                        # Attempt to acquire lock
                        if not obj.lock.acquire(False):
                                # Skip to next element if lock is not acquired
                                i=i+1;
                        else:
                                # if lock is acquired
                                try:
                                        # Check if event is set
                                        if obj.done.isSet():
                                                # If it is, increment
                                                i=i+1;
                                        # If it is not
                                        else:
                                                #Calculate M
                                                if i%2==0:
                                                        #even
                                                        dat1= i/2
                                                        self.list[dat1].done.wait()
                                                        A = self.list[dat1].M
                                                        B = A
                                                else:
                                                        #odd
                                                        dat1= (i+1)/2
                                                        dat2= (i-1)/2
                                                        self.list[dat2].done.wait()
                                                        self.list[dat1].done.wait()
                                                        A = self.list[dat1].M
                                                        B = self.list[dat2].M
                                                obj.M = multiplyMatrix(A, B);
                                                obj.done.set();
                                # Release lock
                                finally:
                                        obj.lock.release();
                        
class cPeer(threading.Thread):
        def __init__(self, aMatrix):
                # Initilize Object
                super(cPeer, self).__init__()
                self.list  = aMatrix;
        # Run Thread
        def run(self):
                # Initilize running operation
                running=True;
                myName=self.getName();
                i=2
                N = len(self.list[1].A)
                while(running):        
                        if (i==len(self.list)-2):
                                running=False
                        obj = self.list[i];
                        # Attempt to acquire lock
                        if not obj.lock.acquire(False):
                        # Skip to next element if lock is not acquired
                                i=i+1;
                        else:
                                # if lock is acquired
                                try:
                                        # Check if event is set
                                        if obj.done.isSet():
                                                # If it is, increment
                                                i=i+1;
                                        # If it is not
                                        else:
                                                #Calculate A to the ith power
                                                if i%2==0:
                                                        #even
                                                        dat1= i/2
                                                        self.list[dat1].done.wait()
                                                        A1 = self.list[dat1].A
                                                        A2 = A1
                                                else:
                                                        #odd
                                                        dat1= (i+1)/2
                                                        dat2= (i-1)/2
                                                        self.list[dat2].done.wait()
                                                        self.list[dat1].done.wait()
                                                        A1 = self.list[dat1].A
                                                        A2 = self.list[dat2].A
                                                #CALCULATE A POWER FROM A1 and A2
                                                A3 = [[0 for x in xrange(N)]for x in xrange(N)]
                                                for j in range(0, N):
                                                        for l in range(0, N):
                                                                for k in range(0,N):
                                                                        if ((A1[l][k] != 0) and (A2[k][j] != 0)):
                                                                                C1 = A1[l][k]
                                                                                C2 = A2[k][j]
                                                                                A3[l][j] = multiplyMatrix(C1, C2)
                                                obj.A = A3                                                              
                                                obj.done.set();
                                # Release lock
                                finally:
                                        obj.lock.release();



class kPeer (threading.Thread):
        def __init__(self, sub_m, A):
                super(kPeer, self).__init__();
                self.C = []
                self.mList=[]
                self.sub_m = sub_m
                self.A = A
                self.S = []
                self.R = [[]]
        def run(self):
                myName = self.getName()
                running = True;
                mPeers=[]
                mList=[]
                m_current=subMatrix(self.A, len(self.A[0])-self.sub_m);
                numOfThreads = int(math.ceil(math.log(len(self.A[0])-self.sub_m, 2)))
                S = deepcopy([row[self.sub_m-1] for row in self.A])
                self.R[0] = deepcopy(self.A[self.sub_m-1])
                for i in range(0,self.sub_m):
                        self.R[0].pop(0);
                        S.pop(0);
                R=self.R
                for i in range(0,len(S)):
                        self.S.append([S[i]])
                mList.append(mElement(self.A[self.sub_m-1][self.sub_m-1]));
                mList.append(mElement(m_current));
                mList[0].done.set()
                mList[1].done.set()

                # Calculate all powers of m_current
                for i in range(2, len(self.A)-self.sub_m):
                        m = mElement(None);
                        mList.append(m);
                for i in range(0, numOfThreads):
                        p = mPeer(mList);
                        mPeers.append(p);
                for i in range(0, numOfThreads):
                        mPeers[i].start()
                for i in range(0, numOfThreads):
                        mPeers[i].join();
                column = len(self.A)-self.sub_m+2
                self.C = [[0 for x in xrange(column-1)]for x in xrange(column)]
                self.C[0][0]=1
                self.C[1][0]=self.A[self.sub_m-1][self.sub_m-1]
                RS=0
                RMS=0
                for i in range(0, len(self.R)):
                        RS=multiplyMatrix(self.R,self.S)
                self.C[2][0]=RS[0][0]

                for i in range(1,column-2):
                        M=mList[i].M
                        RM = multiplyMatrix(self.R, M)
                        RMS= multiplyMatrix(RM, self.S)
                        self.C[i+2][0]=RMS[0][0]
                        
                for i in range(1, column-1):
                        for j in range(i, column):
                                k=j-i
                                self.C[j][i]=self.C[k][0]
