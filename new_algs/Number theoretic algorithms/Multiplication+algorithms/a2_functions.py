import sys, math, random
from copy import deepcopy
# Print an N by N matrix to console.

def printMatrix(M):
        COL = len(M);
        ROW = len(M[1]);
        for i in range (0, COL):
                print;
                for j in range(0, ROW):
                        print M[i][j],
        print;

# Multiples two matricies

def multiplyMatrix(A, B):
    A_ROW = len(A)
    A_COL = len(A[0])
    B_ROW = len(B)
    B_COL = len(B[0])
    new = [[0 for x in xrange(B_COL)] for x in xrange(A_ROW)]
    if (A_COL==B_ROW):
        for i in range (0, A_ROW):
            for j in range(0, B_COL):
                for k in range(0, A_COL):
                    #print "%d %d %d"%(i,j,k)
                    new[i][j]=(new[i][j])^(A[i][k]&B[k][j])
        return new  
    else:
        print "ERROR IN multiplyMatrix() MATRIX DIMENSIONS DO NOT MATCH."
        sys.exit(0)

def getRMS(R, M, S):
        LEN = len(R)
        RM = [0 for x in xrange(LEN)]
        for i in range(0,LEN):
                for j in range(0,LEN):
                         RM[i]=RM[i]^(R[j]&M[j][i])
        RMS = 0
        for i in range(0, LEN):
                RMS=RMS^(RM[i]&S[i])
        return int(RMS)


# Generate an N by N matrix, and fill it with random bits.
def randomMatrix(N):
        sys.stdout.flush();
        M = [[0 for x in xrange(N)]for x in xrange(N)]
        for i in range (0, N):
                for j in range(0, N):
                        M[i][j]=random.getrandbits(1);
        return M;

# Determine the submatrix M of a matrix A. N is the NEW matrix size.
def subMatrix(A, N):
        shift=len(A[0])-N;
        M = [[0 for x in xrange(N)] for x in xrange(N)]
        for i in range(0, N):
                for j in range (0, N):
                        #Get and set shifted element from A
                        tmp     = A[i+shift][j+shift];
                        M[i][j] = tmp;
        return M;

def testRes(N, A, p):
        temp = [[0 for x in xrange(N)] for x in xrange(N)]
        zer0 = deepcopy(temp)
        Ai = deepcopy(A)
        if (p[N][0]==1):
                for i in range(0, N):
                        temp[i][i]=1
        for i in range(0, N):
                if (p[N-1-i][0]==1):
                        for j in range(0,N):
                                for k in range(0,N):
                                        temp[j][k] = temp[j][k]^Ai[j][k]
                Ai = multiplyMatrix(Ai,A)
        if (temp==zer0):
                print "Passed"
        else:
                print "Failed"
                
