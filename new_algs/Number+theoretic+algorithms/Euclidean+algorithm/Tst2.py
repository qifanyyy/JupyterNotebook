# -*- coding: utf-8 -*-
import os

print ("Iniciando")

#qtdPts = ['10','20','30','40','50','60','70','80','90','100','250','500','1000']	# Qtd de Pontos
qtdPts = ['20','40','60','80','100']	# Qtd de Pontos
qtdInst = 15													# Qtd de instancias por Pontos
qtdTestes = 30													# qtd de testes

dirBase = os.getcwd() + "/"
dirProb = dirBase + "grafos/problemas/"
dirSol = dirBase + "grafos/solucoes/"
dirSaida = dirBase + "saida/"

#qtdInd = '50'
indCruz = '90'
indMut = '0'
#qtdIter = '1000'

for qtdPt in qtdPts:
	qtdPontos = int(qtdPt)
	qtdInd = 50
	qtdIter = qtdPontos * 5
	for inst in range(1, qtdInst + 1):
		arq = qtdPt + "." + str(inst)
		arqGrafo = dirProb + "estein" + arq
		arqSol = dirSol + "estein" + arq
		
		# Leitura
		sol = open(arqSol, 'r')
		smtSol = float(sol.readline())		# tamanho da smt solucao
		sol.close()
		
		for teste in range(1, qtdTestes + 1):
			arqSaida = dirSaida + arq + "_tst" + str(teste)

			comando = dirBase + "GA_SMT_CORE " + arqGrafo + " " + \
			str(qtdInd) + " " + indCruz + " " + indMut + " " + str(qtdIter) + " " + \
			str(smtSol) + " " + arqSaida #+ " " + str(teste)
			
			print (comando + "\n")
			os.system(comando)

print ("Concluido.\n")
#print "Desligando computador em 10s."
#time.sleep(10)
#os.system('systemctl poweroff') 
