import multiprocessing
import sys
import os
import time

def input_mat():
    print("Enter First Dimension of Matrix:")
    n=int(input())
    print("Enter Second Dimension of Matrix:")
    k=int(input())
    matrix=[]
    print("Enter elements of Matrix:")
    for i in range(n):
        row=list(map(int,input().split()))
        matrix.append(row)
    return n,k,matrix

def calc(pipe_l,pipe_r,pipe_t,pipe_b,n,m,k,i,j,result):
    ans=0
    for l in range(k):
        ip1=pipe_l.recv()
        ip2=pipe_t.recv()
        ans+=ip1*ip2
        pipe_r.send(ip1)
        pipe_b.send(ip2)

    row_result=result[i]
    row_result[j]=ans
    result[i]=row_result

if __name__=='__main__':
    n,k1,matrix1=input_mat()
    k2,m,matrix2=input_mat()
    if k1!=k2:
        sys.exit(-1)
    else:
        k=k1

    manager=multiprocessing.Manager()
    result=manager.list()
    for i in range(0,n):
        row=manager.list()
        for j in range(0,m):
            row.append(0)
        result.append(row)

    parent_pipe_t=[]
    child_pipe_t=[]

    for i in range(n+1):
        rowp=[]
        rowc=[]
        for j in range(m+1):
            parent,child=multiprocessing.Pipe()
            rowp.append(parent)
            rowc.append(child)
        parent_pipe_t.append(rowp)
        child_pipe_t.append(rowc)

    parent_pipe_l = []
    child_pipe_l = []

    for i in range(n+1):
        rowp=[]
        rowc=[]
        for j in range(m+1):
            parent,child=multiprocessing.Pipe()
            rowp.append(parent)
            rowc.append(child)
        parent_pipe_l.append(rowp)
        child_pipe_l.append(rowc)

    process=[]

    for i in range(n):
        row=[]
        for j in range(m):
            p=multiprocessing.Process(target=calc,args=(child_pipe_l[i][j],parent_pipe_l[i][j+1],child_pipe_t[i][j],parent_pipe_t[i+1][j],n,m,k,i,j,result))
            row.append(p)

        process.append(row)

    for i in range(n):
        for j in range(m):
            process[i][j].start()


    for i in range(n):
        for j in range(k-1,-1,-1):
            parent_pipe_l[i][0].send(matrix1[i][j])


    for i in range(m):
        for j in range(k):
            parent_pipe_t[0][i].send(matrix2[j][i])

    for i in range(n):
        for j in range(m):
            process[i][j].join()

    print("Answer")
    for i in range(len(result)):
        print(result[i])



