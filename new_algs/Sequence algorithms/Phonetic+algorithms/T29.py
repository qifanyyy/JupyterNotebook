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
#T29.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 06 de Julio del 2015

#Funcion:

#	T29 ( palabra_a_fonetizar )

#Sinopsis


#Esta funcion toma como entrada una palabra bien escrita en minusculas,
#con la vocal tonica indicada en mayuscula y con la x en alguno de sus 
#4 contextos #que seran los siguientes.

# Si esta funcion ve:

#x significa que se trata del sonido por default /ks/ como en "sexto"
#J significa que se trata del sonido /x/ como en "mexico"
#S sinifica que se trata del sonido /esh/ como en "xolos"
#$ significa que se trata del sonido /s/ como en "xilofono"

#Al final esta funcion devuelve la palabra fonetizada en 
#alfabeto Mexbet T29.

#Hay que recordar que la funcion T29() es igual a la funcion T22() que 
#se conserva por compatibilidad.

#El numero 29 refleja el numero de simbolos MEXBET utilizados en
#en la transcripcion a nivel fonologico.


#Nota: Si el archivo de salida ya existia, este programa lo sobre-escribe
#Nota: Exactamente la primer linea de este programa sirve para manejar la letra Ñ y acentos
#############################################################################################
#Importar modulos necesarios

#Modulo para trabajar con el sistema operativo
import sys

#Modulo para expresiones regulares
import re

#Modulo creado por mi donde viene la funcion TT()
from fonetica3.TT import TT

#Modulo creado por mi donde viene la funcion div_sil()
from fonetica3.div_sil import div_sil

#############################################################################################
#FUNCION PRINCIPAL T22()
#############################################################################################

