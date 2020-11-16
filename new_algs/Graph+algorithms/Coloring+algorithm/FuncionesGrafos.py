# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

from graph_tool import Graph
from graph_tool.draw import graph_draw
import random

def aplanaSolucion(solucion):
    colores= list() #Será la solución pero con los colores entre 0 y el número máximo de colores
    relacion= list() #Variable que usaremos para mantener la concordancia
    
    for x in solucion:
        if  len(colores)== 0: #Primera iteacion
            i=0 #Color nuevo
            colores.append(i) #Añadimos el color nuevo a la lista de colores
            relacion.append(x) #Asociamos el index con el color que tenia en el cromosoma
        else:
            if x in relacion: #Si ya hemos asignado un color a ese número del cromosoma
                pos= relacion.index(x) #Tomamos la posición que tenga en la relacion
                colores.append(pos)  #Añadimos esa posición (color) a la lista de colores
            else:
                i+=1 #Color nuevo
                colores.append(i) #Añadimos el color nuevo a la lista de colores
                relacion.append(x) #Asociamos el index con el color que tenia en el cromosoma
                
    return (len(relacion), colores) #Devolvemos el número de colores diferentes y los colores       

#Fuente de los siguientes 3 métodos: https://gist.github.com/adewes/5884820
          
def getOneColor():
    #Devuelve un color rgb (a,b,c) donde a,b,c estará comprendido entre 1 y 2
    #Hacemos un array [x,x,x] donde x sea un aleatorio 3 veces
    
    color= [x for x in [random.uniform(0,1.0) for i in[1,2,3,4]]]  
    color[3]=1
    return color


def getDistancia(c1,c2): #Es cambiable por una función que compare contrastes 
    #Devuelve¡la distancia de manhatam de los colores
    #Sumamos el valor absoluto de la resta de cada componente de los colores
    #Zip construía una tupla
    return sum([abs(x[0]-x[1]) for x in zip(c1,c2)])   

def getNewColor(coloresExistentes):
    maxDistancia= None #Variable donde guardaremos la distancia
    res= None
    
    for i in range(1,50): # Cogeremos el mejor color de 50 aleatorios, cambiar ese valor si se quiere un mejor contraste
        color= getOneColor() #Generamos un color
        if not coloresExistentes: #Si no hay colores existente
            return color #Se devuelve el color
        distancia= min([getDistancia(color,c) for c in coloresExistentes]) #La distancia será la minima entre todos los colores existentes
        
        if not maxDistancia or distancia > maxDistancia:
            #En caso de que sea una distancia mayor a la que habia anteriormente se toma ese color
            maxDistancia = distancia
            res=color
   
    if maxDistancia==0: #Si todos los colores generados han sido uno de los que ya habia, entonces se llama recursivamente a esta función para que se vuelva a recalcular uno diferente
        res=getNewColor(coloresExistentes)
    
    return res
            
            
    
    

def generaColores(solucion):
    numColores, indexColores= aplanaSolucion(solucion) #Obtenemos el numero de colores que necesitamos
    colores= list() #Lista donde guardaremos los colores
    res = list() #Lista que usaremos para relacionar cada index con un color
    
    for i in range(0,numColores): #Generamos colores nuevos
        color=(getNewColor(res))
        res.append(color)

    for i in range(0,len(indexColores)): #Añadimos a colores segun el index
        colores.append(res[indexColores[i]])
    
    return colores
    
    
    
def coloreaGrafo(graph,solucion):
    plot_color= graph.new_vertex_property('vector<double>') #Añadimos una nueva propiedad a los vertices, un array de double para el formato rgb
    graph.vertex_properties['plot_color']=plot_color #Indicamos que la propiedad plot color añadida es el vecto de double
    
    colores = generaColores(solucion) #Generamos el vector con los colores a partir de la solución
    numVertices=len(colores)
    print("Lista de colores en formato hex, puede comprobar que son validos en www.color-hex.com")
    for i in range(0,numVertices):
        plot_color[i]= colores[i] #A cada vértice le asignamos el color que le corresponda
        #Pasamos los colores al formato hex
        colorR= str(hex(int(colores[i][0]*255))).split("x")[1]
        if len(colorR) == 1:
            colorR="0"+colorR
            
        colorG= str(hex(int(colores[i][1]*255))).split("x")[1]
        if len(colorG) == 1:
            colorG="0"+colorG
            
        colorB= str(hex(int(colores[i][2]*255))).split("x")[1]
        if len(colorB) == 1:
            colorB="0"+colorB
            
        colorTotal= colorR+colorG+colorB
        
        print("Vértice "+ str(i) +" con color: #" + colorTotal )
    #Por último dibujamos el grafo
    base=200 #Calculos para hacer el tamaño de imagen relativo al número de vértices
    if numVertices > 3:
        base=base+(numVertices-3)*20
    graph_draw(graph, vertex_text=graph.vertex_index, vertex_font_size=18, vertex_fill_color= graph.vertex_properties['plot_color'],output_size=(base, base), output="colorGraph.png")




