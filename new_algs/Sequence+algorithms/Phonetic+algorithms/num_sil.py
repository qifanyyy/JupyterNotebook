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

#Este funcion toma como entrada una palabra en minusculas con su
#vocal tonica indicada con una mayuscula y devuelve un entero que 
#representa el numero de silabas que contiene la palabra.

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
#FUNCION PRINCIPAL num_sil()
#############################################################################################

def num_sil(palabra_in):

	#Divide la palabra de entrada en silabas
	en_silabas = div_sil(palabra_in)

	#Divide la cadena resultante por medio de split()
	lista_silabas = en_silabas.split(".")

	#Devuelve el numero de silabas que tiene la palabra de entrada
	return len(lista_silabas)

#ENDDEF

#############################################################################################
#FIN DE LA FUNCION
#############################################################################################
