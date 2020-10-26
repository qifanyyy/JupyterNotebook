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
                fator = fator + 1
                potencia = 0
            else:
                fator = fator + 1
    else:
        print "O numero fatorado deve ser maior ou igual a 2"
    return vetor_fator
#fim fatoracao_ingenua

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

#definindo algoritmo potenciacao modular
def alg_potenciacao_modular(base,exp,mod):
    r = 1
    A = base
    E = exp

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
#fim potenc.potenciacao_modular_fermat

k = input()
while (k>0):
    b = 2
    n = input()
    fator = []
    flag = 1
    fator = fatoracao_ingenua(n-1)

    while (flag==1):
        print "Usando b =",b
        flag = 0
        r_aux = 0
        i = 0
        print n-1
        r = alg_potenciacao_modular(b,n-1,n)
        if (r!=1):
            print "COMPOSTO"
            print "---"
            break
        while (i<len(fator) and flag!=1):
            print "Potencia eh",((n-1)/fator[i])
            r_aux = alg_potenciacao_modular(b,((n-1)/fator[i]),n)
            if (r_aux==1):
                print "BREAK"
                b = b + 1
                flag = 1
            i = i + 1
        if (flag==0):
            print "PRIMO"
            print "---"
        if (b==n-1 and flag==1):
            print "COMPOSTO"
            print "---"
            break
    k = k - 1
