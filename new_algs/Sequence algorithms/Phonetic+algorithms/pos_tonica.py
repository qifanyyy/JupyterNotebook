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
#pos_tonica_Ejemplo.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 13 de Diciembre del 2015

#Funcion:

#	$ python pos_tonica_Ejemplo.py

#Sinopsis

#Este funcion toma como entrada una palabra en español con
#la vocal tonica indicada en mayuscula y devuelve un entero negativo 
#que indica la posicion de la vocal tonica de derecha a izquierda, por ejemplo:
#-1 significa que la tonica esta en la ultima silaba, -2 significa que la tonica
#esta en la penultima silaba y asi sucesivamente.

#La vocal tonica podria tambien estar indicada por medio del acento grafico 
#de la palabra.

#Si no existe ninguna vocal tonica indicada, esta funcion devuelve "None".

#Hay que tener cuidado con los adverbios terminados en "mente" por que
#esta funcion solo da la ubicacion de la tonica que no esta en esa terminacion,
#por ejemplo: "clA.ra.mEn.te" tiene dos tonicas, pero esta funcion dara por
#resultado -4 que es la que esta en pla primera silaba e ignorará la tonica
#que esta en la terminacion "mente"

#Nota: Si el archivo de salida ya existia, este programa lo sobre-escribe
#Nota: Exactamente la primer linea de este programa sirve para manejar la letra Ñ y acentos
#############################################################################################
#Importar modulos necesarios

#Modulo para trabajar con el sistema operativo
import sys

#Modulo para expresiones regulares
import re

#Modulo creado por mi donde viene la funcion div_sil()
from fonetica3.div_sil import div_sil

#Modulo creado por mi donde viene la funcion num_sil()
from fonetica3.num_sil import num_sil

#############################################################################################

#############################################################################################
#FUNCION PRINCIPAL pos_tonica()
#############################################################################################

def pos_tonica(palabra_in):

	#Divide la palabra de entrada en silabas
	en_silabas = div_sil(palabra_in)

	#Todas las palabras que entregue div_sil() tendran
	#un acento grafico en el lugar donde tienen la tonica,
        #por lo tanto, hay que convertir ese cartacter acentuado
	#en una mayuscula.
	en_silabas = en_silabas.replace("á","A")
	en_silabas = en_silabas.replace("é","E")
	en_silabas = en_silabas.replace("í","I")
	en_silabas = en_silabas.replace("ó","O")
	en_silabas = en_silabas.replace("ú","U")

	#Divide la cadena "en_silabas" por medio de split()
	lista_silabas = en_silabas.split(".")

	posicion_tonica = None
	#Recorre la lista_silabas en busca de la vocal tonica
	for index in range(0,len(lista_silabas)):

		#Rescata la silaba actual
		silaba = lista_silabas[index]

		#Busca si en la silaba actual esta la vocal tonica
		if re.match(r'.*[AEIOU]',silaba) != None:
			posicion_tonica = -1 * (len(lista_silabas)-index)
			#Este break es para que ignore la tonica
			#de la terminacion "mente" en adverbios como 
			#"claramente"
			break
		#ENDIF
	#ENDFOR

	return posicion_tonica

#ENDDEF

#############################################################################################
#FIN DE LA FUNCION
#############################################################################################
