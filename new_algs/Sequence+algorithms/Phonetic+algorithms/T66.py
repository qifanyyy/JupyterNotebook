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
#T66.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 06 de Julio del 2015

#Funcion:

#	T66 ( palabra_a_fonetizar )

#Sinopsis


#Esta funcion toma como entrada una palabra bien escrita en minusculas,
#con la vocal tonica indicada en mayuscula y con la x en alguno de sus 
#4 contextos que seran los siguientes.

# Si esta funcion ve:

#x significa que se trata del sonido por default /ks/ como en "sexto"
#J significa que se trata del sonido /x/ como en "mexico"
#S sinifica que se trata del sonido /esh/ como en "xolos"
#$ significa que se trata del sonido /s/ como en "xilofono"

#Al final esta funcion devuelve la palabra fonetizada en 
#alfabeto Mexbet T66.

#Hay que recordar que la funcion T66() es igual a la funcion T50() que 
#se conserva por compatibilidad.

#El numero 66 refleja el numero de simbolos MEXBET utilizados en
#en la transcripcion a nivel fonetico.


#Nota: Si el archivo de salida ya existia, este programa lo sobre-escribe
#Nota: Exactamente la primer linea de este programa sirve para manejar la letra Ñ y acentos
#############################################################################################
#Importar modulos necesarios

#Modulo para trabajar con el sistema operativo
import sys

#Modulo para expresiones regulares
import re

#Añadir el path donde esta la carpeta "fonetica3"
sys.path.append(".")

##Modulo creado por mi donde viene la funcion TT()
#from fonetica3.TT import TT

##Modulo creado por mi donde viene la funcion  TT_INV()
#from fonetica3.TT_INV import TT_INV

##Modulo creado por mi donde viene la funcion div_sil()
#from fonetica3.div_sil import div_sil

##Modulo creado por mi donde viene la funcion vocal_tonica()
#from fonetica3.vocal_tonica import vocal_tonica

#Modulo creado por mi donde viene la funcion T29()
from fonetica3.T29 import T29

#############################################################################################
#FUNCION PRINCIPAL T50()
#############################################################################################

