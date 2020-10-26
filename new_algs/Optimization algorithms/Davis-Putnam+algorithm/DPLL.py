"Algoritmo DPLL"

'''
class Clausula:
    def __init__(self, atributos[]):
        self.atributos
        print("Clausula inicializada")

class Clausulas:
    def __init__(self, clausulas[]):
        self.clausulas = clausulas

class Atributo_
def __init__(self, literal, negado = False):
    self.literal = literal
    self.negado = negado
    print("Atributo inicializado")

def DPLL(estrutura):
    evaluar(estructura)
    if not estructura:
        return True
    for clausula in clausulas:
        if not clausula or (clausula == False):
            return false
        if len(estructura) == 1:
            "Tomar valor de variable"
        "Actualizar matriz (metodo)"
        "Obtener clausula más pequeña"
        for i in range(len(puros)):
            if (incidencias[i] > 0 and puros[i] == True):
                variable = variables[i]
            break

x = None
print(x)
'''
import string

encontropuro = False
variables = []

class Variable:
    def __init__(self, var, incidencias = 1, anterior = None, puro = True):
        self.var = var
        self.incidencias = incidencias
        self.anterior = anterior
        self.puro = puro

def InicializarTabla():
    global variables 
    variables = None
    anterior = None

def EvaluarSentencia(sentencia):
    aux=[]
    quita = False
    for clausula in sentencia:
        quita = False
        for caracter in clausula:
            if caracter == '0':
                clausula = clausula.replace(caracter, '')
                #print("Calusula ", clausula)
            if caracter == '1':
                quita=True
                #print("Sentencia ", sentencia)
                break
        if quita is False:
            aux.append(clausula)
    
    return aux

def Sustituye(sentencia, caracter):
    aux = []
    if sentencia is None:
        print("nulo")
    else:
        for clausula in sentencia:
            if(caracter in string.ascii_uppercase):
                clausula = clausula.replace(caracter, '1')
                clausula = clausula.replace(caracter.lower(),'0')
            if(caracter in string.ascii_lowercase):
                clausula = clausula.replace(caracter, '1')
                clausula = clausula.replace(caracter.upper(),'0')
            aux.append(clausula)
    return aux;

def ActualizaMatriz(clausula):
    global variables
    anterior = True;
    for caracter in clausula:
        seencontro = False
        if not variables:
            variables = []
            if(caracter in string.ascii_lowercase):
                anterior = False
            if(caracter in string.ascii_uppercase):
                anterior = True
            variables.append( Variable(caracter, 1, anterior, True) )
        else:
            for variable in variables:
                if variable.var.upper() == caracter.upper():
                    seencontro = True
                    variable.incidencias = variable.incidencias + 1
                    if variable.anterior is None:
                        if(caracter in string.ascii_uppercase):
                            variable.anterior = True
                        else:
                            variable.anterior = False
                    else:
                        if variable.anterior is False:
                            if(caracter in string.ascii_uppercase):
                                variable.anterior = True
                                variable.puro = False
                            else:
                                variable.anterior = False
                        else:
                            if variable.anterior is True:
                                if(caracter in string.ascii_lowercase):
                                    variable.anterior = False
                                    variable.puro = False
            if not seencontro:
                if(caracter in string.ascii_lowercase):
                    anterior = False
                if(caracter in string.ascii_uppercase):
                    anterior = True
                variables.append( Variable(caracter, 1, anterior, True) )


def BuscaPuro(sentencia):
    global variables
    global encontropuro
    
    for variable in variables:
        if variable.puro == True:
            if variable.incidencias > 0 :
                encontropuro = True
                print("entonctro puro")
                if variable.anterior is True:
                    return Sustituye(sentencia, variable.var.upper())
                if variable.anterior is False:
                    return Sustituye(sentencia, variable.var.lower())
    return sentencia
'''
    if(True in puro and incidencias[puro.index(True)] > 0):
        if(anterior[puro.index(True)]):
            entcontropuro = True
            return variables[puro.index(True)].upper()
        else:
            entcontropuro = True
            return variables[puro.index(True)].lower()
        
        '''
def BuscaHeuristica(sentencia):
    print("heur")
    global variables
    tamMayor=0;
    if(variables is None):
        print()
    else:
        for variable in variables:
            if tamMayor < variable.incidencias:
                tamMayor = variable.incidencias
                aSustituir = []
                aSustituir.append(variable.var)
            elif tamMayor == variable.incidencias:
                aSustituir.append(variable.var)
        clausulaMinima = len(sentencia[0])
        for variable in aSustituir:
            for clausula in sentencia:
                if variable in clausula:
                    #print(clausula.index(variable))
                    if len(clausula) <= clausulaMinima:
                        clausulaMinima = len(clausula)
                        variablesustituida = variable

    return Sustituye(sentencia, variablesustituida)

def DPLL(sentencia):
    sustituido = False
    InicializarTabla()
    global encontropuro
    
    print ("sent ",sentencia)
    sent = EvaluarSentencia(sentencia)
    print ("Evalua ",sent)
    if not sent:
        return True
    for i in range(len(sent)):
        if(len(sent[i]) == 0):
            return False
        if(len(sent[i]) == 1):
            sent = Sustituye(sent, sent[i][0])
            sustituido = True
        ActualizaMatriz(sent[i])
    if not sustituido:
        sent = BuscaPuro(sent)
        print("bandera ", encontropuro)
    if encontropuro is False and sustituido is False:
        sent = BuscaHeuristica(sent)
    if(DPLL(sent)):
        return True
    return False

print(DPLL(["AbCdf","aBcDE","BD","F","bde"]))




