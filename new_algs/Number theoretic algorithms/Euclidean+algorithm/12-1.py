def fatoracao_ingenua(numero):
    potencia = 0
    fator = 2
    vetor_fator = []
    vetor_potencia = []
    if (numero>=2):
        while (numero>1)or(fator<pow(numero,0.5)):
            if (numero%fator==0):
                while (numero%fator==0):
                    numero = numero/fator
                    potencia = potencia + 1
                print fator, potencia
                vetor_fator.insert(len(vetor_fator),fator)
                vetor_potencia.insert(len(vetor_potencia),potencia)
                fator = fator + 1
                potencia = 0
            else:
                fator = fator + 1
    else:
        print "O numero fatorado deve ser maior ou igual a 2"
    return vetor_fator,vetor_potencia
#fim fatoracao_ingenua

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

def potenciacao_modular_fermat(base,exp,mod):
    r = 1
    A = base
    E = exp
    #trocando o E por algo mais curto!
    E = exp%(mod-1)

    while (E!=0):

        #agora o algoritmo em si
        if(E%2!=0):
            r = modprod(r,A,mod)
            E = (E-1)/2
        else:
            E = E/2
        A = modprod(A,A,mod)
    #fim do while
    return r
#fim
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
#fim

k = input()
while (k>0):
    numero = input()
    fatores,potencias = fatoracao_ingenua(numero-1)
    lista_h = []
    i = 0
    print fatores, "sao os fatores"
    print potencias, "sao as potencias"

    while (i<len(fatores)):
        print "Estudando o fator",fatores[i]
        a = 2
        auxiliar = potenciacao_modular_fermat(a,(numero-1)/fatores[i],numero)
        print "o auxiliar eh",auxiliar
        while(auxiliar==1):
            a = a + 1
            auxiliar = potenciacao_modular_fermat(a,(numero-1)/fatores[i],numero)
        print "O a eh",a
        h = potenciacao_modular_fermat(a,(numero-1)/fatores[i]**potencias[i],numero)
        print "O h eh",h
        lista_h.insert(len(lista_h),h)
        i = i + 1
    g = 1
    i = 0
    print lista_h
    while (i<len(fatores)):
        g = g * lista_h[i]
        i = i + 1
    print "O g original eh",g
    print "O g pos mod eh", mod(g,numero)
    k = k - 1