def T29(palabra_in):

	#NOTA: La palabra de entrada no debe contener salto de linea

	#Antes de dividir en silabas, tratar el caso de la "x"

	palabra_in = palabra_in.replace("xa","ksa")
	palabra_in = palabra_in.replace("xe","kse")
	palabra_in = palabra_in.replace("xi","ksi")
	palabra_in = palabra_in.replace("xo","kso")
	palabra_in = palabra_in.replace("xu","ksu")

	palabra_in = palabra_in.replace("xá","ksA")
	palabra_in = palabra_in.replace("xé","ksE")
	palabra_in = palabra_in.replace("xí","ksI")
	palabra_in = palabra_in.replace("xó","ksO")
	palabra_in = palabra_in.replace("xú","ksU")
	palabra_in = palabra_in.replace("xü","ksW")

	palabra_in = palabra_in.replace("xÁ","ksA")
	palabra_in = palabra_in.replace("xÉ","ksE")
	palabra_in = palabra_in.replace("xÍ","ksI")
	palabra_in = palabra_in.replace("xÓ","ksO")
	palabra_in = palabra_in.replace("xÚ","ksU")
	palabra_in = palabra_in.replace("xÜ","ksW")

	palabra_in = palabra_in.replace("xA","ksA")
	palabra_in = palabra_in.replace("xE","ksE")
	palabra_in = palabra_in.replace("xI","ksI")
	palabra_in = palabra_in.replace("xO","ksO")
	palabra_in = palabra_in.replace("xU","ksU")
	palabra_in = palabra_in.replace("xW","ksW")

	palabra_in = palabra_in.replace("xc","ks")
	palabra_in = palabra_in.replace("xs","ks")

	#Trata el caso de sce y sci (como escena y escision)
	palabra_in = palabra_in.replace("sce","se")
	palabra_in = palabra_in.replace("sci","si")

	#Casos de la "x"
	palabra_in = palabra_in.replace("x","K")
	palabra_in = palabra_in.replace("$","s")
	palabra_in = palabra_in.replace("J","j")
	palabra_in = palabra_in.replace("S","8")

	#La "b" y la "v"
	palabra_in = palabra_in.replace("v","b")

	#la "z" y la "s"
	palabra_in = palabra_in.replace("z","s")

	#Antes de dividir en silabas trata el caso de la 
	#vibrante multiple en posicion inicial de palabra.

	#Y tambien el caso de las palabras como
	#deshacer
	#deshecho
	#deshidratar
	#dehonesto
	#deshumanizar

	#Ya que aqui la "sh" no debe sewr tomada por el fonema esh /S/
	
	palabra_in = "#"+palabra_in
	palabra_in = palabra_in.replace("#r","R")
	palabra_in = palabra_in.replace("#desh","des")
	palabra_in = palabra_in.replace("#","")

	#Tambien se trata el caso de la w al final de palabra como en "show"
	palabra_in = palabra_in + "#"
	palabra_in = palabra_in.replace("w#","u")
	palabra_in = palabra_in.replace("#","")

	#####################################################################################
	#Dividir en silabas
	en_silabas = div_sil(palabra_in)
	#####################################################################################

	#Transformar el texto de entrada
	texto_tt = TT(en_silabas)

	#Trata el caso de la vibrante multiple escrita como simple
	
	texto_tt = texto_tt.replace("n.r","n.R")
	texto_tt = texto_tt.replace("l.r","l.R")
	texto_tt = texto_tt.replace("s.r","s.R")

	#Cambiar las grafias por los fonemas correspondientes en Mexbet T22

	#Esta es una "x" seguida de consonante
	texto_tt = texto_tt.replace("K"," k s ")

	#Grupo de fonemas ts y tz
	texto_tt = texto_tt.replace("2"," t s ")
	
	#La "h" es muda
	texto_tt = texto_tt.replace("h","")

	#El fonema /esh/
	texto_tt = texto_tt.replace("S","8")

	#Consonantes
	texto_tt = texto_tt.replace("p"," p ")
	texto_tt = texto_tt.replace("b"," b ")
	texto_tt = texto_tt.replace("t"," t ")
	texto_tt = texto_tt.replace("d"," d ")

	texto_tt = texto_tt.replace("k"," k ")
	texto_tt = texto_tt.replace("c"," k ")
	texto_tt = texto_tt.replace("Q"," k ")
	texto_tt = texto_tt.replace("q"," k ")


	texto_tt = texto_tt.replace("g"," g ")
	texto_tt = texto_tt.replace("G"," g ")

	texto_tt = texto_tt.replace("H"," tS ")

	texto_tt = texto_tt.replace("f"," f ")

	texto_tt = texto_tt.replace("s"," s ")
	texto_tt = texto_tt.replace("5"," s ")
	texto_tt = texto_tt.replace("P"," s ")
	texto_tt = texto_tt.replace("$"," s ") #<---

	texto_tt = texto_tt.replace("8"," S ")
	#texto_tt = texto_tt.replace("S"," S ") #<---

	texto_tt = texto_tt.replace("j"," x ")
	texto_tt = texto_tt.replace("X"," x ")
	texto_tt = texto_tt.replace("J"," x ") #<---

	texto_tt = texto_tt.replace("y"," Z ")
	texto_tt = texto_tt.replace("L"," Z ")

	texto_tt = texto_tt.replace("m"," m ")

	texto_tt = texto_tt.replace("n"," n ")
	texto_tt = texto_tt.replace(".~","~.")#-------------- ???
	texto_tt = texto_tt.replace("n ~"," n~ ")

	texto_tt = texto_tt.replace("N"," n~ ")

	texto_tt = texto_tt.replace("r"," r( ")
	texto_tt = texto_tt.replace("R"," r ")

	texto_tt = texto_tt.replace("l"," l ")


	#Vocales
	texto_tt = texto_tt.replace("a"," a ")
	texto_tt = texto_tt.replace("e"," e ")
	texto_tt = texto_tt.replace("i"," i ")
	texto_tt = texto_tt.replace("o"," o ")
	texto_tt = texto_tt.replace("u"," u ")

	texto_tt = texto_tt.replace("A"," a_7 ")
	texto_tt = texto_tt.replace("E"," e_7 ")
	texto_tt = texto_tt.replace("I"," i_7 ")
	texto_tt = texto_tt.replace("O"," o_7 ")
	texto_tt = texto_tt.replace("U"," u_7 ")

	texto_tt = texto_tt.replace("1"," i ")
	texto_tt = texto_tt.replace("W"," u ")

	#Casos especiales

	texto_tt = texto_tt.replace(".Z"," t . s ")

	texto_tt = texto_tt.replace("w u"," g u ")

	texto_tt = texto_tt.replace("w"," g u ")

#	texto_tt = texto_tt.replace("","")

	#Trascribe el fonema tl
	texto_tt = texto_tt + "#"
	texto_tt = texto_tt.replace("T#"," tl ")

	texto_tt = texto_tt.replace("#","")
	texto_tt = texto_tt.replace("T"," t l ")

	#Quitar los espacios en blanco extras
	texto_tt = texto_tt + "#"
	texto_tt=re.sub(r'\s*#','',texto_tt)

	texto_tt = "#" + texto_tt
	texto_tt=re.sub(r'#\s*','',texto_tt)

	texto_tt=re.sub(r'\s+',' ',texto_tt)

	#Si se trata de la conjuncion "y" transcribe asi
	texto_tt = "#"+texto_tt+"#"
	texto_tt = texto_tt.replace("#i#","i_7")
	texto_tt = texto_tt.replace("#","")

	#Entrega la transcripcion final
	return texto_tt

#ENDIF

#############################################################################################
#FIN DE LA FUNCION
#############################################################################################
