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
    print "O n menos um eh",n-1
    fator = []
    fator = fatoracao_ingenua(n-1)
    expoente = []
    i = 0
    contador = 0

    ''' Montando vetor expoentes'''
    while (i<len(fator)):
        expoente.insert(len(expoente), (n-1)/ fator[i])
        i = i+1
    print "Os expoentes sao",expoente
    ''' Fim deste treci'''

    while (1):
        
        
        
        if (contador == len(expoente)):
            print "PRIMO"
            print "---"
            break

        print "Usando b =",b
        r_aux = 0
        i = 0
        
        r = alg_potenciacao_modular(b,n-1,n)
        print b,"^",n-1,"=",r,"(mod",n,")"
        if (r!=1):
            print "COMPOSTO"
            print "---"
            break

        

        while (i<len(fator)):
            if (expoente[i]!=0):
                print "Potencia eh",(expoente[i])
                r_aux = alg_potenciacao_modular(b,expoente[i],n)
                print b,"^",expoente[i],"=",r_aux,"(mod",n,")"
            if (r_aux!=1 and expoente[i]!=0):
                print "Como o resto (",r_aux,") eh diferente de um, cortamos o expoente",expoente[i]
                expoente[i] = 0
                print "expoente[",i,"] =",expoente[i]
                contador = contador + 1
                    
                    
            i = i + 1
        print "BREAK! Vamos para o proximo numero!"
        b = b + 1

    k = k - 1
