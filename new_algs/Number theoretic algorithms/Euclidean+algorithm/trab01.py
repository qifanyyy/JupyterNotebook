# D E F I N I N D O  F U N C O E S

#definindo funcao mod
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


#definindo funcao soma mod#definindo funcao multiplicacao em mod
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
    print "---"
    return r

#FIM DE DEFINIR FUNCOES, AGORA EH MAIN

n,b = input()
q = n-1
k = 0
i = 0
while ((q%2)==0):
    q = q/2
    k = k + 1
print "Este eh o q",q,"Este eh o k",k
print "---"
aux = alg_potenciacao_modular(b,q,n)
modulo = mod(aux,n)
arg = False
arg2 = False

if (modulo==1):
    print "Resultado inconclusivo, pseudoprimo para base",b
    arg = True
while (i<b) and arg is False:
    i = i + 1
    aux = aux * aux
    aux = mod(aux,n)
    if (aux==-1):
        print "Resultado inconclusivo, pseudoprimo para base",b
        arg2 = True
        break
    if (aux==1):

        break
if arg2 is not True:
    print "O numero",n,"eh composto"
