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
#TT_INV.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 19 de Junio del 2014

#Funcion:

#	TT_INV( palabra_transformada_por_TT )

#Sinopsis

#Las siglas TT significan en español "Transformacion del Texto",
#o en ingles "Text Transformation". Y la aberiatura INV significa
#"inversa". 

#Esto quiere decir que esta es la funcion de "Transformacion de Texto Inversa"

#Esta funcion recibe como argumento una palabra previamente transformada
#por la funcion TT() y devuelve la palbra original en mimusculas
#(con acentos y caracteres especiales) sin transformar.

#Nota: Si el archivo de salida ya existia, este programa lo sobre-escribe
#Nota: Exactamente la primer linea de este programa sirve para manejar la letra Ñ y acentos
#############################################################################################


#Importar modulos necesarios

#Modulo para trabajar con el sistema operatibo
import sys

#############################################################################################
#INICIO DE LA FUNCION TT_INV()
#############################################################################################

def TT_INV(palabra_in):

	#Antes de este proceso no se marca la tonica sino despues


	#Añadir puntos al principio y al final de la palabra
	#para hacer ciertas sustituciones utiles

	palabra_in = "#" + palabra_in + "#"
	
	#Hacer sustituciones sencillas

	#La "W" se sustituye por "ü"
	palabra_in = palabra_in.replace("W","ü")

	#La "N" se sustituye por "ñ"
	palabra_in = palabra_in.replace("N","ñ")


	#SUSTITUIR LETRAS DOBLES 

	#H -> ch
	#C -> cc
	#L -> ll
	#R -> rr
	#T -> tl
	#Z -> zz
	#2 -> ts
	#3 -> tz

	#8 -> sh
	#P-> ps 


	##############

	#H -> ch
	palabra_in = palabra_in.replace("H","ch")

	#CC -> cc	
	#palabra_in = palabra_in.replace("CC","cc")

	#L -> ll
	palabra_in = palabra_in.replace("L","ll")

	#R -> rr
	palabra_in = palabra_in.replace("R","rr")

	#T -> tl
	palabra_in = palabra_in.replace("T","tl")

	#Z -> zz
	palabra_in = palabra_in.replace("Z","zz")

	#2 -> ts
	palabra_in = palabra_in.replace("2","ts")

	#3 -> tz
	palabra_in = palabra_in.replace("3","tz")

	

	#8 -> sh
	palabra_in = palabra_in.replace("8","sh")

	# .P -> ps 
	palabra_in = palabra_in.replace("#P","ps")


	#SUSTITUIR LETRAS TRIPLES

	#Ge -> gue
	#Gi -> gui
	#GE -> guE
	#GI -> guI


	#Qe ->  que
	#Qi ->  qui
	#QE ->  quE
	#QI ->  quI

	##############


	#Ge -> gue
	palabra_in = palabra_in.replace("Ge","gue")
	#Gi -> gui
	palabra_in = palabra_in.replace("Gi","gui")

	#GE -> guE
	palabra_in = palabra_in.replace("GE","guE")
	#GI -> guI
	palabra_in = palabra_in.replace("GI","guI")


	#Qe ->  que
	palabra_in = palabra_in.replace("Qe","que")
	#Qi ->  qui
	palabra_in = palabra_in.replace("Qi","qui")

	#QE ->  quE
	palabra_in = palabra_in.replace("QE","quE")
	#QI ->  quI
	palabra_in = palabra_in.replace("QI","quI")

	#SUSTITUIR CASOS ESPECIALES

	#Xe ->  ge
	#Xi ->  gi

	#XE ->  gE
	#XI ->  gI

	#5e ->  ce
	#5i ->  ci 

	#5E ->  cE
	#5I ->  cI

	#1. ->  y

	##############

	#Xe ->  ge
	palabra_in = palabra_in.replace("Xe","ge")
	#Xi ->  gi
	palabra_in = palabra_in.replace("Xi","gi")
	#XE ->  gE
	palabra_in = palabra_in.replace("XE","gE")
	#XI ->  gI
	palabra_in = palabra_in.replace("XI","gI")


	#5e ->  ce
	palabra_in = palabra_in.replace("5e","ce")
	#5i ->  ci 
	palabra_in = palabra_in.replace("5i","ci")
	#5E ->  cE
	palabra_in = palabra_in.replace("5E","cE")
	#5I ->  cI
	palabra_in = palabra_in.replace("5I","cI")


	#1. ->  y
	palabra_in = palabra_in.replace("1#","y")


	#ACENTOS

	#Sustituye las vocales en mayusculas por vocales con acento
	palabra_in = palabra_in.replace("A","á")
	palabra_in = palabra_in.replace("E","é")
	palabra_in = palabra_in.replace("I","í")
	palabra_in = palabra_in.replace("O","ó")
	palabra_in = palabra_in.replace("U","ú")


	##############
	#QUITAR LOS PUNTOS POR SI LOS LLEGA A HABER
	palabra_in = palabra_in.replace("#","")

	#DEVOLVER RESULTADO
	return palabra_in

#ENDDEF

#############################################################################################
#FIN DE LA FUNCION
#############################################################################################


