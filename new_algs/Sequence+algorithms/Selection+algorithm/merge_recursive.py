#!/usr/bin/python
#RECURSIVE FUNCTION
   
def insert_elements():
    print ("Do you want to enter numbers Manually(Yes - 1/ No- 0):?")
    x=input()
    a=[]
    if(x==0):
        a=[3,2,4,7,31,2,-1,4,1,2,3,1,2,1,3]
    elif(x==1):
        print ("please enter input: ")
        print ("press -1 to exit ")
        x=input()
        while(x!= -1):
            a.append(x)
            x=input()
    else:
        print ("Not a avalid input")
    return a




def append(a):
    N=len(a)
    global y
    y=0

    if(N>0):
        y=float(math.log(N)/(math.log(2)))
        y=math.ceil(y)
    
        while((2**y) > N):

            a.append(9999)
            N=len(a)
    return a


def merge(a,i):
    if(i<y+1):
        N=len(a)
        l=0
        m=2**i
        x=2**i
        b=[]
        print("#######################################")
        print( "m  & l :",(m,l))
        print ("the unsorted list at the stage ",i,"is:")
        print (a)
        while(m<=N):
            p=l
            q=m-(x/2)
            print ("p & q",(p,q))
            while((p<(m-(x/2))) and q< m):
                
                if(a[p]<a[q]):
                    b.append(a[p])
                    p=p+1                   
                else :
                    b.append(a[q])
                    q=q+1

            while( q<m):
                b.append(a[q])
                q=q+1
            while(p<(m-(x/2))):
                b.append(a[p])
                p=p+1
            print (b)
            l=m
            m=m+x
            
        i=i+1
        a=merge(b,i)
    return a


if(__name__=='__main__'):
    import math
    a=insert_elements()
    print ("\nthe input array is:")
    print (a)
    print (" ")
    a=append(a)
    print ("The input array after appending some numbers")
    print (a)
    y=int(y)# gives the number of times the merge has to be done 
    #print y
    a=merge(a,1)
    print ("\n\n\nsorted array is :\n")
    print (a)



        
    
