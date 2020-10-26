import random

#function to multiply two integer
#it uses the Karatsuba Mutiplication: km
def km(x,y):
    sizex=len(x)
    sizey=len(y)

    # check if the size of number is odd
    if (sizex%2!=0 ):
        x='0'+x
        sizex=len(x)
    if(sizey%2!=0):
        y='0'+y
        sizey=len(y)
    if sizex==2:
        a=x[0];b=x[1];c=y[0];d=y[1]
        a=int(a);b=int(b);c=int(c);d=int(d)
        result=100*(a*c)+10*(a*d+b*c)+b*d
        return result
    else:
        #Devide and conqure x,y and
        #create new x,y
        xa=x[0:sizex/2]
        xb=x[sizex/2:sizex]
        yc=y[0:sizex/2]
        yd=y[sizex/2:sizex]
        return 10**sizex*km(xa,yc)+10**((sizex)/2)*(km(xa,yd)+km(xb,yc))+km(xb,yd)

def km_testcases(n):
    for i in range(n):
        print i
        x=str(random.randint(0,2**1000))
        y=str(random.randint(0,2**1000))
        print x,y
        sizex=len(x)
        sizey=len(y)
        diffsize=max(sizex,sizey)
        x=x.zfill(diffsize)
        y=y.zfill(diffsize)
        final_result=km(x,y)
        print final_result
        
print "how many test cases you wish to run?"
test_number=input()
km_testcases(test_number)

