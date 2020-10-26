# -*- coding: utf-8 -*-
import math
import os

print "Iniciando"

#qtdPts = ['10','20','30','40','50','60','70','80','90','100','250','500','1000']	# Qtd de Pontos
qtdPts = ['10','20','30','40','50','60','70']#,'80','90','100']	# Qtd de Pontos
qtdInst = 15																		# Qtd de instancias por Pontos
qtdTestes = 30																		# qtd de testes

dirBase = os.getcwd() + "/"
dirSol = dirBase + "grafos/solucoes/"
dirSaida = dirBase + "saida/"

print "N\tMaior(%)\tMedia(%)\tDesv. Padrão\tTempo(s)"
for qtdPt in qtdPts:						# Qtd de pontos
	maiorPorPt = 0.0
	redPorPt = 0.0
	tempoPorPt = 0.0
	somaDesvioPorPt = 0.0
	qtdGeralPts = 0;
	for inst in range(1, qtdInst + 1):			# Instancia
		redPorInst = []			# redução por instancia
		tempoPorInst = 0.0		# soma tempo por instancia
		
		arq = qtdPt + "." + str(inst)
		arqSol = dirSol + "estein" + arq
		
		# Leitura
		sol = open(arqSol, 'r')
		smtSol = float(sol.readline())		# tamanho da smt solucao
		mstSol = float(sol.readline())		# tamanho da mst solucao
		sol.close()
			
		for teste in range(1, qtdTestes + 1):
			arqSaida = dirSaida + arq + "_tst" + str(teste)
			
			# Leitura
			try:
				sai = open(arqSaida, 'r')
			except IOError:
				exit(0)
			sai = open(arqSaida, 'r')
			sai.readline()						# dir do problema
			tempoSai = float(sai.readline())	# tempo de execucao
			sai.readline()						# parametros utilizados
			smtSai = float(sai.readline())		# tamanho da SMT
			sai.close()
			
			# Calculo
			reducao = ((mstSol - smtSai) * 100) / mstSol
			redPorInst.append(reducao)
			tempoPorInst += tempoSai
		
		maiorPorInst = max(redPorInst)
		mediaPorInst = sum(redPorInst) / float(qtdTestes)		# média de redução por instância
		tempoPorInst = tempoPorInst / float(qtdTestes)			# média de velocidade por instância
		
		maiorPorPt += maiorPorInst
		redPorPt += mediaPorInst
		tempoPorPt += tempoPorInst
		
		# Desvio Padrão
		for teste in range(0, qtdTestes):
			somaDesvioPorPt += (mediaPorInst - redPorInst[teste]) ** 2
			qtdGeralPts += 1
	
	mediaMaiorPorPt = maiorPorPt / float(qtdInst)
	mediaRedPorPt = redPorPt / float(qtdInst)
	mediaTempoPorPt = tempoPorPt / float(qtdInst)
	desvioPadrao = math.sqrt(somaDesvioPorPt / float(qtdGeralPts))
	
	#print qtdPt + "\t" + str(mediaMaiorPorPt).replace(".", ",") + "\t" + str(mediaRedPorPt).replace(".", ",") + "\t" + str(desvioPadrao).replace(".", ",") + "\t" + str(mediaTempoPorPt).replace(".", ",")
	print qtdPt + "\t" + "{:.2f}".format(mediaMaiorPorPt).replace(".", ",") + "\t\t" + "{:.2f}".format(mediaRedPorPt).replace(".", ",") + "\t\t" + "{:.2f}".format(desvioPadrao).replace(".", ",") + "\t\t" + "{:.2f}".format(mediaTempoPorPt).replace(".", ",")

print "Concluido."
