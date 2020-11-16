import random
from deap import base, creator, tools, algorithms
import numpy
import importlib.util
from math import exp
import copy


spec = importlib.util.spec_from_file_location("introduceGrafo", "FuncionesGrafos.py")
foo = importlib.util.module_from_spec(spec) #foo es la variable que se usará como representación de la clase con el código de Ángel
spec.loader.exec_module(foo)

##########################################################################################################################################
def seleccionaColores():
    #Pedimos al usuario que introduzca el número de vertices
    numColores= input("Introduzca el número de colores que tendrá su grafo (al menos 3). Si no asigna una cantidad igual o superior se le asignará '3' por defecto:")
    
    #En el siguiente bucle comprobaremos si efectivamente ha metido un número, en caso contrario le seguiremos pidiendo que lo introduzca
    while 1:
        if numColores==None or not numColores.strip().isdigit():
            print("\n Ha introducido: "+numColores+", que no es un número")
            numColores=input("Por favor introduzca un número de colores (mayor o igual a '3' para la ejecución):")
        else:
            numColores= int(numColores.strip()) # Convertimos el string en un número.
            break;
    
    if numColores>2:
        return(numColores)
    else:
        return(3)

##########################################################################################################################################

def seleccionarPoblacion():
    #Pedimos al usuario que introduzca el número de vertices
    numPoblacion= input("Introduzca la población que tendrá su grafo, al menos 50. Si no asigna una cantidad superior igual, se le asignará '50' por defecto:")
    
    #En el siguiente bucle comprobaremos si efectivamente ha metido un número, en caso contrario le seguiremos pidiendo que lo introduzca
    while 1:
        if numPoblacion==None or not numPoblacion.strip().isdigit():
            print("\n Ha introducido: "+numPoblacion+", que no es un número")
            numPoblacion=input("Por favor introduzca un número de población (mayor o igual a '50' para la ejecución):")
        else:
            numPoblacion= int(numPoblacion.strip()) # Convertimos el string en un número.
            break;
    
    if numPoblacion>=50:
        return(numPoblacion)
    else:
        return(50)
    
##########################################################################################################################################

def seleccionarIteracionesAG():
    #Pedimos al usuario que introduzca el número de vertices
    iteraciones = input("Introduzca el número de iteraciones que tendrá el algoritmo genético. Si selecciona '0' sólo se realizará el coloreado mediante enfriamiento simulado.")
    
    #En el siguiente bucle comprobaremos si efectivamente ha metido un número, en caso contrario le seguiremos pidiendo que lo introduzca
    while 1:
        if iteraciones==None or not iteraciones.strip().isdigit():
            print("\n Ha introducido: "+iteraciones+", que no es un número")
            iteraciones=input("Por favor introduzca el número de iteraciones que tendrá el algoritmo genético.")
        else:
            iteraciones= int(iteraciones.strip()) # Convertimos el string en un número.
            break;
    
    if iteraciones>=0:
        return(iteraciones)
    else:
        return(0)
        
def seleccionarIteracionesSA():
    #Pedimos al usuario que introduzca el número de iteraciones de SA
    iteraciones = input("Introduzca el número de iteraciones que tendrá el enfriamiento simulado. Si selecciona '0' sólo se realizará el coloreado mediante algoritmo genéticos:")
    
    #En el siguiente bucle comprobaremos si efectivamente ha metido un número, en caso contrario le seguiremos pidiendo que lo introduzca
    while 1:
        if iteraciones==None or not iteraciones.strip().isdigit():
            print("\n Ha introducido: "+iteraciones+", que no es un número")
            iteraciones=input("Por favor introduzca el número de iteraciones que tendrá el enfriamiento simulado:")
        else:
            iteraciones= int(iteraciones.strip()) # Convertimos el string en un número.
            break;
    
    if iteraciones>=0:
        return(iteraciones)
    else:
        return(0)
    
##########################################################################################################################################


def evaluacion1(individuo):
        

    #AQUÍ DEBEMOS VER EL SI LOS VÉRTICES TIENEN VECINOS CON EL MISMO COLOR QUE ELLOS
    numColorRepetido = 0
    i = 0
    coloresTotales = set(individuo)
    for n in diccionario.keys():
        listaVecinos = numpy.array(diccionario[n]).tolist()
        for v in listaVecinos:
            coloresTotales.add(individuo[i])
            if individuo[i]==individuo[int(v)]:
                numColorRepetido += 100
        i+=1
    numColorRepetido += len(coloresTotales)
    
    return (numColorRepetido,)

