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
#div_sil.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 20 de Junio del 2014

#Funcion:

#	div_sil( palabra_a_dividir)

#Sinopsis


#Esta funcion recibe como argumento una palabra en minusculas
#y la devuelve dividida en silabas.


#Nota: Si el archivo de salida ya existia, este programa lo sobre-escribe
#Nota: Exactamente la primer linea de este programa sirve para manejar la letra Ñ y acentos
#############################################################################################
#Importar modulos necesarios

#Modulo para trabajar con el sistema operatibo
import sys

#Modulo creado por mi donde viene la funcion TT()
from fonetica3.TT import TT

#Modulo creado por mi donde viene la funcion  TT_INV()
from fonetica3.TT_INV import TT_INV

#############################################################################################
#VARIABLES GLOBALES

VOCALES = ['a','e','i','o','u','A','E','I','O','U','1','W']

DEBILES = ['i','u','1','W']


#############################################################################################
#FUNCIONES GLOBALES

#Convertir caracteres especiales
def car_esp(palabra_in):

	#NOTA: se asume que para usar esta funcion 
	#los caracteres ya deben estar en minusculas absolutas

	#Delimitar inicio y fin de palabra

	palabra_in = "#"+palabra_in+"#"

	palabra_in = palabra_in.replace("á","A")
	palabra_in = palabra_in.replace("é","E")
	palabra_in = palabra_in.replace("í","I")
	palabra_in = palabra_in.replace("ó","O")
	palabra_in = palabra_in.replace("ú","U")

	palabra_in = palabra_in.replace("ü","W")
	palabra_in = palabra_in.replace("ñ","N")

	palabra_in = palabra_in.replace("y#","1")


	#Quita los puntos que delimitan el inicio y fin de palabra
	#en caso de que los haya
	palabra_in = palabra_in.replace("#","")

	return palabra_in
#ENDDEF


#Regresar los caracteres especiales convertidos a su
#estado original
def car_esp_INV(palabra_in):


	#Delimitar inicio y fin de palabra

	palabra_in = "#"+palabra_in+"#"

	palabra_in = palabra_in.replace("A","á")
	palabra_in = palabra_in.replace("E","é")
	palabra_in = palabra_in.replace("I","í")
	palabra_in = palabra_in.replace("O","ó")
	palabra_in = palabra_in.replace("U","ú")

	palabra_in = palabra_in.replace("W","ü")
	palabra_in = palabra_in.replace("N","ñ")

	palabra_in = palabra_in.replace("1#","y#")

	#Quita los puntos que delimitan el inicio y fin de palabra
	#en caso de que los haya
	palabra_in = palabra_in.replace("#","")

	return str(palabra_in)

#ENDDEF

#Definir patron consonante-vocal
def patron_CV(palabra_in):
	#NOTA: La palabra de entrada no debe tener salto de linea

	acumulador = ""

	#Recorrer la palabra de entrada caracter por caracter
	#para definir este parton Consonante-Vocal (patrnCV)
	for car in palabra_in:

		#Si el caracter no esta dentro del conjunto de las vocales
		#es una consonante

		if car not in VOCALES:

			acumulador = acumulador + "C"

		else:

			if car in DEBILES:
				#Si es vocal debil
				acumulador = acumulador + "v"
			else:
				#Si vocal fuerte
				acumulador = acumulador + "V"
			#ENDIF
	#ENDFOR

	return acumulador
#ENDDEF

#Funcion que redistribuye los grupos de consonantes
#juntas para formar los patrones silabicos como deben ser.
def forma_grupos_sil(patron_in):

	#NOTA: el patron de entrada no debe tener salto de linea

	#Delimitar inicio y fin de patron
	patron_in = "#" +patron_in+"#"

	#Esta funcion trabaja con puras sustituciones.
	#En el español el numero maximo de consonantes
	#posibles es 4.


	#Trabajar con inicios y fines de palabra

	#Inicios
	patron_in = patron_in.replace("#CCCC","#kkkk")
	patron_in = patron_in.replace("#CCC","#kkk")
	patron_in = patron_in.replace("#CC","#kk")
	patron_in = patron_in.replace("#C","#k")

	#Fines
	patron_in = patron_in.replace("CCCC#","kkkk#")
	patron_in = patron_in.replace("CCC#","kkk#")
	patron_in = patron_in.replace("CC#","kk#")
	patron_in = patron_in.replace("C#","k#")

	#Redistribuir grupos de consonantes

	#grupos de 4
	patron_in = patron_in.replace("CCCC","kk.kk")

	#Grupos de 3
	patron_in = patron_in.replace("CCC","k.kk")

	#Grupos de 2
	patron_in = patron_in.replace("CC","k.k")

	#Grupos de 1
	#patron_in = patron_in.replace("c","k")


	#Localizar los patrones consonante-vocal (CV)
	patron_in = patron_in.replace("Cv",".kv")
	patron_in = patron_in.replace("CV",".kV")

	#Romper diptongos
	patron_in = patron_in.replace("VV","V.V")

	#Se aplica otra vez para romper triptongos en caso de haberlos
	patron_in = patron_in.replace("VV","V.V")

	#Quitar puntos de mas
	patron_in = patron_in.replace("...",".")
	patron_in = patron_in.replace("..",".")

	#Quitar los delimitadores de inicio y fin si los hubiera
	patron_in = patron_in.replace("#.","")
	patron_in = patron_in.replace(".#","")
	patron_in = patron_in.replace("#","")

	return patron_in
