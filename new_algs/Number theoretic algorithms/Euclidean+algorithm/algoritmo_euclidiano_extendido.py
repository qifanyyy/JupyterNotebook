#Algoritmo Euclidiano Estendido/ extended euclidean algorithm
#this basically finds the gcd between two numbers and the linear combination with those two numbers to find gdc
def algoritmo_euclidiano(a,b):
    # alfa*a + beta*b = mdc
    ao = a
    bo = b
    xo = 1
    xi = 0
    yo = 0
    yi = 1
    if (a!=0)and(b!=0):
        q = a//b
        print a,"*m + ",b,"*n = mdc(",a,",",b,")"
        print "R Q M N"
        print a,"- 1 0"
        print b,"- 0 1"
        while (b>0):
            # operacoes de divisao
            d = b
            b = a%b
            a = d
            if (b!=0):
                # operacoes entre x e y
                dummyx = xi
                dummyy = yi
                xi = xo - q*xi
                yi = yo - q*yi
                xo = dummyx
                yo = dummyy
                #fim operacoes x e y
                print b,q,xi,yi
                q = a//b
            else:
                print b,q,"- -"
        mdc = (xi*ao)+(yi*bo)
        #O xi eh o alfa e o yi eh o beta!
        return mdc
print "Insert the numbers you want to find the gcd of:"
a,b = input()
c = algoritmo_euclidiano(a,b)
print "gcd:",c
