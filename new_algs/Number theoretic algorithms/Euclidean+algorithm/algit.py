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

def grupo_mdc1(n):
    #num eh o numero em si
    vetor = []
    vetor.insert(len(vetor),1)
    i = 2
    while (i<n):
        if (algoritmo_euclidiano(n,i)==1):
            vetor.insert(len(vetor),i)
        i = i+1
    print vetor
    return vetor
#fim grupo grupo_mdc1

def mod(x,z):
    if (x<0):
        aauxiliar = -1*x
        if (aauxiliar%z != 0):
            naquociente = aauxiliar//z + 1
            moduloa = naquociente * z - aauxiliar
        else:
            moduloa = 0
    else:
        moduloa = x%z
    return moduloa
#fim mod

n = input()
vetor_origem = grupo_mdc1(n)
vetor_subgrupo = []
i = 0
j = 1
valor = 0
while (i<len(vetor_origem)):
    while (valor!=1):
        valor =  mod(vetor_origem[i]**j,n)
        vetor_subgrupo.insert(len(vetor_subgrupo),valor)
        j = j+1
    vetor_subgrupo.sort()
    print vetor_subgrupo
    vetor_subgrupo = []
    valor = 0
    j = 1
    i=i+1