def T66(palabra_in):

	#Fonetizar la palabra en Mexbet T22
	fonetizada = T29(palabra_in)

	#Delimitar la la palabra
	fonetizada = "#. "+fonetizada + " .#"

	#Hacer la conversion a Mexbet T50
	#No en el orden en que vienen las tablas de Cuetara

	##############
	#Fonema /k/
	##############

	#k
	#Inicial de silaba, mantiene sus rasgos originales

	#k_j
	#Se palataliza ante vocales anteriores (palatales)

	fonetizada = fonetizada.replace("k e","k_j e")
	fonetizada = fonetizada.replace("k i","k_j i")

	##############
	#Fonema /a/
	##############

	#a_j
	#Ante consonante palatal: /tS/, /S/, /Z/, /n~/

	fonetizada = fonetizada.replace("a tS","a_j tS")
	fonetizada = fonetizada.replace("a S","a_j S")
	fonetizada = fonetizada.replace("a Z","a_j Z")
	fonetizada = fonetizada.replace("a n~","a_j n~")
	fonetizada = fonetizada.replace("a tl","a_j tl")

	fonetizada = fonetizada.replace("a . tS","a_j . tS")
	fonetizada = fonetizada.replace("a . S","a_j . S")
	fonetizada = fonetizada.replace("a . Z","a_j . Z")
	fonetizada = fonetizada.replace("a . n~","a_j . n~")
	fonetizada = fonetizada.replace("a . tl","a_j . tl")

	fonetizada = fonetizada.replace("a_7 tS","a_j_7 tS")
	fonetizada = fonetizada.replace("a_7 S","a_j_7 S")
	fonetizada = fonetizada.replace("a_7 Z","a_j_7 Z")
	fonetizada = fonetizada.replace("a_7 n~","a_j_7 n~")
	fonetizada = fonetizada.replace("a_7 tl","a_j_7 tl")

	fonetizada = fonetizada.replace("a_7 . tS","a_j_7 . tS")
	fonetizada = fonetizada.replace("a_7 . S","a_j_7 . S")
	fonetizada = fonetizada.replace("a_7 . Z","a_j_7 . Z")
	fonetizada = fonetizada.replace("a_7 . n~","a_j_7 . n~")
	fonetizada = fonetizada.replace("a_7 . tl","a_j_7 . tl")

	#En diptongo decreciente con /i/

	fonetizada = fonetizada.replace("a i","a_j i")
	fonetizada = fonetizada.replace("a_7 i","a_j_7 i")

	#a_2
	#En diptongo decreciente con /u/
	
	fonetizada = fonetizada.replace("a u","a_2 u")
	fonetizada = fonetizada.replace("a_7 u","a_2_7 u")

	#Ante /o/

	fonetizada = fonetizada.replace("a . o","a_2 . o")
	fonetizada = fonetizada.replace("a_7 . o","a_2_7 . o")

	#En silaba cerrada trabada por /l/

	fonetizada = fonetizada.replace("a l .","a_2 l .")
	fonetizada = fonetizada.replace("a_7 l .","a_2_7 l .")

	#Ante el fonema consonantico /x/
	fonetizada = fonetizada.replace("a x","a_2 x")
	fonetizada = fonetizada.replace("a_7 x","a_2_7 x")

	fonetizada = fonetizada.replace("a . x","a_2 . x")
	fonetizada = fonetizada.replace("a_7 . x","a_2_7 . x")

	#En todos los demas contextos

	##############
	#Fonema /e/
	##############

	#Es mas facil invertir el fonema por el alofono
	fonetizada = fonetizada.replace("e","E")

	#e
	#Libre, en silaba abierta
	fonetizada = fonetizada.replace("E .","e .")
	fonetizada = fonetizada.replace("E_7 .","e_7 .")

	fonetizada = fonetizada.replace("E u","e u")
	fonetizada = fonetizada.replace("E_7 u","e_7 u")


	#En silaba cerrada trabado por /m/, /n/, /s/ o /d/
	fonetizada = fonetizada.replace("E m .","e m .")
	fonetizada = fonetizada.replace("E n .","e n .")
	fonetizada = fonetizada.replace("E s .","e s .")
	fonetizada = fonetizada.replace("E d .","e d .")

	fonetizada = fonetizada.replace("E_7 m .","e_7 m .")
	fonetizada = fonetizada.replace("E_7 n .","e_7 n .")
	fonetizada = fonetizada.replace("E_7 s .","e_7 s .")
	fonetizada = fonetizada.replace("E_7 d .","e_7 d .")

	#E
	#- En silaba cerrada, trabada por consonante (salvo /m, n, s, d/)

	#- En contacto con /r/
	fonetizada = fonetizada.replace("r e","r E")
	fonetizada = fonetizada.replace("r( e","r( E")

	fonetizada = fonetizada.replace("r . e","r . E")
	fonetizada = fonetizada.replace("r( . e","r( . E")

	fonetizada = fonetizada.replace("e . r","E . r")
	fonetizada = fonetizada.replace("e_7 . r","E_7 . r")


	#- En diptongo decreciente con /i/

	#- Ante /x/ (sin condicion silabica)

	fonetizada = fonetizada.replace("e . x","E . x")
	fonetizada = fonetizada.replace("e_7 . x","E_7 . x")

	##############
	#Fonema /o/
	##############

	#Es mas facil invertir el fonema por el alofono
	fonetizada = fonetizada.replace("o","O")

	#o

	#Libre, en silaba abierta
	fonetizada = fonetizada.replace("O .","o .")
	fonetizada = fonetizada.replace("O_7 .","o_7 .")

	fonetizada = fonetizada.replace("O u","o u")
	fonetizada = fonetizada.replace("O_7 u","o_7 u")
	
	#O

	#En silaba cerrada, trabada por consonante sin excepcion

	#En contacto con /r/

	fonetizada = fonetizada.replace("r o","r O")
	fonetizada = fonetizada.replace("r( o","r( O")

	fonetizada = fonetizada.replace("o r","O r")
	fonetizada = fonetizada.replace("o_7 r","O_7 r")

	fonetizada = fonetizada.replace("o . r","O . r")
	fonetizada = fonetizada.replace("o_7 . r","O_7 . r")

	#En diptongo decreciente /i/

	#Ante /x/ (sin condicion silabica)

	fonetizada = fonetizada.replace("o x","O x")
	fonetizada = fonetizada.replace("o . x","O . x")
	fonetizada = fonetizada.replace("o_7 x","O_7 x")
	fonetizada = fonetizada.replace("o_7 . x","O_7 . x")

	##############
	#Fonema /i/
	##############

	#Es mas facil invertir el fonema por el alofono
	fonetizada = fonetizada.replace("i","I")

	#i
	#Libre, en silaba abierta
	
	fonetizada = fonetizada.replace("I .","i .")
	fonetizada = fonetizada.replace("I_7 .","i_7 .")

	#I
	#En silaba cerrada 

	#En contacto con /r/

	fonetizada = fonetizada.replace("r i","r I")
	fonetizada = fonetizada.replace("r( i","r( I")

	fonetizada = fonetizada.replace("i r","I r")
	fonetizada = fonetizada.replace("i_7 r","I_7 r")

	fonetizada = fonetizada.replace("i . r","I . r")
	fonetizada = fonetizada.replace("i_7 . r","I_7 . r")

	#Ante /x/ (sin condicion silabica)

	fonetizada = fonetizada.replace("i . x","I . x")
	fonetizada = fonetizada.replace("i_7 . x","I_7 . x")

	#j
	#En posicion inicial de diptongo

	fonetizada = fonetizada.replace("I a","j a")

	fonetizada = fonetizada.replace("I u","j u")
	fonetizada = fonetizada.replace("I_7 u","j_7 u")

	fonetizada = fonetizada.replace("I e","j e")
	fonetizada = fonetizada.replace("I E","j E")

	fonetizada = fonetizada.replace("I o","j o")
	fonetizada = fonetizada.replace("I O","j O")

	#En posicion final de diptongo

	fonetizada = fonetizada.replace("a_j i","a_j i(")
	fonetizada = fonetizada.replace("a_j_7 i","a_j_7 i(")
	fonetizada = fonetizada.replace("a_j I","a_j i(")
	fonetizada = fonetizada.replace("a_j_7 I","a_j_7 i(")

	fonetizada = fonetizada.replace("E i","E i(")
	fonetizada = fonetizada.replace("E_7 i","E_7 i(")
	fonetizada = fonetizada.replace("E I","E i(")
	fonetizada = fonetizada.replace("E_7 I","E_7 i(")

	fonetizada = fonetizada.replace("O i","O i(")
	fonetizada = fonetizada.replace("O_7 i","O_7 i(")
	fonetizada = fonetizada.replace("O I","O i(")
	fonetizada = fonetizada.replace("O_7 I","O_7 i(")

	fonetizada = fonetizada.replace("u i ","u i( ")
	fonetizada = fonetizada.replace("u i_7 ","u i(_7 ")

	fonetizada = fonetizada.replace("u I ","u i( ")
	fonetizada = fonetizada.replace("u I_7 ","u i(_7 ")

	fonetizada = fonetizada.replace("u_7 i ","u_7 i( ")
	fonetizada = fonetizada.replace("u_7 I ","u_7 i( ")

	fonetizada = fonetizada.replace("U i ","U i( ")
	fonetizada = fonetizada.replace("U i_7 ","U i(_7 ")

	fonetizada = fonetizada.replace("U I ","U i( ")
	fonetizada = fonetizada.replace("U I_7 ","U i(_7 ")

	fonetizada = fonetizada.replace("U_7 i ","U_7 i( ")
	fonetizada = fonetizada.replace("U_7 I ","U_7 i( ")

	##############
	#Fonema /u/
	##############

	#Es mas facil invertir el fonema por el alofono
	fonetizada = fonetizada.replace("u","U")

	#i
	#Libre, en silaba abierta
	
	fonetizada = fonetizada.replace("U .","u .")
	fonetizada = fonetizada.replace("U_7 .","u_7 .")

	#I
	#En silaba cerrada 

	#En contacto con /r/

	fonetizada = fonetizada.replace("r u","r U")
	fonetizada = fonetizada.replace("r( u","r( U")

	fonetizada = fonetizada.replace("u . r","U . r")
	fonetizada = fonetizada.replace("u_7 . r","U_7 . r")

	#Ante /x/ (sin condicion silabica)

	fonetizada = fonetizada.replace("u . x","U . x")
	fonetizada = fonetizada.replace("u_7 . x","U_7 . x")

	#j
	#En posicion inicial de diptongo

	fonetizada = fonetizada.replace("U a","w a")

	fonetizada = fonetizada.replace("U i(","w i(")
	fonetizada = fonetizada.replace("U_7 i(","w_7 i(")

	fonetizada = fonetizada.replace("U e","w e")
	fonetizada = fonetizada.replace("U E","w E")

	fonetizada = fonetizada.replace("U o","w o")
	fonetizada = fonetizada.replace("U O","w O")


	#En posicion final de diptongo

	fonetizada = fonetizada.replace("a_2 u","a_2 u(")
	fonetizada = fonetizada.replace("a_2_7 u","a_2_7 u(")
	fonetizada = fonetizada.replace("a_2 U","a_2 u(")
	fonetizada = fonetizada.replace("a_2_7 U","a_2_7 u(")

	fonetizada = fonetizada.replace("e u","e u(")
	fonetizada = fonetizada.replace("e_7 u","e_7 u(")
	fonetizada = fonetizada.replace("E u","E u(")
	fonetizada = fonetizada.replace("E_7 u","E_7 u(")
	fonetizada = fonetizada.replace("e U","e u(")
	fonetizada = fonetizada.replace("e_7 U","e_7 u(")
	fonetizada = fonetizada.replace("E U","E u(")
	fonetizada = fonetizada.replace("E_7 U","E_7 u(")

	fonetizada = fonetizada.replace("o U","o u(")
	fonetizada = fonetizada.replace("o_7 U","o_7 u(")
	fonetizada = fonetizada.replace("O U","O u(")
	fonetizada = fonetizada.replace("O_7 U","O_7 u(")
	fonetizada = fonetizada.replace("o u","o u(")
	fonetizada = fonetizada.replace("o_7 u","o_7 u(")
	fonetizada = fonetizada.replace("O u","O u(")
	fonetizada = fonetizada.replace("O_7 u","O_7 u(")

	fonetizada = fonetizada.replace("j u","j u(")
	fonetizada = fonetizada.replace("j_7 u","j_7 u(")
	fonetizada = fonetizada.replace("j u_7","j u(_7")
	fonetizada = fonetizada.replace("j U","j u(")
	fonetizada = fonetizada.replace("j_7 U","j_7 u(")
	fonetizada = fonetizada.replace("j U_7","j u(_7")

	##############
	#Fonema /p/
	##############

	##############
	#Fonema /t/
	##############

	##############
	#Fonema /b/
	##############

	#Es mas facil sustituir le fonema por su alofono

	fonetizada = fonetizada.replace("b","V")

	#b
	#Inicial absoluto, despues de pausa y despues de nasal, permanese oclusivo
	
	fonetizada = fonetizada.replace("#. V","#. b")

	#Despues de nasal
	fonetizada = fonetizada.replace("m . V","m . b")
	fonetizada = fonetizada.replace("n . V","n . b")
	fonetizada = fonetizada.replace("n~ . V","n~ . b")

	fonetizada = fonetizada.replace("m V","m b")
	fonetizada = fonetizada.replace("n V","n b")
	fonetizada = fonetizada.replace("n~ V","n~ b")

	#V
	#Se presenta fricatiado (aproximante) en todos los demas contextos

	##############
	#Fonema /d/
	##############

	#Es mas facil sustituir le fonema por su alofono
	fonetizada = fonetizada.replace("d","D")

	#d

	#Inicial absoluto, despues de pausa, despues de nasal y de /l/,
	#permanece oclusivo

	fonetizada = fonetizada.replace("#. D","#. d")

	#Despues de nasal

	fonetizada = fonetizada.replace("m . D","m . d")
	fonetizada = fonetizada.replace("n . D","n . d")
	fonetizada = fonetizada.replace("n~ . D","n~ . d")

	fonetizada = fonetizada.replace("m D","m d")
	fonetizada = fonetizada.replace("n D","n d")
	fonetizada = fonetizada.replace("n~ D","n~ d")

	#Despues de /l/

	fonetizada = fonetizada.replace("l . D","l . d")
	fonetizada = fonetizada.replace("l D","l d")
	
	#D

	#Se presenta fricatizado (aproximante) en todos
	#los demas contextos

	##############
	#Fonema /g/
	##############
	
	#Es mas facil sustituir el fonema por su alofono
	fonetizada = fonetizada.replace("g","G")

	#g
	#Inicial absoluto, despues de pausa, y despues de nasal
	#permanece oclusivo

	fonetizada = fonetizada.replace("#. G","#. g")
	
	#Despues de nasal
	
	fonetizada = fonetizada.replace("m . G","m . g")
	fonetizada = fonetizada.replace("n . G","n . g")
	fonetizada = fonetizada.replace("n~ . G","n~ . g")

	fonetizada = fonetizada.replace("m G","m g")
	fonetizada = fonetizada.replace("n G","n g")
	fonetizada = fonetizada.replace("n~ G","n~ g")

	#G
	#En todos los demás contextos se presenta fricativo
	#(o aproximante)

	##############
	#Fonema /tS/
	##############

	##############
	#Fonema /f/
	##############

	##############
	#Fonema /x/
	##############

	##############
	#Fonema /n~/
	##############

	##############
	#Fonema /r/
	##############

	##############
	#Fonema /Z/
	##############

	#dZ
	#Modifica su modo de articulacion a africado en posicion
	#inicial absoluta, despues de nasal y de lateral

	fonetizada = fonetizada.replace("#. Z ","#. dZ ")

	#Despues de nasal

	fonetizada = fonetizada.replace("m . Z","m . dZ")
	fonetizada = fonetizada.replace("n . Z","n . dZ")
	fonetizada = fonetizada.replace("n~ . Z","n~ . dZ")

	fonetizada = fonetizada.replace("m Z","m dZ")
	fonetizada = fonetizada.replace("n Z","n dZ")
	fonetizada = fonetizada.replace("n~ Z","n~ dZ")

	#Despues de lateral

	fonetizada = fonetizada.replace("l . Z","l . dZ")
	fonetizada = fonetizada.replace("l Z","l dZ")

	#Z

	#En todos los demas conceptos

	##############
	#Fonema /m/
	##############

	#m
	#En todos los contextos, principalmente inicial de silaba

	#m_n (DECIDI NO INCLUIR ESTE CASO)
	#La union de nasales alveolar y bilabial combina la articulacion