###############################################################################################################

def seleccionarProbabilidadCruce():
    #Pedimos al usuario que introduzca el número de vertices
    probCruce= input("Introduzca la probabilidad de que dos individuos se crucen. Debe ser un valor entre 30 y 99%. De lo contrario, se le asignará 30%.")
    
    #En el siguiente bucle comprobaremos si efectivamente ha metido un número, en caso contrario le seguiremos pidiendo que lo introduzca
    while 1:
        if probCruce==None or not probCruce.strip().isdigit():
            print("\n Ha introducido: "+probCruce+", que no es un número")
            probCruce=input("Por favor  introduzca la probabilidad de que dos individuos se crucen. Debe ser un valor entre 30 y 99%. De lo contrario, se le asignará 30%")
        else:
            probCruce= int(probCruce.strip()) # Convertimos el string en un número.
            break;
    
    if probCruce>=30 and probCruce<=99:
        return(probCruce/100)
    else:
        return(0.3)

###############################################################################################################

def seleccionarProbabilidadMutacion():
    #Pedimos al usuario que introduzca el número de vertices
    probMutacion= input("Introduzca la probabilidad de que un individuo mute. Debe ser un valor entre 30 y 99. De lo contrario, se le asignará 30%.")
    
    #En el siguiente bucle comprobaremos si efectivamente ha metido un número, en caso contrario le seguiremos pidiendo que lo introduzca
    while 1:
        if probMutacion==None or not probMutacion.strip().isdigit():
            print("\n Ha introducido: "+probMutacion+", que no es un número")
            probMutacion=input("Por favor  introduzca la probabilidad de que un individuo mute. Debe ser un valor entre 30 y 99%. De lo contrario, se le asignará 30%:")
        else:
            probMutacion= int(probMutacion.strip()) # Convertimos el string en un número.
            break;
    
    if probMutacion>=30 and probMutacion<=99:
        return(probMutacion/100)
    else:
        return(0.3)
        

###############################################################################################################

def seleccionarProbabilidadMutacionGen():
    #Pedimos al usuario que introduzca el número de vertices
    probMutacionGen= input("Introduzca la probabilidad de que mute cada gen del cromosoma. Debe ser un valor entre 5 y 99. De lo contrario, se le asignará 10%.")
    
    #En el siguiente bucle comprobaremos si efectivamente ha metido un número, en caso contrario le seguiremos pidiendo que lo introduzca
    while 1:
        if probMutacionGen==None or not probMutacionGen.strip().isdigit():
            print("\n Ha introducido: "+probMutacionGen+", que no es un número")
            probMutacionGen=input("Por favor  introduzca la probabilidad de que mute cada gen del cromosoma. Debe ser un valor entre 5 y 99%. De lo contrario, se le asignará 10%:")
        else:
            probMutacionGen= int(probMutacionGen.strip()) # Convertimos el string en un número.
            break;
    
    if probMutacionGen>=5 and probMutacionGen<=99:
        return(probMutacionGen/100)
    else:
        return(0.1)
        
###############################################################################################################

def mutaSA(individuo):
    toolbox = base.Toolbox()
    toolbox.register('mutate', tools.mutUniformInt,low=0, up=NUMERO_COLORES-1, indpb=PROB_GENMUT)
    
    estado=copy.copy(individuo)
    
    #Si se cumple la probabilidad de mutación, mutamos.
    if random.uniform(0,1.0)< PROB_MUTACION:
        nextEstado= toolbox.mutate(estado)[0]
    else:
        nextEstado=estado
    
    return nextEstado

def aceptaCambioBoltzman(incr,temperatura):
    aleatorio= random.uniform(0,1.0)
    
    if incr<0: #Si el individuo es mejor que el que tenia lo cojo siempre
        res=1.0
    elif temperatura==0: #Si nos hemos quedao sin temperatura ya no cambiamos mas
        res=0.0
    else:
        res=exp(-incr/temperatura) #En caso de que sea peor dependerá de la temperatura, al principio será más facil que coja individuos peores
    
    return res > aleatorio
        
    

