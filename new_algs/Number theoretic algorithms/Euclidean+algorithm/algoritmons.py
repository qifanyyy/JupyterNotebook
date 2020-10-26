#Definindo funcoes

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
                q = a//b
        mdc = (xi*ao)+(yi*bo)
        #O xi eh o alfa e o yi eh o beta!
        return mdc
#fim Euclidiano


k = input()
#k eh o numero de vezes de operacao
while (k>0):
    n = input()
    #num eh o numero em si
    vetor = []
    vetor.insert(len(vetor),1)
    i = 2
    while (i<n):
        if (algoritmo_euclidiano(n,i)==1):
            vetor.insert(len(vetor),i)
        i = i+1
    print vetor
    print "---"
    k = k - 1
