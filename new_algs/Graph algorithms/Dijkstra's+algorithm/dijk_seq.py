import random
import time

globvar = 1
INT_MAX = 1000000000
N=16384
DEG=16
P=1
u=0
W = [[0 for x in range(DEG)] for x in range(N)]
W_index = [[0 for x in range(DEG)] for x in range(N)]
D = [0 for x in range(N)]
Q = [0 for x in range(N)]


def graph():
    print 'Hello, world!'
    global globvar
    global W
    global W_index
    global P
    global INT_MAX
    global D
    global Q
    global u
    
    for i in range(0,N):
        for j in range(0,DEG):
            W_index[i][j] = i+j
            if W_index[i][j] >= N-1 :
                W_index[i][j] = N-1
            W[i][j] = random.randint(1, 10) + j
            if i==j:
                W[i][j]=0
            #print W[i][j]

def array_init():
    for i in range(0,N):
        D[i] = INT_MAX
        Q[i] = 1
    D[0] = 0

def do_work():
    local_count=N
    u=0
    while local_count!=0:                        #outer loop
        min1 = INT_MAX
        min_index1 = N-1
        
        for j in range(0,DEG):                   #local_min
            if(D[j] < min1 and Q[j]):            #inner loop
                min1 = D[j]
                min_index1 = W_index[u][j]

#barrier
#if tid==0:

#barrier

        u=min_index1
        Q[u]=0
        
        for i in range(0,DEG):                    #relax
            if D[W_index[u][i]] > D[u] + W[u][i]:
                D[W_index[u][i]] = D[u] + W[u][i];
        
        local_count = local_count-1

def main():
    graph()
    array_init()
    
    start_time = time.time()

    do_work()
    
    print time.time()-start_time,"seconds"


if __name__ == "__main__":
    main()
