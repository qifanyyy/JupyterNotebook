#-*- coding: utf-8 -*-
#############################################################################################
#fonetica3 library provide functions to make phonetic and phonological transcriptions of 
#words in Spanish

#Copyright 2016 Carlos Daniel Hernandez Mena 
#Contact: carlos.mena@ciempiess.org

#This file is part of fonetica3 library

#    fonetica3 library is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    fonetica3 library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with fonetica3 library.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################################
#TT.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 19 de Junio del 2014

#Funcion:

#	TT( palabra_de_entrada )

#Sinopsis

#Las siglas TT significan en español "Transformacion del Texto",
#o en ingles "Text Transformation".

#Esta funcion recibe como argumento una palabra en español
#bien escrita en minusculas y devuelve la misma
#palabra pero transformada de tal modo que sea mas facil fonetizarla
#o dividirla en silabas.

#Esta transformacion consiste en simples sustituciones de grupos de
#caracteres en grupos mas simples como por ejemplo: 

#convertir que en Qe.

#Hay que decir tambien que todas estas transformaciones son reversibles
#y la funcion inversa a TT() se llama TT_INV().


#Nota: Si el archivo de salida ya existia, este programa lo sobre-escribe
#Nota: Exactamente la primer linea de este programa sirve para manejar la letra Ñ y acentos
#############################################################################################
#Importar modulos necesarios

#Modulo para trabajar con el sistema operatibo
import sys

#############################################################################################
#INICIO DE LA FUNCION TT()
#############################################################################################

def TT(palabra_in):

	#ANTES DE APLICAR ESTA FUNCION:

	#1. La palabra de entrada debe estar minusculas absolutas
	#2. Deben estar indicados los contextos de la "x"
	#3. NO se marca la tonica sino despues.


	#Añadir puntos al principio y al final de la palabra
	#para hacer ciertas sustituciones utiles

	palabra_in = "#" + palabra_in + "#"
	

	#Hacer sustituciones sencillas

	#Cualquier vocal con acento es vocal tonica
	palabra_in = palabra_in.replace("á","A")
	palabra_in = palabra_in.replace("é","E")
	palabra_in = palabra_in.replace("í","I")
	palabra_in = palabra_in.replace("ó","O")
	palabra_in = palabra_in.replace("ú","U")

	palabra_in = palabra_in.replace("Á","A")
	palabra_in = palabra_in.replace("É","E")
	palabra_in = palabra_in.replace("Í","I")
	palabra_in = palabra_in.replace("Ó","O")
	palabra_in = palabra_in.replace("Ú","U")

	#La "u" con dieresis se sustituye por "W"
	palabra_in = palabra_in.replace("ü","W")
	palabra_in = palabra_in.replace("Ü","W")

	#La "ñ" se sustituye por "N"
	palabra_in = palabra_in.replace("ñ","N")
	palabra_in = palabra_in.replace("Ñ","N")

	#La "x" se sustiuye por su contexto por default "KS"
	#palabra_in = palabra_in.replace("x","KS")

	#SUSTITUIR LETRAS DOBLES POR LETRAS SIMPLES

	#ch -> H
	#cc -> C
	#ll -> L
	#rr -> R
	#tl -> T
	#zz -> Z
	#ts -> 2
	#tz -> 3

	#sh -> 8
	#.ps -> P


	##############

	#ch -> H
	palabra_in = palabra_in.replace("ch","H")

	#cc -> CC	
	#palabra_in = palabra_in.replace("cc","CC")

	#ll -> L
	palabra_in = palabra_in.replace("ll","L")

	#rr -> R
	palabra_in = palabra_in.replace("rr","R")

	#tl -> T
	palabra_in = palabra_in.replace("tl","T")

	#zz -> Z
	palabra_in = palabra_in.replace("zz","Z")

	#ts -> 1
	palabra_in = palabra_in.replace("ts","2")

	#tz -> 2
	palabra_in = palabra_in.replace("tz","3")

	

	#sh -> S
	palabra_in = palabra_in.replace("sh","8")

	#.ps -> P
	palabra_in = palabra_in.replace("#ps","P")

#	#QUITAR LA H YA QUE SIN ELLA SE FORMAN DIPTONGOS
#	palabra_in = palabra_in.replace("h","")  

	#SUSTITUIR LETRAS TRIPLES

	#gue -> Ge
	#gui -> Gi
	#guE -> GE
	#guI -> GI


	#que -> Qe
	#qui -> Qi
	#quE -> QE
	#quI -> QI
	##############


	#gue -> ge
	palabra_in = palabra_in.replace("gue","Ge")
	#gui -> gi
	palabra_in = palabra_in.replace("gui","Gi")

	#guE -> gE
	palabra_in = palabra_in.replace("guE","GE")
	#guI -> gI
	palabra_in = palabra_in.replace("guI","GI")


	#que -> Qe
	palabra_in = palabra_in.replace("que","Qe")
	#qui -> Qi
	palabra_in = palabra_in.replace("qui","Qi")

	#quE -> QE
	palabra_in = palabra_in.replace("quE","QE")
	#quI -> QI
	palabra_in = palabra_in.replace("quI","QI")

	#SUSTITUIR CASOS ESPECIALES

	#ge -> Xe
	#gi -> Xi

	#gE -> XE
	#gi -> XI

	#ce -> 5e
	#ci -> 5i

	#cE -> 5E
	#cI -> 5I

	#y. -> 1

	##############

	#ge -> Xe
	palabra_in = palabra_in.replace("ge","Xe")
	#gi -> Xi
	palabra_in = palabra_in.replace("gi","Xi")
	#gE -> XE
	palabra_in = palabra_in.replace("gE","XE")
	#gI -> XI
	palabra_in = palabra_in.replace("gI","XI")


	#ce -> 5e
	palabra_in = palabra_in.replace("ce","5e")
	#ci -> 5i
	palabra_in = palabra_in.replace("ci","5i")
	#cE -> 5E
	palabra_in = palabra_in.replace("cE","5E")
	#cI -> 5I
	palabra_in = palabra_in.replace("cI","5I")


	#y. -> 1
	palabra_in = palabra_in.replace("y#","1")


	##############
	#QUITAR LOS PUNTOS POR SI LOS LLEGA A HABER
	palabra_in = palabra_in.replace("#","")

	#DEVOLVER RESULTADO
	return palabra_in

#ENDDEF
#############################################################################################
#FIN DE LA FUNCION
#############################################################################################

