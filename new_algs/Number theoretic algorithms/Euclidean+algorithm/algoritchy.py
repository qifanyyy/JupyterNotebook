#Definindo funcoes

def algoritmo_euclidiano_mdc(a,b):
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

def algoritmo_euclidiano_alfa(a,b):
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
        return xi
#fim algoritmo_euclidiano_alfa

def vetor_primos_entre_si(n):
    #num eh o numero em si
    vetor = []
    vetor.insert(len(vetor),1)
    i = 2
    while (i<n):
        if (algoritmo_euclidiano_mdc(n,i)==1):
            vetor.insert(len(vetor),i)
        i = i+1
    return vetor
#fim vetor_primos_entre_si

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
#fim funcaomod

#definindo funcao multiplicacao em mod
def modprod(x,y,z):
    #trabalhando com x
    if (x<0):
        aauxiliar = -1*x
        if (aauxiliar%z != 0):
            naquociente = aauxiliar//z + 1
            moduloa = naquociente * z - aauxiliar
        else:
            moduloa = 0
    else:
        moduloa = x%z

    #trabalhando com y
    if (y<0):
        bauxiliar = -1*y
        if (bauxiliar%z != 0):
            nbquociente = bauxiliar//z + 1
            modulob = nbquociente * z - bauxiliar
        else:
            modulob = 0
    else:
        modulob = y%z
    return (moduloa*modulob)%z
#fim modprod

numero, vetor_subconjunto = input()
vetor_origem = vetor_primos_entre_si(numero)

print vetor_subconjunto, " eh o vetor_subconjunto"
print vetor_origem, " eh o vetor_origem"

vetor_subconjunto.sort()

#   Primeira parte
arg = True
i = 0
while (i<len(vetor_subconjunto)):
    if vetor_subconjunto[i] not in vetor_origem:
        arg = False
        break
    i = i + 1
#fim primeira parte
print "Na primeira parte eh", arg
#   Segunda parte
i = 0
j = 0
if arg is not False:
    while (i<len(vetor_subconjunto)):
        while (j<len(vetor_subconjunto)):
            modproduto = modprod(vetor_subconjunto[i],vetor_subconjunto[j],numero)
            print "O modprod entre",vetor_subconjunto[i],"e",vetor_subconjunto[j],"modulo",numero,"eh",modproduto
            if modproduto not in vetor_subconjunto:
                arg = False
                break
            j = j + 1
        if arg is False:
            break
        i = i + 1
        j = i
if arg is False:
    print "False"
else:
    print "True"

#fim segunda parte

#   Terceira parte
if arg is not False:
    if 1 not in vetor_subconjunto:
        arg = False
#fim terceira parte

#   Quarta parte
i = 0
if arg is not False:
    while (i<len(vetor_subconjunto)):
        if (algoritmo_euclidiano_mdc(vetor_subconjunto[i],numero)==1):
            auxiliar = algoritmo_euclidiano_alfa(vetor_subconjunto[i],numero)
            auxiliar = mod(auxiliar,numero)
            if auxiliar not in vetor_origem:
                arg = False
                break
        else:
            arg = False
            break
        i = i + 1
#fim quarta parte

#Printando a porra
if arg is True:
    print "SIM"
    print "---"
else:
    print "NAO"
    print "---"
