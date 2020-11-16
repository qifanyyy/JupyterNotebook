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
#Algoritmo_PFS_Ejemplo.py

#Autor: Carlos Daniel Hernandez Mena
#Fecha: 21 de Agosto de 2017

#Uso:

#	$ python Algoritmo_PFS_Ejemplo.py <archivo_de_reglas>

#Ejemplo de uso concreto:

#	$ python Algoritmo_PFS_Ejemplo.py REGLAS/reglas_pfs.txt

#Este programa implementa el algoritmo PFS en una palabra de entrada por medio de la
#funcion codigo_pfs()

#############################################################################################
#Importar modulos necesarios

#Modulo para funciones del sistema operativo
import sys

#Añadir el path donde estan las carpeta "fonetica3" y "libpsf"
sys.path.append(".")

#Modulo creado por mi donde viene la funcion leer_reglas()
from libpfs.leer_reglas import leer_reglas

#Modulo creado por mi donde viene la funcion codigo_pfs()
from libpfs.codigo_pfs import codigo_pfs

#############################################################################################
#Llama a la funcion que lee el archivo de reglas.
lista_reglas = leer_reglas(sys.argv[1])



print  (codigo_pfs(lista_reglas,"preproducción"))
print  (codigo_pfs(lista_reglas,"preproducciOn"))



#############################################################################################