#ENDDEF


#Funcion que pasa del patron silabico a la palabra original
#este es el paso previo a la division silabica definitiva
def pre_DIV(palabra_in, patron_in):


	dividida = ""
	indice = -1

	#Recorrer el patron silabico caracter por caracter
	for car in patron_in:

		indice = indice + 1
		
		if car != ".":
			dividida = dividida + palabra_in[indice]

		else:
			dividida = dividida + "."
			indice = indice - 1
		#ENDIF


	#ENDFOR

	return dividida
	

#ENDDEF

#Esta funcion se aplica a una palabra ya divida en silabas
#y une todas las oclusivas que estan tras una liquida
#como pr pl  br, br, , etc.
def une_liquidas(silabas_in):

	silabas_in = silabas_in.replace("p.r",".pr")
	silabas_in = silabas_in.replace("p.l",".pl")

	silabas_in = silabas_in.replace("b.r",".br")
	silabas_in = silabas_in.replace("b.l",".bl")

	silabas_in = silabas_in.replace("t.r",".tr")
	silabas_in = silabas_in.replace("t.l",".tl")

	silabas_in = silabas_in.replace("d.r",".dr")
	silabas_in = silabas_in.replace("d.l",".dl")

	silabas_in = silabas_in.replace("k.r",".kr")
	silabas_in = silabas_in.replace("k.l",".kl")

	silabas_in = silabas_in.replace("g.r",".gr")
	silabas_in = silabas_in.replace("g.l",".gl")

	silabas_in = silabas_in.replace("c.r",".cr")
	silabas_in = silabas_in.replace("c.l",".cl")

	silabas_in = silabas_in.replace("f.r",".fr")
	silabas_in = silabas_in.replace("f.l",".fl")

	#Arregla el casi ts o tz seguida de vocal
	silabas_in = silabas_in.replace(".tsa","t.sa")
	silabas_in = silabas_in.replace(".tse","t.se")
	silabas_in = silabas_in.replace(".tsi","t.si")
	silabas_in = silabas_in.replace(".tso","t.so")
	silabas_in = silabas_in.replace(".tsu","t.su")


	silabas_in = silabas_in.replace(".tza","t.za")
	silabas_in = silabas_in.replace(".tze","t.ze")
	silabas_in = silabas_in.replace(".tzi","t.zi")
	silabas_in = silabas_in.replace(".tzo","t.zo")
	silabas_in = silabas_in.replace(".tzu","t.zu")

	silabas_in = silabas_in.replace(".tsá","t.sá")
	silabas_in = silabas_in.replace(".tsé","t.sé")
	silabas_in = silabas_in.replace(".tsí","t.sí")
	silabas_in = silabas_in.replace(".tsó","t.só")
	silabas_in = silabas_in.replace(".tsú","t.sú")


	silabas_in = silabas_in.replace(".tzá","t.zá")
	silabas_in = silabas_in.replace(".tzé","t.zé")
	silabas_in = silabas_in.replace(".tzí","t.zí")
	silabas_in = silabas_in.replace(".tzó","t.zó")
	silabas_in = silabas_in.replace(".tzú","t.zú")

	#Arregla estos casos raros
	silabas_in = silabas_in.replace("n.st","ns.t")

	#Arregla el caso del fonema /tl/
	silabas_in = silabas_in + "#"
	silabas_in = silabas_in.replace("tl#",".tl")
	silabas_in = silabas_in.replace("#","")

	#Devuelve las silabas corregidas
	return silabas_in

#ENDDEF


#############################################################################################
#FUNCION PRINCPIAL div_sil()
#############################################################################################


#Funcion para dividir en silabas
def div_sil(palabra_in):

	#A esta funcion llega una palabra en español
	#bien escrita en minusculas y sin salto de linea
	
	#Transformar texto con TT()
	tt = TT(palabra_in)

	#Obtener patron consonante-vocal con patron_CV()
	patron_cons_voc = patron_CV(tt)

	#Obtener grupos silabicos con forma_grupos_sil()
	grupos_sil = forma_grupos_sil(patron_cons_voc)

	#Obtener la palabra casi dividida en silabas con pre_DIV()
	#en este punto ya solo pasa aplicar la transformacion 
	#inversa del texto para obtener la palabra bien dividida
	#en silabas
	casi_div = pre_DIV(tt,grupos_sil)

	#Aplicar la transformacion inversa del texto con TT_INV()
	tt_inv = TT_INV(casi_div)

	#Une las liquidas a las oclusivas mediante une_liquidas()
	silabas_out = une_liquidas(tt_inv)
	
	#Devolver el resultado
	return silabas_out

#ENDDEF

#############################################################################################
#FIN DE LA FUNCION
#############################################################################################

