# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 00:04:21 2017

@author: Milton

"""

from foneticaBR import foneticaBR
from buscabr import buscaBR
from metaphoneBR import metaphoneBR


# Soundex - Instalar no Python as bibliotecas soundex e silpa_common

from soundex import Soundex

chaveRoberto = foneticaBR()
chavebr = buscaBR()
chavemeta = metaphoneBR()
chavesoundex = Soundex()

texto = 'JOSSEPH'
print (chaveRoberto.chavefonetica(texto))
print(chavebr.chaveBR(texto, False))
print(chavebr.chaveBR(texto, True))
print(chavemeta.chaveMetaphoneBR(texto))
print(chavesoundex.soundex(texto))
