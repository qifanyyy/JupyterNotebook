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
#codigo_pfs_us.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 21 de Agosto de 2017

#Esta funcion calcula el codigo PFS-US de una palabra de entrada.

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

#Modulo creado por mi donde viene la funcion T29()
from fonetica3.T29 import T29

#############################################################################################

def codigo_pfs_us(lista_reglas,p_tonica):

	#La variable "fono" contiene una transcripcion fonologica de la palabra
	#de entrada p_tonica (basado en la transcripcion fonologica MEXBET T29)
	fono = T29(p_tonica)

	#Busca dejar intacta la ultima silaba
	lista_fono = fono.split(".")

	#Si la palabra tiene mas de una silaba guarda esa ultima silaba
	#para dejarla intacta, si no, no hace nada.
	ultima_silaba=""
	if len(lista_fono)>1:
		#Guarda la ultima silaba
		ultima_silaba = lista_fono[-1]
		#Quita la ultima silaba de lista_fono
		lista_fono.pop(-1)
		#Vuelve a unir lista_fono
		fono = ".".join(lista_fono)
	#ENDIF
	
	for regla in lista_reglas:
		#Se toma una regla y se le convierte a tipo string
		#regla=str(r)	
		
		#Se divide la regla en base a los espacios en blanco
		lista_elementos_regla=regla.split(" ")

		#Exactamete el primer elemento de lista_elementos_regla es 
		#el simbolo con el cual se quiere sustituir a los demas
		#por ejemplo en la regla:
		# 1 b p
		#La "b" y la "p" se sustituyen por "1"

		#Entonces se debe iterar sobre "lista_elementos_regla" para 	
		#poder aplicar toda la regla a la variable fono
		for index in range(1,len(lista_elementos_regla)):
			fono = fono.replace(str(lista_elementos_regla[index]),str(lista_elementos_regla[0]))
		#ENDFOR
	#ENDFOR
	#Añade la ultima silaba
	if ultima_silaba!="":
		fono =  fono + "."+ultima_silaba
	#ENDIF

	#Es preciso cambiar el punto que divide a la transcripcion fonologica
	#por un guion y quitar los espacios en blanco

	#Separar la variable "fono" en base a los espacios en blanco
	lista_fono = fono.split(" ")

	#Volver a juntar los elementos de "lista_fono" con join
	codigo = "".join(lista_fono)

	#Cambiar los puntos por guiones
	codigo=codigo.replace(".","-")

	#-------------------------------------------------------------------------#
	#EN ESTE PUNTO LA VARIABLE "codigo" CONTIENE EL CODIGO PFS-US DE LA PALABRA 
	#DE ENTRADA.
	#-------------------------------------------------------------------------#
	return codigo
#ENDDEF

#############################################################################################