def introduceGrafo():
    #Pedimos al usuario que introduzca el número de vertices
    numVertex= input("Buenas, introduzca el número de vértices que tendrá su grafo (al menos 2):")
    
    #En el siguiente bucle comprobaremos si efectivamente ha metido un número, en caso contrario le seguiremos pidiendo que lo introduzca
    while 1:
        if numVertex==None or not numVertex.strip().isdigit():
            print("\n Ha introducido: "+numVertex+", que no es un número")
            numVertex=input("Por favor introduzca un número de vértices (menor o igual a 1 para la ejecución):")
        else:
            intVertex= int(numVertex.strip()) # Convertimos el string en un número.
            break;
            
    if intVertex>1:
        g= Graph(directed=False) #Creamos el grafo simple
        vlist=g.add_vertex(intVertex) #Le añadimos tantos vértices como haya dicho el usuario
        print("\n===============================================")
        print("Sus vértices serán numerados del 0 al "+str(intVertex-1) )
        print("===============================================")
        print("A continuación, se le preguntará con que otros vértices desea unir cada nodo. Recuerde que solo podrá unir i con j si i<j pues es lo mismo unir i con j que j con i. Por ejemplo, si quiere una arista entre el vértice 2 y 5 deberá decirlo en el vértice 2.")
        print("\nEn caso de que ponga un número menor o igual al actual, o si introduce un número mayor que el número de vértices no se tendrá en cuenta para pintar el grafo")
        print("===============================================")
        error=False; #Variable para, posteriormente, controlar que el usuario mete datos correctos
        
        for v0 in vlist: #Iteramos sobre la lista de vértices 
            if error: #Si hay un error paramos la ejecución
                break;
            elif int(v0) == (intVertex-1): #Cuando lleguemos al útlimo vértice paramos el bucle, pues ya se habrán introducido sus vértices incidentes en los anteriores
                break;
            
           
            cadenaIncidentes= input("Introduzca los vértices incidentes al vértices "+ str(v0)+ " separados por \",\" :")
            cadenaIncidentes= cadenaIncidentes.replace(" ","") #Quitamos los espacios a la cadena que ha introducido el usuario
            setIncidentes= set(cadenaIncidentes.split(",")) #Lo convertimos a conjunto para evitar repetidos
           
            for v1 in setIncidentes: #Iteramos sobre los candidatos a incidentes
               
                if v1!="": #Por si el usuario quiere algún vértice suelto y no introduce nada
                    if v1.isdigit():#Si es un digito
                        addVertext= int(v1) #Convertimos a entero
                        if addVertext < intVertex and addVertext > int(v0):
                           #Si el candidato a incidente es menor que el número de vertices (porque estan enumerados de 0 a N-1) y mayor que el vértice sobre el que incide
                            g.add_edge(v0,addVertext) #Entonces añadimos la arista
                    else: #Si no es un digito error
                        error=True
                        break;
                
    
    if error:
        print("Oops parece que hubo un error, quizás introdujo letras/símbolos o introdujo más vértices de los que había disponibles")
        raise Exception()
         
    else:
        base=200 #Calculos para hacer el tamaño de imagen relativo al número de vértices
        if intVertex > 3:
            base=base+(intVertex-3)*20
        #Por último, pintamos el grafo
        graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(base, base), output="uncolorGraph.png")
         
    
    print("Fin ejecución")
    

               
    return g
                
def generaDiccionarioVecinos(graph):
     d={} #Creamos un diccionario
     for v in graph.vertices(): #Reccorremos todos los vertices del grafo
         d.setdefault(int(v),graph.get_in_neighbors(v).tolist()) #Al diccionario le añado las claves de vertice y como valor sus vecinos
     return d 
       
            



