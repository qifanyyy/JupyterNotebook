#-*- coding: utf-8 -*-
#############################################################################################
#Algoritmo PFS provide functions to implement the PFS and the PFS-US algorithms

#Copyright 2017 Carlos Daniel Hernandez Mena 
#Contact: carlos.mena@ciempiess.org

#This file is part of Algoritmo PFS

#    Algoritmo PFS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Algoritmo PFS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Algoritmo PFS.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################################
#leer_reglas.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 23 de Mayo de 2017

#Este programa toma como entrada un archivo de reglas y las devuelve en forma de una
#lista de python.

#Directorios en python: http://librosweb.es/libro/python/capitulo_10/modulos_de_sistema.html
#Nota: Si el archivo de salida ya existia, este programa lo sobre-escribe
#Nota: Exactamente la primer linea de este programa sirve para manejar la letra Ñ y acentos
#############################################################################################
#Importar modulos necesarios

#Modulo para funciones del sistema operativo
import sys

#Modulo para manejar expresiones regulares
import re

#Modulo para manejar funciones del sistema operativo
import os

#Modulo para hacer operaciones con archivos y carpetas
import shutil

#Modulo para capturar lo que entrea un os.system()
import commands

#############################################################################################

#Abrir el archivo de entrada cuyo nombre es tomado de la linea de comandos
	
#Nota:
#sys.argv[0] me entrga el nombre de este script
#sys.argv[1] me entrega el primer argumento enviado desde la linea de comandos
#sys.argv[n] me entrega el enesimo argumento enviado desde la linea de comandos
#sys.argv    me entrega una lista con todos los argumentos desde el argv[0] hasta el argv[n]

#############################################################################################

#Lista con caracteres a ignorar en una linea
#(como el caracter para los comentarios)
ignorar=["#","\n"," ","	"]

#Lista que contiene las reglas del archivo de reglas
lista_reglas=[]

#Abre el archivo de entrada y lo lee linea por linea
def leer_reglas(archivo_reglas):
	archivo_in = open(archivo_reglas,'r')
	for linea in archivo_in.xreadlines():

		#Si la linea empieza con #, "\n" o espacio en blanco se ignora
		if linea[0] not in ignorar:

			#Convertir cada linea a tipo string
			linea=str(linea)

			#Quitar el salto de linea de la linea
			linea=linea.replace("\n","")
		
			lista_reglas.append(linea)
		#ENDIF
	#ENDFOR
	archivo_in.close()

	return lista_reglas
#ENDDEF



#############################################################################################