def simulatedAnnelingGeneraPoblacion(mejorSolucionEncontrada, temperaturaInicial):
    
    #Generamos un estado aleatorio
    toolInd = base.Toolbox()
    toolInd.register("attr_int", random.randint, 0, NUMERO_COLORES-1) #Este atributo es cada casilla del cromosoma, queremos que sea un INT entre [0, Colores-1]
    toolInd.register("individuo", tools.initRepeat, creator.Individuo,
                 toolInd.attr_int, n=LONGITUD_CROMOSOMA)
    
    estado= toolInd.individuo()
    
    #Asignamos valores a la temperatura y a la mejorSolucion
    if not mejorSolucionEncontrada:
        mejorSolucionEncontrada=estado
    if not temperaturaInicial:
        temperaturaInicial=1000
    
    #Como las listas son tipos mutables generamos una copia para estar seguro de que no vamos a cambiar la anterior
    estadoAMutar=copy.copy(estado)
    nextEstado= mutaSA(estadoAMutar) #Mutamos el estado
    incr= float(evaluacion1(nextEstado)[0]) - float(evaluacion1(estado)[0]) #Calculamos el incremento (como estamos minimizando, si el incr es negativo significa que es mejor. OJO no es la función fitness es una definida por nosotros)
       
    if aceptaCambioBoltzman(incr, temperaturaInicial): #Comprobamos si se realiza el cambio
        estado=nextEstado
    if evaluacion1(estado) < evaluacion1(mejorSolucionEncontrada): #Obtenemos la mejor solución
        mejorSolucionEncontrada= copy.copy(estado)
    
    return mejorSolucionEncontrada, temperaturaInicial, estado


def ejecutaSimulatedAnneling(poblacion, mejorSolucionEncontrada, temperaturaInicial):
       
    poblacion_enfriada=list()
    temperatura= temperaturaInicial*0.8
    
    for estado in poblacion:
        
        #Como las listas son tipos mutables generamos una copia para estar seguro de que no vamos a cambiar la anterior
        estadoAMutar=copy.copy(estado)
        nextEstado= mutaSA(estadoAMutar) #Mutamos el estado
        incr= float(evaluacion1(nextEstado)[0]) - float(evaluacion1(estado)[0]) #Calculamos el incremento (como estamos minimizando, si el incr es negativo significa que es mejor. OJO no es la función fitness es una definida por nosotros)
           
        if aceptaCambioBoltzman(incr, temperatura): #Comprobamos si se realiza el cambio
            estado=nextEstado
        if evaluacion1(estado) < evaluacion1(mejorSolucionEncontrada): #Obtenemos la mejor solución
            mejorSolucionEncontrada= copy.copy(estado)
            
        poblacion_enfriada.append(estado)
    
    return mejorSolucionEncontrada, temperatura, poblacion_enfriada
            
        
        
    
    
 
