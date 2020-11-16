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
#num_sil.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 13 de Diciembre del 2015

#Funcion:

#	num_sil( palabra_de_entrada )

#Sinopsis

#Este funcion toma como entrada una palabra en español, en minusculas y 
#con su vocal tonica indicada con una mayuscula; y al final devuelve la 
#misma palabra pero con su acento grafico si es que se requiere, por ejemplo:

#	acento_grafico(canciOn) ==> canción
#	acento_grafico(pErro) ==> perro

#Si la palabra de entrada ya cuenta con una acento grafico, pero en una posicion
#incorrecta, esta funcion ignorara ese acento y decidira ponerlo o no, en base 
#a las reglas de acentuacion del español.

#En las palabras con una sola silaba la decisión de poner o no el acento grafico
#dependera de si la palabra tiene o no su vocal tonica indicada en mayuscula.

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

#Modulo creado por mi donde viene la funcion pos_tonica()
from fonetica3.pos_tonica import pos_tonica
#############################################################################################
#VARIABLES GLOBALES
#############################################################################################

N_S_o_VOCAL = ["n","s","a","e","i","o","u","A","E","I","O","U"]

PATRON_DIPTONGOS_ROTOS = r'.*?(aI|aU|eI|eU|oI|oU|Ia|Ua|Ie|Ue|Io|Uo)'
#############################################################################################
#FUNCION PRINCIPAL acento_grafico()
#############################################################################################

def acento_grafico(palabra_in):

	#Banderas utiles
	termina_en_mente = False

	#####################################################################
	#Preguntar si la palabra termina en mente

	#Pone un # para marcar el final de palabra
	palabra_in = palabra_in+"#"
	t_mente = re.match(r'.+(mente#|mEnte#)',palabra_in)

	if t_mente != None:
		
		#Si la palabra termina en mente se quita
		#momentaneamente esta terminacion
		palabra_in = palabra_in.replace("mente#","")
		palabra_in = palabra_in.replace("mEnte#","")
				
		termina_en_mente = True
	#ENDIF

	#Ya sea que la palabra termine en mente o no, no debe de ir ningun #
	#en la palabra que se va a procesar.
	palabra_in = palabra_in.replace("#","")
	#####################################################################

	#Pregunta cuantas silabas tiene la palabra entrante
	#para decidir si es un monosilabo o no
	if num_sil(palabra_in) == 1:

		#Si es un monosilabo la palabra el acento grafico
		#dependera de si la palabra o no tiene la vocal
		#tonica indicada con una mayuscula.

		palabra_in = palabra_in.replace("A","á")
		palabra_in = palabra_in.replace("E","é")
		palabra_in = palabra_in.replace("I","í")
		palabra_in = palabra_in.replace("O","ó")
		palabra_in = palabra_in.replace("U","ú")

		palabra_in = palabra_in.replace("Á","á")
		palabra_in = palabra_in.replace("É","é")
		palabra_in = palabra_in.replace("Í","í")
		palabra_in = palabra_in.replace("Ó","ó")
		palabra_in = palabra_in.replace("Ú","ú")


		palabra_out = palabra_in

	else:
		#Si no es un monosilabo:


		#Homogeiniza la entrada
		#####################################################################
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
		#####################################################################

		#Variable local util
		lleva_acento = False
		
		#Recopila la informacion necesaria para saber si la palabra
		#lleva acento grafico o no.

		#Primero se fija en la terminacion de la palabra
		terminacion = palabra_in[-1]

		#Luego se fija en que silaba esta la vocal tonica
		#-1 significaria que la ultima silaba
		#-2 significaria que es la penultima silaba
		#Etc. Se usa la funcion pos_tonica() para calcular
		#la posicion de la vocal tonica de la palabra actual
		posicion_tonica = pos_tonica(palabra_in)

		#En base a la informacion recabada decide si la palabra
		#lleva acento grafico o no:

		#Palabras agudas: llevan acento grafico si la tonica 
		#esta en la ultima silaba (silaba -1) y si terminan
		#en n, s, o vocal
		if posicion_tonica == -1 and terminacion in N_S_o_VOCAL:
			lleva_acento = True

		#Palabras graves: Llevan acento grafico si la tonica
		#esta en la penultima silaba (silaba -2) y si la palabra no
		#termina en n, s o vocal
		elif posicion_tonica == -2 and terminacion not in N_S_o_VOCAL:
			lleva_acento = True

		#Las palabras que lleven acento mas allá de la penultima silaba
		#llevan acento grafico en todos los casos
		elif posicion_tonica <= -3:
			lleva_acento = True

		#Busca diptongos rotos
		elif re.match(PATRON_DIPTONGOS_ROTOS, palabra_in) != None:
			lleva_acento = True

		else:
			lleva_acento = False
		#ENDIF

		#Aqui se ejecuta la desicion sobre la palabra de salida de si la 
		#palabra de entrada lleva acento o no
		palabra_out = palabra_in

		if lleva_acento == True:

			palabra_out = palabra_out.replace("A","á")
			palabra_out = palabra_out.replace("E","é")
			palabra_out = palabra_out.replace("I","í")
			palabra_out = palabra_out.replace("O","ó")
			palabra_out = palabra_out.replace("U","ú")

			palabra_out = palabra_out.replace("Á","á")
			palabra_out = palabra_out.replace("É","é")
			palabra_out = palabra_out.replace("Í","í")
			palabra_out = palabra_out.replace("Ó","ó")
			palabra_out = palabra_out.replace("Ú","ú")
		else:

			palabra_out = palabra_out.replace("á","a")
			palabra_out = palabra_out.replace("é","e")
			palabra_out = palabra_out.replace("í","i")
			palabra_out = palabra_out.replace("ó","o")
			palabra_out = palabra_out.replace("ú","u")

			palabra_out = palabra_out.replace("A","a")
			palabra_out = palabra_out.replace("E","e")
			palabra_out = palabra_out.replace("I","i")
			palabra_out = palabra_out.replace("O","o")
			palabra_out = palabra_out.replace("U","u")

			palabra_out = palabra_out.replace("Á","a")
			palabra_out = palabra_out.replace("É","e")
			palabra_out = palabra_out.replace("Í","i")
			palabra_out = palabra_out.replace("Ó","o")
			palabra_out = palabra_out.replace("Ú","u")
		
		#ENDIF

	#ENDIF

	#####################################################################
	if termina_en_mente == True:
		palabra_out = palabra_out + "mente"

	#ENDIF
	#####################################################################

	#Regresa el resultado de la funcion
	return palabra_out

#ENDDEF

#############################################################################################
#FIN DE LA FUNCION
#############################################################################################
