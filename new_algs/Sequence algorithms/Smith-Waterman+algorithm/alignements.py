#!/usr/bin/python


import sys
import string
import numpy as np
import blossum62 as blo62



# Attribution des valeurs
match = 2
mismatch = -1
gap_start = -3
gap_extension = -1


# Creer matrice vide
def init_matrice(lignes, colonnes, data_type):
	return np.zeros((lignes, colonnes), dtype=data_type)


# Retourner le score partiel
def check(a, b):
	if a == b:
		return match
#	elif a == '-' or b == '-': #Pas utile
#		return gap_start
	else:
		return mismatch



# Algorithme de Needleman, alignement global
def needleman(seq1, seq2, boolean):
	lenS1i, lenS2j = len(seq1)+1, len(seq2)+1

	score=init_matrice(lenS1i, lenS2j, 'float')
	traceback=init_matrice(lenS1i, lenS2j, 'string')

	# Initialisation des cases [0][1] et [1][0]
	score[0][1], score[1][0] = gap_start, gap_start
	traceback[0][1], traceback[1][0] = 'left', 'up'


	# Initialisation de la premiere ligne et colonne
	for i in range(2, lenS1i):
		score[i][0] = score[1][0] + gap_extension*(i-1)
		traceback[i][0] = 'up'
	for j in range(2, lenS2j):
		score[0][j] = score[0][1] + gap_extension*(j-1)
		traceback[0][j] = 'left'


	# Calcul et remplissage des matrices score et traceback
	for i in range(1, lenS1i):
		for j in range(1, lenS2j):
			# Score partiel - diagonale
			if boolean==True: # on travaille sur des seq proteiques
				qdiag = score[i-1][j-1]+blo62.blossum62(seq1[i-1], seq2[j-1])
			else:
				qdiag = score[i-1][j-1]+check(seq1[i-1], seq2[j-1])

			# Score partiel - up
			if traceback[i-1][j] == 'u':
				qup = score[i-1][j] + gap_extension
			else:
				qup = score[i-1][j] + gap_start
			
			# Score partiel - left
			if traceback[i][j-1] == 'l':
				qleft = score[i][j-1] + gap_extension				
			else:
				qleft = score[i][j-1] + gap_start


			score[i][j] = max(qdiag, qup, qleft)			
			if score[i][j] == qdiag:
				traceback[i][j] = 'd'
			elif score[i][j] == qup:
				traceback[i][j] = 'u'
			else:
				traceback[i][j] = 'l'


	seq1Aligned=''
	seq2Aligned=''



	# Traceback
	i,j = len(seq1), len(seq2) # Commencer a la fin de la matrice
	while i > 0 and j > 0:
		if traceback[i][j] == 'd':
			seq1Aligned += seq1[i-1]
			seq2Aligned += seq2[j-1]
			i -= 1
			j -= 1
		elif traceback[i][j] == 'l':
			seq1Aligned += '-'
			seq2Aligned += seq2[j-1]
			j -= 1
		else:
			seq1Aligned += seq1[i-1]
			seq2Aligned += '-'
			i -= 1


	# Revenir a la case (0,0) si on est sur un bord
	while i > 0:
		seq1Aligned += seq1[i-1]
		seq2Aligned += '-'
		i -= 1
	while j > 0:
		seq1Aligned += '-'
		seq2Aligned += seq2[j-1]
		j -= 1


	f = open('alignement_needleman.txt', 'w+')
	f.write(seq1Aligned[::-1]+'\n'+seq2Aligned[::-1])
	f.close()


# Algorithme de Smith & Waterman, alignement local
def waterman(seq1, seq2, boolean):
	lenS1i, lenS2j = len(seq1)+1, len(seq2)+1

	score=init_matrice(lenS1i, lenS2j, 'float')
	traceback=init_matrice(lenS1i, lenS2j, 'string')

	# Waterman & Smith, initialisations deja faites, matrice de 0

	# Calcul et remplissage des matrices score et traceback
	for i in range(1, lenS1i):
		for j in range(1, lenS2j):
			# Score partiel - diagonale
			if boolean==True: # on travaille sur des seq proteiques
				qdiag = score[i-1][j-1]+blo62.blossum62(seq1[i-1], seq2[j-1])
			else:
				qdiag = score[i-1][j-1]+check(seq1[i-1], seq2[j-1])

			# Score partiel - up
			if traceback[i-1][j] == 'u':
				qup = score[i-1][j] + gap_extension
			else:
				qup = score[i-1][j] + gap_start
			
			# Score partiel - left
			if traceback[i][j-1] == 'l':
				qleft = score[i][j-1] + gap_extension				
			else:
				qleft = score[i][j-1] + gap_start


			score[i][j] = max(0, qdiag, qup, qleft)			
			if score[i][j] == qdiag:
				traceback[i][j] = 'd'
			elif score[i][j] == qup:
				traceback[i][j] = 'u'
			elif score[i][j] == qleft:
				traceback[i][j] = 'l'
			else:
				traceback[i][j] = '0'

	seq1Aligned=''
	seq2Aligned=''



	# Traceback
	i,j = np.unravel_index(score.argmax(), score.shape) # Commencer a la 1ere valeur la plus grande de la matrice
		
	while score[i][j] != 0.0 and (i > 0 and j > 0):
		if traceback[i][j] == 'd':
			seq1Aligned += seq1[i-1]
			seq2Aligned += seq2[j-1]
			i -= 1
			j -= 1
		elif traceback[i][j] == 'l':
			seq1Aligned += '-'
			seq2Aligned += seq2[j-1]
			j -= 1
		else:
			seq1Aligned += seq1[i-1]
			seq2Aligned += '-'
			i -= 1


	print score
	print traceback
	f = open('alignement_waterman.txt', 'w+')
	f.write(seq1Aligned[::-1]+'\n'+seq2Aligned[::-1])
	f.close()

