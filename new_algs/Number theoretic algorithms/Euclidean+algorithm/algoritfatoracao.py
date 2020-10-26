print "algoritmo de potenciacao modular"
print "numero de vezes executado"

n = input ()

# D E F I N I N D O  F U N C O E S

#definindo funcao soma mod
'''x e y sao os numeros que queremos somar e z eh o mod'''
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


# A L G O R I T M O  D E  P O T E N C I A C A O  M O D U L A R    
          

while (n>0):
    base,exp,mod = input()
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
    n = n - 1
    print "---"
