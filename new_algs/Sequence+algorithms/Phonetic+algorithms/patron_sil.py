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
#patron_sil.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 14 de Diciembre del 2015

#Funcion:

#	patron_sil( palabra_de_entrada )

#Sinopsis

#Esta funcion recibe una palabra en español, en minusculas, ya sea bien 
#escrita o con su vocal tonica indicada en mayusculas y devuelve el patron 
#silabico de dicha palabra.

#Bien escrita significa que puede llevar acentos, ñ y ü como dicta la
#ortografia española.

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
#VARIABLES GLOBALES
#############################################################################################
VOCALES = ["a","e","i","o","u","A","E","I","O","U","W"]

#############################################################################################
#FUNCION PRINCIPAL patron_sil()
#############################################################################################

def patron_sil(palabra_in):

	#Divide la palabra de entrada en silabas
	en_silabas = div_sil(palabra_in)

	#Acondiciona la palabra divida para que todo quede ASCII
	en_silabas = en_silabas.replace("á","A")
	en_silabas = en_silabas.replace("é","E")
	en_silabas = en_silabas.replace("í","I")
	en_silabas = en_silabas.replace("ó","O")
	en_silabas = en_silabas.replace("ú","U")

	en_silabas = en_silabas.replace("Á","A")
	en_silabas = en_silabas.replace("É","E")
	en_silabas = en_silabas.replace("Í","I")
	en_silabas = en_silabas.replace("Ó","O")
	en_silabas = en_silabas.replace("Ú","U")

	en_silabas = en_silabas.replace("ñ","N")
	en_silabas = en_silabas.replace("ü","W")
	en_silabas = en_silabas.replace("Ñ","N")
	en_silabas = en_silabas.replace("Ü","W")

	patron_out = ""
	#Recorre caracter cambiando por una C si es consonante
	#y por una V si se trata de vocal.
	for car in en_silabas:

		if car in VOCALES and car != ".":
			patron_out = patron_out + "V"
		elif car == ".":
			patron_out = patron_out + "."			
		else:
			patron_out = patron_out + "C"
		#ENDIF
	#ENDFOR

	#Devuelve el patron silabico obtenido
	return patron_out
#ENDDEF

#############################################################################################
#FIN DE LA FUNCION
#############################################################################################
