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
#fim alg_potenciacao_modular

m = input()
while (m>0):
    n = input()
    fermat = 2**(2**n)+1
    print fermat
    r = alg_potenciacao_modular(5,((fermat-1)/2),fermat)
    if(r==(fermat-1)):
        print "PRIMO"
        print "---"
    else:
        print "COMPOSTO"
        print "---"
    m = m - 1
