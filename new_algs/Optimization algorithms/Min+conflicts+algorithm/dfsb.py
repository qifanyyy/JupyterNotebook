import sys
import time
import copy
from collections import deque

global count
global cnt
global prunes
prunes=0
count=0
cnt=0

#------------------------------------------------------- DFSB---------------------------------------------------------------------------------
# This is the naive DFSB algorithm
def backtrack(v, x, out_file, adjList):
    #if time.time() - start_time > 60:
        # time.stop()
        # print(time.time()-start_time)

       #print("count:", cnt)
        #return 0
    if v == N:
        print(x)

        #print("count:", cnt)
        file = open(out_file, 'w')
        for i in x:
            file.write(str(i) + '\n')
        return 1
    else:

        global cnt
        for c in range(0, C):
            if (possible(v, c, x, adjList)):
                x[v] = c
                cnt=cnt+1
                if (backtrack(v + 1, x, out_file, adjList) == 1):
                    return 1
            x[v] = -1

        return 0


def possible(v, i, x, adjList):
    for j in adjList[v]:
        # print(j)
        if i == x[j]:
            return 0

    return 1

#------------------------------------------------ DFSB+----------------------------------------------------------------------------------------------
# This is improved DFSB algorithm with MRV, LCV and AC-3 heuristics

def inference(x,l,adjList,domainListnew): # This performs the AC-3 consistency check heuristic
    while len(l)!=0:
        a = l.popleft()
        #print(a)
        [remove,domainListnew] = remove_inconsistent_values(a,domainListnew)

        if remove==1:
            global prunes
            prunes = prunes+1
            if len(domainListnew[a[0]])==0:
                return (0,domainListnew)
            adjlisttemp = [item for item in adjList[a[0]] if item!=a[1]]

            for j in adjlisttemp:#adjList[a[0]]:
                b = [j,a[0]]
                if assigned[j]!=1:
                    l.append(b)
        #print("modified l:",l)


    return (1,domainListnew)

def remove_inconsistent_values(a,domainListnew):

    removed= 0
    if len(domainListnew[a[1]])==1:
        #print("a[1]:",a[1])
        c = domainListnew[a[1]][0]
        #print("c:",c)
        if c in domainListnew[a[0]]:
            domainListnew[a[0]].remove(c)
            removed = 1
    return (removed,domainListnew)




def order_domain_values(v,adjList,domainList): # This function orders the domain values of the variable according to LCV heuristic
    order=[]
    for c in domainList[v]:

        min=100
        for i in adjList[v]:

            temp = len(domainList[i])
            #print(i,temp)
            if c in domainList[i]:
                temp = temp-1
                #print(temp)
            if(temp<min):
                min = temp
        order.append([c,min])
        #o = sorted(order,reverse=True)
        o = sorted(order, key=lambda x: x[1],reverse=True)
        color = [item[0] for item in o]
    return color



def select_unassigned(domainList,assigned): # This function selects unassigned variables according to MRV heuristic
    min = 1000
    next = -1

    for i in range(N):

        if (len(domainList[i]) < min and assigned[i] !=1):
            min = len(domainList[i])

            next = i
    #print("next:", next)
    return next

def is_possible(v,i,x,adjList):

    for j in adjList[v]:
        #print(j)
        if i ==x[j]:
            return 0

    return 1

def backtrackplus(x,out_file,adjList,domainList,assigned): # This is the main backtracking code to implement DFSB+
    if -1 not in assigned:
        #print(x)
        file = open(out_file, 'w')
        for i in x:
            file.write(str(i) + '\n')
        return x
    v = select_unassigned(domainList, assigned)

    c_order = order_domain_values(v,adjList,domainList)
    for c in c_order: #domainList[v]:

        domainListnew=copy.deepcopy(domainList)
        if (is_possible(v, c, x, adjList)):


            domainListnew[v] = [item for item in domainList[v] if item == c]
            #print(domainListnew)
            array = []
            for j in adjList[v]:
                a = [j,v]
                if assigned[j]!=1:
                    array.append(a)
                l=deque(array)
            #print(l)
            [inferences,dlist] = inference(v,l,adjList,domainListnew)
            #print("inferences:",inferences,"dlist:",dlist)
            if inferences==1:
                x[v] = c
                #print("x:", x)
                assigned[v] = 1
                #print("assigned:", assigned)
                domainListnew = dlist
                global count
                count=count+1
                result = backtrackplus(x,out_file,adjList,domainListnew,assigned)
                if result!=0:
                    return result
        x[v]=-1
        assigned[v]=-1

    return 0


if __name__ == "__main__":
    global N,M,C

    if len(sys.argv) == 4:
        in_file = sys.argv[1]
        out_file = sys.argv[2]
        Algorithm = int(sys.argv[3])

    else:
       print('Wrong number of arguments.')


    d = []
    with open(in_file, 'r') as f:
        for line in f:
            data = line.split()
            for i in data:
                d.extend(i.split(','))

        k = [int(x) for x in d]
        print(k)
    N = k[0]
    #print(N)
    M = k[1]
   # print(M)
    C = k[2]
    #print(C)
    x = [-1 for i in range(N)]

    adjList = [[] for k in range(N)]
    for i in range(3,2*(M+1),2):

        adjList[k[i]].append(k[i+1])
        adjList[k[i+1]].append(k[i])

    for i in range(N):
        j = list(set(adjList[i]))
        adjList[i] = j

    print(adjList)

    assigned = [-1 for i in range(N)]

    domainList = [[] for k in range(N)]
    for i in range(0,N):
        for j in range(0,C):
            domainList[i].append(j)


    if Algorithm==0:
        cnt=0
        global start_time
        start_time = time.time()
        if (backtrack(0, x, out_file, adjList) == 0):
            print("No answer")
            file = open(out_file, 'w')
            file.write("No answer")
        print("--- %s Seconds ---" % (time.time() - start_time))


    if Algorithm==1:
        start_time = time.time()
        res = backtrackplus( x, out_file, adjList, domainList,assigned)
        if res==0:
            file=open(out_file,'w')
            file.write("No answer")
            print("No answer")
        print("--- %s seconds ---" % (time.time() - start_time))
        print(res)
        #print("count:",count)
        #print(" Arc prunes:",prunes)

        for i in range(N):
            for j in adjList[i]:
                if res[i]==res[j]:
                    print("error")
        print("No error")