def generaGenetico():
    
    
    creator.create("FitnessMin", base.Fitness, weights=(-1,)) #Es -1 porque queremos minimizar.
    creator.create("Individuo", list, fitness=creator.FitnessMin)  #Hacemos que la fitness sea el FitnessMin

    toolbox1 = base.Toolbox()
    toolbox1.register("attr_int", random.randint, 0, NUMERO_COLORES-1) #Este atributo es cada casilla del cromosoma, queremos que sea un INT entre [0, Colores-1]
    toolbox1.register("individuo", tools.initRepeat, creator.Individuo,
                 toolbox1.attr_int, n=LONGITUD_CROMOSOMA)
    
    
    mejorSolucionEncontrada=None 
    temperatura= LONGITUD_CROMOSOMA*250 + NUMERO_COLORES #Le asignamos un poco más del fitness máximo
   
    #El usuario ha pedidio iteraciones de SA
    if ITERACIONES_SA>0:
        poblacion_sa=list()
        for i in range(0,POBLACION_INICIAL):
            mejorSolucionEncontrada, temperatura, estado= simulatedAnnelingGeneraPoblacion(mejorSolucionEncontrada,temperatura)
            poblacion_sa.append(estado)
        
        for i in range(0, ITERACIONES_SA-1):
            mejorSolucionEncontrada, temperatura, poblacion_sa= ejecutaSimulatedAnneling(poblacion_sa,mejorSolucionEncontrada,temperatura)
           
    
    #EL usuario ha pedido iteraciones de AG
    if  ITERACIONES_AG>0:
        toolbox1.register('población', tools.initRepeat,
                                    container=list, func=toolbox1.individuo, n=POBLACION_INICIAL) 
        
        
        toolbox1.register('evaluate', evaluacion1)
    
        toolbox1.register('mate', tools.cxOnePoint)
        toolbox1.register('mutate',  tools.mutUniformInt,low=0, up=NUMERO_COLORES-1, indpb=PROB_GENMUT) #La mutación hace que cambia un el valor del individuo entre 0 y nº colores -1.
        toolbox1.register('select', tools.selTournament, tournsize=3)
    
    
    
        salon_fama1 = tools.HallOfFame(1)
        random.seed(12345)
       
        if ITERACIONES_SA>0:
            poblacion_inicial=poblacion_sa
        else:
            poblacion_inicial=toolbox1.población()
       
        población, registro = algorithms.eaSimple(poblacion_inicial,
                                              toolbox1,
                                              cxpb=PROB_CRUCE, # Probabilidad de que dos individuos contiguos se crucen
                                              mutpb=PROB_MUTACION, # Probabilidad de que un individuo mute
                                              ngen=ITERACIONES_AG, # Número de generaciones
                                        
                                              halloffame=salon_fama1)
        
        
        
       
    #Elegimos el ganador
    
    if ITERACIONES_AG>0:
        ganador= salon_fama1[0]
        
        if ITERACIONES_SA>0 and evaluacion1(ganador)[0] > evaluacion1(mejorSolucionEncontrada)[0]:
            ganador=mejorSolucionEncontrada
            
    else:
        ganador=mejorSolucionEncontrada
        
    print("LONGITUD DEL CROMOSOMA = "+str(LONGITUD_CROMOSOMA))
    print("NÚMERO DE COLORES = "+str(NUMERO_COLORES))
    print("POBLACIÓN INCIAL = "+str(POBLACION_INICIAL))
    print("PROBABILIDAD DE CRUCE = "+str(PROB_CRUCE))
    print("PROBABILIDAD DE MUTACION = "+str(PROB_MUTACION))
    print("La solución se representará como una lista donde la posición indica el vértice y el valor en la lista indicará un tipo de color")
    print('La mejor solución encontrada ha sido:')
    print(ganador)
    print('Individuo con fitness: '+str(evaluacion1(ganador)[0]))
   

    return ganador

###############################################################################################################
       
### EJECUCIÓN DEL CÓDIGO ###

#Opciones del problema
try:
    falloEjecucion=False
    grafo = foo.introduceGrafo()
    diccionario = foo.generaDiccionarioVecinos(grafo) 
    NUMERO_COLORES = seleccionaColores()
except:
    falloEjecucion= True
    print("No se pudo continuar la ejecucción, asegurese de introducir correctamente el grafo siguiendo las instrucciones que aparecen en patalla")
    
        

#Opciones del algoritmo
if not falloEjecucion:
    try:  
        porDefecto=input("Si desea asignar valores por defecto en algoritmo genéticos introduzca 1, para asignación manual pulse otra cosa:")
        if porDefecto=="1":
            POBLACION_INICIAL = 50
            PROB_CRUCE = 0.8
            PROB_MUTACION = 0.4
            PROB_GENMUT = 0.3
            ITERACIONES_SA= 30
            ITERACIONES_AG= 100
        else:
            POBLACION_INICIAL = seleccionarPoblacion()
            PROB_CRUCE = seleccionarProbabilidadCruce()
            PROB_MUTACION = seleccionarProbabilidadMutacion()
            PROB_GENMUT = seleccionarProbabilidadMutacionGen()
            ITERACIONES_SA= seleccionarIteracionesSA()
            ITERACIONES_AG= seleccionarIteracionesAG()
        
        
        LONGITUD_CROMOSOMA = len(diccionario.keys())
    
        solucion=generaGenetico()
        
    except:
        falloEjecucion=True
        print("\nParece que hubo un error en la ejecución de los algoritmos genéticos, por favor introduzca los datos correctos")

if not falloEjecucion:
    foo.coloreaGrafo(grafo,solucion)
