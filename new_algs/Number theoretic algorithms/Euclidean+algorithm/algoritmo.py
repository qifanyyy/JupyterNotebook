def fatoracao_ingenua(numero):
    potencia = 0
    fator = 2
    vetor = []
    if (numero>=2):
        while (numero>1)or(fator<pow(numero,0.5)):
            if (numero%fator==0):
                while (numero%fator==0):
                    numero = numero/fator
                    potencia = potencia + 1
                print fator, potencia
                vetor.insert(len(vetor),fator)
                fator = fator + 1
                potencia = 0
            else:
                fator = fator + 1
    else:
        print "O numero fatorado deve ser maior ou igual a 2"
    return vetor
#fim fatoracao_ingenua

def modsoma(x,y,z):
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
    return (moduloa+modulob)%z
#fim modsoma

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

def potenciacao_fermat(base,exp,mod):
    r = 1
    A = base
    E = exp
    #trocando o E por algo mais curto!
    E = exp%(mod-1)
    print E

    while (E!=0):
        #argumento se E eh impar ou nao
        if (E%2!=0):
            arg = "S"
        else:
            arg = "N"

        print r,A,E,arg

        #agora o algoritmo em si
        if(E%2!=0):
            r = modprod(r,A,mod)
            E = (E-1)/2
        else:
            E = E/2
        A = modprod(A,A,mod)
    #fim do while

    #argumento se E eh impar ou nao
    if (E%2!=0):
        arg = "S"
    else:
        arg = "N"

    print r,A,E,arg
    return r
#fim potenciacao_fermat

def algoritmo_euclidiano(a,b):
    ao = a
    bo = b
    xo = 1
    xi = 0
    yo = 0
    yi = 1
    if (a!=0)and(b!=0):
        q = a//b
        print a,"- 1 0"
        print b,"- 0 1"
        while (b>0):
            ''' operacoes de divisao  '''
            d = b
            b = a%b
            a = d
            if (b!=0):
                ''' operacoes entre x e y'''
                dummyx = xi
                dummyy = yi
                xi = xo - q*xi
                yi = yo - q*yi
                xo = dummyx
                yo = dummyy
                '''fim operacoes x e y'''
                print b,q,xi,yi
                q = a//b
            else:
                print b,q,"- -"
        mdc = (xi*ao)+(yi*bo)
        #O xi eh o alfa e o yi eh o beta!
    return mdc,xi,yi
#Fim algoritmo_euclidiano

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
#Fim funcao mod

def algoritmo_chines(vetor_a,vetor_b):
    #O vetor_a  eh o vetor que contem a parte direita da equacao modular
    #exemplo
    # x = vetor_a[i] (mod vetor_b[i])
    #funciona para quantos forem o numero de equacoes modulares!
    i = 0

    while (i<(len(vetor_a)-1)):
        mdc,alfa,beta = algoritmo_euclidiano(vetor_b[i],vetor_b[i+1])
        print alfa,beta
        if (mdc==1):
            aux1a = (vetor_a[i+1] - vetor_a[i])*alfa
            aux1b = mod(aux1a,vetor_b[i+1])
            aux2 = vetor_b[i]*vetor_b[i+1]
            aux1b = (aux1b*vetor_b[i])+vetor_a[i]
            vetor_a[i+1] = aux1b
            vetor_b[i+1] = aux2
            print vetor_a[i+1],vetor_b[i+1]
            i =  i+1
        else:
            quit()
    print "---"
#fim algoritmo_chines


print "Suponha que n eh composto, todos seus fatores primos sao distintos!"
num,exp,modulo =  input()
vetor_fatores = fatoracao_ingenua(modulo)
print "Os fatores de",modulo,"sao",vetor_fatores
i = 0
vetor_a = []
vetor_b = []
while (i<len(vetor_fatores)):
    if (num%vetor_fatores[i]!=0):
        aux = potenciacao_fermat(num,exp,vetor_fatores[i])
        vetor_a.insert(len(vetor_a),aux)
        vetor_b.insert(len(vetor_b),vetor_fatores[i])
    else:
        print "0"
        vetor_a.insert(len(vetor_a),0)
        vetor_b.insert(len(vetor_b),vetor_fatores[i])
    i = i + 1

print "O vetor a eh",vetor_a
print "O vetor b eh", vetor_b

algoritmo_chines(vetor_a,vetor_b)
