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
#vocal_tonica.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 22 de Junio del 2014

#Funcion:

#	vocal_tonica( palabra_de_entrada )

#Sinopsis


#Este funcion toma como entrada una palabra bien escrita en minusculas
#y la devuelve con la vocal tonica en mayuscula.

#NOTA: Debido a que esta funcion marca la vocal tonica con una mayuscula
#no debe tener ninguna vocal en mayuscula a la entrada, debido
#a que esto produce resultados indeseados en la palabra de salida,
#por lo tanto las vocales en mayusculas se ponen en minusculas.

#Sin embargo, si es valido que la palabra entrante tenga acento grafico, 
#el cual se respeta y se asume que convierte a la vocal que lo porta en tonica.


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
#############################################################################################


#############################################################################################
#FUNCIONES GLOBALES GLOBALES
#############################################################################################

#Esta funcion recibe una palabra divida en silabas
#y cuenta cuantas silabas tiene
def cuenta_silabas(en_silabas):

	lista_silabas = en_silabas.split(".")

	return len(lista_silabas)


#ENDDEF

#############################################################################################
#FUNCION PRINCIPAL vocal_tonica()
#############################################################################################


def vocal_tonica(palabra_in):

	#Debido a que esta funcion marca la vocal tonica con una mayuscula
	#no debe tener ninguna vocal en mayuscula a la entrada, debido
	#a que esto produce resultados indeseados en la palabra de salida,
	#por lo tanto las vocales en mayusculas se ponen en minusculas.
	#Sin embargo, como se ve mas adelante en este codigo, si se vale 
	#que la palabra entrante tenga acento grafico, el cual se respeta
	#y se asume que convierte a la vocal que lo porta en tonica.
	palabra_in = palabra_in.replace("A","a")
	palabra_in = palabra_in.replace("E","e")
	palabra_in = palabra_in.replace("I","i")
	palabra_in = palabra_in.replace("O","o")
	palabra_in = palabra_in.replace("U","u")

	#Quitar momentaneamente las ñ y ü
	palabra_in = palabra_in.replace("ñ","N")
	palabra_in = palabra_in.replace("ü","W")

	#Hay problemas con la "q" como en quiero
	palabra_in = palabra_in.replace("qu","K")

	#Banderas utiles

	acabo = False
	termina_en_mente = False
	es_y = False

	#####################################################################
	#Preguntar si se trata de la conjuncion "y"

	if palabra_in == "y":
		es_y = True
		acabo = True
	#ENDIF

	#####################################################################
	#####################################################################
	#Preguntar si tiene acento ortografico
	tilde = re.match(r'.*[áéíóú]',palabra_in)

	#Si si tiene acento, se sutituye por la vocal correspondiente
	#en mayuscula
	if tilde != None:

		palabra_in = palabra_in.replace("á","A")
		palabra_in = palabra_in.replace("é","E")
		palabra_in = palabra_in.replace("í","I")
		palabra_in = palabra_in.replace("ó","O")
		palabra_in = palabra_in.replace("ú","U")

		acabo = True

	#ENDIF
	#####################################################################
	#####################################################################
	#Preguntar si la palabra termina en mente

	#Pone un "#" para marcar el final de palabra
	palabra_in = palabra_in+"#"
	t_mente = re.match(r'.+(mente#|mEnte#)',palabra_in)

	if t_mente != None:
		
		#Si la palabra termina en mente se quita
		#momentaneamente esta terminacion
		palabra_in = palabra_in.replace("mente#","")
		palabra_in = palabra_in.replace("mEnte#","")
				
		termina_en_mente = True
	#ENDIF

	#Ya sea que la palabra termine en mente o no, no debe de ir ningun "#"
	#en la palabra que se va a procesar.
	palabra_in = palabra_in.replace("#","")
	#####################################################################
	#####################################################################
	#FUNCION PRINCIPAL

	if acabo == False:

		#Primero hace los cambios en terminaciones conocidas
	
		#Añade un fin de palabra para hacer los cambios

		word = palabra_in + "#"

		#Hace los cambios en terminaciones conocidas

		#Termina en: ar, er, ir, or, ur
		word = word.replace("ar#","Ar")	
		word = word.replace("er#","Er")
		word = word.replace("ir#","Ir")
		word = word.replace("or#","Or")
		word = word.replace("ur#","Ur")

		#Termina en: al, el, il, ol, ul
		word = word.replace("al#","Al")	
		word = word.replace("el#","El")
		word = word.replace("il#","Il")
		word = word.replace("ol#","Ol")
		word = word.replace("ul#","Ul")

		#Terminaciones varias
		word = word.replace("ion#","iOn")
		word = word.replace("ad#","Ad")
		word = word.replace("ias#","Ias")
		word = word.replace("ia#","Ia")
		word = word.replace("oy#","Oy")

		#VER OTROS CASOS
		#Verificar si estas modificaciones fueron suficientes

		busca_delimitador = re.match(r'.*#',word)
		if busca_delimitador!=None:

			#Divide la palabra en silabas
			en_silabas = div_sil(word)

			#Cuenta el numero de silabas
			num_silabas = cuenta_silabas(en_silabas)

			#Si es monosilaba
			if num_silabas == 1:

				#Monosilabo con diptongo debil
				word = word.replace("ui","uI")
				word = word.replace("iu","iU")

				#En los demas casos acentuar la vocal fuerte
				ya_acentuada = re.match(r'.*[AEOIU]',word)

				if ya_acentuada == None:
					word = word.replace("a","A")
					word = word.replace("e","E")
					word = word.replace("o","O")
				#ENDIF

				#Si no se cumple nada tiene que acentuar la i o la u de la
				#ultima silaba, pero tiene que verificar que no este	
				#en un triptongo

				triptongo = re.match(r'.*[AEOIU]',word)

				if triptongo == None:
					word = word.replace("i","I")
					word = word.replace("u","U")				
				#ENDIF

			#Si no es monosilaba procesar la penultima silaba
			else:

				#Extraer la penultima silaba
				lista_silabas = en_silabas.split(".")

				#Extraer le penultima silaba
				penultima_sil = lista_silabas[-2]

				#Acentuar estos casos en la penultima silaba
				
				#Penultima silaba terminada en: ar, er, ir, or, ur
				penultima_sil = penultima_sil.replace("ar","Ar")
				penultima_sil = penultima_sil.replace("er","Er")
				penultima_sil = penultima_sil.replace("ir","Ir")
				penultima_sil = penultima_sil.replace("or","Or")
				penultima_sil = penultima_sil.replace("ur","Ur")

				#Penultima silaba terminada en: al, el, il, ol, ul
				penultima_sil = penultima_sil.replace("al","Al")
				penultima_sil = penultima_sil.replace("el","El")
				penultima_sil = penultima_sil.replace("il","Il")
				penultima_sil = penultima_sil.replace("ol","Ol")
				penultima_sil = penultima_sil.replace("ul","Ul")

				#Diptongo debil en la penultima silaba
				penultima_sil = penultima_sil.replace("ui","uI")
				penultima_sil = penultima_sil.replace("iu","iU")

				#Si no se cumple que ocurra ninguna de estas
				#terminaciones hay que acentuar la vocal fuerte,
				#pero antes hay que evaluar que no haya ya alguna
				#acentuada del proceso anterior
				ya_acentuada = re.match(r'.*[AEOIU]',penultima_sil)

				if ya_acentuada == None:
					#En los demas casos acentuar la vocal fuerte
					penultima_sil = penultima_sil.replace("a","A")
					penultima_sil = penultima_sil.replace("e","E")
					penultima_sil = penultima_sil.replace("o","O")
				#ENDIF


				#Si no se cumple nada tiene que acentuar la i o la u de la
				#penultima silaba, pero tiene que verificar que no este	
				#en un triptongo

				triptongo = re.match(r'.*[AEOIU]',penultima_sil)

				if triptongo == None:
					penultima_sil = penultima_sil.replace("i","I")
					penultima_sil = penultima_sil.replace("u","U")				
				#ENDIF

				#Meter la silaba acentuada a la lista de silabas
				lista_silabas[-2] = penultima_sil

				#Volver a integrar la palabra ya acentuada
				word = "".join(lista_silabas)
			#ENDIF

			#Quita triptongos del tipo VvV, es decir, una vocal debil entre 2 fuertes
			triptongo_VvV = re.match(r'.*?(A|E|O)(i|u)(A|E|O)',word)

			if triptongo_VvV != None:
				word = word.replace("iA","ia")
				word = word.replace("iE","ie")
				word = word.replace("iO","io")
				word = word.replace("uA","ua")
				word = word.replace("uE","ue")
				word = word.replace("uO","uo")
			#ENDDIF

			#Quita casos en los que varias vocales debiles estan juntas,
			#solo para evitar que esta funcion ponga mas de una tonica
			word = word.replace("III","iIi")
			word = word.replace("II","iI")
			word = word.replace("UUU","uUu")
			word = word.replace("UU","uU")
			word = word.replace("UI","Ui")
			word = word.replace("IU","Iu")
		#ENDDIF
	#ENDIF
	#####################################################################
	#####################################################################
	if es_y == True:
		con_tonica = "y"
	elif acabo == True:
		if termina_en_mente == True:
			con_tonica = palabra_in + "mEnte"
		else:
			con_tonica = palabra_in
		#ENDIF
	elif termina_en_mente == True:
		con_tonica = word + "mEnte"
	else:
		con_tonica = word
	#ENDIF

	#Devuelve la ñ y ü
	con_tonica = con_tonica.replace("N","ñ")
	con_tonica = con_tonica.replace("W","ü")

	#Devuelve la "qu"
	con_tonica = con_tonica.replace("K","qu")

	#Quitar el delimitador en caso de haberlo
	con_tonica = con_tonica.replace("#","")

	#####################################################################
	#####################################################################
	#Devolver la palabra con la vocal tonica indicada

	return con_tonica

#ENDDEF
#############################################################################################
#FIN DE LA FUNCION
#############################################################################################