#	fonetizada = fonetizada.replace("n . m",". m_n")
#	fonetizada = fonetizada.replace(" n m "," m_n ")

	##############
	#Fonema /l/
	##############

	#l_[
	#Dentalizado ante dental
	fonetizada = fonetizada.replace("l . t ","l_[ . t ")
	fonetizada = fonetizada.replace("l . d ","l_[ . d ")
	fonetizada = fonetizada.replace("l . D","l_[ . D")

	fonetizada = fonetizada.replace("l t ","l_[ t ")
	fonetizada = fonetizada.replace("l d ","l_[ d ")
	fonetizada = fonetizada.replace("l D","l_[ D")

	#l_j
	#Palatalizado ante palatal

	fonetizada = fonetizada.replace("l . tS","l_j . tS")
	fonetizada = fonetizada.replace("l . S","l_j . S")
	fonetizada = fonetizada.replace("l . Z","l_j . Z")
	fonetizada = fonetizada.replace("l . dZ","l_j . dZ")
	fonetizada = fonetizada.replace("l . n~","l_j . n~")
	fonetizada = fonetizada.replace("l . tl","l_j . tl")

	fonetizada = fonetizada.replace("l tS","l_j tS")
	fonetizada = fonetizada.replace("l S","l_j S")
	fonetizada = fonetizada.replace("l Z","l_j Z")
	fonetizada = fonetizada.replace("l dZ","l_j dZ")
	fonetizada = fonetizada.replace("l n~","l_j n~")
	fonetizada = fonetizada.replace("l tl","l_j tl")

	#l_0
	#Ensordecido despues de /p/, /k/ y /f/
	fonetizada = fonetizada.replace("p l ","p l_0 ")
	fonetizada = fonetizada.replace("k l ","k l_0 ")
	fonetizada = fonetizada.replace("f l ","f l_0 ")

	#l
	#En todos los demas contextos

	##############
	#Fonema / r( /
	##############

	#r(_0
	#Ensordecido, tras de /p/, /t/, /k/ y /f/
	
	fonetizada = fonetizada.replace("p r( ","p r(_0 ")
	fonetizada = fonetizada.replace("t r( ","t r(_0 ")
	fonetizada = fonetizada.replace("k r( ","k r(_0 ")
	fonetizada = fonetizada.replace("f r( ","f r(_0 ")

	#r(_\
	#Se relaja en posicion final de silaba o palabra
	
	fonetizada = fonetizada.replace("r( .","r(_\\ .")

	#r(
	#En todos los demas contextos

	##############
	#Fonema /s/
	##############

	#z
	#Sonorizado ante consonantes sonoras

	fonetizada = fonetizada.replace("s . b","z . b")
	fonetizada = fonetizada.replace("s . g","z . g")
	fonetizada = fonetizada.replace("s . V","z . V")
	fonetizada = fonetizada.replace("s . G","z . G")
	fonetizada = fonetizada.replace("s . Z","z . Z")
	fonetizada = fonetizada.replace("s . dZ","z . dZ")
	fonetizada = fonetizada.replace("s . m","z . m")
	fonetizada = fonetizada.replace("s . n","z . n")
	fonetizada = fonetizada.replace("s . n~","z . n~")
	fonetizada = fonetizada.replace("s . r ","z . r ")
	fonetizada = fonetizada.replace("s . l_[","z . l_[")
	fonetizada = fonetizada.replace("s . l_j","z . l_j")
	fonetizada = fonetizada.replace("s . l ","z . l ")

	fonetizada = fonetizada.replace("s b","z b")
	fonetizada = fonetizada.replace("s g","z g")
	fonetizada = fonetizada.replace("s V","z V")
	fonetizada = fonetizada.replace("s G","z G")
	fonetizada = fonetizada.replace("s Z","z Z")
	fonetizada = fonetizada.replace("s dZ","z dZ")
	fonetizada = fonetizada.replace("s m","z m")
	fonetizada = fonetizada.replace("s n","z n")
	fonetizada = fonetizada.replace("s n~","z n~")
	fonetizada = fonetizada.replace("s r ","z r ")
	fonetizada = fonetizada.replace("s l_[","z l_[")
	fonetizada = fonetizada.replace("s l_j","z l_j")
	fonetizada = fonetizada.replace("s l ","z l ")

	#s_[
	#Dentalizado ante consonante dental sorda

	fonetizada = fonetizada.replace("s . t ","s_[ . t ")
	fonetizada = fonetizada.replace("s t ","s_[ t ")

	#z_[
	#Sonorizado y dentalizado ante consonante dental sonora

	fonetizada = fonetizada.replace("s . d ","z_[ . d ")
	fonetizada = fonetizada.replace("s . D","z_[ . D")

	fonetizada = fonetizada.replace("s d ","z_[ d ")
	fonetizada = fonetizada.replace("s D","z_[ D")

	#En todos los demas contextos

	##############
	#Fonema /n/
	##############

	#m
	#Ante labial, se labializa

	fonetizada = fonetizada.replace("n . p","m . p")
	fonetizada = fonetizada.replace("n . b","m . b")
	fonetizada = fonetizada.replace("n . V","m . V")
	fonetizada = fonetizada.replace("n . m","m . m")

	fonetizada = fonetizada.replace("n p","m p")
	fonetizada = fonetizada.replace("n b","m b")
	fonetizada = fonetizada.replace("n V","m V")
	fonetizada = fonetizada.replace("n m","m m")

	#M
	#Ante labiodental, se labiodentaliza
	
	fonetizada = fonetizada.replace("n . f","M . f")
	fonetizada = fonetizada.replace("n f","M f")

	#n_[
	#Ante dental, se dentaliza

	fonetizada = fonetizada.replace("n . t ","n_[ . t ")
	fonetizada = fonetizada.replace("n . d ","n_[ . d ")
	fonetizada = fonetizada.replace("n . D","n_[ . D")

	fonetizada = fonetizada.replace("n t ","n_[ t ")
	fonetizada = fonetizada.replace("n d ","n_[ d ")
	fonetizada = fonetizada.replace("n D","n_[ D")

	#n_j
	#Ante palatal, se palataliza

	fonetizada = fonetizada.replace("n . tS","n_j . tS")
	fonetizada = fonetizada.replace("n . S","n_j . S")
	fonetizada = fonetizada.replace("n . dZ","n_j . dZ")
	fonetizada = fonetizada.replace("n . Z","n_j . Z")
	fonetizada = fonetizada.replace("n . n~","n_j . n~")
	fonetizada = fonetizada.replace("n . tl","n_j . tl")

	fonetizada = fonetizada.replace("n tS","n_j tS")
	fonetizada = fonetizada.replace("n S","n_j S")
	fonetizada = fonetizada.replace("n dZ","n_j dZ")
	fonetizada = fonetizada.replace("n Z","n_j Z")
	fonetizada = fonetizada.replace("n n~","n_j n~")
	fonetizada = fonetizada.replace("n tl","n_j tl")

	#N
	#Ante velar,  se velariza

	fonetizada = fonetizada.replace("n . k","N . k")
	fonetizada = fonetizada.replace("n . g","N . g")
	fonetizada = fonetizada.replace("n . G","N . G")
	fonetizada = fonetizada.replace("n . x","N . x")

	fonetizada = fonetizada.replace("n k","N k")
	fonetizada = fonetizada.replace("n g","N g")
	fonetizada = fonetizada.replace("n G","N G")
	fonetizada = fonetizada.replace("n x","N x")

	#n
	#Inicial sin condicion

	######################################################
	#Correccion de Bugs
	fonetizada = fonetizada.replace(" u(( "," u( ")
	#fonetizada = fonetizada.replace("u(( ","u( ")

	######################################################

	#Quitar los espacios en blanco extras
	fonetizada=re.sub(r'\s+',' ',fonetizada)

	#Quitar los delimitadores de inicio y fin 
	fonetizada = fonetizada.replace("#. ","")
	fonetizada = fonetizada.replace(" .#","")
	
	######################################################
	#ENTREGAR RESULTADO FINAL
	######################################################
	return fonetizada

#ENDDEF
#############################################################################################
#FIN DE LA FUNCION PRINCIPAL
#############################################################################################

